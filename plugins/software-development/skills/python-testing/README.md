# Python Testing - pytest Patterns

Progressive disclosure resource for Python testing with pytest.

## Basic Test Structure

```python
# tests/test_user.py
import pytest
from src.user import User

def test_create_user():
    """Test user creation"""
    user = User(name="Alice", email="alice@example.com")
    assert user.name == "Alice"
    assert user.email == "alice@example.com"

def test_invalid_email():
    """Test email validation"""
    with pytest.raises(ValueError):
        User(name="Bob", email="invalid")
```

## Fixtures

```python
@pytest.fixture
def sample_user():
    """Reusable test user"""
    return User(name="Test", email="test@example.com")

def test_with_fixture(sample_user):
    assert sample_user.name == "Test"
```

## Mocking

```python
from unittest.mock import Mock, patch

def test_api_call():
    """Test with mocked HTTP request"""
    with patch('requests.get') as mock_get:
        mock_get.return_value.json.return_value = {"status": "ok"}
        result = fetch_data()
        assert result["status"] == "ok"
```

## Coverage

```bash
# Run with coverage
pytest --cov=src tests/

# Generate HTML report
pytest --cov=src --cov-report=html tests/
```

## Token Budget

This skill: ~500 tokens
