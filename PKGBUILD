# Defined outside:
#   - _project
#   - _base
#   - _version
pkgname="${_project}"
pkgver="${_version}"
pkgrel=1

unset -f _do_prepare _do_build _do_check _do_package
source ${_base}/PKGBUILD
# TODO: various checks that nothing forbidden has been touched

_has_function() {
	declare -f "$1" >/dev/null
}

prepare() {
    ! _has_function _do_prepare || _do_prepare "$@"
}

build() {
	cd "${_base}"
    ! _has_function _do_build || _do_build "$@"
}

check() {
	cd "${_base}"
    ! _has_function _do_check || _do_check "$@"
}

package() {
	cd "${_base}"
    ! _has_function _do_package || DESTDIR="${pkgdir}" _do_package "$@"
}
