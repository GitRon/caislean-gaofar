# caislean-gaofar
PyGame inspired by Castle of the Winds

## Getting Started

### Running the Game

```bash
# Install dependencies
uv sync

# Run the game
python main.py
```

The project uses `uv` for dependency management (Python 3.13+). Dependencies are locked in `uv.lock` for reproducible builds.

### Testing

This project maintains **100% branch coverage** on all core logic modules.

```bash
# Install dependencies (including test dependencies)
uv sync

# Run all tests
uv run pytest

# Run tests with coverage report
uv run pytest --cov=. --cov-report=term-missing --cov-branch tests/

# Generate HTML coverage report
uv run pytest --cov=. --cov-report=html --cov-branch tests/
```

**Note**: Use `uv run` to execute commands in the uv-managed environment.

See [Coverage Requirements](docs/patterns/coverage_requirements.md) for detailed information.

**Current Status**: 264 tests, 100% branch coverage on core modules

## Development

### Code Quality & Pre-commit Hooks

This project uses pre-commit hooks to enforce code quality and consistency automatically. The hooks run before each commit to ensure code adheres to project standards.

#### Configured Hooks

- **ruff-check**: Fast Python linter that checks for code quality issues and applies automatic fixes
- **ruff-format**: Automatic Python code formatter for consistent style
- **boa-restrictor**: Restricts problematic Python patterns (python-only mode)

#### Local Setup

1. Install pre-commit:
   ```bash
   pip install pre-commit
   ```

2. Install the git hook scripts:
   ```bash
   pre-commit install
   ```

3. (Optional) Run against all files manually:
   ```bash
   pre-commit run --all-files
   ```

Once installed, the hooks will run automatically on `git commit`. If any hook fails, the commit will be blocked until issues are resolved.

### CI/QA Pipeline

The project includes a GitHub Actions workflow (`.github/workflows/qa.yml`) that automatically runs quality checks on:
- Push events to the `main` branch
- Pull requests targeting the `main` branch
- Manual workflow dispatch (via GitHub Actions UI)

#### Pipeline Jobs

The pipeline consists of three separate jobs:

**Job 1: Check Hook Updates** (runs independently, allowed to fail)
1. **Checkout**: Clones the repository
2. **Python Setup**: Configures Python 3.13 environment
3. **Install pre-commit**: Installs pre-commit package
4. **Check for Updates**: Runs `pre-commit autoupdate` and displays available hook updates with warnings

This job provides visibility into available hook updates without blocking the pipeline.

**Job 2: Code Linting**
1. **Checkout**: Clones the repository
2. **Python Setup**: Configures Python 3.13 environment
3. **Install pre-commit**: Installs pre-commit package
4. **Pre-commit Checks**: Runs all configured pre-commit hooks (must pass)

**Job 3: Testing & Coverage** (only runs if linting passes)
1. **Checkout**: Clones the repository
2. **Python Setup**: Configures Python 3.13 environment
3. **Install Dependencies**: Installs pytest, pytest-cov, pytest-mock, and pygame
4. **Run Tests with Coverage**: Executes pytest with branch coverage (must achieve 100%)
5. **Upload Coverage Report**: Uploads coverage data to Codecov (optional)
6. **Coverage Badge**: Validates 100% coverage requirement and fails if not met

The pipeline will fail if any pre-commit hook fails, ensuring code quality standards are maintained. Testing only proceeds after successful linting.

#### Manual Trigger

You can manually trigger the QA pipeline from the GitHub Actions tab by selecting the "QA Pipeline" workflow and clicking "Run workflow".
