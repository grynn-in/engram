# Creating Templates

Templates let you pre-seed projects with domain-specific knowledge.

## Template Structure

```
templates/my-template/
├── seed.toml              # Required: template metadata
├── claude.md.extra        # Optional: template-specific guidance for CLAUDE.md
├── claude.md.snippet      # Generated: protocol block + claude.md.extra
├── semantic/              # Optional: pre-seeded facts
│   ├── domain-patterns.md
│   └── common-issues.md
├── procedural/            # Optional: pre-seeded workflows
│   ├── setup-guide.md
│   └── deployment.md
├── traps/                 # Optional: pre-seeded hard-won lessons
│   └── known-pitfalls.md
└── vision/                # Optional: pre-seeded direction & decisions
    └── design-principles.md
```

A template may seed any **transferable** layer — `semantic/`, `procedural/`,
`traps/` and `vision/`. The set comes from `lib/layers.py`; nothing here
hardcodes it.

### claude.md.extra vs claude.md.snippet

`claude.md.extra` is the only part you write. It holds guidance specific to
this template and must **not** contain the Engram protocol block — that block
is generated from the layer registry, so a copied one would go stale the moment
a layer is added.

`claude.md.snippet` is generated as `protocol block + claude.md.extra`, for
anyone who wants the whole thing to paste. `engram init --template <name>`
writes the generated protocol block and then appends `claude.md.extra`.
Regenerate the snippet with:

```bash
{ python3 lib/layers.py --protocol; echo; cat templates/my-template/claude.md.extra; } \
  > templates/my-template/claude.md.snippet
```

`tests/test_layers.py` fails if a snippet drifts from its generator.

## seed.toml Format

```toml
[meta]
name = "my-template"
description = "Brief description of what this template provides"
version = "0.1.0"

[meta.tags]
domain = "web"
language = "typescript"
framework = "nextjs"
```

## Usage

```bash
# Initialize with template
engram init --template my-template

# Templates are searched in:
# 1. ~/.engram/templates/<name>/
# 2. <engram-install>/templates/<name>/
```

## Writing Good Template Knowledge

### Semantic files should contain:
- Patterns that work in this domain (with examples)
- Common pitfalls and their solutions
- Architecture decisions and trade-offs
- Tool/framework behaviors observed empirically

### Procedural files should contain:
- Step-by-step workflows (numbered steps)
- Setup guides with exact commands
- Troubleshooting decision trees
- Checklists for common operations

### Rules for template content:
- Use placeholders for project-specific values: `<PROJECT_NAME>`, `<COMPANY>`, `<API_URL>`
- Keep files focused on one topic each
- Include "last verified" dates for time-sensitive content
- Avoid opinions — state facts and observed behaviors
- Never include secrets, credentials, or PII

## Sharing Templates

Templates can be distributed as:
1. Directories within the engram repo (`templates/`)
2. Standalone git repos (clone into `~/.engram/templates/`)
3. Tarballs (extract into `~/.engram/templates/`)

Community templates welcome via PR to the main repo.
