<!-- OPENSPEC:START -->
# OpenSpec Instructions

These instructions are for AI assistants working in this project.

Always open `@/openspec/AGENTS.md` when the request:
- Mentions planning or proposals (words like proposal, spec, change, plan)
- Introduces new capabilities, breaking changes, architecture shifts, or big performance/security work
- Sounds ambiguous and you need the authoritative spec before coding

Use `@/openspec/AGENTS.md` to learn:
- How to create and apply change proposals
- Spec format and conventions
- Project structure and guidelines

Keep this managed block so 'openspec update' can refresh the instructions.

<!-- OPENSPEC:END -->

# Claude Code Spec-Driven Development

OpenSpec-based spec-driven development. See `openspec/AGENTS.md` for detailed workflow instructions.

## Project Context

### Repository Information
- Owner: `YuSabo90002`
- Repository: `typsphinx`
- GitHub URL: https://github.com/YuSabo90002/typsphinx

### Key Files
- **Project Context**: `openspec/project.md` - Project conventions, tech stack, and guidelines
- **AI Instructions**: `openspec/AGENTS.md` - OpenSpec workflow and detailed instructions
- **Issue Templates**: `.github/ISSUE_TEMPLATE/` - Bug reports, feature requests, questions

## Development Guidelines

- **思考**: English (for technical analysis and planning)
- **回答の生成**: 日本語 (generate responses in Japanese)
- **GitHub interactions**: Always English (issues, PRs, commit messages)
- **When creating issues**: Always reference issue templates in `.github/ISSUE_TEMPLATE/`
  - Bug Report: `bug_report.yml`
  - Feature Request: `feature_request.yml`
  - Question: `question.yml`

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

