all:
	@echo "usage: make (dist|i18n|clean|virtualenv|test)"
.PHONY: all

dist: test
	virtualenv/bin/python3 setup.py sdist bdist_wheel
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

virtualenv:
	virtualenv -p /usr/bin/python3 virtualenv
	virtualenv/bin/pip install -r requirements.txt
.PHONY: virtualenv

test:
	virtualenv/bin/mypy unidump
	virtualenv/bin/pep8 unidump
	virtualenv/bin/python3 -m doctest unidump/__init__.py unidump/[a-z]*.py
.PHONY: test
