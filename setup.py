"""
Z Model: Control-Theoretic Heuristic for Governed Adaptive Systems
"""

from setuptools import setup, find_packages
from pathlib import Path

# Read long description from README
this_directory = Path(__file__).parent
long_description = (this_directory / "README.md").read_text()

setup(
    name="z-model",
    version="1.6.0",
    author="jnotary",
    author_email="jnotary@hotmail.com",
    description="A control-theoretic heuristic for governed adaptive systems",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/jnotary/z-model",
    project_urls={
        "Bug Tracker": "https://github.com/jnotary/z-model/issues",
        "Documentation": "https://github.com/jnotary/z-model",
        "Source Code": "https://github.com/jnotary/z-model",
        "Website": "https://cloudsystems.online",
    },
    packages=find_packages(),
    classifiers=[
        "Development Status :: 4 - Beta",
        "Intended Audience :: Developers",
        "Intended Audience :: Science/Research",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
        "Topic :: Scientific/Engineering :: Artificial Intelligence",
        "Topic :: Software Development :: Libraries :: Python Modules",
        "Topic :: System :: Monitoring",
    ],
    keywords=[
        "ai-safety",
        "control-theory",
        "governance",
        "llm-safety",
        "alignment",
        "feedback-control",
        "adaptive-systems",
        "constitutional-ai",
    ],
    python_requires=">=3.8",
    install_requires=[
        "numpy>=1.24.0",
        "scipy>=1.10.0",
    ],
    extras_require={
        "llm": [
            "sentence-transformers>=2.2.0",
            "torch>=2.0.0",
        ],
        "viz": [
            "matplotlib>=3.7.0",
        ],
        "dev": [
            "pytest>=7.0.0",
            "pytest-cov>=4.0.0",
            "jupyter>=1.0.0",
            "flake8>=6.0.0",
            "black>=23.0.0",
        ],
        "all": [
            "sentence-transformers>=2.2.0",
            "torch>=2.0.0",
            "matplotlib>=3.7.0",
            "pytest>=7.0.0",
            "pytest-cov>=4.0.0",
            "jupyter>=1.0.0",
        ],
    },
    entry_points={
        "console_scripts": [
            "z-model=src.z_model:main",
        ],
    },
    license="MIT",
    platforms="any",
)
