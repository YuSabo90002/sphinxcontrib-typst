# Proposal: Fix Image Relative Paths in Nested Documents

## Summary

Fix the bug where image references in nested documents (documents in subdirectories) generate incorrect Typst paths that fail to resolve during compilation. Sphinx normalizes all image URIs to be relative to the source directory root, but sphinx-typst outputs these paths directly without adjusting them based on the output file location.

## Problem Statement

**Issue**: [#69 - Image relative paths broken in nested documents](https://github.com/YuSabo90002/typsphinx/issues/69)

When reStructuredText documents in subdirectories reference images, sphinx-typst generates incorrect Typst code:

```rst
# File: chapter1/section1.rst
.. image:: ../images/logo.png
   :width: 200px
```

**Current Behavior** (chapter1/section1.typ):
```typst
image("images/logo.png", width: 200px)
```

Typst looks for: `chapter1/images/logo.png` ❌ **File not found**

**Expected Behavior** (chapter1/section1.typ):
```typst
image("../images/logo.png", width: 200px)
```

Typst looks for: `images/logo.png` ✓ **Correct**

**Root Cause**: Sphinx normalizes all image URIs to source-root-relative paths, but sphinx-typst outputs these paths directly without adjusting them based on the output file's location in the directory tree.

## Why

This fix is necessary because:

1. **Blocks Nested Document Workflows**: Users cannot use images in nested documents, which is essential for organizing large documentation projects with chapter/section structure.

2. **Inconsistent with Toctree Fix**: Issue #5 fixed the same problem for `#include()` paths in toctrees, but image paths were not addressed at the same time.

3. **Breaks Typst Compilation**: Documents with images in nested directories fail to compile, making the feature non-functional for typical documentation structures.

4. **Common Use Case**: Multi-chapter documentation with shared image directories is a standard pattern (e.g., `chapters/chapter1/`, `chapters/chapter2/`, shared `images/` directory).

## What Changes

### Code Changes

**Modified**: `typsphinx/translator.py`

1. Add `_compute_relative_image_path()` method (similar to `_compute_relative_include_path()` from Issue #5):
   - Calculate relative paths from output file location to image location
   - Handle root documents (no adjustment needed)
   - Handle nested documents (add `../` prefixes as needed)
   - Handle cross-directory references

2. Update `visit_image()` method to use path adjustment:
   - Get `current_docname` from builder
   - Call `_compute_relative_image_path()` to adjust URI
   - Output adjusted path in `image()` function

### Test Changes

**Modified**: `tests/test_translator.py`

Add comprehensive test coverage:
- Unit tests for path calculation logic
- Tests for root document images (no adjustment)
- Tests for nested document images (with `../`)
- Tests for deeply nested documents
- Tests for cross-directory references

**Modified**: `tests/test_integration_advanced.py` or new integration test

Add end-to-end tests:
- Build nested documents with images
- Verify Typst compilation succeeds
- Verify images are correctly resolved

## Impact

- **Severity**: High - Blocks image usage in nested documents
- **Scope**: All nested documents with images
- **User Facing**: Yes - Currently broken functionality becomes working
- **Breaking Changes**: None - Root document images continue to work, nested documents are currently broken

## Solution Approach

Mirror the approach from Issue #5 (toctree relative paths):

1. **Reuse Path Calculation Pattern**: The `_compute_relative_include_path()` method already solves this exact problem for include directives. Apply the same logic to image paths.

2. **Minimal Changes**: Only modify the `visit_image()` method to call the new path calculation helper.

3. **Consistent Behavior**: Images and includes will use the same relative path calculation logic, ensuring consistency.

## Scope

### In Scope
- Fix `visit_image()` to adjust image paths for nested documents
- Add `_compute_relative_image_path()` method
- Add comprehensive test coverage
- Verify existing tests still pass (backward compatibility)

### Out of Scope
- Changes to image copying logic (already works correctly)
- Changes to figure handling
- Changes to other asset types (CSS, JS)
- Performance optimizations

## Related Work

- **Issue #5**: Fixed toctree relative paths for nested documents (same class of problem)
- **`_compute_relative_include_path()` method**: Reference implementation for path calculation
- **document-conversion spec**: Existing image handling requirements

## Validation Criteria

1. **Functional**:
   - Root document images continue to work (no regression)
   - Nested document images work correctly
   - Deeply nested documents work correctly
   - Cross-directory references work correctly

2. **Test Coverage**:
   - Unit tests for `_compute_relative_image_path()` logic
   - Unit tests for various nesting levels
   - Integration test: Build and compile nested documents with images
   - All existing tests pass

3. **No Regressions**:
   - Existing image tests pass
   - Root document images unchanged
   - Image copying logic unchanged

## Dependencies

None - self-contained fix similar to Issue #5.

## Timeline

- Estimated effort: Small (2-3 hours)
- Low complexity: Reuse existing pattern from Issue #5
- No breaking changes
- Similar scope to Issue #68 (empty table cells)

## Questions for Review

None - straightforward bug fix following established patterns (Issue #5).
