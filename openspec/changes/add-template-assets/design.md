# Design: Template Asset Support

## Overview

This design extends the template system to automatically copy assets (fonts, images, logos) referenced by custom Typst templates. The implementation follows the existing `copy_image_files()` pattern established in Issue #38.

## Implementation Options

### Option 1: Automatic Directory Copy (Recommended)

**Approach**: When `typst_template` points to a file, automatically copy all files in the same directory.

```python
# conf.py
typst_template = "_templates/corporate/template.typ"
```

**Behavior**:
- Copy `_templates/corporate/` directory (entire folder) to output directory
- Preserves directory structure
- Simple for users - no configuration needed

**Pros**:
- ✅ Zero configuration
- ✅ Intuitive - "template directory contains everything"
- ✅ Handles most use cases

**Cons**:
- ⚠️ May copy unnecessary files
- ⚠️ Less granular control

### Option 2: Configuration-Based Asset List

**Approach**: Add `typst_template_assets` configuration for explicit asset specification.

```python
# conf.py
typst_template = "_templates/template.typ"
typst_template_assets = [
    "_templates/logo.png",
    "_templates/fonts/",
    "_templates/icons/*.svg"
]
```

**Behavior**:
- Copy only specified files/directories
- Supports glob patterns
- Explicit control

**Pros**:
- ✅ Granular control
- ✅ Avoid copying unnecessary files
- ✅ Clear documentation of dependencies

**Cons**:
- ⚠️ Requires manual configuration
- ⚠️ Users must know what assets are needed

### Option 3: Automatic Asset Detection (Future Enhancement)

**Approach**: Parse template file to detect `#image()`, `#font()`, etc. and copy referenced files.

**Example**:
```typst
// template.typ
#image("logo.png")  // Detected → copy logo.png
#set text(font: "CustomFont.otf")  // Detected → copy CustomFont.otf
```

**Pros**:
- ✅ Fully automatic
- ✅ No configuration needed
- ✅ Copies only what's used

**Cons**:
- ⚠️ Complex parsing required
- ⚠️ May miss dynamic references
- ⚠️ Deferred to future version

## Recommended Approach

**Hybrid: Option 1 + Option 2**

1. **Default Behavior (Option 1)**: Automatically copy template directory
2. **Override (Option 2)**: Use `typst_template_assets` for granular control

```python
# Simple case - automatic
typst_template = "_templates/template.typ"
# Copies entire _templates/ directory

# Advanced case - explicit
typst_template = "_templates/template.typ"
typst_template_assets = [
    "_templates/logo.png",
    "_templates/fonts/"
]
# Copies only specified assets
```

## Architecture

### Modified Components

#### 1. `TypstBuilder` Class ([builder.py](../../typsphinx/builder.py))

Add new method `copy_template_assets()` similar to `copy_image_files()`:

```python
def copy_template_assets(self) -> None:
    """
    Copy template-associated assets to the output directory.

    If typst_template_assets is configured, copies specified files.
    Otherwise, copies the entire template directory.
    """
    template_path = getattr(self.config, "typst_template", None)
    if not template_path:
        return  # No custom template

    template_assets = getattr(self.config, "typst_template_assets", None)

    if template_assets:
        # Option 2: Explicit asset list
        self._copy_explicit_assets(template_assets)
    else:
        # Option 1: Automatic directory copy
        self._copy_template_directory(template_path)
```

#### 2. Configuration Registration ([__init__.py](../../typsphinx/__init__.py))

Add new configuration value:

```python
app.add_config_value("typst_template_assets", None, "html", [list, type(None)])
```

#### 3. Build Process Integration

Call `copy_template_assets()` in `finish()` method:

```python
def finish(self) -> None:
    """Finish the build process."""
    self.copy_image_files()      # Existing
    self.copy_template_assets()  # New
```

### File Copying Logic

#### Automatic Directory Copy (Option 1)

```python
def _copy_template_directory(self, template_path: str) -> None:
    """Copy entire template directory to output."""
    template_dir = os.path.dirname(template_path)
    src_dir = os.path.join(self.srcdir, template_dir)
    dest_dir = os.path.join(self.outdir, template_dir)

    if not os.path.exists(src_dir):
        return

    # Copy directory, excluding template file itself
    # (template file is handled separately in write_template_file())
    for root, dirs, files in os.walk(src_dir):
        for file in files:
            if file.endswith('.typ'):
                continue  # Skip .typ files

            src_file = os.path.join(root, file)
            rel_path = os.path.relpath(src_file, src_dir)
            dest_file = os.path.join(dest_dir, rel_path)

            ensuredir(os.path.dirname(dest_file))
            shutil.copy2(src_file, dest_file)
```

#### Explicit Asset Copy (Option 2)

```python
def _copy_explicit_assets(self, assets: List[str]) -> None:
    """Copy explicitly specified assets."""
    for asset_pattern in assets:
        # Support glob patterns
        if '*' in asset_pattern:
            matches = glob.glob(os.path.join(self.srcdir, asset_pattern))
            for match in matches:
                self._copy_single_asset(match)
        else:
            src = os.path.join(self.srcdir, asset_pattern)
            self._copy_single_asset(src)

def _copy_single_asset(self, src_path: str) -> None:
    """Copy a single asset file or directory."""
    if os.path.isdir(src_path):
        # Copy directory recursively
        ...
    elif os.path.isfile(src_path):
        # Copy single file
        ...
```

## Edge Cases and Considerations

### 1. Typst Universe Packages

**Question**: Should this affect `typst_package` configuration?

**Answer**: **No**. Typst Universe packages (e.g., `@preview/charged-ieee:0.1.0`) are handled by the Typst compiler itself. Package assets are downloaded and managed automatically by Typst. This feature only applies to **local custom templates** (`typst_template`).

```python
# This does NOT need asset copying (Typst handles it)
typst_package = "@preview/charged-ieee:0.1.0"

# This DOES need asset copying (local template)
typst_template = "_templates/custom.typ"
```

### 2. Template File Duplication

**Issue**: Template file itself is already copied by `write_template_file()`. Should `copy_template_assets()` also copy it?

**Answer**: **No**. Skip `.typ` files to avoid duplication. `write_template_file()` already handles template copying.

### 3. Relative Paths in Templates

**Issue**: Template references `assets/logo.png`. Should we preserve directory structure?

**Answer**: **Yes**. Preserve relative paths so template references remain valid.

```
Source:
  _templates/
    template.typ         → references "assets/logo.png"
    assets/
      logo.png

Output:
  _templates/
    template.typ         → references still valid
    assets/
      logo.png
```

### 4. Non-Existent Assets

**Issue**: What if specified assets don't exist?

**Answer**: Log a warning, but don't fail the build. Similar to `copy_image_files()` behavior.

```python
if not os.path.exists(src):
    logger.warning(f"Template asset not found: {src}")
    continue
```

### 5. Performance Impact

**Issue**: Copying large template directories could slow builds.

**Answer**:
- Only copy when `typst_template` is set
- Skip if template directory hasn't changed (use timestamp comparison in future optimization)
- Users can use `typst_template_assets` for granular control

## Testing Strategy

### Unit Tests

1. Test `copy_template_assets()` with various configurations
2. Test automatic directory copy
3. Test explicit asset list
4. Test glob pattern matching
5. Test missing asset handling

### Integration Tests

1. Build project with custom template and assets
2. Verify assets are copied correctly
3. Verify Typst compilation succeeds
4. Verify no regression for projects without templates

### E2E Tests

1. Create example project with logo, fonts, images
2. Build PDF and verify assets are rendered
3. Test both `typst` and `typstpdf` builders

## Documentation Updates

### User Guide

Add section "Using Custom Templates with Assets":

```markdown
## Custom Templates with Assets

### Automatic Asset Copying (Recommended)

Place your template and assets in the same directory:

├── _templates/
│   ├── template.typ
│   ├── logo.png
│   └── fonts/
│       └── CustomFont.otf

Configure template path:

```python
typst_template = "_templates/template.typ"
```

All files in `_templates/` will be automatically copied.

### Explicit Asset Specification

For granular control, specify assets explicitly:

```python
typst_template = "_templates/template.typ"
typst_template_assets = [
    "_templates/logo.png",
    "_templates/fonts/*.otf"
]
```

## Migration Guide

### Existing Projects

**No migration needed**. This feature is backward compatible:

- Projects without `typst_template` → no change
- Projects with `typst_template` but no assets → no change
- Projects with manually copied assets → automatic copying takes over (can remove manual steps)

### Opting Out

To disable automatic asset copying (e.g., for performance):

```python
typst_template = "_templates/template.typ"
typst_template_assets = []  # Empty list = no automatic copying
```

## Future Enhancements

1. **Asset Detection**: Parse template files to auto-detect referenced assets (Option 3)
2. **Incremental Copying**: Only copy changed assets (timestamp comparison)
3. **Asset Validation**: Warn about unused assets or missing references
4. **Remote Assets**: Support HTTP URLs for downloading remote assets

## Implementation Sequence

See `tasks.md` for detailed implementation tasks.
