# document-conversion Spec Delta

## MODIFIED Requirements

### Requirement: Reference node translation

Reference nodes (`nodes.reference`) must be translated to Typst `link()` functions with proper URL validation. Empty URLs must be handled gracefully without generating invalid Typst code (MUST).

#### Scenario: Valid external URL (existing behavior - no change)

- **GIVEN** a reStructuredText document contains
  ```rst
  Visit `Python <https://python.org>`_ for more info.
  ```
- **WHEN** the document is converted to Typst
- **THEN** the output contains
  ```typst
  Visit #link("https://python.org", [Python]) for more info.
  ```
- **AND** no warnings are emitted
- **AND** Typst compilation succeeds

#### Scenario: Valid internal reference (existing behavior - no change)

- **GIVEN** a reStructuredText document contains
  ```rst
  See :ref:`my-section` for details.
  ```
- **AND** `my-section` is a valid label
- **WHEN** the document is converted to Typst
- **THEN** the output contains
  ```typst
  See #link(<my-section>, [My Section]) for details.
  ```
- **AND** no warnings are emitted
- **AND** Typst compilation succeeds

#### Scenario: Empty URL - skip link generation (new behavior)

- **GIVEN** a reference node has an empty `refuri` attribute
- **AND** the reference text is "broken link"
- **WHEN** `visit_reference()` is called
- **THEN** no `link()` function is generated
- **AND** the reference content is rendered as plain text: `[broken link]`
- **AND** a warning is emitted:
  ```
  WARNING: Reference node has empty URL. Link will be rendered as plain text.
  Check for broken references in source: broken link
  ```

#### Scenario: Unresolved cross-reference

- **GIVEN** a reStructuredText document contains
  ```rst
  See :ref:`nonexistent-section` for details.
  ```
- **AND** `nonexistent-section` does not exist
- **AND** Sphinx resolves the reference node with empty `refuri`
- **WHEN** the document is converted to Typst
- **THEN** the output contains
  ```typst
  See [nonexistent-section] for details.
  ```
- **AND** no `link()` function is generated
- **AND** a warning is logged
- **AND** Typst compilation succeeds (no "URL must not be empty" error)

#### Scenario: Malformed external link

- **GIVEN** a reStructuredText document contains
  ```rst
  Visit `the website <>`_ for more info.
  ```
- **AND** the URL is empty
- **WHEN** the document is converted to Typst
- **THEN** the output contains
  ```typst
  Visit [the website] for more info.
  ```
- **AND** no `link()` with empty URL is generated
- **AND** a warning is emitted

#### Scenario: Empty URL validation in visit_reference()

- **GIVEN** `visit_reference()` is processing a reference node
- **WHEN** `node.get("refuri", "")` returns an empty string
- **THEN** the method sets `self._skip_link_wrapper = True`
- **AND** the method returns early without generating `link(` syntax
- **AND** a warning is logged via `logger.warning()`
- **AND** child nodes are still processed normally (for text content)

#### Scenario: Empty URL handling in depart_reference()

- **GIVEN** `visit_reference()` set `self._skip_link_wrapper = True`
- **WHEN** `depart_reference()` is called
- **THEN** the method checks `getattr(self, "_skip_link_wrapper", False)`
- **AND** if True, skips generating the closing `)`
- **AND** resets `self._skip_link_wrapper = False`
- **AND** returns early without other depart logic

#### Scenario: Typst 0.14.1 compatibility

- **GIVEN** the translator handles empty URLs gracefully
- **WHEN** Typst 0.14.1 is used for compilation
- **AND** the generated `.typ` file contains no empty URLs
- **THEN** Typst compilation succeeds
- **AND** no "URL must not be empty" error occurs
- **AND** CI/CD pipeline passes

#### Scenario: Warning message format

- **GIVEN** a reference node has empty `refuri`
- **AND** the node text is "example text"
- **WHEN** the warning is emitted
- **THEN** the warning includes:
  - Description: "Reference node has empty URL"
  - Action: "Link will be rendered as plain text"
  - Debug info: "Check for broken references in source: example text"
- **AND** the warning level is `WARNING` (not ERROR or INFO)

### Requirement: Build stability with invalid references

Document builds must not fail due to empty URLs in reference nodes. Invalid references must be handled gracefully with warnings (MUST).

#### Scenario: Build continues despite empty URLs

- **GIVEN** a document contains multiple empty URL references
- **WHEN** the Typst build is executed
- **THEN** warnings are emitted for each empty URL
- **AND** the build completes successfully
- **AND** the PDF is generated
- **AND** no exceptions are raised

#### Scenario: Multiple empty URLs in single document

- **GIVEN** a document contains 3 references with empty URLs
- **WHEN** the document is converted
- **THEN** 3 separate warnings are emitted
- **AND** each warning identifies the specific reference
- **AND** all 3 references are rendered as plain text
- **AND** the build succeeds

## ADDED Requirements

### Requirement: Empty URL detection and logging

The translator must detect empty URLs before generating Typst code and log warnings to help users identify broken references (MUST).

#### Scenario: Empty refuri attribute

- **GIVEN** a reference node exists
- **WHEN** `node.get("refuri", "")` is called
- **AND** the result is `""`
- **THEN** the condition `if not refuri:` evaluates to True
- **AND** empty URL handling is triggered

#### Scenario: None refuri attribute

- **GIVEN** a reference node exists
- **AND** the node has no `refuri` attribute
- **WHEN** `node.get("refuri", "")` is called
- **THEN** the result is `""`  (default value)
- **AND** empty URL handling is triggered

#### Scenario: Whitespace-only refuri

- **GIVEN** a reference node has `refuri = "   "`
- **WHEN** `node.get("refuri", "")` is called
- **THEN** the result is `"   "`
- **AND** the condition `if not refuri:` evaluates to False
- **AND** `link("   ", ...)` is generated
- **NOTE**: This is acceptable - whitespace URLs will fail Typst validation,
  but are distinguishable from truly empty strings

### Requirement: State management for skipped links

The translator must track when link wrappers are skipped to prevent mismatched `link()` calls (MUST).

#### Scenario: Skip flag initialization

- **GIVEN** `visit_reference()` detects an empty URL
- **WHEN** the method sets the skip flag
- **THEN** `self._skip_link_wrapper` is set to `True`
- **AND** the flag persists until `depart_reference()` is called

#### Scenario: Skip flag cleanup

- **GIVEN** `depart_reference()` runs with `_skip_link_wrapper = True`
- **WHEN** the method completes
- **THEN** `self._skip_link_wrapper` is reset to `False`
- **AND** the flag does not affect subsequent reference nodes

#### Scenario: Skip flag isolation

- **GIVEN** document contains 2 references: one empty, one valid
- **WHEN** both are processed
- **THEN** the empty URL reference sets `_skip_link_wrapper = True`
- **AND** the flag is cleared before the valid reference
- **AND** the valid reference generates proper `link()` syntax

### Requirement: Backward compatibility with valid links

Changes to empty URL handling must not affect the behavior of valid links (MUST).

#### Scenario: No regression for valid HTTP URLs

- **GIVEN** a reference with `refuri = "https://example.com"`
- **WHEN** the reference is processed
- **THEN** the empty URL check passes (non-empty)
- **AND** existing `link()` generation logic runs unchanged
- **AND** output matches previous behavior exactly

#### Scenario: No regression for internal references

- **GIVEN** a reference with `refuri = "#section-label"`
- **WHEN** the reference is processed
- **THEN** the empty URL check passes (non-empty)
- **AND** `link(<section-label>, ...)` is generated as before

#### Scenario: Existing test suite passes

- **GIVEN** 317 existing tests in the test suite
- **WHEN** tests are run after implementing empty URL handling
- **THEN** all existing tests pass
- **AND** no test output changes for valid links
- **AND** test coverage remains ≥94%
