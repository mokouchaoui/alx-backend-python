# Unittests and Integration Tests

This contains unit and integration tests for a Python backend project, following ALX School's Software Engineering backend specialization curriculum.

## 📚 Project Structure
```
.
├── client.py
├── utils.py
├── test_client.py
├── test_utils.py
├── fixtures.py
└── README.md
```

## 🚀 Features

- **Unit Tests** for:
  - `utils.py` functions: `access_nested_map`, `get_json`, and `memoize`
  - `GithubOrgClient` methods in `client.py`

- **Integration Tests**:
  - Tests for `GithubOrgClient` fetching data from the GitHub API.

## 🧪 Testing

### Setup

Install dependencies:

```bash
pip install -r requirements.txt
```

### Run Tests

```python
python3 -m unittest discover
```

## Tools Used

- `unittest`

- `parameterized`

- `unittest.mock`

## 💡 Key Learnings

- Unit testing with unittest

- Mocking external API calls

- Parameterizing tests

- Writing integration tests for real-world APIs

## 🔖 Author
[Yasir Musa](https://github.com/baydre) | ALX Pro-Dev Backend Track

---