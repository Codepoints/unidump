all:
.PHONY: all

deploy:
	python setup.py sdist bdist_wheel
	twine upload dist/*
.PHONY: deploy

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
