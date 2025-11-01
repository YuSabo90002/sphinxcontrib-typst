# Minimal makefile for Sphinx documentation
#

# You can set these variables from the command line, and also
# from the environment for the first two.
SPHINXOPTS    ?=
SPHINXBUILD   ?= sphinx-build
SOURCEDIR     = source
BUILDDIR      = _build

# Put it first so that "make" without argument is like "make help".
help:
	@$(SPHINXBUILD) -M help "$(SOURCEDIR)" "$(BUILDDIR)" $(SPHINXOPTS) $(O)

.PHONY: help Makefile gettext locale-init locale-update html-ja multilang serve-multilang

# Internationalization (i18n) targets
gettext:
	@$(SPHINXBUILD) -M gettext "$(SOURCEDIR)" "$(BUILDDIR)" $(SPHINXOPTS) $(O)
	@echo "Build finished. The message catalogs are in $(BUILDDIR)/gettext."

locale-init:
	sphinx-intl update -p $(BUILDDIR)/gettext -l ja
	@echo "Locale initialized. Translation files are in locale/ja/LC_MESSAGES/."

locale-update:
	sphinx-intl update -p $(BUILDDIR)/gettext -l ja
	@echo "Locale updated. Translation files are in locale/ja/LC_MESSAGES/."

html-ja:
	@$(SPHINXBUILD) -b html "$(SOURCEDIR)" "$(BUILDDIR)/html-ja" -D language=ja $(SPHINXOPTS) $(O)
	@echo "Build finished. The Japanese HTML pages are in $(BUILDDIR)/html-ja."

# Multi-language build for GitHub Pages
multilang:
	python build_multilang.py
	@echo "Multi-language build complete. Output in $(BUILDDIR)/multilang/"

# Serve multi-language docs locally
serve-multilang: multilang
	@echo "Starting local server at http://localhost:8000"
	@echo "Press Ctrl+C to stop"
	cd $(BUILDDIR)/multilang && python -m http.server 8000

# Catch-all target: route all unknown targets to Sphinx using the new
# "make mode" option.  $(O) is meant as a shortcut for $(SPHINXOPTS).
%: Makefile
	@$(SPHINXBUILD) -M $@ "$(SOURCEDIR)" "$(BUILDDIR)" $(SPHINXOPTS) $(O)
