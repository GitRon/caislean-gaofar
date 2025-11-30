# ADR 0006: ty Type Checker Integration

## Status

Accepted

## Context

Python is a dynamically typed language, which provides flexibility but can lead to type-related bugs that are only discovered at runtime. Type checkers help catch these issues during development and provide better IDE support through static analysis.

Key requirements for a type checker:
- Fast execution (especially for CI/CD and watch mode)
- Python 3.13+ support
- Accurate type inference
- Minimal configuration overhead
- Integration with existing uv-based workflow

The project already has strong quality gates (100% branch coverage, pre-commit hooks), but lacks static type checking to catch type-related issues before runtime.

### Existing Type Checkers

**mypy**
- Most mature and widely used
- Good type system coverage
- Slower performance (especially on large codebases)
- Sometimes requires extensive configuration

**pyright**
- Fast performance (written in TypeScript/Node.js)
- Good IDE integration (VS Code)
- Requires Node.js runtime
- More opinionated than mypy

**pytype** (Google)
- Infers types without annotations
- Very slow on medium/large codebases
- Less actively maintained

## Decision

We will use **ty** (https://github.com/astral-sh/ty) as our type checker.

### Why ty?

#### 1. Performance
- Written in Rust (extremely fast)
- Designed for sub-second feedback
- Excellent watch mode for real-time feedback
- Minimal CI overhead

#### 2. Modern Toolchain Alignment
- From Astral (same team as uv and ruff)
- Designed to work seamlessly with uv
- Consistent tooling philosophy across project
- Single vendor for Python tooling reduces friction

#### 3. Python 3.13+ Support
- First-class support for latest Python features
- Active development and maintenance
- Targets modern Python ecosystem

#### 4. Developer Experience
- Fast feedback loop encourages usage
- Clear, actionable error messages
- Watch mode for continuous checking
- Minimal configuration needed

#### 5. CI/CD Integration
- Fast enough to run on every commit
- Concise output format for CI
- Can be configured to not block merges initially

### Gradual Adoption Strategy

**Phase 1: Non-blocking Integration (Current)**
- Add ty to development dependencies
- Configure to check only `src/` (exclude `tests/`)
- Run in CI with `continue-on-error: true`
- Document usage for developers
- Treat as informational only

**Phase 2: Stabilization (Future)**
- Fix high-priority type issues
- Refine configuration based on real-world usage
- Add specific rule severity overrides
- Begin tracking type issue count

**Phase 3: Enforcement (Future)**
- Remove `continue-on-error` from CI
- Block merges on type errors
- Optionally include tests in type checking
- Achieve high type coverage

### Configuration

Configuration in `pyproject.toml`:

```toml
[tool.ty.environment]
python-version = "3.13"

[tool.ty.src]
exclude = ["tests/**"]  # Phase 1: focus on production code
respect-ignore-files = true

[tool.ty.terminal]
output-format = "concise"  # Better for CI parsing
```

### CI Integration

New job in `.github/workflows/qa.yml`:

```yaml
typechecking:
  name: Type Checking (ty)
  runs-on: ubuntu-latest
  continue-on-error: true  # Phase 1: informational only

  steps:
    - name: Checkout code
      uses: actions/checkout@v4

    - name: Set up Python 3.13
      uses: actions/setup-python@v5
      with:
        python-version: '3.13'

    - name: Install uv
      uses: astral-sh/setup-uv@v4
      with:
        enable-cache: true
        cache-dependency-glob: "uv.lock"

    - name: Install dependencies
      run: uv sync --frozen

    - name: Run ty type checker
      run: uv run ty check src/
```

### Developer Workflow

Developers can run ty locally:

```bash
# Check all source files
uv run ty check

# Check specific files
uv run ty check src/caislean_gaofar/core/

# Watch mode (continuous checking)
uv run ty check --watch

# Verbose output
uv run ty check -v
```

## Consequences

### Positive

- **Early bug detection**: Catch type errors before runtime
- **Better IDE support**: Improved autocomplete and hints
- **Documentation**: Type hints serve as inline documentation
- **Refactoring confidence**: Type checking catches issues during refactors
- **Performance**: Fast enough for watch mode and CI
- **Consistency**: Aligns with uv/ruff tooling strategy
- **Gradual adoption**: No immediate breaking changes to workflow
- **Developer velocity**: Fast feedback loop doesn't slow development

### Negative

- **Alpha software**: ty is pre-1.0 (currently v0.0.1a27)
- **API changes**: Configuration and behavior may change
- **Ecosystem maturity**: Less documentation and community support than mypy
- **Type annotations required**: May need to add/improve type hints
- **Learning curve**: Team must learn type system and ty-specific diagnostics
- **Initial noise**: Existing codebase has 133 type issues in source code

### Neutral

- **Not blocking merges**: Initially informational only
- **Test exclusion**: Tests not type-checked in Phase 1
- **Manual fixes**: Type issues must be fixed manually (no auto-fix)
- **Migration path**: Could switch to mypy/pyright if needed

## Alternatives Considered

### 1. mypy
**Pros**: Mature, widely used, extensive documentation
**Cons**: Slower performance, more configuration needed
**Rejected because**: Speed is critical for watch mode and developer adoption. ty's performance enables continuous checking without friction.

### 2. pyright
**Pros**: Fast, good VS Code integration, mature
**Cons**: Requires Node.js runtime, more opinionated
**Rejected because**: Adding Node.js to Python project adds complexity. ty better aligns with Rust-based Python tooling (uv, ruff).

### 3. No type checker
**Pros**: No new tooling, no learning curve
**Cons**: Miss type errors until runtime, worse IDE support
**Rejected because**: Type checking catches real bugs and improves code quality. Performance overhead with ty is negligible.

### 4. pytype
**Pros**: Infers types without annotations
**Cons**: Very slow, less maintained
**Rejected because**: Performance is unacceptable for watch mode. Requires type annotations is actually a benefit for documentation.

## Future Considerations

- **IDE integration**: Language server support for VS Code/PyCharm
- **Type coverage metrics**: Track percentage of code with type hints
- **Stricter enforcement**: Move from warnings to errors
- **Test type checking**: Include tests once source code is clean
- **Custom rules**: Configure specific diagnostic severities
- **Type stubs**: Add stubs for third-party libraries without types

## Related Decisions

- [ADR 0005: UV for Dependency Management](0005-uv-dependency-management.md) - ty integrates seamlessly with uv
- Development workflow emphasizes fast feedback loops
- CI/CD pipeline structure supports parallel quality checks

## References

- ty GitHub: https://github.com/astral-sh/ty
- ty Documentation: https://docs.astral.sh/ty/
- Astral (uv/ruff/ty): https://astral.sh/
- Python Type System (PEP 484): https://peps.python.org/pep-0484/
