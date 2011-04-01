# Default target

TESTS = web369
COVERAGE_INCLUDES = --include=parts/*,src/web369/*
SHELL = /bin/bash
MYSQL_CMD = mysql -uroot

.PHONY: all develop deploy run tags todo test flake8 syncdb createdb dropdb reloaddb

all: develop

dump:
	bin/django dumpdata --indent=4 --natural \
			sites \
			web369 \
		> dump.json

shell:
	bin/django shell_plus

develop: var/develop.lock \
         buildout.cfg \
         bin/buildout \
         src/web369/settings.py \
         bin/django \
         var/htdocs/static \
         docs/build/html

deploy: var/deploy.lock \
        buildout.cfg \
        bin/buildout \
        src/web369/settings.py \
        bin/django \
        var/htdocs/static \
        docs/build/html

dropdb:
	$(MYSQL_CMD) -e 'DROP DATABASE web369;'

createdb:
	$(MYSQL_CMD) -e 'CREATE DATABASE web369 CHARACTER SET utf8 COLLATE utf8_unicode_ci;'

reloaddb: bin/django
	$(MYSQL_CMD) -e 'DROP DATABASE web369;'
	$(MYSQL_CMD) -e 'CREATE DATABASE web369 CHARACTER SET utf8 COLLATE utf8_unicode_ci;'
	bin/django syncdb

crawl:
	bin/scrapy crawl delfi_lt

quickcrawl:
	bin/scrapy crawl delfi_lt_quick


run:
	bin/django runserver

tags:
	bin/ctags -v

todo:
	@egrep -n 'FIXME|TODO' $$(find parts -iname '*.py' ; \
	                          find src -iname '*.py')

test:
	bin/django test $(TESTS)

coverage:
	bin/coverage run $(COVERAGE_INCLUDES) bin/django test $(TESTS)
	bin/coverage html -d var/htmlcov/ $(COVERAGE_INCLUDES)
	bin/coverage report $(COVERAGE_INCLUDES)
	@echo "Also try xdg-open var/htmlcov/index.html"

flake8:
	@bin/flake8 \
	    src/

upgrade: 
	hg pull -u
	bin/buildout -N
	bin/django syncdb --migrate

# circo dot fdp neato nop nop1 nop2 twopi
graph:
	bin/django graph_models \
	    --group-models \
	    --all-applications \
	    -o var/graph.png
	if [ "$$(uname)" = "Darwin" ]; then \
	    open var/graph.png; \
	else \
	    xdg-open var/graph.png; \
	fi

var:
	mkdir var

# lock which indecates development environment:
var/deploy.lock: var
	if [ -f var/develop.lock ]; then rm var/develop.lock; fi
	touch var/deploy.lock

# lock which indecates deployment environment:
var/develop.lock: var
	if [ -f var/deploy.lock ]; then rm var/deploy.lock; fi
	touch var/develop.lock

buildout.cfg: buildout/base.cfg buildout/develop.cfg buildout/deploy.cfg
	echo "[buildout]" > buildout.cfg
	if [ -f var/deploy.lock ]; then \
	    echo "extends = buildout/deploy.cfg" >> buildout.cfg; \
	else \
	    echo "extends = buildout/develop.cfg" >> buildout.cfg; \
	fi

bin/buildout: buildout.cfg
	mkdir -p eggs downloads
	if which buildout > /dev/null ; then \
	    $$(which buildout) init ; \
	else \
	    python bootstrap.py --distribute ; \
	fi

bin/django: bin/buildout
	bin/buildout -N

src/web369/settings.py:
	if [ -f var/deploy.lock ]; then \
	    echo "from web369.conf.deploy import * " > src/web369/settings.py; \
	else \
	    echo "from web369.conf.develop import * " > src/web369/settings.py; \
	fi

var/htdocs/static: bin/django src/web369/settings.py
	bin/django collectstatic --noinput

docs/build/html: $(find docs -type f -not -wholename 'docs/build/*')
	cd docs ; make html ; cd ..

