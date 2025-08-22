# ❓ Frequently Asked Questions - cohereants

## 🧬 **Getting Started with Insect Olfaction Research**

### **Q: What is the cohereants project about?**
**A:** cohereants is a research project investigating the vibrational theory of olfaction in insects. We explore how insects may detect infrared radiation from semiochemicals rather than relying solely on molecular binding mechanisms, with computational models of insect sensory systems and spectral analysis.

### **Q: How do I use this research framework?**
**A:** Clone the repository and customize it for your entomological research. The framework includes specialized modules for insect sensory system modeling, infrared spectroscopy analysis, atmospheric transmission calculations, and professional scientific manuscript generation.

### **Q: What computational methods does this support?**
**A:** The framework is designed for Python-based computational entomology research, with specialized modules for spectral analysis, morphological modeling, and behavioral data analysis. All research code maintains 100% test coverage for scientific reproducibility.

## 🏗️ **Entomological Research Structure**

### **Q: Why is the project structured this way?**
**A:** The structure follows the "thin orchestrator pattern" specialized for entomological research, separating insect sensory models (`src/`) from research orchestration (`scripts/`). This ensures scientifically accurate, testable models while keeping analysis scripts focused on specific entomological investigations.

### **Q: What's the difference between `src/` and `scripts/`?**
**A:**
- **`src/`** contains all insect sensory algorithms, spectral analysis models, and morphological calculations with 100% test coverage
- **`scripts/`** are lightweight analysis wrappers that import and use entomological models, never implement sensory algorithms

### **Q: Do I need to keep the 100% test coverage requirement?**
**A:** Absolutely! For scientific research, maintaining 100% test coverage ensures the validity and reproducibility of your entomological models. The build pipeline enforces this to maintain scientific standards and prevent errors in sensory system calculations.

## 📚 **Scientific Manuscript & Analysis Generation**

### **Q: How does the scientific manuscript generation work?**
**A:** The framework uses Pandoc to convert entomological research markdown to LaTeX, then XeLaTeX to generate scientific manuscripts. The `render_pdf.sh` script orchestrates spectral analysis, morphological modeling, and cross-referencing for insect sensory research.

### **Q: Can I customize the manuscript output format?**
**A:** Yes! The LaTeX templates and Pandoc configurations can be customized for entomological publications. You can modify scientific formatting, add entomology-specific notation, or generate formats suitable for journals like Journal of Insect Physiology or Entomologia Experimentalis et Applicata.

### **Q: How do I add cross-references between research sections?**
**A:** The framework includes a scientific cross-referencing system for insect sensory research. You can reference spectral analyses, morphological data, and behavioral experiments between manuscript sections using LaTeX labels and the `\ref{}` command.

### **Q: What if I don't need manuscript generation?**
**A:** You can use just the computational entomology modules in `src/` for spectral analysis and morphological modeling without the manuscript generation features. The framework is modular and supports pure computational research workflows.

## 🧪 **Entomological Research Testing & Development**

### **Q: Why is test coverage so important for insect olfaction research?**
**A:** Test coverage ensures that your insect sensory models and spectral analysis algorithms work correctly and remain scientifically valid as you develop new research findings. In entomological research, accuracy is critical for drawing valid conclusions about insect perception and behavior.

### **Q: How do I add new tests for entomological models?**
**A:** Create test files in the `tests/` directory following the naming convention `test_*.py`. Use real entomological datasets and ensure your tests cover all code paths in your insect sensory modules. Include tests for edge cases like different sensilla dimensions or atmospheric conditions.

### **Q: Can I use different testing frameworks for research validation?**
**A:** While pytest is the default for maintaining research reproducibility, you can adapt the framework to use other testing tools. However, maintaining the 100% coverage requirement is essential for scientific validity, so any changes must preserve this standard.

## 🔧 **Customization & Extension**

### **Q: How do I rename the project?**
**A:** Use the `rename_project.sh` script in `repo_utilities/` to automatically update all references to the project name throughout the codebase.

### **Q: Can I add new output formats?**
**A:** Absolutely! The template is designed to be extensible. You can add new output formats by creating new scripts and updating the build pipeline.

### **Q: How do I integrate with other tools?**
**A:** The template provides hooks and utilities that make it easy to integrate with CI/CD systems, documentation generators, and other development tools.

## 🚨 **Troubleshooting**

### **Q: The build pipeline fails - what should I check?**
**A:** 
1. Ensure all tests pass with 100% coverage
2. Check that all required dependencies are installed
3. Verify that your markdown files are properly formatted
4. Check the build logs for specific error messages

### **Q: My PDFs aren't generating correctly**
**A:** 
1. Verify Pandoc and LaTeX are properly installed
2. Check that your markdown syntax is correct
3. Ensure all referenced figures and files exist
4. Review the LaTeX templates for any syntax issues

### **Q: How do I debug test failures?**
**A:** 
1. Run tests with verbose output: `pytest -v`
2. Use pytest's debugging features: `pytest --pdb`
3. Check coverage reports: `pytest --cov=src --cov-report=html`
4. Review the test output for specific error messages

## 🌟 **Advanced Usage**

### **Q: Can I use this for collaborative research?**
**A:** Yes! The template includes issue templates, pull request templates, and contribution guidelines that make collaboration easy and professional.

### **Q: How do I contribute improvements back to the template?**
**A:** Fork the repository, make your improvements, and submit a pull request. See `CONTRIBUTING.md` for detailed guidelines.

### **Q: Can I use this template commercially?**
**A:** Yes, the template is licensed under the Apache License 2.0, which allows commercial use, modification, and distribution.

### **Q: How do I stay updated with template improvements?**
**A:** Watch the repository for updates, check the changelog, and consider contributing improvements back to the community.

## 📞 **Getting Help**

### **Q: Where can I get more help?**
**A:** 
1. Check the comprehensive documentation in the markdown directory
2. Open an issue on GitHub for specific problems
3. Review the examples and workflow guides
4. Join the community discussions

For detailed documentation, see **[`README.md`](README.md)**, **[`ARCHITECTURE.md`](ARCHITECTURE.md)**, and **[`WORKFLOW.md`](WORKFLOW.md)**.

### **Q: Can I request new features?**
**A:** Yes! Use the feature request issue template to suggest improvements. We welcome all suggestions that would benefit the broader community.

---

**Still have questions? [Open an issue](https://github.com/docxology/template/issues) and we'll help you out! 🚀**

For more information, see **[`CONTRIBUTING.md`](CONTRIBUTING.md)** and **[`CODE_OF_CONDUCT.md`](CODE_OF_CONDUCT.md)**.
