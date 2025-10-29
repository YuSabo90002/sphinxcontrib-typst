# Proposal: Fix Empty Table Cell Rendering

## Summary

Fix the bug where empty table cells generate invalid Typst syntax. Currently, empty cells output bare commas (`,`) without content blocks (`{}`), causing Typst compilation errors. This proposal ensures all table cells are wrapped in content blocks (`{}`) as required by Typst's type system.

## Problem Statement

**Issue**: [#68 - Empty table cells cause Typst compilation errors](https://github.com/YuSabo90002/typsphinx/issues/68)

When reStructuredText tables contain empty cells, sphinx-typst generates invalid Typst code:

```typst
table(
  columns: 2,
  par({text("A")}),
  ,                    // ❌ ERROR: unexpected comma
  ,                    // ❌ ERROR: unexpected comma
  par({text("D")}),
)
```

**Root Cause**: The `_format_table_cell()` method (translator.py:1218) outputs content directly:
```python
return f"{indent}{content},\n"
```

When `content` is empty, this produces `,` which is invalid Typst syntax.

**Typst Requirement**: Table cells are `content` type and must be wrapped in content blocks:
- Non-empty cells: `{par({text("data")})},`
- Empty cells: `{},`

## Why

This fix is necessary because:

1. **Blocks User Workflows**: Users cannot build documents with tables containing empty cells, which is a common use case in documentation (e.g., comparison tables, template tables, partially filled data tables).

2. **Violates Typst Type System**: Typst's `table()` function requires all cells to be `content` type. Bare commas without content blocks violate this requirement and cause compilation failures.

3. **Inconsistent with Typst Idioms**: The Unified Code Mode guideline already established that we use content types directly. All table cells should consistently use content blocks `{}`, whether empty or not.

4. **High-Severity Bug**: This is a compilation blocker - documents with empty table cells cannot be built at all, making this a high-priority fix.

5. **Simple Fix, High Impact**: The fix is a single-line change, but it unlocks the ability to use empty cells in all table types (list-table, grid table, simple table, csv-table) across all cell configurations (normal, colspan, rowspan, headers).

## Impact

- **Severity**: High - Causes compilation failures for any table with empty cells
- **Scope**: All table types (list-table, grid table, simple table, csv-table)
- **User Facing**: Yes - Blocks document generation

## Solution Approach

Wrap all table cells in content blocks (`{}`), consistent with Typst's type requirements:

```python
# Normal cell (no spanning)
if colspan == 1 and rowspan == 1:
    return f"{indent}{{{content}}},\n"
```

This ensures:
- Non-empty cells: `{par({text("data")})},`
- Empty cells: `{},` ✓ Valid Typst syntax

**Note**: Spanning cells using `table.cell()` already handle content correctly as the first argument is typed as `content`, so no changes needed there.

## Scope

### In Scope
- Fix `_format_table_cell()` to wrap normal cells in content blocks
- Add test cases for empty cells
- Verify existing tests still pass (backwards compatibility)

### Out of Scope
- Changes to spanning cell logic (already correct)
- Changes to table structure generation
- Performance optimizations

## Related Work

- **Unified Code Mode**: This aligns with the Unified Code Mode guideline that uses content types directly
- **Issue #5**: Similar path resolution fix for nested documents
- **Table Rendering Spec**: Updates existing `table-rendering` spec

## Validation Criteria

1. **Functional**:
   - Empty cells compile without errors
   - Non-empty cells continue to work
   - Spanning cells continue to work

2. **Test Coverage**:
   - Unit test: `test_table_empty_cells()` - All empty cells
   - Unit test: `test_table_mixed_empty_and_content()` - Mixed empty/non-empty
   - Unit test: `test_table_empty_colspan_cells()` - Empty cells with colspan
   - Unit test: `test_table_empty_rowspan_cells()` - Empty cells with rowspan
   - Unit test: `test_table_empty_colspan_rowspan_cells()` - Empty cells with both
   - Integration test: Build and compile tables with empty cells

3. **No Regressions**:
   - All existing table tests pass
   - `test_table_conversion()`, `test_table_cell_colspan()`, etc.

## Dependencies

None - self-contained fix to a single method.

## Timeline

- Estimated effort: Small (1-2 hours)
- Low complexity: Single line change + tests
- No breaking changes

## Questions for Review

None - straightforward bug fix with clear solution.
