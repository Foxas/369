#!/usr/bin/env python

import os
import sys
from django.core import management

try:
    from web369 import settings
except ImportError:
    sys.stderr.write("Cannot import threesixnine.settings.")
    sys.stderr.write("You can create it from threesixnine/settings.py-sample")


def main():
    try:
        management.execute_manager(settings)
    except KeyboardInterrupt:
        print ""
        print "Exiting script."
        sys.exit(0)


if __name__ == "__main__":
    main()
