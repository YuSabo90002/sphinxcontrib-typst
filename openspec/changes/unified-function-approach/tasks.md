# Implementation Tasks: Unified Function Approach

This document outlines all tasks required to implement the unified function approach for Typst element generation in sphinx-typst.

---

## Phase 1: Simple Elements (No State Changes)

These elements can be converted by simple string replacements without changing state management.

### 1.1 Emphasis Conversion

- [ ] Update `visit_emphasis()` to generate `#emph[` instead of `_`
- [ ] Update `depart_emphasis()` to generate `]` instead of `_`
- [ ] Update test fixture `tests/fixtures/emphasis.typ` with new syntax
- [ ] Add test for nested emphasis cases

### 1.2 Strong Conversion

- [ ] Update `visit_strong()` to generate `#strong[` instead of `*`
- [ ] Update `depart_strong()` to generate `]` instead of `*`
- [ ] Update test fixture `tests/fixtures/strong.typ` with new syntax
- [ ] Add test for underscores within strong text (e.g., `file_name.txt`)
- [ ] Add test for nested strong + emphasis combinations

### 1.3 Subtitle Conversion

- [ ] Update `visit_subtitle()` to generate `#emph[` instead of `_`
- [ ] Update `depart_subtitle()` to generate `]` instead of `_\n\n`
- [ ] Update test fixture `tests/fixtures/subtitle.typ` with new syntax
- [ ] Add test for subtitle with special characters

### 1.4 Field Name Conversion (API Documentation)

- [ ] Update `visit_field_name()` to generate `#strong[` instead of `*`
- [ ] Update `depart_field_name()` to generate `]` with colon instead of `:*\n`
- [ ] Update test fixtures for API documentation
- [ ] Add test for field names with complex content

---

## Phase 2: Heading Conversion (Parameter Calculation)

Headings require passing the level as a parameter instead of generating `=` prefixes.

### 2.1 Heading Function Generation

- [ ] Update `visit_title()` to generate `#heading(level: N)[` using `self.section_level`
- [ ] Update `depart_title()` to generate `]` instead of just newlines
- [ ] Handle edge case: level 0 (if any)
- [ ] Handle deep nesting (levels > 6)

### 2.2 Heading Test Updates

- [ ] Update test fixture for level 1 heading
- [ ] Update test fixture for level 2 heading
- [ ] Update test fixture for level 3 heading
- [ ] Add test for level 6 heading
- [ ] Add test for deeply nested sections (level > 6)
- [ ] Update integration tests with multiple heading levels

---

## Phase 3: List Conversion (State Redesign)

Lists require significant state management changes to collect items before generating function calls.

### 3.1 List State Redesign

- [ ] Add `list_items_stack` to `__init__` for tracking collected items
- [ ] Design item collection mechanism (list of content strings)
- [ ] Handle nested list state (stack-based approach)
- [ ] Design flush mechanism to output collected items

### 3.2 Bullet List Conversion

- [ ] Update `visit_bullet_list()` to initialize item collection
- [ ] Update `depart_bullet_list()` to generate `#list([item1], [item2], ...)`
- [ ] Update `visit_list_item()` to collect content instead of emitting `-`
- [ ] Update `depart_list_item()` to finalize item content
- [ ] Handle empty lists edge case
- [ ] Handle single-item lists
- [ ] Update test fixture for simple bullet lists
- [ ] Add test for nested bullet lists (2 levels)

### 3.3 Enumerated List Conversion

- [ ] Update `visit_enumerated_list()` to initialize item collection
- [ ] Update `depart_enumerated_list()` to generate `#enum([item1], [item2], ...)`
- [ ] Update `visit_list_item()` to handle both bullet and enum collection
- [ ] Handle enumeration starting number edge case (if supported)
- [ ] Update test fixture for simple enumerated lists
- [ ] Add test for nested enumerated lists (2 levels)

### 3.4 Mixed Nested Lists

- [ ] Implement state management for bullet lists containing enum lists
- [ ] Implement state management for enum lists containing bullet lists
- [ ] Add test for bullet list with nested enum list
- [ ] Add test for enum list with nested bullet list
- [ ] Add test for 3-level mixed nesting

### 3.5 Complex List Item Content

- [ ] Handle paragraphs within list items
- [ ] Handle code blocks within list items
- [ ] Handle emphasis/strong within list items
- [ ] Handle nested lists within paragraphs within list items
- [ ] Add comprehensive test for complex list item content

---

## Phase 4: Integration & Testing

### 4.1 Test Fixture Updates

- [ ] Update all `.typ` test fixtures to use function syntax
- [ ] Verify all fixtures compile with Typst
- [ ] Compare PDF output before/after (must be identical)
- [ ] Update fixture README with new syntax examples

### 4.2 Unit Test Updates

- [ ] Update `test_translator.py` for emphasis changes
- [ ] Update `test_translator.py` for strong changes
- [ ] Update `test_translator.py` for subtitle changes
- [ ] Update `test_translator.py` for heading changes
- [ ] Update `test_translator.py` for list changes
- [ ] Update `test_translator.py` for field name changes

### 4.3 Integration Test Updates

- [ ] Update `test_integration.py` for multi-element documents
- [ ] Add integration test for nested elements (emphasis in strong in list)
- [ ] Add integration test for complex document structure
- [ ] Add integration test for API documentation with field names

### 4.4 Regression Testing

- [ ] Run full test suite with pytest
- [ ] Verify no regressions in existing functionality
- [ ] Test with real-world Sphinx projects (if available)
- [ ] Compare generated PDFs (before/after conversion)

---

## Phase 5: Code Quality & Documentation

### 5.1 Code Quality Checks

- [ ] Run `uv run black .` to format code
- [ ] Run `uv run ruff check .` to check linting
- [ ] Run `uv run mypy typsphinx/` to check types
- [ ] Fix any type errors or linting issues
- [ ] Run `uv run tox` for full test matrix

### 5.2 Code Documentation

- [ ] Update docstrings for modified `visit_*` methods
- [ ] Update docstrings for modified `depart_*` methods
- [ ] Add inline comments explaining list collection mechanism
- [ ] Update module-level docstring with architecture notes

### 5.3 User Documentation

- [ ] Update `README.md` with breaking change notice
- [ ] Update `CHANGELOG.md` with detailed change list
- [ ] Add migration guide for users
- [ ] Update example outputs in documentation
- [ ] Document new architectural principle (function-first)

---

## Phase 6: PDF Output Verification

### 6.1 Visual Comparison Tests

- [ ] Generate PDFs from old fixtures (sugar syntax)
- [ ] Generate PDFs from new fixtures (function syntax)
- [ ] Visual diff comparison (must be identical)
- [ ] Automate PDF comparison in CI (if feasible)

### 6.2 Complex Document Testing

- [ ] Test with large documents (>100 pages)
- [ ] Test with documents containing all element types
- [ ] Test with documents with deep nesting (lists, headings)
- [ ] Verify compilation time remains acceptable

---

## Phase 7: Validation & Release Preparation

### 7.1 OpenSpec Validation

- [ ] Run `openspec validate unified-function-approach --strict`
- [ ] Fix any validation errors
- [ ] Ensure all requirements are testable
- [ ] Ensure all scenarios have corresponding tests

### 7.2 Version Bump

- [ ] Decide on version number (v0.3.0 or v1.0.0)
- [ ] Update `pyproject.toml` version
- [ ] Update version in `__init__.py` (if applicable)
- [ ] Update version references in documentation

### 7.3 Changelog & Release Notes

- [ ] Write comprehensive changelog entry
- [ ] Highlight breaking changes prominently
- [ ] Document migration steps for users
- [ ] Include "what's changed" summary for contributors

### 7.4 Final Review

- [ ] Code review by maintainers
- [ ] Review test coverage report (aim for >95%)
- [ ] Review documentation completeness
- [ ] Final approval for merge

---

## Task Dependencies

**Phase 1** (Simple Elements) can be done in parallel.

**Phase 2** (Headings) depends on Phase 1 completion for integration testing.

**Phase 3** (Lists) is independent but complex - can start in parallel with Phase 1/2.

**Phase 4** (Integration & Testing) depends on Phases 1, 2, and 3 completion.

**Phase 5** (Code Quality) depends on Phase 4 completion.

**Phase 6** (PDF Verification) can run in parallel with Phase 5.

**Phase 7** (Validation & Release) depends on Phases 4, 5, and 6 completion.

---

## Estimated Effort

- **Phase 1**: 4 hours (simple string replacements + tests)
- **Phase 2**: 3 hours (parameter calculation + tests)
- **Phase 3**: 12 hours (state redesign + complex tests)
- **Phase 4**: 8 hours (integration tests + fixture updates)
- **Phase 5**: 4 hours (code quality + documentation)
- **Phase 6**: 4 hours (PDF verification)
- **Phase 7**: 3 hours (validation + release prep)

**Total**: ~38 hours (approximately 5 working days)

---

## Success Criteria

1. ✅ All sugar syntax converted to function calls (except Typst standard)
2. ✅ All tests passing (pytest, mypy, black, ruff, tox)
3. ✅ PDF output identical to previous version
4. ✅ No syntax errors in generated `.typ` files
5. ✅ Documentation updated with migration guide
6. ✅ OpenSpec validation passing
7. ✅ Code review approved
8. ✅ Ready for v0.3.0 or v1.0.0 release
