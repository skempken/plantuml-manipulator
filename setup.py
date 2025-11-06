"""Setup configuration for PlantUML Manipulator."""

from setuptools import setup, find_packages
from pathlib import Path

# Read README for long description
readme = Path(__file__).parent / "README.md"
long_description = readme.read_text(encoding="utf-8") if readme.exists() else ""

setup(
    name="plantuml-manipulator",
    version="0.1.0-dev",
    description="Structured manipulation of PlantUML sequence diagrams",
    long_description=long_description,
    long_description_content_type="text/markdown",
    author="PlantUML Manipulator Contributors",
    author_email="",
    url="https://github.com/your-org/plantuml-manipulator",
    license="MIT",
    packages=find_packages(where="src"),
    package_dir={"": "src"},
    python_requires=">=3.8",
    install_requires=[
        "click>=8.1.0",
        "rich>=13.0.0",
    ],
    extras_require={
        "dev": [
            "pytest>=7.4.0",
            "pytest-cov>=4.1.0",
            "pytest-mock>=3.11.0",
            "black>=23.7.0",
            "mypy>=1.5.0",
            "flake8>=6.1.0",
            "isort>=5.12.0",
        ],
    },
    entry_points={
        "console_scripts": [
            "plantuml-manipulator=plantuml_manipulator.cli:main",
        ],
    },
    classifiers=[
        "Development Status :: 3 - Alpha",
        "Intended Audience :: Developers",
        "Topic :: Software Development :: Documentation",
        "Topic :: Text Processing :: Markup",
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
        "Programming Language :: Python :: 3.12",
    ],
    keywords="plantuml diagram manipulation cli batch-processing",
    project_urls={
        "Documentation": "https://github.com/your-org/plantuml-manipulator/tree/main/docs",
        "Source": "https://github.com/your-org/plantuml-manipulator",
        "Tracker": "https://github.com/your-org/plantuml-manipulator/issues",
    },
)
