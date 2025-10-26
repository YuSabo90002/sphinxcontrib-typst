# Proposal: Fix Table Cell Unified Code Mode Compliance

## Status
- **State**: Draft
- **Related Spec**: table-rendering
- **Breaking Change**: No (output change only, API unchanged)
- **Created**: 2025-10-26

## Summary

現在のtableセル生成が Unified Code Mode 指針に違反しています。マークアップモード `[...]` を使用せず、content型を直接渡すように修正します。

### Current Behavior

```typst
#{
  table(
    columns: 2,
    [par({text("Cell 1")})],              # マークアップモード内で#なし → 指針違反
    table.cell(colspan: 2)[content],      # 引数順序が間違い
  )
}
```

### Expected Behavior

```typst
#{
  table(
    columns: 2,
    par({text("Cell 1")}),                # content型を直接渡す
    table.cell(par({text("Spans")}), colspan: 2),  # content型を第1引数に
  )
}
```

## Why

### Unified Code Mode Compliance

[openspec/changes/archive/2025-10-25-unified-function-approach/proposal.md](../archive/2025-10-25-unified-function-approach/proposal.md) で定義された指針：

1. **ドキュメント全体を `#{...}` で囲む**
2. **コードモード内では関数名に `#` を付けない**
3. **マークアップモード `[...]` 内では関数名に `#` を付ける**
4. **できるだけ `text()` 関数を使い、マークアップモードを避ける**

### Current Problems

1. **マークアップモードの不要な使用**
   - tableセルで `[content]` を使用
   - Unified Code Mode指針の「マークアップモードを避ける」に反する

2. **マークアップモード内での `#` 省略**
   - `[par({text(...)})]` のように `#` なしで関数を呼び出し
   - 指針の「マークアップモード内では `#` を付ける」に反する

3. **`table.cell()` の引数順序が間違い**
   - 現在: `table.cell(colspan: 2)[content]`
   - 正しい: `table.cell(content, colspan: 2)`
   - Typst公式: 第1引数がcontent型のbody

### Benefits

1. **完全な一貫性**
   - すべてのTypst要素がUnified Code Mode指針に従う
   - マークアップモードを使わず、content型を直接渡す

2. **正しい構文**
   - `table.cell()` の引数順序がTypst公式と一致
   - より読みやすく、予測可能なコード

3. **保守性の向上**
   - 一貫したパターンで新機能の追加が容易
   - デバッグとテストが簡単

## What

### Changes

#### 1. `_format_table_cell()` Method

**File**: `typsphinx/translator.py:1201-1228`

**Normal cells (no colspan/rowspan)**:
```python
# Before
return f"{indent}[{content}],\n"

# After
return f"{indent}{content},\n"
```

**Spanning cells**:
```python
# Before
return f"{indent}table.cell({params_str})[{content}],\n"

# After
return f"{indent}table.cell({content}, {params_str}),\n"
```

### Affected Components

- `typsphinx/translator.py`: `_format_table_cell()` method only
- Tests: 10 table tests (validation only, no changes needed)

### Migration Path

なし。出力形式の変更のみで、APIは変更なし。既存のSphinxドキュメントは再ビルドで自動的に新しい形式で生成される。

## Validation

### Test Strategy

1. **既存テストの実行**
   - 10個のtableテスト全てがパス
   - テスト自体は文字列含有チェックのみなので変更不要

2. **Typst構文検証**
   - 生成されたTypstファイルがコンパイル可能
   - PDFが正しく生成される

3. **統合テスト**
   - ドキュメントビルドが成功
   - table-renderingの全シナリオが動作

### Success Criteria

- ✅ すべてのtableテストがパス
- ✅ Typstファイルがエラーなくコンパイル
- ✅ ドキュメントPDFが正しく生成
- ✅ Unified Code Mode指針に完全準拠

## Dependencies

なし。独立した変更。

## Alternatives Considered

### Alternative 1: マークアップモード内で `#` を付ける

```typst
#{
  table(
    columns: 2,
    [#par({text("Cell 1")})],  # マークアップモード内で#を付ける
  )
}
```

**却下理由**:
- Unified Code Mode指針の「マークアップモードを避ける」に反する
- 不要な複雑さを導入

### Alternative 2: 現状維持

**却下理由**:
- Unified Code Mode指針に違反し続ける
- 不一貫な実装パターンが残る
- 将来的なメンテナンスコストが高い

## Implementation Plan

See [tasks.md](./tasks.md) for detailed implementation tasks.
