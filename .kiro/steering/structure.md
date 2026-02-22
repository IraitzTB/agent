# Project Structure

## Directory Organization

```
.
├── .kiro/                  # Kiro IDE configuration
│   ├── steering/          # AI assistant guidance documents
│   └── specs/             # Feature specifications (requirements, design, tasks)
└── .vscode/               # VSCode/Kiro settings
```

## Kiro-Specific Directories

### `.kiro/steering/`
Contains markdown files that guide the AI assistant:
- `product.md` - Product overview and purpose
- `tech.md` - Technology stack and common commands
- `structure.md` - Project organization (this file)

### `.kiro/specs/`
Feature specifications following the spec-driven development workflow:
- Each feature gets its own subdirectory: `.kiro/specs/{feature-name}/`
- Required files per spec: `requirements.md`, `design.md`, `tasks.md`

## Source Code Organization

Source code structure will be established as the project develops. Common patterns:
- `src/` - Main source code
- `tests/` - Test files
- `docs/` - Documentation and changes (all markdowns)
- `scripts/` - Utility scripts

## Conventions

- Use kebab-case for directory names (e.g., `user-authentication`)
- Keep configuration files at project root
- Co-locate tests with source files when appropriate (`.test.ts` suffix)
