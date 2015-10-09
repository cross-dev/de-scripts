from __future__ import print_function
import os.path
import sys

def find():
    curdir = os.getcwd()
    olddir = None
    while curdir != '/' and curdir != olddir:
        if not os.path.isdir(os.path.join(curdir, '.cross-dev')):
            olddir = curdir
            curdir = os.path.dirname(curdir)
        else:
            return curdir
    return None

def check_and_die():
    root = find()
    if not root:
        print("You are not inside development environment - .cross-dev folder was not found anywhere up the path", file=sys.stderr)
        sys.exit(1)
    return root

if __name__ == "__main__":
    root = check_and_die()
    print(root)
