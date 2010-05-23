# Contributor: Matthew Bauer <mjbauer95@gmail.com>
___pkgname=todo
__pkgname=$___pkgname.txt
_pkgname=$__pkgname-gtk
pkgname=$_pkgname-git
pkgver=20100523
pkgrel=1
pkgdesc="Graphical User Interface for $__pkgname in Python"
url="http://github.com/paradoq/$_pkgname"
license=('GPL')
arch=('any')
depends=('gtk'
         'python'
         'pygtk'
         'todotxt')
makedepends=('git')
provides=($_pkgname)
conflicts=($_pkgname)
replaces=($_pkgname)

_gitroot="git://github.com/paradoq/$_pkgname.git"
_gitname="$_pkgname"

build() {
  cd "$srcdir"
  msg "Connecting to GIT server...."

  if [ -d $_gitname ] ; then
    cd $_gitname && git pull origin
    msg "The local files are updated."
  else
    git clone $_gitroot $_gitname
  fi

  msg "GIT checkout done or server timeout"
  msg "Starting make..."

  cd $_gitname

  mkdir -p $pkgdir/usr/bin
  cp todo-txt-gtk.py $pkgdir/usr/bin
}
