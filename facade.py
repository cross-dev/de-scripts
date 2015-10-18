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

def junest_to_path(env):
    new_path = "{0}:{1}".format(os.path.join(base, "..", "3rdparty", "junest", "bin"), env["PATH"])
    return dict(env, PATH=new_path)

class JuNest:
    def __init__(self, mountpoint=os.path.join(base, "..", "mnt", "all"), env=os.environ):
        self.env = junest_to_path(env)
        self.env = dict(self.env, JUNEST_HOME=mountpoint)

    def _run(self, junest_args, shell_command, cwd):
        runner = os.path.join(base, "junest-run")
        p = subprocess.Popen([runner] + junest_args + ['--'] + shell_command, cwd=cwd, env=self.env)
        return p.wait()

    def run_privileged(self, shell_command, cwd="."):
        return self._run(junest_args=["-f"], shell_command=shell_command, cwd=cwd)

    def run_unprivileged(self, shell_command, cwd="."):
        return self._run(junest_args=[], shell_command=shell_command, cwd=cwd)

def sanitize(args):
    sanitize = os.path.join(base, "sanitize")
    p = subprocess.Popen(sanitize, cwd=root, env=junest_to_path(os.environ))
    return p.wait()

def shell(args):
    junest = JuNest()
    return junest.run_unprivileged(args.cmd)

def sudo(args):
    junest = JuNest()
    return junest.run_privileged(args.cmd)

def tools(args):
    input = open(os.path.join(base, "tools.sh.in"), "r")
    print(input.read().replace("%FACADE_PATH%", os.path.realpath(__file__)).replace("%DE_ROOT%", root))
    input.close()

def menuconfig(args):
    junest = JuNest()
    return junest.run_unprivileged(["kconfig-nconf", "Kconfig"], cwd=root)

def buildpkg(args):
    _project = args.project
    _version = subprocess.check_output([os.path.join(base, "get-project-version"), root, _project]).rstrip()
    _base = subprocess.check_output([os.path.join(base, "get-project-base"), root, _project]).rstrip()
    env = dict(os.environ, _version=_version, _project=_project, _base=_base)
    junest = JuNest(env=env)
    _args = [os.path.join(base, "buildpkg")]
    if args.ignorearch:
        _args += ["--ignorearch"]
    if args.nodeps:
        _args += ["--nodeps"]
    if args.force:
        _args += ["--force"]
    if args.geninteg:
        _args += ["--geninteg"]
    if args.install:
        _args += ["--install"]
    if args.log:
        _args += ["--log"]
    if args.nocolor:
        _args += ["--nocolor"]
    if args.rmdeps:
        _args += ["--rmdeps"]
    if args.repackage:
        _args += ["--repackage"]
    if args.syncdeps:
        _args += ["--syncdeps"]
    if args.check:
        _args += ["--check"]
    if args.config is not None:
        _args += ["--config", args.config]
    if args.noarchive:
        _args += ["--noarchive"]
    if args.nocheck:
        _args += ["--nocheck"]
    if args.noprepare:
        _args += ["--noprepare"]
    if args.asdeps:
        _args += ["--asdeps"]
    if args.needed:
        _args += ["--needed"]
    if args.noconfirm:
        _args += ["--noconfirm"]
    if args.noprogressbar:
        _args += ["--noprogressbar"]

    return junest.run_privileged(_args, cwd=root)


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

parser_buildpkg = subparsers.add_parser("buildpkg", help="Build project package from the universal PKGBUILD")
parser_buildpkg.set_defaults(func=buildpkg)
parser_buildpkg.add_argument("--ignorearch", "-A", help="Ignore incomplete arch field in PKGBUILD", action="store_true")
#parser_buildpkg.add_argument("--clean", "-c", help="Clean up work files after build", action="store_true")
#parser_buildpkg.add_argument("--cleanbuild", "-C", help="Remove $srcdir/ dir before building the package", action="store_true")
parser_buildpkg.add_argument("--nodeps", "-d", help="Skip all dependency checks", action="store_true")
#parser_buildpkg.add_argument("--noextract", "-e", help="Do not extract source files (use existing $srcdir/ dir)", action="store_true")
parser_buildpkg.add_argument("--force", "-f", help="Overwrite existing package", action="store_true")
parser_buildpkg.add_argument("--geninteg", "-g", help="Generate integrity checks for source files", action="store_true")
parser_buildpkg.add_argument("--install", "-i", help="Install package after successful build", action="store_true")
parser_buildpkg.add_argument("--log", "-L", help="Log package build process", action="store_true")
parser_buildpkg.add_argument("--nocolor", "-m", help="Disable colorized output messages", action="store_true")
#parser_buildpkg.add_argument("--nobuild", "-o", help="Download and extract files only", action="store_true")
#parser_buildpkg.add_argument("-p", dest="file", help="Use an alternate build script (instead of 'PKGBUILD')")
parser_buildpkg.add_argument("--rmdeps", "-r", help="Remove installed dependencies after a successful build", action="store_true")
parser_buildpkg.add_argument("--repackage", "-R", help="Repackage contents of the package without rebuilding", action="store_true")
parser_buildpkg.add_argument("--syncdeps", "-s", help="Install missing dependencies with pacman", action="store_true")
#parser_buildpkg.add_argument("--source", "-S", help="Generate a source-only tarball without downloaded sources", action="store_true")
#parser_buildpkg.add_argument("--version", "-V", help="Show version information and exit", action="store_true")
#parser_buildpkg.add_argument("--allsource", help="Generate a source-only tarball including downloaded sources", action="store_true")
parser_buildpkg.add_argument("--check", help="Run the check() function in the PKGBUILD", action="store_true")
parser_buildpkg.add_argument("--config", help="Use an alternate config file (instead of '/etc/makepkg.conf')")
#parser_buildpkg.add_argument("--holdver", help="Do not update VCS sources", action="store_true")
#--key
parser_buildpkg.add_argument("--noarchive", help="Do not create package archive", action="store_true")
parser_buildpkg.add_argument("--nocheck", help="Do not run the check() function in the PKGBUILD", action="store_true")
parser_buildpkg.add_argument("--noprepare", help="Do not run the prepare() function in the PKGBUILD", action="store_true")
#--nosign
#--pkg
#--sign
#--skipchecksums
#--skipinteg
#--skippgpcheck
#--verifysource
parser_buildpkg.add_argument("--asdeps", help="Install packages as non-explicitly installed", action="store_true")
parser_buildpkg.add_argument("--needed", help="Do not reinstall the targets that are already up to date", action="store_true")
parser_buildpkg.add_argument("--noconfirm", help="Do not ask for confirmation when resolving dependencies", action="store_true")
parser_buildpkg.add_argument("--noprogressbar", help="Do not show a progress bar when downloading files", action="store_true")
parser_buildpkg.add_argument("project", help="Project name as defined by manifest")

args = parser.parse_args()
sys.exit(args.func(args))
