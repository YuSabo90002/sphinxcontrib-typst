# Implementation Tasks: Convert to Function Syntax

## 1. Heading Conversion

- [ ] **Update visit_title() method** - Change from `= ` to `#heading(level: {level})[`
- [ ] **Update depart_title() method** - Change closing to `]\n\n`
- [ ] **Test heading conversion** - Verify all heading levels (1-6) work correctly
- [ ] **Update heading tests** - Update all test expectations in test_translator.py

## 2. Emphasis Conversion

- [ ] **Update visit_emphasis() method** - Change from `_` to `#emph[`
- [ ] **Update depart_emphasis() method** - Change from `_` to `]`
- [ ] **Test emphasis conversion** - Verify emphasis rendering
- [ ] **Update emphasis tests** - Update test expectations

## 3. Strong Conversion

- [ ] **Update visit_strong() method** - Change from `*` to `#strong[`
- [ ] **Update depart_strong() method** - Change from `*` to `]`
- [ ] **Test strong conversion** - Verify strong rendering
- [ ] **Update strong tests** - Update test expectations
- [ ] **Test nested emphasis/strong** - Verify `#strong[text with #emph[emphasis]]` works

## 4. Subtitle Conversion

- [ ] **Update visit_subtitle() method** - Change from `_` to `#emph[`
- [ ] **Update depart_subtitle() method** - Change from `_\n\n` to `]\n\n`
- [ ] **Test subtitle conversion** - Verify subtitle rendering
- [ ] **Update subtitle tests** - Update test expectations

## 5. Bullet List Conversion

- [ ] **Redesign bullet list implementation** - Implement item collection and batch output
- [ ] **Update visit_bullet_list() method** - Initialize list item collection
- [ ] **Update depart_bullet_list() method** - Output `#list([item1], [item2], ...)` format
- [ ] **Update visit_list_item() method** - Collect list items instead of immediate output
- [ ] **Update depart_list_item() method** - Finalize list item collection
- [ ] **Test simple bullet lists** - Verify basic list rendering
- [ ] **Test nested bullet lists** - Verify nested list structure
- [ ] **Update bullet list tests** - Update all test expectations

## 6. Enumerated List Conversion

- [ ] **Redesign enumerated list implementation** - Implement item collection and batch output
- [ ] **Update visit_enumerated_list() method** - Initialize list item collection
- [ ] **Update depart_enumerated_list() method** - Output `#enum([item1], [item2], ...)` format
- [ ] **Update list_item handling for enum** - Handle both bullet and enum in same method
- [ ] **Test simple enumerated lists** - Verify basic enum rendering
- [ ] **Test nested enumerated lists** - Verify nested enum structure
- [ ] **Test mixed nested lists** - Verify bullet lists containing enum lists and vice versa
- [ ] **Update enumerated list tests** - Update all test expectations

## 7. Integration Testing

- [ ] **Run full test suite** - Execute `uv run pytest` and verify all tests pass
- [ ] **Test complex documents** - Verify documents with mixed elements
- [ ] **Test nested structures** - Verify deeply nested lists, emphasis in headings, etc.
- [ ] **Regression test** - Verify existing functionality still works

## 8. Documentation Updates

- [ ] **Update CHANGELOG.md** - Document breaking change
- [ ] **Create migration guide** - Explain changes to users
- [ ] **Update examples** - Regenerate example .typ files
- [ ] **Update documentation** - Reflect new output syntax in docs

## 9. PDF Output Verification

- [ ] **Build typsphinx docs** - Generate PDF with new syntax
- [ ] **Visual comparison** - Verify PDF output is identical to previous version
- [ ] **Test with real projects** - Verify compatibility with actual use cases

## 10. Validation and Quality

- [ ] **Run mypy** - Type-check new code with `uv run mypy typsphinx/`
- [ ] **Run black** - Format code with `uv run black .`
- [ ] **Run ruff** - Lint code with `uv run ruff check .`
- [ ] **Run tox** - Test across all supported Python versions
- [ ] **Verify spec compliance** - Run `openspec validate convert-to-function-syntax --strict`
