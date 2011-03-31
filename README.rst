Install for designers
=====================

Sorry for these a bit difficult instructions. We will automate these steps 
in near future.

Install these system packages:

  - python

Create these directories:

  - eggs
  - downloads

Create configuration files as fallows:

  - Create ``buildout.cfg`` with fallowing content::

      [buildout]
      extends = buildout/designer.cfg

  - Create ``src/web369/settings.py`` with fallowing content::

      from web369.conf.designer import *


Perform these commands::

    python bootstrap.py --distribute
    bin\buildout.exe -N

Now you ready to work.

  - Run django server: ``bin\django.exe runserver``

  - Open this url in browser: ``http://127.0.0.1:8000/``

File locations:

  - Templates: ``src/web369/templates/``

  - Static files: ``src/web369/static/``


Install for developers
======================

  - Configure your mysql database so that it can be accessed 
    with `root` user and empty password.

  - Run::

      make

You can rebuild database any time with::

    make rebuilddb


Basic usage for developers
==========================

``bin/scapy carwl delf_lt`` : Run delfi.lt scrapper.

``bin/supervisord`` : Run supervisor server. It can be accessed from:
http://127.0.0.1:8010/ . Django website can be accessed at port 8000.

``make run`` : Run django server, without supervisor.

``make shell`` : Open django shell-plus

``make test`` : Run tests

``make dump`` : Dump nice data to dump.json.
