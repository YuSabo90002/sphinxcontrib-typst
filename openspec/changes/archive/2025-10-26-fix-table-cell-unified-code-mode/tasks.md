# Tasks: fix-table-cell-unified-code-mode

## Overview

tableセル生成をUnified Code Mode指針に準拠させる。マークアップモード `[...]` を削除し、content型を直接渡すように修正する。

## Task List

### 1. Create feature branch
- [x] Create branch `fix/table-cell-unified-code-mode` from `main`
- [x] Verify branch is clean and up-to-date

**Validation**: `git status` shows clean working directory

---

### 2. Modify `_format_table_cell()` - Normal cells
- [x] Update `typsphinx/translator.py:1218`
- [x] Change `return f"{indent}[{content}],\n"` to `return f"{indent}{content},\n"`
- [x] Remove markdown wrapping `[...]` from normal cells (already done in previous work)

**File**: `typsphinx/translator.py`
**Location**: Line 1218 (in the `if colspan == 1 and rowspan == 1:` block)

**Before**:
```python
# Normal cell (no spanning)
if colspan == 1 and rowspan == 1:
    return f"{indent}[{content}],\n"
```

**After**:
```python
# Normal cell (no spanning)
if colspan == 1 and rowspan == 1:
    return f"{indent}{content},\n"
```

**Validation**: Code review - verify syntax is correct

---

### 3. Modify `_format_table_cell()` - Spanning cells
- [x] Update `typsphinx/translator.py:1228`
- [x] Change `return f"{indent}table.cell({params_str})[{content}],\n"` to `return f"{indent}table.cell({content}, {params_str}),\n"`
- [x] Fix argument order: content as first positional argument
- [x] Remove markdown wrapping `[...]`

**File**: `typsphinx/translator.py`
**Location**: Line 1228 (in the spanning cell block)

**Before**:
```python
params_str = ", ".join(params)
return f"{indent}table.cell({params_str})[{content}],\n"
```

**After**:
```python
params_str = ", ".join(params)
return f"{indent}table.cell({content}, {params_str}),\n"
```

**Validation**: Code review - verify argument order matches Typst signature

---

### 4. Run all table tests
- [x] Execute `uv run pytest tests/test_translator.py -k table -v`
- [x] Verify all 11 table tests pass (updated test assertions for new syntax)
- [x] Review test output for any unexpected failures

**Expected**: All 10 tests pass without modifications

**Tests**:
- `test_table_conversion`
- `test_table_no_duplication_all_types`
- `test_table_header_wrapping`
- `test_table_without_header`
- `test_table_multi_row_header`
- `test_table_cell_colspan`
- `test_table_cell_rowspan`
- `test_table_cell_colspan_and_rowspan`
- `test_table_header_cell_with_colspan`
- `test_table_normal_cells_without_spanning`

**Validation**: All tests green in pytest output

---

### 5. Verify Typst syntax with manual test
- [x] Create test Typst file with new syntax
- [x] Compile with `typst compile` to verify syntax
- [x] Compare output with old syntax

**Test file** (`/tmp/test-new-table-syntax.typ`):
```typst
#{
  // Normal cells without markup mode
  table(
    columns: 2,
    par({text("Cell 1")}),
    par({text("Cell 2")}),
  )

  // Spanning cells with content as first argument
  table(
    columns: 3,
    table.cell(par({text("Spans 2 cols")}), colspan: 2),
    par({text("Col 3")}),
  )
}
```

**Validation**: `typst compile /tmp/test-new-table-syntax.typ /tmp/output.pdf` succeeds

---

### 6. Build documentation with new syntax
- [x] Build Typst output: `uv run tox -e docs` (builds both HTML and PDF)
- [x] Build PDF: `uv run tox -e docs` (included in docs target)
- [x] Verify no compilation errors
- [x] Inspect generated table in `docs/_build/pdf/user_guide/builders.typ`

**Validation**:
- Build succeeds
- Generated Typst uses new syntax (no `[...]` around table cells)
- PDF renders correctly

---

### 7. Run full test suite
- [x] Execute `uv run pytest`
- [x] Verify all 375 tests pass
- [x] Check coverage remains ≥91%

**Validation**:
- Test output: `375 passed`
- Coverage: `TOTAL ... 91%`

---

### 8. Code quality checks
- [x] Run formatter: `uv run black typsphinx/translator.py tests/test_translator.py`
- [x] Run linter: `uv run ruff check typsphinx/translator.py tests/test_translator.py`
- [x] Run type checker: `uv run mypy typsphinx/translator.py`

**Validation**: All checks pass with no errors

---

### 9. Commit changes
- [x] Stage changes: `git add typsphinx/translator.py tests/test_translator.py`
- [x] Commit with message:

```
fix: table cells use content type directly without markup mode

Remove `[...]` markup mode wrapping from table cells to comply with
Unified Code Mode guideline. Table cells now pass content type directly.

Changes:
- Normal cells: `[{content}]` → `{content}`
- Spanning cells: `table.cell({params})[{content}]` → `table.cell({content}, {params})`

This fixes the argument order for table.cell() to match Typst signature
(content as first positional argument) and removes unnecessary markup mode.

Refs: openspec/changes/fix-table-cell-unified-code-mode

🤖 Generated with [Claude Code](https://claude.com/claude-code)

Co-Authored-By: Claude <noreply@anthropic.com>
```

**Validation**: `git log -1` shows commit

---

### 10. Push and create PR
- [x] Push branch: `git push origin fix/table-cell-unified-code-mode`
- [x] Create PR to `main` with description from proposal
- [x] Link to OpenSpec change in PR description

**PR URL**: https://github.com/YuSabo90002/typsphinx/pull/65

**PR Title**: `Fix: Table cells comply with Unified Code Mode`

**PR Description**: See `openspec/changes/fix-table-cell-unified-code-mode/proposal.md`

**Validation**: PR created on GitHub

---

## Dependencies

None. This is an isolated change to table cell formatting.

## Parallel Work

None. All tasks must be completed sequentially.

## Success Criteria

- ✅ All 375 tests pass
- ✅ Code quality checks pass (black, ruff, mypy)
- ✅ Documentation builds successfully
- ✅ Generated Typst files use new syntax (no `[...]` around cells)
- ✅ PDF output is correct
- ✅ Unified Code Mode compliance achieved
