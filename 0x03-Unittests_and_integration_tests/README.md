# 0x03. Unittests and Integration Tests

This project focuses on writing **unit tests** and **integration tests** in Python using the `unittest` module. You will learn how to:

- Write test cases for Python functions and classes.
- Use `parameterized.expand` for multiple input/output pairs.
- Use `assertEqual`, `assertRaises`, and other assertion methods.
- Mock methods and functions using `unittest.mock`.
- Structure your tests properly with setup and teardown methods.

## 📁 Project Structure

```
alx-backend-python/
├── 0x03-Unittests_and_integration_tests/
│   ├── test_utils.py
│   ├── test_client.py
│   ├── utils.py
│   ├── client.py
│   └── README.md
```

## 🧪 test_utils.py

Contains tests for `utils.access_nested_map()` function.

### ✅ Unit tests implemented

- **test_access_nested_map**: Tests that the correct value is returned for valid nested maps.
- **test_access_nested_map_exception**: Tests that `KeyError` is raised with the expected message when accessing invalid keys.

Tests are parameterized using the `@parameterized.expand` decorator for multiple test scenarios.

### Example test:

```python
@parameterized.expand([
    ({"a": {"b": 2}}, ("a", "b"), 2),
])
def test_access_nested_map(self, nested_map, path, expected):
    self.assertEqual(access_nested_map(nested_map, path), expected)
```

Exception testing with context manager:

```python
with self.assertRaises(KeyError) as cm:
    access_nested_map({}, ("a",))
self.assertEqual(str(cm.exception), "'a'")
```

## 🧰 Tools and Libraries

* Python 3.10+
* `unittest` — standard library for testing
* `parameterized` — for cleaner, data-driven test cases

Install `parameterized` if not already installed:

```bash
pip install parameterized
```

## 🚀 Run Tests

You can run the tests using `unittest` or `pytest`:

```bash
# With unittest
python3 -m unittest discover

# Or with pytest (if installed)
pytest
```

## 🧠 Author

This project was developed as part of the ALX Software Engineering Backend Curriculum.