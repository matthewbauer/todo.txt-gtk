#!/usr/bin/python

import gtk
import sys
import subprocess
#import re

class todotxt:
	def __init__(self, TODO_SH):
		self.TODO_SH=TODO_SH
	def addTask(self, task):
		stdout = subprocess.Popen([self.TODO_SH, "add", task], stdout=subprocess.PIPE).communicate()[0]
		return stdout
	def doTask(self, task_num):
		stdout = subprocess.Popen([self.TODO_SH, "do", str(task_num)], stdout=subprocess.PIPE).communicate()[0]
		return stdout
	def undoTask(self, task_num):
		# doesn't work
		#subprocess.Popen([self.TODO_SH, "move", str(task_num), "todo.txt", "done.txt"])
		return
	def getTasks(self):
		# this uses todo.sh list, it would probably be better to use the todo.txt file

		tasks=[]

		todotxtList = subprocess.Popen([self.TODO_SH, "list"], stdout=subprocess.PIPE).communicate()[0]
		data = todotxtList.split("\n")

		# remove the last two items
		l=len(todotxtList.split("\n"))
		data.pop(l-1)
		data.pop(l-2)
		data.pop(l-3)

		data.sort()
		for line in data:
			num = line.split(" ")[0]
			task = " ".join(line.split(" ")[1:])
			tasks.append([num, task])

		return tasks

class mainWindow(gtk.Window):
	def __init__(self, todotxt):
		super(mainWindow, self).__init__()

		self.set_title("todo.txt-gtk")
		self.set_border_width(10)

		self.todotxt = todotxt

		vbox = gtk.VBox(False, 0)

		hbox1 = gtk.HBox(False, 0)

		vbox.pack_start(hbox1, False, False, 0)

		entry = gtk.Entry()
		entry.set_max_length(50)
		entry.connect("activate", self.enter_callback, entry)
		hbox1.pack_start(entry, True, True, 0)

		button = gtk.Button(stock=gtk.STOCK_ADD)
		button.connect("clicked", self.enter_callback, entry)
		hbox1.pack_start(button, False, False, 0)

		hbox2 = gtk.HBox(False, 0)

		vbox.pack_start(hbox2, True, True, 0)

		scrolled_window = gtk.ScrolledWindow()
		scrolled_window.set_border_width(10)
		scrolled_window.set_policy(gtk.POLICY_AUTOMATIC, gtk.POLICY_AUTOMATIC)
		hbox2.pack_start(scrolled_window, True, True, 0)

		target_vbox = gtk.VBox(False, 5)
		target_vbox.border=5

		self.target_vbox = target_vbox

		scrolled_window.add_with_viewport(self.target_vbox)

		self.insertTasks(todotxt, self.target_vbox)

		hbox3 = gtk.HBox(False, 0)
		self.label=gtk.Label("Done.")
		hbox3.pack_start(self.label, False, False, 0)
		vbox.pack_start(hbox3, False, False, 0)

		self.add(vbox)

		self.connect("destroy", gtk.main_quit)

		self.show_all()

	def enter_callback(self, widget, entry):
		output=self.todotxt.addTask(entry.get_text())
		widget.set_text("")
		self.label.set_text(output)
		self.insertTasks(self.todotxt, self.target_vbox)

	def check_callback(self, widget, data=None):
		if widget.get_active(): # on
			if data:
				output = self.todotxt.doTask(data)
				self.label.set_text(output)
		else: # off
			if data:
				output = self.todotxt.undoTask(data)
				if output: self.label.set_text(output)
		self.insertTasks(self.todotxt, self.target_vbox)

	def insertTasks(self, todotxt, vbox):
		for task in todotxt.getTasks():
			hbox=gtk.HBox(False, 0)
			button = gtk.CheckButton()
			button.connect("toggled", self.check_callback, task[0])
			hbox.pack_start(button, False, False, 0)
			label=gtk.Label(task[1])
			hbox.pack_start(label, False, True, 0)
			vbox.add(hbox)
		vbox.show()

def main(argv=None):
	if argv is None:
		argv = sys.argv

	mytodotxt=todotxt("todo.sh")

	mainWindow(mytodotxt)

	gtk.main()

if __name__ == "__main__":
	main()
