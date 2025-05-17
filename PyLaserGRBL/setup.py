from setuptools import setup, find_packages

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setup(
    name="pylasergrbl",
    version="0.1.0",
    author="Votre Nom",
    author_email="votre@email.com",
    description="Une interface moderne pour le contrôle des graveurs laser GRBL",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/votrecompte/pylasergrbl",
    packages=find_packages(where="src"),
    package_dir={"": "src"},
    install_requires=[
        "PyQt6>=6.0.0",
        "pyserial>=3.5",
        "numpy>=1.20.0",
        "matplotlib>=3.4.0",
    ],
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires=">=3.9",
    entry_points={
        "console_scripts": [
            "pylasergrbl=pylasergrbl.main:main",
        ],
    },
)
