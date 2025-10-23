# Proposal: Rename Package to typsphinx

## Why

現在のパッケージ名 `sphinxcontrib-typst` は `sphinxcontrib-*` 名前空間の慣例に従っており、これは伝統的にディレクティブ、ロール、その他のマークアップ処理機能を追加するSphinx**拡張機能**に使用されています。

しかし、`sphinxcontrib-typst` は主にSphinxドキュメントをTypst形式に変換し、PDF出力を生成する**ビルダー**です。このパッケージは2つのエコシステム（SphinxとTypst）を橋渡しするものであり、この統合を反映するユニークで覚えやすい名前が相応しいと考えます。

`typsphinx` への改名には以下の利点があります：

- **ユニークで覚えやすい**: 短くキャッチーな名前で目立つ
- **双方向の関係性**: TypstとSphinxの両方の統合を示唆する名前
- **エコシステムの橋渡し**: 2つのコミュニティを結ぶパッケージの役割を反映
- **検索性の向上**: 両方の技術名を組み合わせることで発見しやすい

### 追加のメリット

- **明確な意図**: Typst + Sphinxの統合であることが即座に伝わる
- **シンプルなインポート**: `import typsphinx` がクリーンで簡潔
- **優れたブランディング**: ユニークで覚えやすく、推奨しやすい名前
- **早期段階での改名**: v0.2.2でユーザーが少ない今が、この破壊的変更を行う理想的なタイミング

## What

パッケージ名を `sphinxcontrib-typst` から `typsphinx` に変更し、以下を更新：

1. **パッケージ構造**: `sphinxcontrib/typst/` → `typsphinx/`
2. **インポート名前空間**: `sphinxcontrib.typst` → `typsphinx`
3. **リポジトリ名**: `sphinxcontrib-typst` → `typsphinx` (GitHub)
4. **PyPIパッケージ**: `sphinxcontrib-typst` → `typsphinx`
5. **すべての参照**: ドキュメント、例、テスト、設定を更新

これは **v0.3.0** としてリリースされます（破壊的変更 - 0.xシリーズでのマイナーバージョンアップ）。

## Impact

### 破壊的変更

- **ユーザーは `conf.py` の更新が必要**:
  ```python
  # 旧 (v0.2.x)
  extensions = ['sphinxcontrib.typst']

  # 新 (v0.3.0+)
  extensions = ['typsphinx']
  ```

- **ユーザーはパッケージの再インストールが必要**:
  ```bash
  # 旧パッケージをアンインストール
  pip uninstall sphinxcontrib-typst

  # 新パッケージをインストール
  pip install typsphinx
  ```

### 移行戦略

1. **PyPI**: `typsphinx` v0.3.0を新パッケージとして公開
2. **旧パッケージ**: PyPIから削除（ユーザーが最小限のため）
3. **ドキュメント**: CHANGELOGに破壊的変更を記録（移行ガイドは不要）
4. **GitHub**: リポジトリ名を変更し、旧URLから自動リダイレクト

### リスク評価

- **低リスク**: この段階（v0.2.2）ではユーザー数が最小限
- **明確な移行パス**: `conf.py` の1行変更だけで済む
- **可逆性**: 旧パッケージはPyPIに残る（非推奨版として）
- **タイミング**: v1.0.0と広範な採用の前に実施するのがベスト

## Dependencies

なし（自己完結型の変更）

## Alternatives Considered

1. **現状維持**: よりシンプルだが、命名の混乱が続く
2. **v1.0.0まで待つ**: より多くのユーザーが破壊的変更の影響を受ける
3. **両方の名前をサポート**: 複雑さとメンテナンス負担が増加

## Success Criteria

- 新しいパッケージ構造ですべてのテストがパス
- GitHubリポジトリの改名が成功
- `typsphinx` v0.3.0がPyPIに公開
- ドキュメントが新しいパッケージ名で更新
- 機能に退行なし
