# Defined outside:
#   - _project
#   - _base
#   - _version
pkgname="${_project}"
pkgver="${_version}"
pkgrel=1
epoch=
pkgdesc=""
arch=('any')
url=""
license=('GPL')
groups=()
depends=($(make -sC "${_base}" depends))
makedepends=($(make -sC "${_base}" makedepends))
checkdepends=($(make -sC "${_base}" checkdepends))
optdepends=()
provides=($(make -sC "${_base}" provides))
conflicts=($(make -sC "${_base}" conflicts))
replaces=()
backup=()
options=($(make -sC "${_base}" options))
install=
changelog=
source=()
noextract=()
md5sums=()
validpgpkeys=()

prepare() {
    : not allowed to change the sources
}

build() {
	cd "${_base}"
	make all
}

check() {
	cd "${_base}"
	make -k check
}

package() {
	cd "${_base}"
	make DESTDIR="${pkgdir}/" install
}
