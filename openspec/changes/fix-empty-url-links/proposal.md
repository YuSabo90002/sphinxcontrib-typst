# Proposal: Fix Empty URL Link Generation for Typst 0.14+ Compatibility

## Problem

The translator generates Typst `link("")` calls with empty URLs when processing certain reStructuredText reference nodes. Typst 0.14.1 introduced stricter URL validation that rejects empty URLs, causing CI/CD builds to fail.

### Current Behavior

**Code**: `typsphinx/translator.py:1931-1943`

```python
# Get the reference URI
refuri = node.get("refuri", "")  # ← Can be empty string

# ...

# External reference (HTTP/HTTPS URL or relative path)
self.add_text(f'{prefix}link("{refuri}", ')  # ← Generates link("", ...)
```

**Result**: Empty URLs generate invalid Typst code:
```typst
#link("", [text])  // ❌ Typst 0.14.1: "URL must not be empty"
```

### Root Cause

Reference nodes (`nodes.reference`) can have empty `refuri` attributes when:
1. **Unresolved references**: Links to non-existent targets
2. **Broken cross-references**: References to missing sections/documents
3. **Malformed reStructuredText**: Incomplete link syntax
4. **Sphinx reference resolution failures**: Internal reference mechanisms fail

The current code does not validate `refuri` before generating `link()` calls.

### Impact

- 🔴 **CI/CD Blocked**: PDF documentation generation fails on GitHub Actions
- 📊 **Version Incompatibility**: Works with Typst ≤0.13.7, fails with ≥0.14.1
- ⚠️ **Silent Failures**: Users don't know which references are broken until Typst compilation

### Failed Workflow Examples

- [Run #18989770164](https://github.com/YuSabo90002/typsphinx/actions/runs/18989770164)
- [Run #18989731656](https://github.com/YuSabo90002/typsphinx/actions/runs/18989731656)

**Error**:
```
TypstError: URL must not be empty
```

## Proposed Solution

Add validation and graceful handling for empty URLs in `visit_reference()`.

### Approach: Skip Empty URL Links, Render as Plain Text

When `refuri` is empty:
1. **Skip `link()` generation** - don't create invalid Typst code
2. **Render content as plain text** - preserve the link text
3. **Emit warning** - alert users to broken references during build

**Implementation**:

```python
def visit_reference(self, node: nodes.reference) -> None:
    # ... existing code ...

    # Get the reference URI
    refuri = node.get("refuri", "")

    # Handle empty URLs (Typst 0.14+ rejects empty URLs)
    if not refuri:
        logger.warning(
            f"Reference node has empty URL. "
            f"Link will be rendered as plain text. "
            f"Check for broken references in source: {node.astext()}"
        )
        # Don't generate link(), just render content as text
        # Children will be processed normally, outputting plain text
        self._skip_link_wrapper = True
        return

    # ... rest of existing code (only runs if refuri is non-empty) ...
```

```python
def depart_reference(self, node: nodes.reference) -> None:
    # Skip link wrapper closing if we skipped it in visit
    if getattr(self, "_skip_link_wrapper", False):
        self._skip_link_wrapper = False
        return

    # ... existing code ...
```

### Alternative Approaches Considered

#### Alternative 1: Generate Placeholder URL
```python
if not refuri:
    refuri = "#broken-reference"  # Placeholder
```

**Rejected**: Creates fake links that mislead users. Better to render as plain text and warn.

#### Alternative 2: Raise Build Error
```python
if not refuri:
    raise ValueError("Empty URL in reference")
```

**Rejected**: Too strict - breaks builds for minor documentation issues. Warnings are more user-friendly.

#### Alternative 3: Use Typst's `link()` with content-only
```python
if not refuri:
    # Just output the content without link wrapper
    # (Typst doesn't have content-only link syntax)
```

**Selected**: This is essentially our proposed solution.

## Scope

### In Scope
- Validate `refuri` in `visit_reference()`
- Skip link generation for empty URLs
- Emit warnings for broken references
- Add tests for empty URL handling
- Update to Typst 0.14.1 (to validate fix)

### Out of Scope
- Fixing Sphinx reference resolution bugs (upstream issue)
- Detecting *why* references are empty (requires Sphinx internals analysis)
- Auto-correcting broken references (requires heuristics)

## Use Cases

### Use Case 1: Unresolved Cross-Reference

**reStructuredText**:
```rst
See :ref:`nonexistent-section` for details.
```

**Current Output** (Typst 0.13.7):
```typst
See #link("", [nonexistent-section]) for details.  // Silently accepted
```

**Proposed Output** (Typst 0.14.1):
```typst
See [nonexistent-section] for details.  // Plain text, with warning
```

**Warning**:
```
WARNING: Reference node has empty URL. Link will be rendered as plain text.
Check for broken references in source: nonexistent-section
```

### Use Case 2: Broken External Link

**reStructuredText**:
```rst
Visit `the website <>`_ for more info.
```

**Current Output**: `#link("", [the website])`
**Proposed Output**: `[the website]` + warning

### Use Case 3: Valid Links (No Change)

**reStructuredText**:
```rst
Visit `Python <https://python.org>`_ for more info.
```

**Output** (unchanged):
```typst
Visit #link("https://python.org", [Python]) for more info.
```

## Success Criteria

1. ✅ Empty `refuri` detected and skipped
2. ✅ Link content rendered as plain text (no `link()` wrapper)
3. ✅ Warning emitted with reference text for debugging
4. ✅ Typst 0.14.1 compilation succeeds
5. ✅ CI/CD pipeline restored
6. ✅ Tests cover empty URL scenarios
7. ✅ No regression for valid links

## Related Issues

- **Issue #77**: [BUG] CI PDF generation fails with Typst 0.14.1 due to empty URL validation

## Related Specifications

- `document-conversion` - Reference and link handling

## Constraints

- **Backward Compatibility**: Must not break existing valid links
- **Typst 0.14+ Compatibility**: Must work with stricter URL validation
- **User Experience**: Warnings should be clear and actionable
- **Build Stability**: Don't fail builds for documentation issues (warn instead)

## Migration Path

### For Users
**No migration needed** - this is a bug fix.

If users see new warnings:
1. Review warning messages
2. Fix broken references in source documentation
3. Warnings will disappear once references are fixed

### Version Upgrade
After this fix:
- ✅ Can upgrade to Typst 0.14.1
- ✅ CI/CD will use latest Typst version
- ✅ Builds will be more robust

## Testing Strategy

### Unit Tests
- Empty `refuri` → no `link()` generated
- Empty `refuri` → content rendered as text
- Empty `refuri` → warning emitted
- Valid `refuri` → existing behavior unchanged

### Integration Tests
- Build document with broken references
- Verify Typst code compiles with 0.14.1
- Verify warnings appear in build log

### Regression Tests
- All 317 existing tests pass
- No change in output for valid links

## Implementation Complexity

**Low Complexity**:
- Simple conditional check in `visit_reference()`
- Minimal changes to `depart_reference()`
- Clear edge case (empty string validation)

**Estimated Effort**: 2-4 hours (implementation + tests + validation)
