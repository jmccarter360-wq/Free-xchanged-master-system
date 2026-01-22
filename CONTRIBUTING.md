# Contributing to Free-xchanged-master-system

Thank you for your interest in contributing to the Free-xchanged-master-system! This document provides guidelines for contributing to the project.

## Code of Conduct

Please be respectful and professional in all interactions.

## How to Contribute

### Reporting Bugs

If you find a bug, please create an issue with:
- A clear, descriptive title
- Steps to reproduce the issue
- Expected behavior vs actual behavior
- Your environment (OS, Python version, etc.)

### Suggesting Features

Feature suggestions are welcome! Please create an issue that describes:
- The problem you're trying to solve
- Your proposed solution
- Any alternatives you've considered

### Pull Requests

1. **Fork the repository** and create a new branch from `main`
2. **Make your changes** following our coding standards
3. **Add tests** for any new functionality
4. **Run the test suite** to ensure all tests pass
5. **Update documentation** if needed
6. **Submit a pull request** with a clear description

### Coding Standards

- Follow PEP 8 style guidelines
- Use type hints where appropriate
- Write docstrings for functions and classes
- Keep functions focused and small
- Add comments for complex logic

### Testing

- All new features must include tests
- Maintain test coverage
- Run tests before submitting: `pytest tests/ -v`

### Commit Messages

Use clear, descriptive commit messages:
```
feat: Add customer referral system
fix: Correct cashback calculation for large transactions
docs: Update API documentation for payouts
test: Add tests for gift card redemption
```

## Development Setup

1. Clone your fork:
```bash
git clone https://github.com/YOUR_USERNAME/Free-xchanged-master-system.git
cd Free-xchanged-master-system
```

2. Create a virtual environment:
```bash
python -m venv venv
source venv/bin/activate
```

3. Install dependencies:
```bash
pip install -r requirements.txt
```

4. Initialize the database:
```bash
python init_db.py seed
```

5. Run tests:
```bash
pytest tests/ -v
```

## Project Structure

```
├── main.py              # FastAPI application
├── models.py           # Database models
├── schemas.py          # Pydantic schemas
├── services.py         # Business logic
├── database.py         # Database configuration
├── config.py           # Application configuration
├── init_db.py          # Database initialization
├── integrations/       # External integrations
│   └── stripe.py      # Stripe payment processing
├── utils/             # Utility functions
│   ├── error_handlers.py
│   ├── retry_logic.py
│   └── validators.py
└── tests/             # Test suite
    ├── test_api.py
    └── conftest.py
```

## Questions?

Feel free to open an issue for any questions or concerns!

## License

By contributing, you agree that your contributions will be licensed under the same license as the project.
