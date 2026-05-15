# Contributing to Thai Food Image Classification API

Thank you for your interest in contributing! This document provides guidelines for contributing to this project.

## Getting Started

1. Fork the repository
2. Clone your fork: `git clone https://github.com/YOUR_USERNAME/thai-food-image-classification-api.git`
3. Create a virtual environment: `python -m venv venv`
4. Activate the virtual environment:
   - Linux/Mac: `source venv/bin/activate`
   - Windows: `venv\Scripts\activate`
5. Install dependencies: `pip install -r requirements.txt -r requirements-dev.txt`

## Development Workflow

### 1. Create a Feature Branch

```bash
git checkout -b feature/your-feature-name
```

Use descriptive branch names:
- `feature/` for new features
- `fix/` for bug fixes
- `docs/` for documentation
- `refactor/` for code refactoring

### 2. Make Your Changes

- Write clean, readable code
- Follow PEP 8 style guidelines
- Add docstrings to functions and classes
- Update tests as needed

### 3. Run Tests

```bash
# Run all tests
pytest

# Run with coverage
pytest --cov=. --cov-report=html

# Run specific test file
pytest tests/test_api.py
```

### 4. Code Quality Checks

```bash
# Format code with Black
black .

# Run linter
flake8 .

# Type checking (if using mypy)
mypy .
```

### 5. Commit Your Changes

Write clear, descriptive commit messages:

```bash
git add .
git commit -m "Add feature: description of what you added"
```

Good commit messages:
- `Add endpoint for batch image processing`
- `Fix rate limiting bug for concurrent requests`
- `Update README with deployment instructions`

### 6. Push and Create Pull Request

```bash
git push origin feature/your-feature-name
```

Then create a pull request on GitHub with:
- Clear title and description
- Reference any related issues
- Screenshots (if applicable)

## Code Style Guidelines

### Python

- Follow PEP 8
- Maximum line length: 100 characters
- Use type hints where appropriate
- Write docstrings for all public functions/classes

Example:
```python
def predict_image(image_path: str, model_name: str = 'xception') -> list:
    """
    Predict Thai food dish from image.

    Args:
        image_path: Path to image file
        model_name: Model to use ('xception' or 'mobilenet')

    Returns:
        List of predictions with confidence scores
    """
    pass
```

### Testing

- Write tests for new features
- Maintain test coverage above 80%
- Use descriptive test names
- Follow AAA pattern (Arrange, Act, Assert)

Example:
```python
def test_upload_image_success(client, mock_mongo):
    """Test successful image upload and prediction."""
    # Arrange
    image_file = create_test_image()

    # Act
    response = client.post('/api/upload', data={'image': image_file})

    # Assert
    assert response.status_code == 201
    assert 'predict_result' in response.json
```

## Project Structure

```
thai-food-image-classification-api/
├── src/
│   ├── api/          # API routes and endpoints
│   ├── services/     # Business logic
│   ├── config/       # Configuration files
│   └── utils/        # Utility functions
├── tests/            # Test files
├── models/           # ML model files
└── docs/             # Documentation
```

## Pull Request Guidelines

### Before Submitting

- [ ] All tests pass
- [ ] Code is formatted with Black
- [ ] No linting errors
- [ ] Documentation is updated
- [ ] Commit messages are clear

### PR Description Template

```markdown
## Description
Brief description of changes

## Type of Change
- [ ] Bug fix
- [ ] New feature
- [ ] Breaking change
- [ ] Documentation update

## Testing
Describe how you tested your changes

## Checklist
- [ ] Tests pass locally
- [ ] Code follows style guidelines
- [ ] Documentation updated
- [ ] No new warnings
```

## Reporting Issues

When reporting bugs, include:
- Clear description of the problem
- Steps to reproduce
- Expected vs actual behavior
- Environment details (OS, Python version)
- Error messages/logs

## Questions?

Feel free to open an issue for questions or discussions.

## License

By contributing, you agree that your contributions will be licensed under the MIT License.
