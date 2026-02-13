# Contributing to StoryCircuit

Thank you for your interest in contributing to StoryCircuit! This document provides guidelines for contributing to the project.

## 🚀 Getting Started

1. **Fork the repository** on GitHub
2. **Clone your fork** locally:
   ```bash
   git clone https://github.com/YOUR-USERNAME/storycircuit.git
   cd storycircuit
   ```
3. **Create a branch** for your changes:
   ```bash
   git checkout -b feature/your-feature-name
   ```

## 📋 Development Process

### Before Making Changes

1. Read the project specifications:
   - [REQUIREMENTS.md](REQUIREMENTS.md) - Functional requirements
   - [ARCHITECTURE.md](ARCHITECTURE.md) - System architecture
   - [API_SPEC.md](API_SPEC.md) - API contracts
   - [SECURITY.md](SECURITY.md) - Security guidelines

2. Check existing issues and pull requests to avoid duplication

3. For major changes, open an issue first to discuss the proposed changes

### Making Changes

1. **Follow the coding standards:**
   - Python: PEP 8 style guide
   - Use type hints for Python code
   - Write clear, descriptive variable and function names
   - Add docstrings to functions and classes

2. **Write tests:**
   - Add unit tests for new functionality
   - Maintain or improve code coverage (70%+ target)
   - Ensure all tests pass before submitting

3. **Update documentation:**
   - Update README.md if adding features
   - Update API_SPEC.md for API changes
   - Add inline code comments for complex logic

### Testing Your Changes

```bash
# Run all tests
cd backend
pytest tests/

# Run with coverage
pytest tests/ --cov=app --cov-report=html

# Check code style
flake8 app/
black --check app/
```

### Committing Changes

1. **Commit message format:**
   ```
   <type>(<scope>): <subject>
   
   <body>
   
   <footer>
   ```

2. **Commit types:**
   - `feat`: New feature
   - `fix`: Bug fix
   - `docs`: Documentation changes
   - `style`: Code style changes (formatting, no logic change)
   - `refactor`: Code refactoring
   - `test`: Adding or updating tests
   - `chore`: Maintenance tasks

3. **Examples:**
   ```
   feat(content): add support for Instagram platform
   
   - Add Instagram content formatting
   - Update parser to handle Instagram-specific rules
   - Add tests for Instagram content generation
   
   Closes #123
   ```

### Submitting a Pull Request

1. **Push your branch** to your fork:
   ```bash
   git push origin feature/your-feature-name
   ```

2. **Open a Pull Request** on GitHub with:
   - Clear title describing the change
   - Description of what changed and why
   - Reference to related issues (e.g., "Closes #123")
   - Screenshots for UI changes

3. **Wait for review:**
   - Address reviewer feedback
   - Keep your PR up to date with main branch
   - Be patient and respectful

## 🔒 Security Guidelines

**IMPORTANT:** Never commit sensitive information:
- ❌ API keys, passwords, or credentials
- ❌ Azure subscription IDs or tenant IDs
- ❌ `.env` files (use `.env.example` instead)
- ❌ Personal identifiable information (PII)

If you accidentally commit sensitive data:
1. **Do NOT** just delete it in a new commit
2. Contact maintainers immediately
3. We'll help you properly remove it from git history

## 🧪 Code Quality Standards

### Python Code Standards

- **Style:** Follow PEP 8
- **Type Hints:** Use type hints for function signatures
- **Docstrings:** Use Google-style docstrings
- **Line Length:** Max 100 characters
- **Imports:** Group and sort imports (standard lib, third-party, local)

### Testing Standards

- **Unit Tests:** Test individual functions/methods
- **Integration Tests:** Test component interactions
- **Coverage:** Aim for 70%+ code coverage
- **Test Naming:** `test_<function>_<scenario>_<expected_result>`

Example:
```python
def test_generate_content_with_valid_topic_returns_content():
    """Test that content generation succeeds with valid topic."""
    # Arrange
    topic = "Azure Functions"
    platforms = ["linkedin"]
    
    # Act
    result = generate_content(topic, platforms)
    
    # Assert
    assert result is not None
    assert "linkedin" in result
```

## 🐛 Reporting Bugs

When reporting bugs, please include:

1. **Description:** Clear description of the bug
2. **Steps to Reproduce:**
   - Step-by-step instructions
   - Input data used
   - Expected vs actual behavior
3. **Environment:**
   - Python version
   - Operating system
   - Relevant dependencies
4. **Logs:** Error messages or relevant log output
5. **Screenshots:** If applicable

Use the GitHub issue template when creating a new issue.

## 💡 Suggesting Features

For feature requests:

1. **Check existing issues** first
2. **Describe the feature:**
   - What problem does it solve?
   - Who would benefit?
   - How should it work?
3. **Provide examples:** Mock-ups, code snippets, or user stories
4. **Consider scope:** Is it aligned with project goals?

## 📚 Documentation

Good documentation helps everyone:

- **README.md:** High-level overview and quick start
- **API_SPEC.md:** API endpoints and contracts
- **Code comments:** Explain "why" not "what"
- **Docstrings:** Document all public functions/classes

## ✅ Pull Request Checklist

Before submitting a PR, ensure:

- [ ] Code follows project style guidelines
- [ ] All tests pass (`pytest tests/`)
- [ ] New code has tests (70%+ coverage)
- [ ] Documentation is updated
- [ ] Commit messages follow convention
- [ ] No sensitive data in commits
- [ ] PR description is clear and complete
- [ ] Related issues are referenced

## 🤝 Code of Conduct

### Our Standards

- Be respectful and inclusive
- Welcome newcomers and beginners
- Focus on constructive feedback
- Assume good intentions
- Accept constructive criticism gracefully

### Unacceptable Behavior

- Harassment or discrimination
- Trolling or insulting comments
- Personal or political attacks
- Publishing others' private information
- Unprofessional conduct

## 📞 Questions?

- Open a [GitHub Discussion](https://github.com/vrengar/storycircuit/discussions)
- Create an [Issue](https://github.com/vrengar/storycircuit/issues) for bugs
- Check existing documentation

## 🎉 Recognition

Contributors will be:
- Listed in the repository contributors
- Acknowledged in release notes
- Appreciated by the community!

Thank you for contributing to StoryCircuit! 🚀

---

**Remember:** The best contribution is one that follows the guidelines, is well-tested, and helps make StoryCircuit better for everyone.
