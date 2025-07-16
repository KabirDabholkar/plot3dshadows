from setuptools import setup, find_packages

# Read the README file for long description
with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setup(
    name="plot3dshadows",
    version="0.1.0",
    description="A package for 3D plotting with shadows on coordinate planes",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/KabirDabholkar/plot3dshadows",
    packages=find_packages(),
    python_requires=">=3.7",
    install_requires=[
        "matplotlib>=3.3.0",
        "numpy>=1.19.0",
        "seaborn>=0.11.0",
    ],
    extras_require={
        "dev": [
            "pytest>=6.0",
            "pytest-cov>=2.0",
            "black>=21.0",
            "flake8>=3.8",
            "isort>=5.0",
        ],
    },
    keywords="matplotlib, 3d, plotting, visualization, shadows",
) 