# Test Coverage Requirements

## Overview

This project enforces **100% branch coverage** on all core logic modules through automated CI/CD pipeline checks.

## Coverage Policy

### Enforced Coverage: 100%

All core business logic modules must maintain 100% branch coverage:

- ✅ `combat.py` - Combat system logic
- ✅ `config.py` - Configuration constants
- ✅ `entity.py` - Base entity class
- ✅ `grid.py` - Grid system utilities
- ✅ `inventory.py` - Inventory management
- ✅ `item.py` - Item types and classes
- ✅ `ui_button.py` - UI button component
- ✅ `warrior.py` - Player character logic
- ✅ `monsters/` - All monster classes including base and specific types

### Excluded from 100% Requirement

The following files are excluded from the 100% coverage requirement as they contain primarily UI/rendering code that requires complex pygame integration testing:

- `game.py` - Main game loop and pygame integration
- `inventory_ui.py` - Inventory UI rendering
- `monster_renderer.py` - Complex monster rendering functions
- `main.py` - Entry point

## Running Coverage Locally

```bash
# Run tests with coverage report
pytest --cov=. --cov-report=term-missing --cov-branch tests/

# Generate HTML coverage report
pytest --cov=. --cov-report=html --cov-branch tests/
# Then open htmlcov/index.html in a browser

# Check if coverage passes (will fail if < 100%)
pytest --cov=. --cov-report=term --cov-branch --cov-fail-under=100 tests/
```

## CI/CD Pipeline

The GitHub Actions pipeline (`qa.yml`) enforces coverage requirements:

1. **Uses uv** for reproducible dependency installation from `uv.lock`
2. **Runs all tests** with branch coverage enabled
3. **Fails the build** if coverage falls below 100%
4. **Generates coverage reports** for review
5. **Uploads to Codecov** (optional integration)

### Pipeline Configuration

```yaml
# Install dependencies from lock file
- name: Install uv
  uses: astral-sh/setup-uv@v4
  with:
    enable-cache: true
    cache-dependency-glob: "uv.lock"

- name: Install dependencies
  run: uv sync --frozen

# Run tests with coverage
- name: Run tests with coverage
  run: |
    pytest --cov=. --cov-report=term-missing --cov-report=xml \
      --cov-branch --cov-fail-under=100 tests/ -v
```

The `--frozen` flag ensures dependencies exactly match `uv.lock`, providing reproducible builds.

## Coverage Configuration

Coverage settings are defined in `pyproject.toml`:

```toml
[tool.coverage.run]
branch = true
omit = [
    "tests/*",
    "main.py",
    "game.py",
    "inventory_ui.py",
    "monster_renderer.py",
]

[tool.coverage.report]
fail_under = 100
precision = 2
```

## Adding New Code

When adding new functionality:

1. **Write tests first** following TDD principles
2. **Ensure 100% branch coverage** for all new logic modules
3. **Run coverage locally** before pushing
4. **Pipeline will verify** coverage on PR

### Example: Adding a New Feature

```bash
# 1. Write failing test
echo "def test_new_feature(): ..." >> tests/test_module.py

# 2. Implement feature
echo "def new_feature(): ..." >> module.py

# 3. Verify coverage
pytest --cov=module --cov-branch tests/test_module.py

# 4. Check overall coverage
pytest --cov=. --cov-branch --cov-fail-under=100 tests/
```

## Best Practices

### Branch Coverage

- **Test all conditional paths**: if/else, try/except, loops
- **Test edge cases**: empty lists, None values, boundary conditions
- **Test error paths**: invalid inputs, exception handling

### Test Quality

- **Atomic tests**: One test case per test function
- **Clear naming**: `test_[function]_[scenario]_[expected_result]`
- **AAA pattern**: Arrange, Act, Assert
- **No test interdependencies**: Each test runs independently

## Troubleshooting

### Coverage Below 100%

If coverage check fails:

```bash
# See which lines are missing
pytest --cov=. --cov-report=term-missing --cov-branch tests/

# Generate detailed HTML report
pytest --cov=. --cov-report=html --cov-branch tests/
```

### Excluding Lines

Use `# pragma: no cover` sparingly for truly untestable code:

```python
def debug_function():  # pragma: no cover
    print("Debug output")
```

## Metrics

Current coverage status:

- **Total Tests**: 264
- **Core Module Coverage**: 100% (branch coverage)
- **Overall Coverage**: ~46% (including UI code)
- **Pipeline**: ✅ Enforced on all PRs

## References

- [Testing Strategy](./testing_strategy.md)
- [Coverage.py Documentation](https://coverage.readthedocs.io/)
- [pytest-cov Plugin](https://pytest-cov.readthedocs.io/)
