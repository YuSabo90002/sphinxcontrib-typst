# Claude Code Spec-Driven Development

Kiro-style Spec Driven Development implementation using claude code slash commands, hooks and agents.

## Project Context

### Repository Information
- Owner: `YuSabo90002`
- Repository: `sphinxcontrib-typst`
- GitHub URL: https://github.com/YuSabo90002/sphinxcontrib-typst

### Paths
- Steering: `.kiro/steering/`
- Specs: `.kiro/specs/`
- Commands: `.claude/commands/`
- Issue Templates: `.github/ISSUE_TEMPLATE/`

### Steering vs Specification

**Steering** (`.kiro/steering/`) - Guide AI with project-wide rules and context
**Specs** (`.kiro/specs/`) - Formalize development process for individual features

### Active Specifications
- **sphinxcontrib-typst**: Sphinx拡張によるTypstビルダーの実装 (Phase: initialized)
- **fix-nested-toctree-paths**: ネストされたtoctreeにおける#include()ディレクティブの相対パス修正 (Phase: initialized) - Issue #5対応
- **simplify-toctree-content-block**: toctree翻訳の簡略化 - 単一コンテンツブロック使用 (Phase: initialized) - Issue #7対応
- **remove-nodehandlerregistry-docs**: NodeHandlerRegistry設計文書の削除とSphinx標準機能の文書化 (Phase: initialized) - Issue #6対応
- Use `/kiro:spec-status [feature-name]` to check progress

## Development Guidelines
- Think in English, but generate responses in Japanese (思考は英語、回答の生成は日本語で行うように)
- **Language for GitHub interactions**: Always write issues and pull requests in English
- **When creating issues**: Always reference issue templates in `.github/ISSUE_TEMPLATE/` and follow the appropriate template format
  - Bug Report: `bug_report.yml`
  - Feature Request: `feature_request.yml`
  - Question: `question.yml`

## Workflow

### Phase 0: Steering (Optional)
`/kiro:steering` - Create/update steering documents
`/kiro:steering-custom` - Create custom steering for specialized contexts

Note: Optional for new features or small additions. You can proceed directly to spec-init.

### Phase 1: Specification Creation
1. `/kiro:spec-init [detailed description]` - Initialize spec with detailed project description
2. `/kiro:spec-requirements [feature]` - Generate requirements document
3. `/kiro:spec-design [feature]` - Interactive: "Have you reviewed requirements.md? [y/N]"
4. `/kiro:spec-tasks [feature]` - Interactive: Confirms both requirements and design review

### Phase 2: Progress Tracking
`/kiro:spec-status [feature]` - Check current progress and phases

## Development Rules
1. **Consider steering**: Run `/kiro:steering` before major development (optional for new features)
2. **Follow 3-phase approval workflow**: Requirements → Design → Tasks → Implementation
3. **Approval required**: Each phase requires human review (interactive prompt or manual)
4. **No skipping phases**: Design requires approved requirements; Tasks require approved design
5. **Update task status**: Mark tasks as completed when working on them
6. **Keep steering current**: Run `/kiro:steering` after significant changes
7. **Check spec compliance**: Use `/kiro:spec-status` to verify alignment

## Steering Configuration

### Current Steering Files
Managed by `/kiro:steering` command. Updates here reflect command changes.

### Active Steering Files
- `product.md`: Always included - Product context and business objectives
- `tech.md`: Always included - Technology stack and architectural decisions
- `structure.md`: Always included - File organization and code patterns

### Custom Steering Files
<!-- Added by /kiro:steering-custom command -->
<!-- Format:
- `filename.md`: Mode - Pattern(s) - Description
  Mode: Always|Conditional|Manual
  Pattern: File patterns for Conditional mode
-->

### Inclusion Modes
- **Always**: Loaded in every interaction (default)
- **Conditional**: Loaded for specific file patterns (e.g., "*.test.js")
- **Manual**: Reference with `@filename.md` syntax

## Project-Specific Guidelines

### Package and Task Management
- **Always use `uv` commands** for package management and task execution
  - Running commands: `uv run <command>`
  - Running tests: `uv run pytest`
  - Installing packages: `uv add <package>`
  - Syncing dependencies: `uv sync`
  - Other pip operations: `uv pip <command>`
- Do NOT use `pip` or bare `python` commands directly
- Do NOT use `poetry` or other package managers

