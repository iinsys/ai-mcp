# Contributing to AI & MCP Toolkit

Thank you for your interest in contributing! This document provides guidelines for contributing to this project.

## 🚀 Getting Started

1. Fork the repository
2. Clone your fork: `git clone https://github.com/[your-username]/ai-mcp.git`
3. Create a feature branch: `git checkout -b feature/your-feature-name`
4. Make your changes
5. Test your changes
6. Commit with a clear message: `git commit -m "Add: description of your changes"`
7. Push to your fork: `git push origin feature/your-feature-name`
8. Create a Pull Request

## 📁 Project Structure

When adding new components:

- **MCP Servers**: Add to `mcp-servers/[server-name]/`
- **Tools**: Add to `tools/[tool-name]/`
- **Examples**: Add to `examples/[example-name]/`
- **Documentation**: Add to `docs/`

## 🔧 Development Guidelines

### Code Style

- Use clear, descriptive variable and function names
- Include docstrings for all public functions
- Follow language-specific style guides (PEP 8 for Python, etc.)
- Add type hints where applicable

### Documentation

- Include a README.md for each new component
- Document installation and usage instructions
- Provide examples of usage
- Update the main README.md if adding new categories

### Testing

- Include tests for new functionality
- Ensure existing tests pass
- Add integration tests for MCP servers

## 🐛 Reporting Issues

When reporting issues, please include:

- Clear description of the problem
- Steps to reproduce
- Expected vs actual behavior
- Environment details (OS, Python version, etc.)
- Relevant error messages or logs

## 💡 Feature Requests

For feature requests:

- Check existing issues first
- Provide clear use case and rationale
- Consider implementation complexity
- Be open to discussion and feedback

## 📋 Pull Request Guidelines

- Keep PRs focused and atomic
- Include tests for new features
- Update documentation as needed
- Ensure CI passes
- Respond to review feedback promptly

## 🏷️ Commit Message Format

Use clear, descriptive commit messages:

```
Add: new MCP server for database operations
Fix: connection timeout in weather server
Update: documentation for tool installation
Remove: deprecated utility functions
```

## 📞 Getting Help

- Check existing documentation first
- Search existing issues
- Create a new issue with the "question" label
- Join discussions in the GitHub Discussions tab

Thank you for contributing! 🎉