# Proposal: Support for Template-Associated Assets

## Problem

When using custom Typst templates via `typst_template` configuration, the template file itself (`_template.typ`) is correctly copied to the output directory. However, assets referenced by the template (fonts, logos, images, icons, watermarks, etc.) are **not** automatically copied, causing Typst compilation to fail with "file not found" errors.

### Current Behavior

```python
# conf.py
typst_template = "_templates/custom_template.typ"
```

```typst
// _templates/custom_template.typ
#import "assets/logo.png"
#set text(font: "assets/CustomFont.otf")
#image("assets/watermark.svg")
```

**Result**:
- ✅ `_template.typ` is copied to output directory
- ❌ `assets/` directory is NOT copied
- ❌ Typst compilation fails: "file not found: assets/logo.png"

### Expected Behavior

Assets referenced by the template should be automatically available in the output directory, similar to how images referenced in the document content are copied via `copy_image_files()`.

## Use Cases

### 1. Corporate Branding
Organizations need to embed company logos, branded fonts, and visual elements in document templates.

```typst
// Company template
#image("logo.png")  // Company logo in header
#set text(font: "CompanyFont.otf")  // Branded font
```

### 2. Academic Papers
Research paper templates (e.g., IEEE, ACM) often require specific logos or symbols.

```typst
// IEEE template
#image("ieee-logo.png")
#image("conference-badge.svg")
```

### 3. Custom Document Designs
Templates with decorative elements, watermarks, or background images.

```typst
// Creative template
#place(center + horizon, image("watermark.svg", width: 100%))
#image("border-design.png")
```

## Related Issues

- **Issue #75**: [FEATURE] Support for template-associated assets

## Related Specifications

- `template-system` - Current template configuration and handling
- `document-conversion` - File copying and asset management (images via `copy_image_files()`)

## Scope

This change affects:
- Template asset discovery and copying
- Configuration for specifying template assets
- Build process (`TypstBuilder` and `TypstPDFBuilder`)

This change does NOT affect:
- Typst Universe packages (`typst_package`) - these handle assets automatically
- Document content images - already handled by `copy_image_files()`
- Template rendering logic - only concerns asset file copying

## Constraints

- **Backward Compatibility**: Must not break existing projects that don't use template assets
- **Opt-in**: Asset copying should only occur when templates reference assets
- **Consistency**: Should follow the same pattern as `copy_image_files()` from Issue #38
- **Performance**: Should not slow down builds for projects without template assets

## Success Criteria

1. ✅ Templates can reference assets (fonts, images, logos) without manual file copying
2. ✅ Assets are automatically copied to the output directory
3. ✅ Builds succeed without "file not found" errors
4. ✅ Configuration is intuitive and well-documented
5. ✅ Backward compatible with existing projects
6. ✅ Works with both `typst` and `typstpdf` builders
