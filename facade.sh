#!/bin/bash

# MVP

BASE_DE_WORKSPACE_FOLDER=$(pwd)

__de_sanitize() {
    PATH=${BASE_DE_WORKSPACE_FOLDER}/.cross-dev/3rdparty/junest/bin:$PATH ${BASE_DE_WORKSPACE_FOLDER}/.cross-dev/sanitizer/sanitize
}

__de_unprivileged_junest() {
    local mountpoint=$1
    shift
    JUNEST_HOME=$mountpoint ${BASE_DE_WORKSPACE_FOLDER}/.cross-dev/3rdparty/junest/bin/junest -- "$@"
}

__de_privileged_junest() {
    local mountpoint=$1
    shift
    JUNEST_HOME=$mountpoint ${BASE_DE_WORKSPACE_FOLDER}/.cross-dev/3rdparty/junest/bin/junest -f -- "$@"
}

__de_privileged_basement_junest() {
    __de_privileged_junest ${BASE_DE_WORKSPACE_FOLDER}/.cross-dev/layers/basement "$@"
}

__de_unprivileged_basement_junest() {
    __de_unprivileged_junest ${BASE_DE_WORKSPACE_FOLDER}/.cross-dev/layers/basement "$@"
}

__de_install_basement() {
    __de_privileged_basement_junest yaourt -S "$@"
}

__de_upgrade_basement() {
    # Hangs due to https://github.com/fsquillace/junest/issues/116
    #__de_privileged_basement_junest pacman-key --populate
    #__de_privileged_basement_junest pacman-key --refresh-keys
    __de_privileged_basement_junest pacman -Syu --noconfirm
}

__de_privileged_all_junest() {
    __de_privileged_junest ${BASE_DE_WORKSPACE_FOLDER}/.cross-dev/mnt/all "$@"
}

__de_unprivileged_all_junest() {
    __de_unprivileged_junest ${BASE_DE_WORKSPACE_FOLDER}/.cross-dev/mnt/all "$@"
}

__de_environment_config() {
    kconfig-mconf ${BASE_DE_WORKSPACE_FOLDER}/Kconfig
}
