from setuptools import setup, find_packages
import os

# Read the README file for long description
here = os.path.abspath(os.path.dirname(__file__))
with open(os.path.join(here, "README.md"), "r", encoding="utf-8") as fh:
    long_description = fh.read()

setup(
    name="diff2latex",
    version="0.1.0",
    author="divadiahim",
    author_email="", # Add email if available
    description="Simple utility that produces diffs in a LaTeX format",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/divadiahim/diff2latex",
    project_urls={
        "Bug Reports": "https://github.com/divadiahim/diff2latex/issues",
        "Source": "https://github.com/divadiahim/diff2latex",
    },
    packages=find_packages(),
    classifiers=[
        "Development Status :: 3 - Alpha",
        "Intended Audience :: Developers",
        "Topic :: Software Development :: Build Tools",
        "Topic :: Text Processing :: Markup :: LaTeX",
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
        "Programming Language :: Python :: 3.12",
        "Operating System :: OS Independent",
    ],
    keywords="diff latex pdf git version-control documentation api library",
    entry_points={
        'console_scripts': [
            'diff2latex=diff2latex.cli:main',
        ],
    },
    python_requires=">=3.7",
    install_requires=[
        "click>=8.0.0",
        "pydantic>=2.0.0",
        "Pygments>=2.0.0",
        "typing-extensions>=4.0.0",
    ],
    extras_require={
        "dev": [
            "pytest",
            "black",
            "isort",
            "mypy",
        ],
    },
    include_package_data=True,
    package_data={
        "diff2latex": ["templates/*.tex"],
    },
)
