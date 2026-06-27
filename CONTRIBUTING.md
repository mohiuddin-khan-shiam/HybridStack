# Contributing to HybridStack

Thank you for your interest in contributing to HybridStack! We welcome contributions from the community and are grateful for any help you can provide — whether it's reporting bugs, suggesting features, improving documentation, or writing code.

## How to Contribute

There are many ways to contribute to this project:

- **Report bugs** you encounter
- **Suggest enhancements** or new features
- **Submit pull requests** with bug fixes or improvements
- **Improve documentation** for clarity and completeness

## Reporting Bugs

If you find a bug, please open an issue on [GitHub Issues](https://github.com/mohiuddin-khan-shiam/HybridStack/issues) using the **Bug Report** template. To help us resolve the issue quickly, please include:

- **A clear and descriptive title** summarizing the problem.
- **Your environment details**: operating system, Python version, and relevant package versions (output of `pip freeze`).
- **Steps to reproduce** the issue, with minimal code examples if possible.
- **Expected behavior** — what you expected to happen.
- **Actual behavior** — what actually happened, including any error messages or tracebacks.
- **Screenshots or logs** if applicable.

## Suggesting Enhancements

We welcome ideas for improving HybridStack. To suggest an enhancement, please open an issue using the **Feature Request** template and include:

- A clear description of the **problem or limitation** you're addressing.
- Your **proposed solution** and how it would benefit users.
- Any **alternatives** you've considered.

## Code Contributions

We follow a standard fork-and-pull workflow:

1. **Fork** the repository on GitHub.
2. **Clone** your fork locally:
   ```bash
   git clone https://github.com/<your-username>/HybridStack.git
   cd HybridStack
   ```
3. **Create a feature branch** from `main`:
   ```bash
   git checkout -b feature/your-feature-name
   ```
4. **Install dependencies**:
   ```bash
   pip install -r requirements.txt
   ```
5. **Make your changes**, following the code style guidelines below.
6. **Test your changes** locally to ensure nothing is broken.
7. **Commit** your changes with a clear, descriptive commit message:
   ```bash
   git commit -m "Add brief description of your change"
   ```
8. **Push** your branch to your fork:
   ```bash
   git push origin feature/your-feature-name
   ```
9. **Open a Pull Request** against the `main` branch of this repository. Fill out the PR template and provide a clear description of your changes.

### Pull Request Guidelines

- Keep pull requests focused — one feature or fix per PR.
- Reference any related issues in your PR description (e.g., "Fixes #42").
- Ensure your code passes all existing checks.
- Update the `CHANGELOG.md` if your change is user-facing.

## Code Style

Please adhere to the following coding standards:

- **PEP 8**: Follow [PEP 8](https://peps.python.org/pep-0008/) style guidelines for all Python code.
- **Docstrings**: Use descriptive docstrings for all public modules, functions, classes, and methods. We recommend the [NumPy/SciPy docstring format](https://numpydoc.readthedocs.io/en/latest/format.html).
- **Type hints**: Use type hints for function signatures where practical.
- **Naming conventions**: Use clear, descriptive variable and function names. Avoid single-letter variable names except for conventional loop counters.
- **Comments**: Add comments to explain *why* something is done, not *what* is done — the code itself should be readable enough to convey the what.

## Documentation

- If your contribution changes any functionality, please update the relevant documentation.
- Ensure that docstrings are up to date with your code changes.
- If you add a new module, script, or notebook, include appropriate documentation explaining its purpose and usage.

## License

By contributing to HybridStack, you agree that your contributions will be licensed under the [Apache License 2.0](LICENSE), the same license that covers this project.

---

Thank you for helping make HybridStack better!
