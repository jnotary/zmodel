# Contributing to the Z Model

Thank you for your interest in contributing to the Z Model project! This is a research framework that values both rigorous mathematical foundations and practical implementations.

## Ways to Contribute

### 1. **Bug Reports & Issues**
Found a bug or have a question? [Open an issue](https://github.com/jnotary/z-model/issues)

**Good bug reports include:**
- Clear description of the problem
- Steps to reproduce
- Expected vs actual behavior
- Environment details (Python version, OS, etc.)
- Minimal code example

### 2. **Feature Requests**
Have an idea for an improvement? Start a [discussion](https://github.com/jnotary/z-model/discussions)

**Good feature requests:**
- Explain the use case
- Describe the desired behavior
- Suggest an implementation approach (optional)
- Note any related work or prior art

### 3. **Code Contributions**
Submit a pull request! See guidelines below.

### 4. **Documentation**
Improve docs, add examples, write tutorials, fix typos.

### 5. **Research Contributions**
- Case studies showing Z Model in practice
- Domain-specific calibrations (Ψ angles for different fields)
- Novel hazard functions H(Q)
- Validation datasets
- Benchmarking against other methods

## Development Setup

```bash
# Clone the repository
git clone https://github.com/jnotary/z-model.git
cd z-model

# Create virtual environment
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Run tests
pytest tests/

# Run the demo
python src/z_model.py
```

## Code Standards

### Style Guidelines
- Follow [PEP 8](https://pep8.org/) style guidelines
- Use type hints for function signatures
- Maximum line length: 100 characters
- Use descriptive variable names

### Documentation
- Add docstrings to all public functions and classes
- Use Google-style docstrings
- Include examples in docstrings when helpful
- Update README.md if adding new features

### Testing
- Write unit tests for new features
- Maintain or improve test coverage
- Run `pytest` before submitting PRs
- Include edge cases and error conditions

### Example of Good Code:

```python
def calculate_z(
    self, 
    A: float, 
    E: float, 
    C: float, 
    Psi_deg: float
) -> float:
    """
    Calculate Z score with governance gating.
    
    Args:
        A: Adaptability (> 0)
        E: Energy/Efficacy (> 0)
        C: Constraints/Cost (> 0)
        Psi_deg: Alignment angle in degrees [0, 180]
    
    Returns:
        Z score (governed capability index)
    
    Raises:
        ValueError: If C <= 0 (singularity)
    
    Example:
        >>> z_model = ZModel()
        >>> z_score = z_model.calculate_z(0.8, 0.9, 0.3, 30)
        >>> print(f"Z = {z_score:.3f}")
        Z = 1.800
    """
    if C <= 0:
        raise ValueError("Cost C must be positive")
    
    base_z = (A * E) / C
    Psi_rad = np.radians(Psi_deg)
    
    return base_z * (np.cos(Psi_rad) ** 2)
```

## Pull Request Process

### 1. Fork & Branch
```bash
# Fork the repository on GitHub, then:
git clone https://github.com/YOUR_USERNAME/z-model.git
cd z-model
git checkout -b feature/amazing-feature
```

### 2. Make Changes
- Write your code
- Add tests
- Update documentation
- Commit with clear messages

```bash
git add .
git commit -m "Add amazing feature: brief description

Longer explanation of what changed and why.
Fixes #123"
```

### 3. Test Locally
```bash
# Run tests
pytest tests/

# Check style (optional but appreciated)
flake8 src/
```

### 4. Push & Create PR
```bash
git push origin feature/amazing-feature
```

Then open a Pull Request on GitHub with:
- Clear title summarizing the change
- Description of what changed and why
- Reference to any related issues
- Screenshots/examples if applicable

### 5. Code Review
- Address reviewer feedback
- Make requested changes
- Push updates to your branch
- PR will be merged once approved

## Areas of Particular Interest

### Domain-Specific Calibrations
What Ψ angles work best for your field?
- Financial systems: strict governance (Ψ = 60°?)
- Creative AI: looser constraints (Ψ = 20°?)
- Medical AI: maximum safety (Ψ = 70°?)

Share your findings!

### Hazard Functions
Novel implementations of H(Q) for specific threats:
- Adversarial prompt detection
- Data poisoning resilience
- Distribution shift monitoring
- Concept drift tracking

### Integration Examples
Show how Z Model integrates with:
- LangChain
- Ray
- Kubernetes operators
- Cloud platforms (AWS, Azure, GCP)
- Monitoring systems (Prometheus, Grafana)

### Validation Studies
Empirical testing:
- Benchmark datasets
- Comparison with baselines
- Real-world deployment results
- A/B test outcomes

## Mathematical Contributions

If proposing changes to the core equations:
1. Provide mathematical justification
2. Show dimensional consistency
3. Prove or argue for stability properties
4. Include simulation results
5. Compare against v1.6 baseline

## Code of Conduct

### Core Principles
- **Be respectful and constructive**
- **Focus on the work, not the person**
- **Assume good intentions**
- **Safety-critical systems require higher scrutiny**

### Expected Behavior
- Use welcoming and inclusive language
- Be respectful of differing viewpoints
- Accept constructive criticism gracefully
- Focus on what is best for the community
- Show empathy towards other contributors

### Unacceptable Behavior
- Harassment or discriminatory language
- Trolling or insulting comments
- Public or private harassment
- Publishing others' private information
- Other conduct inappropriate in a professional setting

## Questions?

- **Email**: jnotary@hotmail.com
- **Discussions**: [GitHub Discussions](https://github.com/jnotary/z-model/discussions)
- **Issues**: [GitHub Issues](https://github.com/jnotary/z-model/issues)

## Recognition

Contributors will be acknowledged in:
- CONTRIBUTORS.md file
- Release notes
- Documentation (for significant contributions)

## License

By contributing, you agree that your contributions will be licensed under:
- **MIT License** for code
- **CC-BY-4.0** for theoretical/documentation contributions

---

*Thank you for helping make the Z Model better!*

*"Life and Technology in Harmony."*
