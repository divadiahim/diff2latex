from setuptools import setup, find_packages

setup(
    name="diff2latex",
    version="0.1.0",
    description="Simple utility that produces diffs in a LaTeX format",
    packages=find_packages(),
    entry_points={
        'console_scripts': [
            'diff2latex=diff2latex.cli:main',
        ],
    },
    python_requires=">=3.7",
    install_requires=[],
)
