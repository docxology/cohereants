# 🤝 Contributing to cohereants - Insect Olfaction Research

Thank you for your interest in contributing to the cohereants project! This research investigates the vibrational theory of olfaction in insects and explores how insects may detect infrared radiation from semiochemicals. Your contributions help advance our understanding of insect sensory systems and perception.

## 🎯 **How to Contribute**

### 🚀 **Using the Research Framework**
The best way to contribute is to **use this framework** for your own entomological research and provide feedback on the insect sensory models, spectral analysis methods, and research workflows.

### 🐛 **Reporting Research Issues**
- **Model validation issues** help us improve insect sensory algorithms
- **Spectral analysis bugs** help us fix infrared detection calculations
- **Documentation improvements** for entomological research methods
- **Feature requests** for new insect species or sensory models

### 🔧 **Entomological Research Contributions**
- **Insect sensory model improvements** - enhance existing algorithms for sensilla morphology or infrared detection
- **New insect species models** - add support for additional insect taxa with different sensory adaptations
- **Spectral analysis enhancements** - improve infrared spectroscopy calculations and atmospheric transmission models
- **Behavioral analysis modules** - add new methods for analyzing insect behavioral responses
- **Research validation tests** - ensure 100% test coverage for all entomological algorithms

## 🏗️ **Entomological Research Development Setup**

### 1. **Fork and Clone**
```bash
git clone https://github.com/YOUR_USERNAME/cohereants.git
cd cohereants
```

### 2. **Install Dependencies**
```bash
# Create virtual environment
python3 -m venv .venv
source .venv/bin/activate  # On Windows: .venv\Scripts\activate

# Install dependencies
pip install -e ".[dev]"
```

### 3. **Run Tests**
```bash
# Run all tests
pytest

# Run with coverage
pytest --cov=src --cov-report=html
```

## 📋 **Entomological Research Contribution Guidelines**

### 🧪 **Research Testing Requirements**
- **100% test coverage** is required for all insect sensory models in `src/`
- **All entomological tests must pass** before research contributions are accepted
- **Add scientific validation tests** for new sensory algorithms
- **Update tests** when fixing spectral analysis or morphological calculation bugs
- **Include real entomological data** in tests, not mocks

### 📝 **Entomological Research Code Style**
- **Follow PEP 8** for Python code with scientific computing conventions
- **Use descriptive entomological names** (e.g., `sensilla_diameter`, `ir_wavelength`, `atmospheric_transmission`)
- **Add comprehensive docstrings** for all entomological functions with units and biological context
- **Keep functions focused** on specific sensory calculations or morphological analyses
- **Include scientific references** in docstrings for theoretical foundations

### 📚 **Entomological Research Documentation**
- **Update README.md** if adding new insect species or sensory models
- **Add comprehensive docstrings** to new entomological functions with biological context
- **Update research methodology** in the markdown directory when adding new analysis methods
- **Include entomological examples** with real insect species data
- **Document scientific assumptions** and theoretical foundations in comments

### 🔄 **Entomological Research Commit Messages**
Use clear, descriptive commit messages that reference the scientific context:
```
feat: add Apis mellifera sensilla morphology model
fix: correct infrared wavelength calculation for Drosophila antenna
docs: update vibrational theory references in methodology
test: add spectral analysis validation for Bombyx mori
refactor: optimize atmospheric transmission algorithm
```

## 🚀 **Making Changes**

### 1. **Create a Branch**
```bash
git checkout -b feature/your-feature-name
# or
git checkout -b fix/issue-description
```

### 2. **Make Your Changes**
- **Implement the feature/fix**
- **Add/update tests**
- **Update documentation**
- **Ensure all tests pass**

### 3. **Test Your Changes**
```bash
# Run the full test suite
pytest

# Check coverage
pytest --cov=src --cov-report=html

# Test the build pipeline
./repo_utilities/render_pdf.sh
```

### 4. **Submit a Pull Request**
- **Clear description** of what the PR accomplishes
- **Reference any issues** being addressed
- **Include screenshots** if UI changes
- **Describe testing** performed

## 🎯 **What We're Looking For**

### 🌟 **High Priority**
- **Bug fixes** that affect template usability
- **Documentation improvements** for clarity
- **Test coverage** improvements
- **Performance optimizations**

### 🔧 **Medium Priority**
- **New utility functions** that benefit many users
- **Enhanced error handling** and user feedback
- **Additional output formats** (HTML, Word, etc.)
- **Integration examples** with popular tools

### 💡 **Low Priority**
- **Cosmetic changes** that don't improve functionality
- **Very specific features** that only benefit niche use cases
- **Breaking changes** without clear migration path

## 🚫 **What We're NOT Looking For**

- **Breaking changes** to the core architecture
- **Dependencies** on proprietary software
- **Platform-specific code** that doesn't work cross-platform
- **Changes** that reduce test coverage

## 🤝 **Getting Help**

### 💬 **Questions?**
- **Open an issue** with the "question" label
- **Check existing issues** for similar questions
- **Review the documentation** in the markdown directory

### 🔍 **Stuck on Something?**
- **Describe what you're trying to do**
- **Include error messages** and stack traces
- **Share your environment** (OS, Python version, etc.)
- **Provide minimal reproduction steps**

## 📚 **Resources**

- **[`ARCHITECTURE.md`](ARCHITECTURE.md)** - System design overview
- **[`WORKFLOW.md`](WORKFLOW.md)** - Development workflow guide
- **[`MARKDOWN_TEMPLATE_GUIDE.md`](MARKDOWN_TEMPLATE_GUIDE.md)** - Writing and formatting guide
- **[`EXAMPLES.md`](EXAMPLES.md)** - Usage examples and customization
- **[`README.md`](README.md)** - Project overview and quick start
- **[`THIN_ORCHESTRATOR_SUMMARY.md`](THIN_ORCHESTRATOR_SUMMARY.md)** - Architecture implementation details

## 🎉 **Thank You!**

Every contribution, no matter how small, helps make this template better for researchers and developers worldwide. Thank you for your time and effort!

---

**Happy contributing! 🚀**
