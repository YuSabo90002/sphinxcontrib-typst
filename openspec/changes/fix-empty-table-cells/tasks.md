# Tasks: Fix Empty Table Cell Rendering

## Overview

Implement the fix for Issue #68 - empty table cells causing Typst compilation errors.

**Estimated Time**: 1-2 hours
**Complexity**: Low
**Risk**: Low (single-line change with clear validation)

## Task List

### 1. Update `_format_table_cell()` method
**File**: `typsphinx/translator.py:1218`

**Change**:
```python
# Before:
return f"{indent}{content},\n"

# After:
return f"{indent}{{{content}}},\n"
```

**Validation**:
- Visual inspection: Verify syntax is correct
- Line unchanged: Spanning cell logic (line 1228) remains the same

**Dependencies**: None

---

### 2. Add unit test for empty cells
**File**: `tests/test_translator.py`

**Test**: `test_table_empty_cells()`

**Implementation**:
```python
def test_table_empty_cells(simple_document, mock_builder):
    """Test that empty table cells are wrapped in content blocks."""
    from typsphinx.translator import TypstTranslator

    translator = TypstTranslator(simple_document, mock_builder)

    # Create table with all empty cells
    table = nodes.table()
    tgroup = nodes.tgroup(cols=2)
    tgroup += nodes.colspec(colwidth=1)
    tgroup += nodes.colspec(colwidth=1)

    tbody = nodes.tbody()
    row1 = nodes.row()
    entry1 = nodes.entry()  # Empty cell
    entry2 = nodes.entry()  # Empty cell
    row1 += entry1
    row1 += entry2
    tbody += row1
    tgroup += tbody
    table += tgroup

    table.walkabout(translator)
    output = translator.astext()

    # Should contain empty content blocks
    assert "{}" in output
    # Should NOT contain bare commas
    assert ",," not in output
    assert "  ,\n" not in output
```

**Validation**:
- Run: `uv run pytest tests/test_translator.py::test_table_empty_cells -v`
- Expected: PASS

**Dependencies**: Task 1

---

### 3. Add unit test for mixed cells
**File**: `tests/test_translator.py`

**Test**: `test_table_mixed_empty_and_content()`

**Implementation**:
```python
def test_table_mixed_empty_and_content(simple_document, mock_builder):
    """Test table with both empty and non-empty cells."""
    from typsphinx.translator import TypstTranslator

    translator = TypstTranslator(simple_document, mock_builder)

    # Create table: A | (empty) / (empty) | D
    table = nodes.table()
    tgroup = nodes.tgroup(cols=2)
    tgroup += nodes.colspec(colwidth=1)
    tgroup += nodes.colspec(colwidth=1)

    tbody = nodes.tbody()

    # Row 1: A | empty
    row1 = nodes.row()
    entry1 = nodes.entry()
    entry1 += nodes.paragraph(text="A")
    entry2 = nodes.entry()  # Empty
    row1 += entry1
    row1 += entry2
    tbody += row1

    # Row 2: empty | D
    row2 = nodes.row()
    entry3 = nodes.entry()  # Empty
    entry4 = nodes.entry()
    entry4 += nodes.paragraph(text="D")
    row2 += entry3
    row2 += entry4
    tbody += row2

    tgroup += tbody
    table += tgroup

    table.walkabout(translator)
    output = translator.astext()

    # Should contain content for non-empty cells
    assert "A" in output
    assert "D" in output
    # Should contain empty content blocks
    assert "{}" in output
    # Should NOT contain bare commas
    assert ",," not in output
```

**Validation**:
- Run: `uv run pytest tests/test_translator.py::test_table_mixed_empty_and_content -v`
- Expected: PASS

**Dependencies**: Task 1

---

### 4. Add unit test for empty spanning cells
**File**: `tests/test_translator.py`

**Test**: `test_table_empty_spanning_cells()`

**Implementation**:
```python
def test_table_empty_spanning_cells(simple_document, mock_builder):
    """Test that empty cells with colspan/rowspan use table.cell with empty content."""
    from typsphinx.translator import TypstTranslator

    translator = TypstTranslator(simple_document, mock_builder)

    # Create table with empty spanning cell
    table = nodes.table()
    tgroup = nodes.tgroup(cols=2)
    tgroup += nodes.colspec(colwidth=1)
    tgroup += nodes.colspec(colwidth=1)

    tbody = nodes.tbody()
    row1 = nodes.row()

    # Empty cell with colspan=2
    entry1 = nodes.entry(morecols=1)  # Empty, spans 2 columns
    row1 += entry1
    tbody += row1
    tgroup += tbody
    table += tgroup

    table.walkabout(translator)
    output = translator.astext()

    # Should use table.cell with empty content
    assert "table.cell({}" in output
    assert "colspan: 2" in output
    # Should NOT contain bare commas or missing content
    assert "table.cell(," not in output
```

**Validation**:
- Run: `uv run pytest tests/test_translator.py::test_table_empty_spanning_cells -v`
- Expected: PASS

**Dependencies**: Task 1

---

### 5. Run existing table tests (regression check)
**Files**: All test files with table tests

**Tests to verify**:
- `test_table_conversion()`
- `test_table_cell_colspan()`
- `test_table_cell_rowspan()`
- `test_table_cell_colspan_and_rowspan()`
- `test_table_header_wrapping()`
- `test_table_without_header()`
- `test_table_multi_row_header()`
- `test_table_header_cell_with_colspan()`
- `test_table_normal_cells_without_spanning()`
- `test_table_no_duplication_all_types()`

**Validation**:
- Run: `uv run pytest tests/test_translator.py -k table -v`
- Expected: All existing tests PASS
- No regressions

**Dependencies**: Tasks 1-4

---

### 6. Integration test with Typst compilation
**File**: Create temporary test in `/tmp`

**Test Script**:
```python
# Similar to Issue #68 reproduction script
# Build RST with empty cells
# Verify Typst compilation succeeds
```

**Validation**:
- Create test RST with empty cells
- Build with sphinx-typst
- Compile generated `.typ` with `typst compile`
- Expected: Compilation SUCCESS (no "unexpected comma" errors)

**Dependencies**: Tasks 1-5

---

### 7. Update test documentation
**File**: `tests/test_translator.py`

**Changes**:
- Add docstring references to Issue #68 in new test functions
- Document the empty cell handling behavior

**Validation**:
- Review docstrings for clarity
- Ensure test names are descriptive

**Dependencies**: Tasks 2-4

---

### 8. Run full test suite
**Command**: `uv run pytest`

**Validation**:
- All tests pass
- No new failures
- No new warnings

**Dependencies**: All previous tasks

---

### 9. Format and lint code
**Commands**:
```bash
uv run black typsphinx/translator.py tests/test_translator.py
uv run ruff check typsphinx/translator.py tests/test_translator.py
```

**Validation**:
- No formatting changes needed (single-line change)
- No lint errors
- Code style compliant

**Dependencies**: Tasks 1-8

---

### 10. Create verification report
**File**: Manual verification checklist

**Checklist**:
- [ ] Code change implemented
- [ ] All new tests pass
- [ ] All existing tests pass
- [ ] Integration test with Typst succeeds
- [ ] No regressions observed
- [ ] Code formatted and linted
- [ ] Issue #68 can be closed

**Dependencies**: All previous tasks

---

## Parallel Work Opportunities

- Tasks 2, 3, 4 can be written in parallel (independent test cases)
- Task 7 can be done alongside tasks 2-4
- Tasks 9 and 10 can run concurrently

## Success Criteria

1. **Functional**: Empty cells compile successfully
2. **Tests**: All new and existing tests pass
3. **No Regressions**: Existing table functionality unchanged
4. **Documentation**: Clear test descriptions
5. **Ready for Archive**: Change can be merged to main specs

## Rollback Plan

If issues arise:
1. Revert line 1218 change
2. Re-run tests to verify revert
3. Investigate further before re-attempting

**Risk**: Very low - isolated change with comprehensive tests.
