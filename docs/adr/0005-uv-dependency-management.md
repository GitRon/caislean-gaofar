# ADR 0005: UV for Dependency Management

## Status

Accepted

## Context

Python projects require dependency management tools for:
- Installing dependencies
- Managing virtual environments
- Ensuring reproducible builds
- Locking dependency versions
- Fast installation for CI/CD

Traditional options include pip, pip-tools, poetry, and pipenv. Each has trade-offs around speed, features, and complexity.

Key requirements:
- Fast installation (especially for CI/CD)
- Reproducible builds via lockfile
- Python 3.13+ support
- Simple workflow for developers
- Compatible with standard pyproject.toml

## Decision

We will use **uv** (https://github.com/astral-sh/uv) as our dependency management tool.

### Why uv?

#### 1. Speed
- Written in Rust (10-100x faster than pip)
- Parallel dependency resolution
- Fast virtual environment creation
- Dramatically improves CI/CD pipeline speed

#### 2. Modern Standards
- Uses standard `pyproject.toml` for dependencies
- Generates `uv.lock` for reproducible builds
- No proprietary configuration format
- Easy migration path if needed

#### 3. Simplicity
- Single tool for venv creation and package installation
- Drop-in replacement for pip commands
- Minimal learning curve
- No complex configuration needed

#### 4. Python 3.13+ Support
- First-class support for latest Python versions
- Active development and maintenance
- Growing adoption in Python community

### Workflow

#### Install Dependencies
```bash
uv sync
```
- Creates virtual environment if needed
- Installs all dependencies from lockfile
- Fast and reproducible

#### Add New Dependency
```bash
uv add package-name
```
- Updates pyproject.toml
- Updates uv.lock
- Installs package

#### Update Dependencies
```bash
uv lock --upgrade
```
- Updates lockfile with latest versions
- Respects version constraints in pyproject.toml

### File Structure
- `pyproject.toml`: Source of truth for dependencies
- `uv.lock`: Locked versions for reproducibility
- `.venv/`: Virtual environment (gitignored)

### Integration Points

#### Pre-commit Hooks
```yaml
# .pre-commit-config.yaml
# No special configuration needed
# Hooks run in uv-managed environment
```

#### CI/CD
```bash
# Fast dependency installation
uv sync
pytest
```

#### PyInstaller
```bash
# Works with standard venv
uv sync
pyinstaller CaisleanGaofar.spec
```

## Consequences

### Positive
- **Speed**: Significantly faster than pip/poetry
- **Simple**: Standard pyproject.toml + lockfile pattern
- **Modern**: Uses latest Python packaging standards
- **Reliable**: Lockfile ensures reproducible builds
- **Compatible**: Works with existing Python tools
- **Low lock-in**: Can migrate to other tools if needed

### Negative
- **Newer tool**: Less mature than pip/poetry
- **Rust dependency**: Requires Rust toolchain to build from source (binaries available)
- **Learning**: Team must learn uv commands
- **Ecosystem**: Some tools may not recognize uv.lock

### Neutral
- **Community adoption**: Growing but not universal
- **Documentation**: Good but less extensive than pip/poetry
- **Platform support**: Excellent (Linux, macOS, Windows)

## Command Reference

### Essential Commands
```bash
# Install all dependencies
uv sync

# Add dependency
uv add pygame

# Add dev dependency
uv add --dev pytest

# Update lockfile
uv lock --upgrade

# Run command in venv
uv run python main.py

# Run tests
uv run pytest
```

### Migration From pip/poetry
```bash
# uv reads existing pyproject.toml
# Just run:
uv sync

# This creates uv.lock from existing dependencies
```

## Performance Benchmarks

Based on uv's published benchmarks:
- **Package installation**: 10-100x faster than pip
- **Dependency resolution**: Near-instantaneous for cached packages
- **Virtual environment creation**: Seconds instead of minutes

Real-world impact:
- CI/CD pipeline: ~5 minutes → ~30 seconds
- Developer setup: ~2 minutes → ~10 seconds

## Alternatives Considered

### 1. pip + pip-tools
**Pros**: Most widely used, well understood
**Cons**: Slow, manual workflow, no venv management

**Rejected because**: Speed is critical for developer experience and CI/CD

### 2. Poetry
**Pros**: Feature-rich, popular, good dependency resolution
**Cons**: Slower than uv, complex configuration, occasional resolution issues

**Rejected because**: uv provides 90% of benefits with better speed

### 3. Pipenv
**Pros**: Combines pip and venv
**Cons**: Slow, sometimes unreliable, declining maintenance

**Rejected because**: Less active development, slower than alternatives

### 4. PDM
**Pros**: PEP 582 support, fast
**Cons**: Less adoption, more opinionated

**Rejected because**: uv has stronger momentum and simpler model

## Future Considerations

- **Monorepo support**: uv workspace features as they mature
- **Dependency groups**: Use uv's group features when stable
- **Scripts**: Consider uv's script management for task automation

## Related Decisions
- Development workflow relies on fast iteration
- CI/CD pipeline optimization
- Reproducible builds for distribution
