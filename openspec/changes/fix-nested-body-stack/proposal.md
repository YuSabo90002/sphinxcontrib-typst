# Proposal: Stream-Based List Rendering (Remove Body Swapping)

## Status
- **State**: Proposed
- **Related Issue**: #61
- **Breaking Change**: No
- **Created**: 2025-10-26
- **Updated**: 2025-10-26

## Summary

Fix the critical bug where `visit_document()`'s code mode wrapper (`#{...}`) is lost when processing documents with nested elements (lists, definitions, terms). The root cause is the **body swapping pattern** where `self.body` is temporarily replaced with a buffer to collect list item content.

**Solution**: Eliminate body swapping entirely by using a **stream-based approach** with state flags, similar to how docutils' HTMLTranslator works. This is simpler, more maintainable, and aligns with standard visitor pattern practices.

## Why

### Current Broken Behavior

For certain documents (e.g., `index.rst`, `contributing.rst`), the generated Typst output is **missing the document-level code mode wrapper**:

**Expected output**:
```typst
#{
heading(level: 1, text("Title"))
par(text("Content"))
}
```

**Actual broken output**:
```typst
heading(level: 1, text("Title"))
par(text("Content"))
```

This causes Typst compilation to fail because heading, par, and other functions are only available inside code mode (`#{...}`).

### Root Cause: Body Swapping Anti-Pattern

The translator currently uses a **body swapping pattern** where `self.body` is temporarily replaced with a buffer to collect list item content:

**Current Problematic Flow**:
1. `visit_document()`: `self.body = ['#{\n']` - Adds code mode wrapper
2. `visit_list_item()`:
   ```python
   self.saved_body = self.body  # Saves ['#{\n']
   self.body = []               # SWAPS to new buffer
   ```
3. **Nested** `visit_list_item()` (inner list):
   ```python
   self.saved_body = self.body  # OVERWRITES! Original ['#{\n'] is LOST
   self.body = []               # SWAPS to new buffer
   ```
4. `depart_list_item()` (inner):
   ```python
   self.body = self.saved_body  # Restores outer buffer
   ```
5. `depart_list_item()` (outer):
   ```python
   self.body = self.saved_body  # Restores outer buffer again
                                 # Original ['#{\n'] is NEVER restored
   ```

**Result**: The `#{\n` added by `visit_document()` is permanently lost.

### Why Body Swapping is Wrong

The body swapping pattern has fundamental issues:

1. **Breaks standard visitor pattern**: Docutils translators (HTMLTranslator, LaTeXTranslator) never swap `self.body`
2. **Complex state management**: Requires `saved_body`, `current_list_item_buffer`, etc.
3. **Fragile with nesting**: Single variable gets overwritten (current bug)
4. **Hard to maintain**: Non-obvious control flow

**How standard translators work** (e.g., HTMLTranslator):
- `self.body` is **never swapped**
- Elements append directly: `self.body.append('<li>')`
- State managed with simple flags: `self.in_list_item`, etc.

### Affected Code Locations

In [typsphinx/translator.py](https://github.com/YuSabo90002/typsphinx/blob/main/typsphinx/translator.py):

1. **List item processing** (L712, L732):
   - `visit_list_item()`: `self.saved_body = self.body`
   - `depart_list_item()`: `self.body = self.saved_body`

2. **Term processing** (L904, L923):
   - `visit_term()`: `self.saved_body = self.body`
   - `depart_term()`: `self.body = self.saved_body`

3. **Definition processing** (L941, L957):
   - `visit_definition()`: `self.saved_body = self.body`
   - `depart_definition()`: `self.body = self.saved_body`

All three use the same single variable `self.saved_body`, making nesting impossible.

### Why Only Certain Documents Are Affected

- **index.rst**: Contains definition lists (`**Dual Builder Integration**:`) with nested content → Bug triggers
- **contributing.rst**: Contains nested lists/definitions → Bug triggers
- **installation.rst**: Simple structure without deep nesting → Works fine

The bug only manifests when document-level elements contain nesting that requires multiple body saves.

### Current Workaround

A workaround was added in [writer.py:75-80](https://github.com/YuSabo90002/typsphinx/blob/main/typsphinx/writer.py#L75-L80):

```python
# WORKAROUND: For some Sphinx documents, visit_document may not be called
# Ensure body is wrapped in code mode block
if not body.startswith("#{"):
    body = "#{\n" + body
if not body.endswith("}\n"):
    body = body + "}\n"
```

This workaround **masks** the bug but doesn't fix the root cause. The proper solution is to fix the nested body management in the translator.

## Proposed Solution

### Core Change: Stream-Based Output with State Flags

Eliminate body swapping entirely and use **state flags** to control separator output, similar to HTMLTranslator.

**Key Insight**: We don't need to buffer list items. We can output them directly to `self.body` and use flags to insert commas and `+` operators at the right places.

**Example - Current (Broken) Approach**:
```python
def visit_list_item(self, node):
    self.saved_body = self.body      # SWAP body
    self.body = []                    # Use buffer

def depart_list_item(self, node):
    content = "".join(self.body)      # Get buffer content
    self.body = self.saved_body       # RESTORE body
    self.items.append(content)        # Collect item

def depart_bullet_list(self, node):
    items_str = ", ".join(self.items) # Join all items
    self.add_text(f"list({items_str})")
```

**New (Stream-Based) Approach**:
```python
def visit_bullet_list(self, node):
    self.add_text("list(")
    self.is_first_list_item = True

def visit_list_item(self, node):
    if not self.is_first_list_item:
        self.add_text(", ")  # Comma before 2nd+ items
    self.is_first_list_item = False
    self.list_item_needs_separator = False  # First element in item doesn't need +

def depart_list_item(self, node):
    pass  # Nothing to do

def depart_bullet_list(self, node):
    self.add_text(")\n\n")

# In elements that appear inside list items (text, emphasis, etc.)
def visit_Text(self, node):
    if self.in_list_item and self.list_item_needs_separator:
        self.add_text(" + ")  # Add + between elements
    # ... output text ...
    if self.in_list_item:
        self.list_item_needs_separator = True  # Next element needs +
```

### State Flags Required

**New flags** (to add in `__init__`):
```python
self.is_first_list_item = True           # Track if current item is first in list
self.list_item_needs_separator = False   # Track if + is needed before next element
```

**Existing flags** (already present, will be reused):
```python
self.in_list_item = False  # Track if currently inside a list item
```

**Flags to remove**:
```python
self.saved_body = None                  # DELETE - no more body swapping
self.current_list_item_buffer = None    # DELETE - no more buffering
```

### Changes Required

#### 1. Remove body swapping infrastructure

- Delete `self.saved_body` from `__init__`
- Delete `self.current_list_item_buffer` from `__init__`
- Delete `self.list_items_stack` (no longer collecting items)

#### 2. Update list methods

**`visit_bullet_list()` / `visit_enumerated_list()`**:
```python
def visit_bullet_list(self, node):
    self.list_stack.append("bullet")
    self.add_text("list(")
    self.is_first_list_item = True
```

**`visit_list_item()`**:
```python
def visit_list_item(self, node):
    self.in_list_item = True
    if not self.is_first_list_item:
        self.add_text(", ")
    self.is_first_list_item = False
    self.list_item_needs_separator = False
```

**`depart_list_item()`**:
```python
def depart_list_item(self, node):
    self.in_list_item = False
    # No more buffer cleanup needed!
```

**`depart_bullet_list()` / `depart_enumerated_list()`**:
```python
def depart_bullet_list(self, node):
    self.list_stack.pop()
    self.add_text(")\n\n")
```

#### 3. Update element methods to add separators

Modify methods for elements that can appear inside list items:

- `visit_Text()`: Add `+` separator logic
- `visit_emphasis()`: Add `+` separator logic
- `visit_strong()`: Add `+` separator logic
- `visit_paragraph()`: Handle paragraph in list items
- Nested lists: Automatically handled by recursive structure

#### 4. Apply same pattern to definition lists

Use the same stream-based approach for `visit_term()` and `visit_definition()`.

### Backward Compatibility

- **No breaking changes**: This is a pure bug fix
- Existing documents that work will continue to work
- Documents that were broken will now work correctly
- No API changes, no configuration changes

### Remove Workaround (Optional)

After confirming the fix works, we can remove the workaround in `writer.py` since it will no longer be needed.

## Benefits

1. **Correctness**: Fixes Issue #61 - document wrapper is never lost
2. **Simplicity**: No body swapping, no stack management, just simple flags
3. **Standard pattern**: Aligns with how docutils translators (HTML, LaTeX) work
4. **Less code**: Removes ~50 lines of body swapping logic
5. **Better performance**: No buffer copying, direct stream output
6. **Maintainability**: Easier to understand and debug
7. **Removes workaround**: Can eliminate the band-aid fix in `writer.py`

## Risks and Mitigation

### Risk: Incorrect Separator Logic

**Risk**: Flags might not correctly track when to add `,` or `+` separators.

**Mitigation**:
- Comprehensive test cases for all separator scenarios
- Test nested lists, mixed content in list items
- Verify output with actual Typst compiler

### Risk: Edge Cases with Complex List Items

**Risk**: List items with multiple paragraphs or complex structures might not format correctly.

**Mitigation**:
- Test with real-world documents (index.rst, contributing.rst)
- Add test cases for complex list item content
- Verify paragraph handling in list items

### Risk: Definition List Complexity

**Risk**: Definition lists have term/definition structure which is more complex.

**Mitigation**:
- Apply same stream-based pattern
- Test with actual definition lists from docs
- May need additional flags for definition-specific formatting

## Testing Strategy

1. **Unit tests**: Test nested list/definition scenarios
2. **Integration tests**: Build `index.rst` and `contributing.rst` and verify output starts with `#{`
3. **Regression tests**: Ensure `installation.rst` and other simple documents still work
4. **Manual verification**: Build documentation and check PDF output

## Migration Path

1. Implement stream-based list rendering for bullet/enumerated lists
2. Update tests to verify correct output
3. Apply same pattern to definition lists (term/definition)
4. Build real documentation (docs/source/) to verify fix
5. (Optional) Remove workaround from `writer.py` in follow-up PR

## Implementation Strategy

**Phase 1**: Lists (bullet, enumerated)
- Remove body swapping from list methods
- Add separator flags
- Update element methods to respect flags

**Phase 2**: Definition Lists
- Apply same pattern to term/definition
- May require definition-specific flags

**Phase 3**: Cleanup
- Remove unused body swapping infrastructure
- Remove workaround from writer.py
- Update documentation

## Related Work

- Issue #61: Investigation and root cause analysis
- Issue #4: Unified code mode architecture
- Commit 05c0a1c: Workaround implementation in writer.py
- PR #60: Unified function approach (established document-level `#{...}` pattern)

## References

- Root cause analysis: https://github.com/YuSabo90002/typsphinx/issues/61#issuecomment-3447906582
- Affected code: [typsphinx/translator.py](https://github.com/YuSabo90002/typsphinx/blob/main/typsphinx/translator.py)
- Current workaround: [typsphinx/writer.py:75-80](https://github.com/YuSabo90002/typsphinx/blob/main/typsphinx/writer.py#L75-L80)
