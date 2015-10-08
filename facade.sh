#!/bin/bash

# MVP

BASE_DE_WORKSPACE_FOLDER=$(pwd)

__de_sanitize() {
    PATH=${BASE_DE_WORKSPACE_FOLDER}/.cross-dev/3rdparty/junest/bin:$PATH ${BASE_DE_WORKSPACE_FOLDER}/.cross-dev/sanitizer/sanitize
}

__de_privileged_junest() {
    JUNEST_HOME=${BASE_DE_WORKSPACE_FOLDER}/.cross-dev/layers/basement ${BASE_DE_WORKSPACE_FOLDER}/.cross-dev/3rdparty/junest/bin/junest -f -- $@
}

__de_unprivileged_junest() {
    JUNEST_HOME=${BASE_DE_WORKSPACE_FOLDER}/.cross-dev/layers/basement ${BASE_DE_WORKSPACE_FOLDER}/.cross-dev/3rdparty/junest/bin/junest -- $@
}

__de_install_basement() {
    __de_privileged_junest yaourt -S $@
}

__de_upgrade_basement() {
    # Hangs due to https://github.com/fsquillace/junest/issues/116
    #__de_privileged_junest pacman-key --populate
    #__de_privileged_junest pacman-key --refresh-keys
    __de_privileged_junest pacman -Syu --noconfirm
}
