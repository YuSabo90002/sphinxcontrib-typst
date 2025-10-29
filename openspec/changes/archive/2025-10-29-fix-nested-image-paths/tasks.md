# Tasks: Fix Image Relative Paths in Nested Documents

## Overview

Implement the fix for Issue #69 - image relative paths broken in nested documents.

**Estimated Time**: 2-3 hours
**Complexity**: Low (reuse existing pattern from Issue #5)
**Risk**: Low (isolated change with existing reference implementation)
**Total Tasks**: 13

## Task List

### 1. Add `_compute_relative_image_path()` method

- [x] Add method to `TypstTranslator` class similar to `_compute_relative_include_path()`

**File**: `typsphinx/translator.py`

**Location**: After `_compute_relative_include_path()` method (around line 1700)

**Implementation**:
```python
def _compute_relative_image_path(
    self, image_uri: str, current_docname: Optional[str]
) -> str:
    """
    Compute relative path for image() function.

    Adjusts image URIs from source-root-relative to output-file-relative.
    This is similar to _compute_relative_include_path() but for images.

    Args:
        image_uri: Image URI from Sphinx (source-root-relative)
        current_docname: Current document name (e.g., "chapter1/section1")

    Returns:
        Adjusted relative path for Typst image()

    Examples:
        >>> _compute_relative_image_path("images/logo.png", "chapter1/section1")
        "../images/logo.png"
        >>> _compute_relative_image_path("images/logo.png", "index")
        "images/logo.png"
        >>> _compute_relative_image_path("images/logo.png", None)
        "images/logo.png"

    Notes:
        This implements Issue #69 fix for nested document image paths.
        Uses the same logic as _compute_relative_include_path() from Issue #5.
    """
    from pathlib import PurePosixPath

    logger.debug(
        f"Computing relative image path: uri={image_uri}, "
        f"current={current_docname}"
    )

    # Fallback to absolute path if current_docname is None
    if not current_docname:
        logger.debug(f"No current document, using absolute path: {image_uri}")
        return image_uri

    current_path = PurePosixPath(current_docname)
    image_path = PurePosixPath(image_uri)
    current_dir = current_path.parent

    logger.debug(
        f"Path components: current_dir={current_dir}, image_path={image_path}"
    )

    # Root directory case: use absolute path (backward compatibility)
    if current_dir == PurePosixPath("."):
        logger.debug(
            f"Current document is in root directory, "
            f"using absolute path: {image_uri}"
        )
        return image_uri

    # Try to compute relative path
    try:
        rel_path = image_path.relative_to(current_dir)
        result = str(rel_path)
        logger.debug(
            f"Same directory reference: {current_dir} -> {image_path}, "
            f"result: {result}"
        )
        return result
    except ValueError:
        # Different directory trees - build path via common parent
        logger.debug(
            "Cross-directory reference detected, calculating via common parent"
        )

        current_parts = current_dir.parts
        image_parts = image_path.parts

        # Find common parent by comparing path components
        common_length = 0
        for i, (c, img) in enumerate(zip(current_parts, image_parts)):
            if c == img:
                common_length = i + 1
            else:
                break

        logger.debug(
            f"Common parent depth: {common_length}, "
            f"current_parts={current_parts}, image_parts={image_parts}"
        )

        # Build path: "../" from current to common parent
        up_count = len(current_parts) - common_length
        up_path = "../" * up_count if up_count > 0 else ""

        # Build path: from common parent to image
        down_parts = image_parts[common_length:]
        down_path = "/".join(down_parts) if down_parts else ""

        relative_path: str = up_path + down_path

        logger.debug(
            f"Cross-directory path calculation: up_count={up_count}, "
            f"up_path='{up_path}', down_path='{down_path}', "
            f"result: {relative_path}"
        )

        return relative_path
```

**Validation**:
- Visual inspection: Verify syntax is correct
- Logic matches `_compute_relative_include_path()`
- Type hints are complete

**Dependencies**: None

---

### 2. Update `visit_image()` to use path adjustment

- [x] Modify `visit_image()` method to call `_compute_relative_image_path()`

**File**: `typsphinx/translator.py:1462-1489`

**Change**:
```python
def visit_image(self, node: nodes.image) -> None:
    """
    Visit an image node.

    Generates image() function call (no # prefix in code mode).
    Adjusts image paths for nested documents (Issue #69).

    Args:
        node: The image node
    """
    uri = node.get("uri", "")

    # Get current document name for path adjustment
    current_docname = getattr(self.builder, "current_docname", None)

    # Adjust path based on output file location (Issue #69)
    adjusted_uri = self._compute_relative_image_path(uri, current_docname)

    # Add proper indentation if inside a figure
    if self.in_figure:
        self.add_text(f'  image("{adjusted_uri}"')
    else:
        # No # prefix in code mode
        self.add_text(f'image("{adjusted_uri}"')

    # Add optional attributes
    if "width" in node:
        width = node["width"]
        self.add_text(f", width: {width}")

    if "height" in node:
        height = node["height"]
        self.add_text(f", height: {height}")

    self.add_text(")")
```

**Validation**:
- Visual inspection: Verify integration is correct
- Logic flow: uri → adjusted_uri → output
- Backward compatibility: `current_docname=None` case handled

**Dependencies**: Task 1

---

### 3. Add unit test for root document images

- [x] Add `test_image_path_adjustment_root()` to verify root documents unchanged

**File**: `tests/test_translator.py`

**Test**: `test_image_path_adjustment_root()`

**Implementation**:
```python
def test_image_path_adjustment_root(simple_document, mock_builder):
    """Test that root document image paths are not adjusted.

    Related to Issue #69: Image paths in root documents should remain unchanged.
    """
    from typsphinx.translator import TypstTranslator

    translator = TypstTranslator(simple_document, mock_builder)

    # Set current_docname to root document
    mock_builder.current_docname = "index"

    # Create image node
    image = nodes.image(uri="images/logo.png")
    image["width"] = "200px"

    image.walkabout(translator)
    output = translator.astext()

    # Root document: path should NOT be adjusted
    assert 'image("images/logo.png"' in output
    assert "../images" not in output
    assert "width: 200px" in output
```

**Validation**:
- Run: `uv run pytest tests/test_translator.py::test_image_path_adjustment_root -v`
- Expected: PASS

**Dependencies**: Task 2

---

### 4. Add unit test for nested document images

- [x] Add `test_image_path_adjustment_nested()` for nested documents

**File**: `tests/test_translator.py`

**Test**: `test_image_path_adjustment_nested()`

**Implementation**:
```python
def test_image_path_adjustment_nested(simple_document, mock_builder):
    """Test that nested document image paths are adjusted with ../ prefix.

    Related to Issue #69: Nested documents need relative path adjustment.
    """
    from typsphinx.translator import TypstTranslator

    translator = TypstTranslator(simple_document, mock_builder)

    # Set current_docname to nested document
    mock_builder.current_docname = "chapter1/section1"

    # Create image node with source-root-relative path
    image = nodes.image(uri="images/logo.png")
    image["width"] = "200px"

    image.walkabout(translator)
    output = translator.astext()

    # Nested document: path should be adjusted
    assert 'image("../images/logo.png"' in output
    assert "width: 200px" in output
```

**Validation**:
- Run: `uv run pytest tests/test_translator.py::test_image_path_adjustment_nested -v`
- Expected: PASS

**Dependencies**: Task 2

---

### 5. Add unit test for deeply nested documents

- [x] Add `test_image_path_adjustment_deep_nested()` for deep nesting

**File**: `tests/test_translator.py`

**Test**: `test_image_path_adjustment_deep_nested()`

**Implementation**:
```python
def test_image_path_adjustment_deep_nested(simple_document, mock_builder):
    """Test that deeply nested documents get correct number of ../ prefixes.

    Related to Issue #69: Deep nesting requires multiple ../ levels.
    """
    from typsphinx.translator import TypstTranslator

    translator = TypstTranslator(simple_document, mock_builder)

    # Set current_docname to deeply nested document
    mock_builder.current_docname = "part1/chapter1/section1"

    # Create image node
    image = nodes.image(uri="images/logo.png")

    image.walkabout(translator)
    output = translator.astext()

    # Deeply nested: should have ../../ prefix
    assert 'image("../../images/logo.png"' in output
```

**Validation**:
- Run: `uv run pytest tests/test_translator.py::test_image_path_adjustment_deep_nested -v`
- Expected: PASS

**Dependencies**: Task 2

---

### 6. Add unit test for cross-directory references

- [x] Add `test_image_path_adjustment_cross_directory()` for cross-directory cases

**File**: `tests/test_translator.py`

**Test**: `test_image_path_adjustment_cross_directory()`

**Implementation**:
```python
def test_image_path_adjustment_cross_directory(simple_document, mock_builder):
    """Test that cross-directory image references are correctly adjusted.

    Related to Issue #69: References from chapter1/ to chapter2/ images.
    """
    from typsphinx.translator import TypstTranslator

    translator = TypstTranslator(simple_document, mock_builder)

    # Set current document in chapter1
    mock_builder.current_docname = "chapter1/section1"

    # Reference image in chapter2
    image = nodes.image(uri="chapter2/images/diagram.png")

    image.walkabout(translator)
    output = translator.astext()

    # Cross-directory: ../chapter2/images/diagram.png
    assert 'image("../chapter2/images/diagram.png"' in output
```

**Validation**:
- Run: `uv run pytest tests/test_translator.py::test_image_path_adjustment_cross_directory -v`
- Expected: PASS

**Dependencies**: Task 2

---

### 7. Add unit test for same directory images

- [x] Add `test_image_path_adjustment_same_directory()` for same-directory references

**File**: `tests/test_translator.py`

**Test**: `test_image_path_adjustment_same_directory()`

**Implementation**:
```python
def test_image_path_adjustment_same_directory(simple_document, mock_builder):
    """Test that same-directory images use simple relative paths.

    Related to Issue #69: Images in the same directory as the document.
    """
    from typsphinx.translator import TypstTranslator

    translator = TypstTranslator(simple_document, mock_builder)

    # Both in chapter1/
    mock_builder.current_docname = "chapter1/section1"

    # Image also in chapter1/
    image = nodes.image(uri="chapter1/local-image.png")

    image.walkabout(translator)
    output = translator.astext()

    # Same directory: just the filename
    assert 'image("local-image.png"' in output
    assert "../" not in output
```

**Validation**:
- Run: `uv run pytest tests/test_translator.py::test_image_path_adjustment_same_directory -v`
- Expected: PASS

**Dependencies**: Task 2

---

### 8. Add unit test for subdirectory images

- [x] Add `test_image_path_adjustment_subdirectory()` for subdirectory (child folder) references

**File**: `tests/test_translator.py`

**Test**: `test_image_path_adjustment_subdirectory()`

**Implementation**:
```python
def test_image_path_adjustment_subdirectory(simple_document, mock_builder):
    """Test that subdirectory images use relative paths to child folders.

    Related to Issue #69: Images in subdirectories relative to the document.
    Example: chapter1/section1.rst references chapter1/img/diagram.jpeg
    """
    from typsphinx.translator import TypstTranslator

    translator = TypstTranslator(simple_document, mock_builder)

    # Document in chapter1/
    mock_builder.current_docname = "chapter1/section1"

    # Image in chapter1/img/ (subdirectory of same directory)
    image = nodes.image(uri="chapter1/img/diagram.jpeg")
    image["width"] = "250px"

    image.walkabout(translator)
    output = translator.astext()

    # Subdirectory: img/diagram.jpeg (relative to current directory)
    assert 'image("img/diagram.jpeg"' in output
    assert "width: 250px" in output
    assert "../" not in output  # No need to go up
```

**Validation**:
- Run: `uv run pytest tests/test_translator.py::test_image_path_adjustment_subdirectory -v`
- Expected: PASS

**Dependencies**: Task 2

---

### 9. Run existing image tests (regression check)

- [x] Run all existing image-related tests to verify no regressions

**Command**: `uv run pytest tests/ -k image -v`

**Tests to verify**:
- Any existing image tests in `test_translator.py`
- Image tests in `test_integration_*` files
- Figure tests (use `visit_image()` internally)

**Validation**:
- All existing tests PASS
- No regressions in image handling
- Root document behavior unchanged

**Dependencies**: Tasks 1-7

---

### 9. Add integration test with nested documents and images

- [x] Create integration test that builds and compiles nested documents with images

**File**: `tests/test_integration_nested_images.py` (new file) or add to existing integration test file

**Test**: `test_nested_documents_with_images_e2e()`

**Implementation**:
```python
def test_nested_documents_with_images_e2e(tmp_path):
    """E2E test: Build nested documents with images and verify Typst compilation.

    Related to Issue #69: Full integration test for image path adjustment.
    """
    import subprocess
    import base64
    from pathlib import Path

    # Create test project structure
    source_dir = tmp_path / "source"
    build_dir = tmp_path / "build"
    (source_dir / "images").mkdir(parents=True)
    (source_dir / "chapter1").mkdir(parents=True)

    # Create conf.py
    (source_dir / "conf.py").write_text("""
project = 'Image Path Test'
extensions = ['typsphinx']
""")

    # Create index.rst with image (root)
    (source_dir / "index.rst").write_text("""
Test
====

.. image:: images/logo.png
   :width: 100px

.. toctree::
   chapter1/section1
""")

    # Create chapter1/section1.rst with image (nested)
    (source_dir / "chapter1/section1.rst").write_text("""
Section 1
=========

.. image:: ../images/logo.png
   :width: 200px
""")

    # Create dummy image
    png_data = base64.b64decode(
        'iVBORw0KGgoAAAANSUhEUgAAAAEAAAABCAYAAAAfFcSJAAAADUlEQVR42mNkYPhfDwAChwGA60e6kgAAAABJRU5ErkJggg=='
    )
    (source_dir / "images/logo.png").write_bytes(png_data)

    # Build with sphinx-typst
    from sphinx.cmd.build import build_main
    result = build_main(['-b', 'typst', str(source_dir), str(build_dir)])
    assert result == 0, "Sphinx build failed"

    # Check generated files
    index_typ = build_dir / "index.typ"
    section_typ = build_dir / "chapter1/section1.typ"
    assert index_typ.exists()
    assert section_typ.exists()

    # Verify root document has non-adjusted path
    index_content = index_typ.read_text()
    assert 'image("images/logo.png"' in index_content

    # Verify nested document has adjusted path
    section_content = section_typ.read_text()
    assert 'image("../images/logo.png"' in section_content

    # Verify Typst compilation succeeds
    try:
        subprocess.run(
            ['typst', 'compile', '--root', str(build_dir), str(section_typ)],
            check=True, capture_output=True, text=True
        )
    except subprocess.CalledProcessError as e:
        pytest.fail(f"Typst compilation failed: {e.stderr}")
```

**Validation**:
- Run: `uv run pytest tests/test_integration_nested_images.py -v`
- Expected: Full build and Typst compilation SUCCESS

**Dependencies**: Tasks 1-9

---

### 11. Run full test suite

- [x] Run complete test suite to verify all tests pass

**Command**: `uv run pytest`

**Validation**:
- All tests pass (380+ tests)
- No new failures
- No new warnings
- Image path adjustment works correctly

**Dependencies**: All previous tasks

---

### 12. Format, lint, and type check code

- [x] Format, lint, and type check the modified code

**Commands**:
```bash
uv run black typsphinx/translator.py tests/
uv run ruff check typsphinx/translator.py tests/
uv run mypy typsphinx/translator.py tests/
```

**Validation**:
- No formatting changes needed
- No lint errors
- No type errors
- Code style compliant

**Dependencies**: Tasks 1-11

---

### 13. Update documentation comments

- [x] Ensure method docstrings reference Issue #69

**File**: `typsphinx/translator.py`

**Changes**:
- Add Issue #69 reference to `_compute_relative_image_path()` docstring
- Add Issue #69 reference to `visit_image()` docstring
- Ensure examples are clear and accurate

**Validation**:
- Review docstrings for clarity
- Verify Issue references are correct

**Dependencies**: Tasks 1-2

---

## Parallel Work Opportunities

- Tasks 3, 4, 5, 6, 7, 8 can be written in parallel (independent test cases)
- Task 13 can be done alongside implementation tasks

## Success Criteria

1. **Functional**: Nested document images compile successfully with Typst
2. **Tests**: All new and existing tests pass
3. **No Regressions**: Root document images unchanged
4. **Documentation**: Clear docstrings with Issue #69 references
5. **Ready for Archive**: Change can be merged to main specs

## Rollback Plan

If issues arise:
1. Revert changes to `visit_image()` and remove `_compute_relative_image_path()`
2. Re-run tests to verify revert
3. Investigate further before re-attempting

**Risk**: Very low - mirrors successful Issue #5 implementation.
