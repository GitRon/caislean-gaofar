# caislean-gaofar
PyGame inspired by Castle of the Winds

## Getting Started

### Running the Game
```bash
python main.py
```

The project uses `uv` for dependency management (Python 3.13+) with pygame as the only dependency.

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

The pipeline consists of two separate jobs that run sequentially:

**Job 1: Code Linting**
1. **Checkout**: Clones the repository
2. **Python Setup**: Configures Python 3.13 environment
3. **Install pre-commit**: Installs pre-commit package
4. **Hook Updates Check**: Runs `pre-commit autoupdate` to check for newer hook versions (allowed to fail)
5. **Pre-commit Checks**: Runs all configured pre-commit hooks (must pass)

**Job 2: Testing** (only runs if linting passes)
1. **Checkout**: Clones the repository
2. **Python Setup**: Configures Python 3.13 environment
3. **Install pytest**: Installs pytest package
4. **Run Tests**: Executes pytest (extensible for future test additions)

The pipeline will fail if any pre-commit hook fails, ensuring code quality standards are maintained. Testing only proceeds after successful linting.

#### Manual Trigger

You can manually trigger the QA pipeline from the GitHub Actions tab by selecting the "QA Pipeline" workflow and clicking "Run workflow".
