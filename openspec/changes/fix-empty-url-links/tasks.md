# Implementation Tasks

## Phase 1: Core Implementation

### Task 1.1: Add empty URL validation in visit_reference()
**Deliverable**: Empty URL detection and early return

- [x] Locate `visit_reference()` method in `typsphinx/translator.py` (line ~1891)
- [x] After line 1931 (`refuri = node.get("refuri", "")`), add empty check:
  ```python
  if not refuri:
      logger.warning(
          f"Reference node has empty URL. "
          f"Link will be rendered as plain text. "
          f"Check for broken references in source: {node.astext()}"
      )
      self._skip_link_wrapper = True
      return
  ```
- [x] Import logger if not already imported:
  ```python
  from sphinx.util import logging
  logger = logging.getLogger(__name__)
  ```

**Validation**:
- Code compiles without syntax errors
- Early return prevents `link()` generation for empty URLs
- Warning message is clear and actionable

**Files**: `typsphinx/translator.py`

---

### Task 1.2: Handle skipped link wrapper in depart_reference()
**Deliverable**: Skip closing parenthesis for empty URL links

- [x] Locate `depart_reference()` method in `typsphinx/translator.py` (line ~1957)
- [x] At the start of the method, add skip check:
  ```python
  # Skip link wrapper closing if we skipped it in visit
  if getattr(self, "_skip_link_wrapper", False):
      self._skip_link_wrapper = False
      # Restore list item separator state if needed
      if hasattr(self, "_reference_was_list_item_needs_separator"):
          if self.in_list_item:
              self.list_item_needs_separator = True
          delattr(self, "_reference_was_list_item_needs_separator")
      return
  ```

**Validation**:
- No mismatched parentheses in generated Typst code
- Skip flag is properly cleaned up
- List item separator state is preserved

**Files**: `typsphinx/translator.py`

---

### Task 1.3: Test empty URL handling locally
**Deliverable**: Verified fix works with test document

- [x] Create test RST document with empty URL:
  ```rst
  Test :ref:`nonexistent` reference.
  ```
- [x] Build with typsphinx
- [x] Verify warning appears in build output
- [x] Verify generated `.typ` file contains `[nonexistent]` not `#link("", ...)`
- [x] Verify Typst compilation succeeds

**Validation**:
- Warning logged during build
- No empty `link()` calls in output
- Typst compiles successfully

**Dependencies**: Tasks 1.1, 1.2

---

## Phase 2: Testing

### Task 2.1: Unit tests for empty URL handling
**Deliverable**: Test coverage for new code paths

- [x] Create test file or add to `tests/test_translator.py`
- [x] Test cases:
  - Empty `refuri` → no `link()` generated
  - Empty `refuri` → content rendered as text
  - Empty `refuri` → warning emitted
  - Valid `refuri` → existing behavior (regression test)
  - Multiple empty URLs → multiple warnings
- [x] Use pytest fixtures and mocks for node creation
- [x] Verify `_skip_link_wrapper` flag behavior

**Validation**:
- All new tests pass
- Coverage for `visit_reference()` and `depart_reference()` ≥90%

**Files**: `tests/test_translator.py`

---

### Task 2.2: Integration test with broken references
**Deliverable**: End-to-end validation

- [x] Create test fixture document with:
  - Unresolved cross-reference
  - Broken external link
  - Valid links (for regression)
- [x] Build with typsphinx
- [x] Verify:
  - Warnings for broken references
  - No warnings for valid links
  - Generated Typst compiles
  - No "URL must not be empty" errors

**Validation**:
- Build succeeds
- Appropriate warnings appear
- Typst 0.14.1 compilation works

**Files**: `tests/fixtures/` or `tests/test_integration.py`

---

### Task 2.3: Regression testing
**Deliverable**: Existing tests pass

- [x] Run full test suite: `uv run pytest`
- [x] Verify all 317 existing tests pass
- [x] Check no unexpected changes in test output
- [x] Verify coverage remains ≥94%

**Validation**:
- Zero test failures
- Coverage maintained or improved

**Dependencies**: Tasks 2.1, 2.2

---

## Phase 3: Typst Version Upgrade

### Task 3.1: Update uv.lock to Typst 0.14.1
**Deliverable**: Dependency upgraded

- [x] Run `uv lock --upgrade-package typst`
- [x] Verify `uv.lock` now specifies typst 0.14.1 or newer
- [x] Or manually edit `pyproject.toml`:
  ```toml
  [project.dependencies]
  typst = ">=0.14.1"
  ```
  Then run `uv lock`

**Validation**:
- `uv.lock` contains typst 0.14.1+
- Local builds use new version

**Files**: `uv.lock`, possibly `pyproject.toml`

---

### Task 3.2: Remove typst constraint from tox.ini (if present)
**Deliverable**: Tox uses locked version

- [x] Check `tox.ini` for `typst>=0.11.1` in deps
- [x] If present, remove it (let tox use `uv.lock`)
- [x] If already removed, skip this task

**Validation**:
- `tox.ini` does not override typst version
- Tox environments use `uv.lock` version

**Files**: `tox.ini`

---

### Task 3.3: Test with Typst 0.14.1
**Deliverable**: Verified compatibility

- [x] Run `uv run tox -e docs-pdf`
- [x] Verify PDF builds successfully
- [x] Check no "URL must not be empty" errors
- [x] Verify warnings for broken references

**Validation**:
- PDF generated successfully
- Typst 0.14.1 compatibility confirmed

**Dependencies**: Tasks 3.1, 3.2, all Phase 1-2 tasks

---

## Phase 4: Documentation and Polish

### Task 4.1: Update CHANGELOG
**Deliverable**: Release notes entry

- [x] Add entry under "Unreleased" or next version
- [x] Describe fix: "Handle empty URLs in references gracefully"
- [x] Mention Typst 0.14.1 compatibility
- [x] Reference Issue #77

**Validation**:
- CHANGELOG follows project conventions
- Entry is clear and informative

**Files**: `CHANGELOG.md`

---

### Task 4.2: Add code comments
**Deliverable**: Documented edge case

- [x] Add comment above empty URL check explaining:
  - Why this check is needed (Typst 0.14.1 validation)
  - What happens (skip link, render text, warn)
  - Example scenarios (unresolved refs, broken links)

**Validation**:
- Code is self-documenting
- Future developers understand the logic

**Files**: `typsphinx/translator.py`

---

### Task 4.3: Code quality checks
**Deliverable**: Passes all linters and type checkers

- [x] Run `uv run black .` (format code)
- [x] Run `uv run ruff check .` (lint)
- [x] Run `uv run mypy typsphinx/` (type check)
- [x] Fix any issues

**Validation**:
- All quality checks pass
- No new warnings

**Dependencies**: All implementation tasks

---

## Phase 5: CI/CD Validation

### Task 5.1: Create pull request
**Deliverable**: PR ready for review

- [ ] Create branch: `fix/empty-url-links`
- [ ] Commit all changes with clear message
- [ ] Push to origin
- [ ] Create PR with description:
  - Problem (empty URL generation)
  - Solution (validation + skip)
  - Impact (Typst 0.14.1 compatibility)
- [ ] Reference Issue #77 with `Closes #77`

**Validation**:
- PR created successfully
- Description is clear and complete

**Dependencies**: All previous tasks

---

### Task 5.2: Verify CI pipeline passes
**Deliverable**: Green CI checks

- [ ] Wait for GitHub Actions to complete
- [ ] Verify all checks pass:
  - Tests (all 317)
  - Lint (ruff, black)
  - Type check (mypy)
  - Documentation build (HTML + PDF)
- [ ] Check PDF builds with Typst 0.14.1

**Validation**:
- All CI checks green ✅
- PDF documentation generated successfully
- No "URL must not be empty" errors

**Dependencies**: Task 5.1

---

### Task 5.3: Review and merge
**Deliverable**: Fix deployed to main

- [ ] Address any review feedback
- [ ] Ensure all discussions resolved
- [ ] Merge PR to main
- [ ] Verify main branch CI also passes

**Validation**:
- PR merged successfully
- Issue #77 automatically closed
- Main branch is green

**Dependencies**: Task 5.2

---

## Dependency Graph

```
Phase 1 (Implementation)
  1.1 ─┬─→ 1.3
  1.2 ─┘

Phase 2 (Testing)
  2.1 ─┬─→ 2.3
  2.2 ─┘

Phase 3 (Typst Upgrade)
  3.1 ─┬─→ 3.3
  3.2 ─┘

Phase 4 (Documentation)
  4.1, 4.2 (parallel) ─→ 4.3

Phase 5 (CI/CD)
  5.1 → 5.2 → 5.3
```

**Critical Path**: 1.1 → 1.2 → 1.3 → 2.1 → 2.2 → 2.3 → 3.1 → 3.3 → 4.3 → 5.1 → 5.2 → 5.3

**Parallelization**:
- Tasks 2.1 and 2.2 can be worked on in parallel
- Tasks 4.1 and 4.2 can be done independently
- Phase 3 can start once Phase 1 is complete (doesn't strictly need Phase 2)

## Estimated Effort

- **Phase 1**: 1 hour (implementation is straightforward)
- **Phase 2**: 1.5-2 hours (writing comprehensive tests)
- **Phase 3**: 30 minutes (dependency update + validation)
- **Phase 4**: 30 minutes (documentation + code quality)
- **Phase 5**: 30 minutes (PR + CI wait time)

**Total**: **4-5 hours** (actual work time)
**Wall-clock time**: ~6 hours (including CI wait time)

## Success Metrics

- ✅ Empty URLs detected and skipped
- ✅ Warnings emitted for broken references
- ✅ Typst 0.14.1 compilation succeeds
- ✅ CI/CD pipeline restored
- ✅ All 317 tests pass
- ✅ Coverage ≥94%
- ✅ Issue #77 closed
- ✅ No regression in valid link handling
