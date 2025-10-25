# Implementation Tasks: Add Autodoc Node Support

## 1. Index Node Support

- [x] **Implement visit_index() method** - Add to translator.py to skip index nodes (Typst doesn't need index entries)
- [x] **Implement depart_index() method** - Add to translator.py
- [x] **Test index node handling** - Add unit test in tests/test_translator.py

## 2. Desc Nodes Support (API Descriptions)

- [x] **Implement visit_desc() method** - Add container for API description blocks
- [x] **Implement depart_desc() method** - Close API description blocks
- [x] **Implement visit_desc_signature() method** - Format function/class signatures
- [x] **Implement depart_desc_signature() method** - Close signature blocks
- [x] **Implement visit_desc_content() method** - Handle description content
- [x] **Implement depart_desc_content() method** - Close content blocks
- [x] **Implement visit_desc_annotation() method** - Format type annotations (e.g., "class" keyword)
- [x] **Implement depart_desc_annotation() method** - Close annotations
- [x] **Implement visit_desc_addname() method** - Handle module name prefixes
- [x] **Implement depart_desc_addname() method** - Close addname
- [x] **Implement visit_desc_name() method** - Format function/class names
- [x] **Implement depart_desc_name() method** - Close name
- [x] **Implement visit_desc_parameterlist() method** - Start parameter list
- [x] **Implement depart_desc_parameterlist() method** - Close parameter list
- [x] **Implement visit_desc_parameter() method** - Format individual parameters
- [x] **Implement depart_desc_parameter() method** - Close parameter
- [x] **Test desc node family** - Add comprehensive tests for all desc nodes
- [x] **Implement desc_sig_* nodes** - Added visit/depart methods for desc_sig_keyword, desc_sig_space, desc_sig_name, desc_sig_punctuation, desc_sig_operator

## 3. Field List Nodes Support

- [x] **Implement visit_field_list() method** - Start field list container
- [x] **Implement depart_field_list() method** - Close field list
- [x] **Implement visit_field() method** - Handle individual fields
- [x] **Implement depart_field() method** - Close field
- [x] **Implement visit_field_name() method** - Format field names (e.g., "Parameters:", "Returns:")
- [x] **Implement depart_field_name() method** - Close field name
- [x] **Implement visit_field_body() method** - Handle field content
- [x] **Implement depart_field_body() method** - Close field body
- [x] **Test field list nodes** - Add tests for field list rendering

## 4. Additional Nodes Support

- [x] **Implement visit_rubric() method** - Format section headings in API docs
- [x] **Implement depart_rubric() method** - Close rubric
- [x] **Implement visit_title_reference() method** - Handle title references
- [x] **Implement depart_title_reference() method** - Close title reference
- [x] **Test additional nodes** - Add tests for rubric and title_reference
- [x] **Implement literal_strong/literal_emphasis** - Added visit/depart methods for literal formatting in field lists

## 5. Integration Testing

- [x] **Create integration test fixture** - Added unit tests in tests/test_translator.py
- [x] **Test full API documentation build** - Full test in test_full_api_description_structure
- [x] **Verify no warnings** - Confirmed "unknown node type" warnings eliminated (0 autodoc warnings)
- [x] **Regression test for Issue #55** - Verified with `uv run tox -e docs-pdf` - no autodoc node warnings

## 6. Validation and Quality

- [x] **Run pytest** - All 85 tests pass with `uv run pytest tests/test_translator.py`
- [x] **Run mypy** - Type-check passed: `Success: no issues found in 1 source file`
- [x] **Run black** - Code formatted: `2 files left unchanged`
- [x] **Run ruff** - Lint passed after fixing import order
- [x] **Build typsphinx docs as PDF** - Build succeeded with 0 "unknown node type" warnings for autodoc nodes
- [x] **Verify spec compliance** - `openspec validate add-autodoc-node-support --strict` passed
