#!/usr/bin/env python

from __future__ import print_function
import argparse
import deroot
import subprocess
import os
import os.path
import sys

root = deroot.check_and_die()
base = os.path.dirname(os.path.realpath(__file__))

def extend_env():
    new_path = "{0}:{1}".format(os.path.join(base, "..", "3rdparty", "junest", "bin"), os.environ["PATH"])
    has_junest_env = dict(os.environ, PATH=new_path)
    return has_junest_env

def sanitize(args):
    has_junest_env = extend_env()
    sanitize = os.path.join(base, "sanitize")
    p = subprocess.Popen(sanitize, cwd=root, env=has_junest_env)
    return p.wait()

def junest_run(mountpoint, junest_args, shell_command, cwd):
    env = dict(extend_env(), JUNEST_HOME=mountpoint)
    runner = os.path.join(base, "junest-run")
    p = subprocess.Popen([runner] + junest_args + ['--'] + shell_command, cwd=cwd, env=env)
    #p = subprocess.Popen(["/bin/bash"])
    return p.wait()

def junest_privileged_run(mountpoint, shell_command, cwd):
    return junest_run(mountpoint=mountpoint, junest_args=["-f"], shell_command=shell_command, cwd=cwd)

def junest_unprivileged_run(mountpoint, shell_command, cwd):
    return junest_run(mountpoint=mountpoint, junest_args=[], shell_command=shell_command, cwd=cwd)

def junest_privileged_base_run(shell_command, cwd="."):
    mountpoint = os.path.join(base, "..", "layers", "base")
    return junest_privileged_run(mountpoint=mountpoint, shell_command=shell_command, cwd=cwd)

def junest_privileged_all_run(shell_command, cwd="."):
    mountpoint = os.path.join(base, "..", "mnt", "all")
    return junest_privileged_run(mountpoint=mountpoint, shell_command=shell_command, cwd=cwd)

def junest_unprivileged_all_run(shell_command, cwd="."):
    mountpoint = os.path.join(base, "..", "mnt", "all")
    return junest_unprivileged_run(mountpoint=mountpoint, shell_command=shell_command, cwd=cwd)

def shell(args):
    return junest_unprivileged_all_run(args.cmd)

def sudo(args):
    return junest_privileged_all_run(args.cmd)

def tools(args):
    pass

def menuconfig(args):
    return junest_unprivileged_all_run(["kconfig-nconf", "Kconfig"], cwd=root)

##### PROGRAM MAIN FLOW

parser = argparse.ArgumentParser()
subparsers = parser.add_subparsers(title="Sub-commands", help="Available sub-commands")

parser_sanitize = subparsers.add_parser("sanitize", help="Sanitize the environment")
parser_sanitize.set_defaults(func=sanitize)

parser_shell = subparsers.add_parser("shell", help="Run a command inside the nested jail")
parser_shell.set_defaults(func=shell)
parser_shell.add_argument('cmd', nargs=argparse.REMAINDER)

parser_sudo = subparsers.add_parser("sudo", help="Run a command inside the nested jail as a super-user")
parser_sudo.set_defaults(func=sudo)
parser_sudo.add_argument('cmd', nargs=argparse.REMAINDER)

tools_description = "Commands: make, makepkg, pacman"
parser_tools = subparsers.add_parser("tools", help="Output a sourceable script for useful commands", description=tools_description)
parser_tools.set_defaults(func=tools)

parser_config = subparsers.add_parser("menuconfig", help="Run graphical configuration tool")
parser_config.set_defaults(func=menuconfig)

args = parser.parse_args()
sys.exit(args.func(args))
