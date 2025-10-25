# Proposal: Unified Function Approach for All Typst Elements

## Status
- **State**: Proposed
- **Related Issue**: #4
- **Breaking Change**: Yes (Major version bump required)
- **Created**: 2025-10-25

## Summary

This proposal establishes a **unified function-based architecture** for all Typst element generation in sphinx-typst. Instead of mixing sugar syntax (`=`, `*`, `_`, `-`, `+`) with function calls, we will convert **all elements that currently use sugar syntax** to their canonical function call forms.

This is an **architectural principle**, not just a set of individual conversions. The goal is to achieve **complete consistency** across the entire translator implementation.

## Problem Statement

### Current State: Inconsistent Syntax Mixing

The current implementation mixes three different approaches:

1. **Sugar Syntax** (shorthand notation):
   - Headings: `= Heading`, `== Heading`
   - Emphasis: `_text_`
   - Strong: `*text*`
   - Bullet lists: `- item`
   - Enum lists: `+ item`
   - Field names in API docs: `*Parameters:*`

2. **Function Syntax** (explicit function calls):
   - Subscript: `#sub[text]`
   - Superscript: `#super[text]`
   - Block quotes: `#quote[...]`
   - Images: `#image("path")`
   - Tables: `#table(...)`
   - Admonitions: `#info[...]`, `#warning[...]`

3. **Typst Standard Syntax** (appropriate to keep):
   - Inline code: `` `code` ``
   - Code blocks: ` ```lang ... ``` `
   - Definition lists: `/ term: definition`
   - Math (native): `$ ... $`

### Core Issues

1. **Maintainability Crisis**
   - Mixed syntax makes code structure unclear
   - Difficult to understand which approach to use for new elements
   - Inconsistent patterns across the 70+ `visit_*` methods

2. **Syntax Error Risks** (Issue #55)
   - Combinations like `*_templates/custom_ieee.typ*:` cause "unclosed delimiter" errors
   - Sugar syntax nesting is fragile and error-prone
   - Hard to debug when syntax combinations fail

3. **No 1:1 Mapping**
   - `visit_emphasis` adds `_` in two places (open/close)
   - Not clear that this generates a specific Typst function
   - Violates visitor pattern clarity

4. **Architectural Inconsistency**
   - Some elements (sub, super, quote) already use functions
   - No clear principle governing when to use sugar vs functions
   - Creates confusion for contributors and maintainers

## Proposed Solution

### Architectural Principle

**ALL elements that have function equivalents MUST use function syntax.**

Sugar syntax is ONLY acceptable when:
1. It is Typst standard syntax (code blocks, inline code, math delimiters)
2. No function equivalent exists
3. The sugar syntax is explicitly required by Typst

### Elements to Convert

#### 1. Headings (6 levels)
**Current**: `= Heading`, `== Heading`, `=== Heading`, etc.
**Target**: `#heading(level: 1)[Heading]`, `#heading(level: 2)[Heading]`, etc.
**Location**: `translator.py:132` (`visit_title`)

#### 2. Emphasis
**Current**: `_text_`
**Target**: `#emph[text]`
**Location**: `translator.py:336` (`visit_emphasis`)

#### 3. Strong
**Current**: `*text*`
**Target**: `#strong[text]`
**Location**: `translator.py:355` (`visit_strong`)

#### 4. Subtitle
**Current**: `_subtitle_`
**Target**: `#emph[subtitle]`
**Location**: `translator.py:152` (`visit_subtitle`)

#### 5. Bullet Lists
**Current**: `- item`
**Target**: `#list([item])`
**Location**: `translator.py:473` (`visit_list_item`)
**Note**: Requires redesign to collect all items before generating `#list()`

#### 6. Enumerated Lists
**Current**: `+ item`
**Target**: `#enum([item])`
**Location**: `translator.py:475` (`visit_list_item`)
**Note**: Requires redesign to collect all items before generating `#enum()`

#### 7. Field Names (API Documentation)
**Current**: `*Parameters:*`
**Target**: `#strong[Parameters:]`
**Location**: `translator.py:1790` (`visit_field_name`)

### Elements to Keep (Typst Standard)

1. **Inline Code**: `` `code` `` (line 374)
2. **Code Blocks**: ` ```lang ... ``` ` (line 536)
3. **Definition Lists**: `/ term: definition` (line 616)
4. **Math Delimiters**: `$ ... $` (line 1461, Typst native mode)

These are **Typst standard syntax**, not sugar syntax for function calls.

## Impact Analysis

### Breaking Changes

⚠️ **Generated `.typ` files will change significantly**

1. **All documents must be rebuilt**
   - Existing `.typ` files use sugar syntax
   - New `.typ` files will use function syntax
   - Version control diffs will be large

2. **PDF output remains identical**
   - Typst compiler produces same PDF from both syntaxes
   - No visual changes for end users
   - This is a **source-level breaking change** only

3. **Version Bump Required**
   - Major version: v0.3.0 or v1.0.0
   - Cannot be a minor or patch release

### Benefits

1. **Complete Consistency**
   - Single clear principle: use functions everywhere
   - Easy to understand and maintain
   - Clear guidelines for contributors

2. **Eliminated Syntax Errors**
   - No more `*_text_*` unclosed delimiter errors
   - Function syntax is robust to nesting
   - Predictable behavior

3. **Clear 1:1 Mapping**
   - `visit_emphasis` → `#emph[]` (clear relationship)
   - `visit_strong` → `#strong[]` (clear relationship)
   - Visitor pattern becomes self-documenting

4. **Future-Proof Architecture**
   - Easy to add new elements following the same pattern
   - Consistent approach scales to new Typst features
   - Maintainable for long-term evolution

## Alternatives Considered

### Alternative 1: Keep Sugar Syntax (Status Quo)
**Rejected**: Continues all current problems

### Alternative 2: Partial Conversion (Original Issue #4 Scope)
**Rejected**: Still leaves inconsistency, doesn't solve architectural issues

### Alternative 3: Make Sugar Syntax Configurable
**Rejected**: Adds complexity, still requires maintaining two code paths

### Alternative 4: Full Function Approach (This Proposal)
**Selected**: Solves all issues, establishes clear architectural principle

## Implementation Strategy

### Phase 1: Simple Elements (No State Changes)
1. Emphasis: `_text_` → `#emph[text]`
2. Strong: `*text*` → `#strong[text]`
3. Subtitle: `_subtitle_` → `#emph[subtitle]`
4. Field Names: `*name*` → `#strong[name]`

### Phase 2: Headings (Parameter Calculation)
- Current: Uses `section_level` to generate `=` count
- Target: `#heading(level: section_level)[...]`
- Requires passing level as parameter

### Phase 3: Lists (State Redesign)
- Current: Incremental generation (`visit_list_item` adds `- ` per item)
- Target: Collect all items, then generate `#list([item1], [item2])`
- Requires significant state management changes

### Phase 4: Integration & Testing
- Update all test fixtures
- Comprehensive integration tests
- PDF output verification (should be identical)

## Validation Criteria

1. **All sugar syntax converted** (except Typst standard)
2. **All tests passing** (mypy, black, ruff, tox)
3. **PDF output identical** for test cases
4. **No syntax errors** in generated `.typ` files
5. **Documentation updated** with new approach

## Migration Guide for Users

### For Library Users (Sphinx Projects)

**Action Required**: Rebuild all documents after upgrading

```bash
# After upgrading sphinx-typst to v0.3.0/v1.0.0
rm -rf _build/typst
make typst
```

**Expected Changes**:
- Generated `.typ` files will have different syntax
- PDF output remains identical
- Version control will show large diffs (source format change)

### For Contributors

**New Contribution Guidelines**:
- ALL new elements MUST use function syntax
- Sugar syntax is only for Typst standard forms
- Follow the consistent pattern across all `visit_*` methods

## References

- **Issue #4**: Convert sugar syntax to function call syntax (examples)
- **Issue #55**: Syntax error from `*_templates/custom_ieee.typ*:` combination
- **Typst Documentation**: Function reference for all element types
- **sphinx-typst Architecture**: Visitor pattern implementation

## Open Questions

None - this proposal is comprehensive and ready for review.

## Timeline

1. **Proposal Review**: 2025-10-25 - 2025-10-27
2. **Implementation**: 2025-10-28 - 2025-11-05 (4 phases)
3. **Testing & Validation**: 2025-11-06 - 2025-11-08
4. **Release**: v0.3.0 or v1.0.0 by 2025-11-10
