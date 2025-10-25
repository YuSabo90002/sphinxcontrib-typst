# Implementation Tasks: Migrate CI to Tox

## 1. Update tox.ini

- [x] 1.1 Add `docs-html` environment for HTML documentation build
- [x] 1.2 Add `docs-pdf` environment for PDF documentation build
- [x] 1.3 Add `docs` environment for both HTML and PDF builds
- [x] 1.4 Update existing `type` environment path (sphinxcontrib/ → typsphinx/)
- [x] 1.5 Update existing `cov` environment path (sphinxcontrib.typst → typsphinx)

## 2. Update docs/source/conf.py

- [x] 2.1 Add `typsphinx` to extensions list (required for PDF builds)

## 3. Update GitHub Actions - ci.yml

- [x] 3.1 Update test job to use `tox -e py{39,310,311,312}`
- [x] 3.2 Update lint job to use `tox -e lint`
- [x] 3.3 Update type-check job to use `tox -e type`
- [x] 3.4 Update coverage job to use `tox -e cov`

## 4. Update GitHub Actions - docs.yml

- [x] 4.1 Update HTML build step to use `tox -e docs-html`
- [x] 4.2 Update PDF build step to use `tox -e docs-pdf`
- [x] 4.3 Update artifact paths to match tox output directories

## 5. Local Testing

- [x] 5.1 Test `tox -e lint` locally
- [x] 5.2 Test `tox -e type` locally
- [x] 5.3 Test `tox -e py311` locally
- [x] 5.4 Test `tox -e docs-html` locally
- [x] 5.5 Test `tox -e docs-pdf` locally (verify it completes)
- [x] 5.6 Test `tox -e docs` locally

## 6. CI Verification

- [ ] 6.1 Verify all CI jobs pass on PR
- [ ] 6.2 Verify documentation builds successfully
- [ ] 6.3 Verify GitHub Pages deployment works
- [ ] 6.4 Verify test matrix (Python 3.9-3.12, Linux/Mac/Windows)

## 7. Documentation

- [x] 7.1 Update README.md with tox commands
- [x] 7.2 Update CHANGELOG.md
- [x] 7.3 Update contributing.rst with tox usage

## 8. Final Validation

- [x] 8.1 Run full tox suite locally
- [x] 8.2 Verify all tests pass
- [x] 8.3 Verify documentation builds
- [ ] 8.4 Confirm CI pipeline works end-to-end
