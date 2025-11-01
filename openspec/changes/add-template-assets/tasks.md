# Implementation Tasks

## Phase 1: Configuration and Foundation

### Task 1.1: Add `typst_template_assets` configuration value
**Deliverable**: New configuration registered in `__init__.py`

- [x] Add `typst_template_assets` to `setup()` function in `typsphinx/__init__.py`
- [x] Type: `list | None`, default: `None`, rebuild: `html`
- [x] Add inline documentation comment

**Validation**:
- Configuration value is accessible via `self.config.typst_template_assets`
- Sphinx accepts list of strings or None
- No errors during extension initialization

**Files**: `typsphinx/__init__.py`

---

### Task 1.2: Create `copy_template_assets()` method skeleton
**Deliverable**: Empty method with docstring in `TypstBuilder`

- [x] Add `copy_template_assets()` method to `TypstBuilder` class in `builder.py`
- [x] Write comprehensive docstring (similar to `copy_image_files()`)
- [x] Add early return if `typst_template` is not configured
- [x] Add logging: `logger.info("Copying template assets...")`

**Validation**:
- Method exists and can be called
- Returns early when no template is configured
- No exceptions raised

**Files**: `typsphinx/builder.py`

---

### Task 1.3: Integrate into build process
**Deliverable**: `copy_template_assets()` called during build

- [x] Call `self.copy_template_assets()` in `finish()` method after `copy_image_files()`
- [x] Ensure it's called for both `TypstBuilder` and `TypstPDFBuilder`

**Validation**:
- Run test build and verify method is called (check logs)
- No regression in existing builds

**Files**: `typsphinx/builder.py`

---

## Phase 2: Automatic Directory Copy (Default Behavior)

### Task 2.1: Implement automatic template directory copy
**Deliverable**: Copy entire template directory when `typst_template_assets` is None

- [x] Extract template directory path from `typst_template` configuration
- [x] Walk template directory recursively using `os.walk()`
- [x] Skip `.typ` files (already handled by `write_template_file()`)
- [x] Copy each file preserving relative path structure
- [x] Use `shutil.copy2()` to preserve metadata
- [x] Create destination directories with `ensuredir()`
- [x] Handle missing source directory gracefully (log warning, continue)

**Validation**:
- Create test project with template directory containing assets
- Run build and verify all assets are copied
- Verify `.typ` files are not duplicated
- Verify directory structure is preserved

**Files**: `typsphinx/builder.py`

---

### Task 2.2: Add error handling and logging
**Deliverable**: Robust error handling for file operations

- [x] Wrap file copy in try-except block
- [x] Log warnings for individual copy failures (don't fail entire build)
- [x] Log debug message for each successfully copied file
- [x] Log info message with total count at the end

**Validation**:
- Manually create permission errors or missing files
- Verify warnings are logged but build continues
- Check log output contains useful information

**Files**: `typsphinx/builder.py`

---

## Phase 3: Explicit Asset Specification

### Task 3.1: Implement explicit asset list copying
**Deliverable**: Support `typst_template_assets` configuration

- [x] Check if `typst_template_assets` is configured and non-empty
- [x] Iterate through asset list
- [x] For each asset path:
  - Resolve absolute path from source directory
  - Check if file or directory
  - Copy file or directory recursively
  - Preserve relative path in output

**Validation**:
- Configure `typst_template_assets = ["_templates/logo.png"]`
- Run build and verify only specified file is copied
- Verify files not in list are not copied

**Files**: `typsphinx/builder.py`

---

### Task 3.2: Add glob pattern support
**Deliverable**: Support wildcards in asset paths

- [x] Import `glob` module
- [x] Detect patterns containing `*` or `?`
- [x] Use `glob.glob()` to expand patterns
- [x] Copy all matched files/directories
- [x] Handle no matches gracefully (log warning)

**Validation**:
- Configure `typst_template_assets = ["_templates/assets/*.png"]`
- Create multiple PNG files in `_templates/assets/`
- Run build and verify all PNGs are copied
- Verify non-PNG files are not copied

**Files**: `typsphinx/builder.py`

---

### Task 3.3: Implement empty list behavior (opt-out)
**Deliverable**: Empty list disables automatic copying

- [x] Check if `typst_template_assets == []` (empty list)
- [x] Return early without copying (similar to no template case)
- [x] Log debug message: "Template asset copying disabled"

**Validation**:
- Configure `typst_template_assets = []`
- Run build and verify no assets are copied
- Verify only template file itself is copied

**Files**: `typsphinx/builder.py`

---

## Phase 4: Testing

### Task 4.1: Unit tests for `copy_template_assets()`
**Deliverable**: Test coverage for new method

- [x] Test with no template configured (early return)
- [x] Test automatic directory copy
- [x] Test explicit asset list
- [x] Test glob patterns
- [x] Test empty list (opt-out)
- [x] Test missing source files (warnings, no failure)
- [x] Test missing template directory (graceful handling)

**Validation**:
- All tests pass
- Coverage for `copy_template_assets()` is >90%

**Files**: `tests/test_builder.py`

---

### Task 4.2: Integration tests with example projects
**Deliverable**: End-to-end validation with real projects

- [x] Create test project with custom template and assets
- [x] Structure:
  ```
  _templates/
    ├── template.typ
    ├── logo.png
    └── fonts/
        └── custom.otf
  ```
- [x] Configure `typst_template = "_templates/template.typ"`
- [x] Run build and verify assets are copied
- [x] Verify template references work (build PDF successfully)

**Validation**:
- Build succeeds
- All assets present in output directory
- PDF renders correctly with logo and fonts

**Files**: `tests/test_integration.py` or `tests/fixtures/`

---

### Task 4.3: Backward compatibility tests
**Deliverable**: Ensure no regression in existing projects

- [x] Run full test suite (317 existing tests)
- [x] Verify all tests pass
- [x] Test projects without `typst_template` (no change)
- [x] Test projects with `typst_template` but no assets (no errors)

**Validation**:
- All 317 existing tests pass
- Coverage remains ≥94%
- No new warnings or errors

**Files**: All existing test files

---

## Phase 5: Documentation

### Task 5.1: Update user guide
**Deliverable**: Documentation for template assets feature

- [x] Add section "Using Custom Templates with Assets" to user guide
- [x] Document automatic directory copy (default behavior)
- [x] Document `typst_template_assets` configuration
- [x] Provide examples:
  - Simple case (automatic)
  - Explicit asset list
  - Glob patterns
  - Opt-out (empty list)
- [x] Explain difference between `typst_template` and `typst_package`

**Validation**:
- Documentation builds without errors
- Examples are clear and tested

**Files**: `docs/usage.rst` or similar

---

### Task 5.2: Add example project
**Deliverable**: Working example with template assets

- [x] Create `examples/template-with-assets/` directory
- [x] Include template file with logo and font references
- [x] Include actual asset files (logo.png, font file)
- [x] Include `conf.py` with minimal configuration
- [x] Include README explaining the example

**Validation**:
- Example builds successfully
- PDF includes logo and uses custom font
- README is clear and helpful

**Files**: `examples/template-with-assets/`

---

### Task 5.3: Update CHANGELOG
**Deliverable**: Release notes entry

- [x] Add entry under "Unreleased" or next version
- [x] Describe new feature: "Template asset auto-copy"
- [x] Mention `typst_template_assets` configuration
- [x] Note backward compatibility

**Validation**:
- CHANGELOG follows project conventions
- Entry is clear and informative

**Files**: `CHANGELOG.md`

---

## Phase 6: Polish and Release

### Task 6.1: Code quality checks
**Deliverable**: Pass all linters and type checkers

- [x] Run `uv run black .` (format code)
- [x] Run `uv run ruff check .` (lint)
- [x] Run `uv run mypy typsphinx/` (type check)
- [x] Fix any issues

**Validation**:
- All quality checks pass
- No new warnings

**Dependencies**: All implementation tasks complete

---

### Task 6.2: Final integration testing
**Deliverable**: Comprehensive validation

- [x] Test on multiple operating systems (if possible)
- [x] Test with different template structures
- [x] Test with large asset directories
- [x] Test error cases (permissions, missing files)

**Validation**:
- All tests pass on all platforms
- Edge cases handled gracefully

**Dependencies**: Task 6.1

---

### Task 6.3: Update version and prepare release
**Deliverable**: Ready for merge

- [x] Update version in `pyproject.toml` (if releasing)
- [x] Finalize CHANGELOG entry
- [x] Create pull request with clear description
- [x] Link to Issue #75

**Validation**:
- PR description explains feature clearly
- References Issue #75 with "Closes #75"
- CI/CD passes

**Dependencies**: All previous tasks

---

## Dependency Graph

```
Phase 1 (Foundation)
  ├─ 1.1 → 1.2 → 1.3

Phase 2 (Auto Copy)
  ├─ 2.1 (depends on 1.3)
  └─ 2.2 (depends on 2.1)

Phase 3 (Explicit Assets)
  ├─ 3.1 (depends on 1.3)
  ├─ 3.2 (depends on 3.1)
  └─ 3.3 (depends on 3.1)

Phase 4 (Testing)
  ├─ 4.1 (depends on 2.2, 3.3)
  ├─ 4.2 (depends on 4.1)
  └─ 4.3 (depends on 4.2)

Phase 5 (Documentation)
  ├─ 5.1 (can start anytime, finalize after 4.3)
  ├─ 5.2 (depends on 4.2)
  └─ 5.3 (depends on 4.3)

Phase 6 (Release)
  ├─ 6.1 (depends on 5.3)
  ├─ 6.2 (depends on 6.1)
  └─ 6.3 (depends on 6.2)
```

## Parallelization Opportunities

- Tasks 2.1-2.2 and 3.1-3.3 can be worked on in parallel (different code paths)
- Tasks 5.1 and 5.2 can be started early and finalized later
- Testing (Phase 4) must wait for implementation complete

## Estimated Effort

- **Phase 1**: 1-2 hours (foundation)
- **Phase 2**: 2-3 hours (auto copy logic)
- **Phase 3**: 2-3 hours (explicit assets + glob)
- **Phase 4**: 3-4 hours (comprehensive testing)
- **Phase 5**: 2-3 hours (documentation)
- **Phase 6**: 1-2 hours (polish)

**Total**: 11-17 hours (approximately 2-3 days of focused work)
