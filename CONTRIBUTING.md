# Contributing to Top 5 Things Email Generator

Thank you for your interest in contributing! This document provides guidelines for contributing to the project.

## Getting Started

1. **Fork the repository**
   ```bash
   # Click "Fork" on GitHub, then clone your fork
   git clone https://github.com/YOUR_USERNAME/t5t.git
   cd t5t
   ```

2. **Set up development environment**
   ```bash
   # Create virtual environment
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   
   # Install dependencies
   pip install -r requirements.txt
   python -m spacy download en_core_web_sm
   ```

3. **Configure environment**
   ```bash
   cp .env.example .env
   # Edit .env with your Azure AD credentials
   ```

4. **Run locally**
   ```bash
   python app.py
   # Open http://localhost:5000
   ```

## Development Workflow

### Creating a Feature Branch

```bash
# Create and checkout a new branch
git checkout -b feature/your-feature-name

# Or for bug fixes
git checkout -b fix/bug-description
```

### Making Changes

1. **Write clean, readable code**
   - Follow PEP 8 style guide for Python
   - Add comments for complex logic
   - Keep functions focused and small

2. **Test your changes**
   ```bash
   # Test imports
   python -c "import app; import auth; import analyzer"
   
   # Run the app
   python app.py
   
   # Test in browser
   # Open http://localhost:5000 and test functionality
   ```

3. **Test with Docker**
   ```bash
   # Build and test
   docker-compose up --build
   ```

### Committing Changes

```bash
# Stage your changes
git add .

# Commit with descriptive message
git commit -m "Add feature: description of what you added"

# Push to your fork
git push origin feature/your-feature-name
```

### Commit Message Guidelines

- Use present tense ("Add feature" not "Added feature")
- Use imperative mood ("Move cursor to..." not "Moves cursor to...")
- First line should be 50 characters or less
- Reference issues and pull requests when relevant

Examples:
```
Add support for custom date ranges
Fix authentication token refresh issue
Update documentation for Azure AD setup
Improve NLP entity extraction accuracy
```

## Pull Request Process

1. **Create Pull Request**
   - Go to your fork on GitHub
   - Click "New Pull Request"
   - Select your feature branch
   - Fill in the PR template

2. **PR Description Should Include:**
   - What changes were made
   - Why the changes were necessary
   - How to test the changes
   - Screenshots (if UI changes)
   - Related issues

3. **Automated Checks**
   - GitHub Actions will automatically run tests
   - Docker image will be built (but not pushed)
   - All checks must pass before merging

4. **Code Review**
   - Wait for maintainer review
   - Address any feedback
   - Make requested changes

5. **Merge**
   - Once approved, maintainer will merge
   - Docker image will be automatically built and pushed to GHCR

## Code Style

### Python

- Follow PEP 8
- Use 4 spaces for indentation
- Maximum line length: 127 characters
- Use meaningful variable names

```python
# Good
def analyze_calendar_events(events, days_back=30):
    """Analyze calendar events for entity extraction."""
    pass

# Bad
def f(e, d=30):
    pass
```

### HTML/CSS

- Use 2 spaces for indentation
- Keep CSS organized by component
- Use semantic HTML

### JavaScript

- Use modern ES6+ syntax
- Use const/let instead of var
- Add comments for complex logic

## Testing

### Manual Testing Checklist

Before submitting a PR, test:

- [ ] Login flow works
- [ ] Calendar data is fetched correctly
- [ ] Email data is fetched correctly
- [ ] Analysis produces reasonable results
- [ ] Email draft is properly formatted
- [ ] Copy to clipboard works
- [ ] Download draft works
- [ ] Logout works
- [ ] Error handling works (try with invalid credentials)

### Docker Testing

```bash
# Build fresh image
docker-compose build --no-cache

# Run and test
docker-compose up

# Test in browser
# Open http://localhost:5000
```

## Areas for Contribution

### High Priority

- [ ] Add unit tests
- [ ] Add integration tests
- [ ] Improve NLP accuracy
- [ ] Add support for more email providers
- [ ] Internationalization (i18n)

### Medium Priority

- [ ] Add email template customization UI
- [ ] Historical draft tracking
- [ ] Export to multiple formats (PDF, Word)
- [ ] Scheduled automatic generation
- [ ] Better error messages

### Low Priority

- [ ] Dark mode UI
- [ ] Mobile app
- [ ] Browser extension
- [ ] Slack integration

## Documentation

When adding features, update:

- `README.md` - If it affects usage
- `SETUP.md` - If it affects setup
- `DEPLOYMENT.md` - If it affects deployment
- Code comments - For complex logic
- Docstrings - For all functions/classes

## Reporting Bugs

### Before Reporting

1. Check existing issues
2. Try with latest version
3. Test with clean environment

### Bug Report Should Include

- Description of the bug
- Steps to reproduce
- Expected behavior
- Actual behavior
- Screenshots (if applicable)
- Environment details:
  - OS (macOS, Windows, Linux)
  - Docker version
  - Python version (if running locally)
  - Browser (if UI issue)

### Bug Report Template

```markdown
**Description**
A clear description of the bug.

**To Reproduce**
1. Go to '...'
2. Click on '...'
3. See error

**Expected Behavior**
What you expected to happen.

**Screenshots**
If applicable, add screenshots.

**Environment**
- OS: [e.g., macOS 13.0]
- Docker: [e.g., 24.0.0]
- Browser: [e.g., Chrome 120]

**Additional Context**
Any other relevant information.
```

## Feature Requests

### Feature Request Template

```markdown
**Problem**
What problem does this solve?

**Proposed Solution**
How would you solve it?

**Alternatives Considered**
What other solutions did you consider?

**Additional Context**
Any other relevant information.
```

## Questions?

- Open an issue with the "question" label
- Check existing documentation
- Review closed issues for similar questions

## License

By contributing, you agree that your contributions will be licensed under the same license as the project.

## Code of Conduct

- Be respectful and inclusive
- Welcome newcomers
- Focus on constructive feedback
- Assume good intentions

## Thank You!

Your contributions make this project better for everyone. Thank you for taking the time to contribute! 🎉

