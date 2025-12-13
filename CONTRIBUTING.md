# Contributing to Law Enforcement Case Data Generator

Thank you for your interest in contributing! This document provides guidelines and instructions for contributing to this project.

## Getting Started

1. Fork the repository
2. Clone your fork: `git clone <your-fork-url>`
3. Create a branch: `git checkout -b feature/your-feature-name`
4. Make your changes
5. Test your changes thoroughly
6. Commit your changes: `git commit -m "Add: description of changes"`
7. Push to your fork: `git push origin feature/your-feature-name`
8. Open a Pull Request

## Development Setup

1. Install dependencies:
```bash
pip install -r requirements.txt
```

2. Run tests (if available):
```bash
python generate_qa_cases.py
python analyze_qa_cases.py
```

## Code Style

- Follow PEP 8 Python style guide
- Use meaningful variable and function names
- Add docstrings to functions and classes
- Keep functions focused and modular
- Comment complex logic

## Adding New Features

### Adding a New Crime Type

1. Add the crime type to the CLI options in `main.py`
2. Add crime-specific generation logic in `src/crime_specific_generators.py`
3. Update `_should_generate_physical_evidence()` in `src/generators.py` if needed
4. Test with various complexity levels

### Adding a New Document Type

1. Create generator function in `src/utils.py` or appropriate module
2. Add to evidence/document generation flow in `src/generators.py`
3. Ensure it respects crime-type appropriateness
4. Test with multiple cases

### Adding a New Modifier

1. Add to modifier list in `main.py` and `web_interface.py`
2. Implement modifier logic in `src/generators.py`
3. Update documentation
4. Test with various crime types

## Testing

Before submitting a PR:

1. Run the QA test suite:
```bash
python generate_qa_cases.py
python analyze_qa_cases.py
```

2. Test the web interface:
```bash
python web_interface.py
```

3. Test the CLI:
```bash
python main.py
```

4. Verify all modules compile:
```bash
python -m py_compile src/*.py
```

## Pull Request Guidelines

- Provide a clear description of changes
- Reference any related issues
- Include screenshots for UI changes
- Ensure all tests pass
- Update documentation as needed

## Reporting Issues

When reporting issues, please include:

- Description of the issue
- Steps to reproduce
- Expected behavior
- Actual behavior
- Environment details (OS, Python version, etc.)
- Relevant error messages or logs

## Questions?

Feel free to open an issue for questions or discussions about the project.

