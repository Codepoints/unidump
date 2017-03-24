VIRTUALENV := virtualenv

all:
	@echo "usage: make (dist|i18n|clean|virtualenv|test)"
.PHONY: all

dist: virtualenv test
	"$(VIRTUALENV)"/bin/python3 setup.py sdist bdist_wheel
.PHONY: dist

upload: dist
	twine upload dist/*
.PHONY: upload

i18n: unidump/locale/de/LC_MESSAGES/unidump.mo
.PHONY: i18n

unidump/locale/de/LC_MESSAGES/unidump.mo: unidump/locale/de/LC_MESSAGES/unidump.po
	msgfmt -o "$@" "$<"

unidump/locale/de/LC_MESSAGES/unidump.po: unidump/locale/unidump.pot
	msgmerge -U "$@" "$<"

unidump/locale/unidump.pot: unidump/cli.py
	xgettext -o "$@" -LPython --from-code utf-8 "$<"

clean:
	rm -fr unidump.egg-info dist build
.PHONY: clean

virtualenv: $(VIRTUALENV)/bin/python3
.PHONY: virtualenv

$(VIRTUALENV)/bin/python3: requirements.txt
	virtualenv -p /usr/bin/python3 "$(VIRTUALENV)"
	"$(VIRTUALENV)"/bin/pip install -r requirements.txt

test: virtualenv
	"$(VIRTUALENV)"/bin/mypy unidump
	"$(VIRTUALENV)"/bin/pep8 unidump
	"$(VIRTUALENV)"/bin/python3 -m doctest unidump/__init__.py unidump/[a-z]*.py
.PHONY: test
