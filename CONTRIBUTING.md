# Contributing to OtelTUI

Thank you for your interest in contributing to OtelTUI! We welcome contributions from everyone.

## Getting Started

### Prerequisites

- Python 3.12 or higher
- [uv](https://docs.astral.sh/uv/) package manager (recommended)
- Git

### Development Setup

1. Fork the repository on GitHub
2. Clone your fork locally:

```bash
git clone https://github.com/yourusername/oteltui.git
cd oteltui
```

3. Set up the development environment:

```bash
# Using uv (recommended)
uv sync --extra dev

# Or using pip
pip install -e ".[dev]"
```

4. Install pre-commit hooks:

```bash
uv run pre-commit install
```

5. Create a branch for your changes:

```bash
git checkout -b feature/your-feature-name
```

## Development Guidelines

### Code Style

We follow these coding standards:

- **Line length**: Maximum 100 characters
- **Type hints**: Use type hints for all function parameters and return values
- **Naming**: Use descriptive names for variables and functions
- **Comments**: Only add comments when necessary to explain business logic or exceptions
- **No docstrings**: Prefer descriptive naming over documentation

### Code Quality Tools

We use several tools to maintain code quality:

#### Automatic checks with pre-commit
Pre-commit hooks run automatically on every commit:

```bash
# Install hooks (run once)
uv run pre-commit install

# Run hooks manually on all files
uv run pre-commit run --all-files
```

#### Manual code formatting and linting

```bash
# Format code with ruff
uv run ruff format

# Check for linting issues
uv run ruff check

# Fix auto-fixable issues
uv run ruff check --fix

# Run type checking with mypy
uv run mypy src/
```

### Testing

Run tests using pytest:

```bash
# Run all tests
uv run pytest

# Run with coverage
uv run pytest --cov=src/oteltui

# Run specific test file
uv run pytest tests/test_specific.py
```

### Testing Your Changes

1. Start the TUI:

```bash
uv run oteltui
```

2. In another terminal, send test traces:

```bash
uv run python client.py
```

3. Verify your changes work as expected in the TUI interface

## Submitting Changes

### Pull Request Process

1. Ensure your code follows the style guidelines
2. Add or update tests for your changes
3. Run the full test suite and ensure all tests pass
4. Update documentation if needed
5. Commit your changes with a clear commit message
6. Push to your fork and submit a pull request

### Commit Messages

Use clear, descriptive commit messages:

```
Add trace filtering functionality

- Implement search box in main interface
- Add filter logic for span names and trace IDs
- Update tests for new filtering features
```

### Pull Request Guidelines

- **Title**: Use a clear, descriptive title
- **Description**: Explain what changes you made and why
- **Testing**: Describe how you tested your changes
- **Screenshots**: Include screenshots for UI changes

## Types of Contributions

### Bug Reports

When reporting bugs, please include:

- Python version and operating system
- Steps to reproduce the issue
- Expected vs actual behavior
- Error messages or logs
- Screenshots if applicable

### Feature Requests

For new features:

- Describe the problem you're trying to solve
- Explain your proposed solution
- Consider alternative approaches
- Discuss potential impact on existing functionality

### Code Contributions

We welcome:

- Bug fixes
- New features
- Performance improvements
- Documentation improvements
- Test coverage improvements

## Architecture Overview

### Project Structure

```
oteltui/
├── src/oteltui/
│   ├── main.py          # Main TUI application
│   ├── server.py        # gRPC server implementation
│   └── __init__.py
├── tests/               # Test files
├── client.py           # Test client
└── pyproject.toml      # Project configuration
```

### Key Components

- **OtelTUIApp**: Main Textual application class
- **TraceStore**: Reactive trace storage
- **TraceServer**: gRPC server for receiving traces
- **TraceDetailModal**: Modal for detailed trace viewing

### Adding New Features

1. **UI Changes**: Modify `main.py` and add appropriate widgets
2. **Server Changes**: Update `server.py` for protocol modifications
3. **Storage Changes**: Extend `TraceStore` for new data handling
4. **Tests**: Add tests in the `tests/` directory

## Development Tips

### Debugging

- Use `print()` statements for quick debugging
- Textual has a development console available
- Check logs for gRPC errors

### Performance

- Keep the UI responsive by using Textual workers
- Limit trace storage to prevent memory issues
- Use reactive properties for efficient UI updates

### Testing

- Test with different trace formats
- Verify UI responsiveness with many traces
- Test error handling for malformed traces

## Getting Help

- Open an issue for questions
- Check existing issues and pull requests
- Review the Textual documentation for UI questions
- Look at OpenTelemetry documentation for protocol details

## Recognition

Contributors will be recognized in:

- GitHub contributors list
- Release notes for significant contributions
- Project documentation

Thank you for contributing to OtelTUI!
