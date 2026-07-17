#!/usr/bin/env python3
"""
Setup script for Toolbox CLI
"""

from setuptools import setup, find_packages
from pathlib import Path
import subprocess
import sys
import os

# Read the contents of README file
this_directory = Path(__file__).parent.resolve()
long_description = (this_directory / "README.md").read_text(encoding="utf-8")

# Get version from toolbox.py
with open(this_directory / "toolbox.py") as f:
    for line in f:
        if line.startswith("__version__"):
            __version__ = line.split('"')[1]
            break


class PostInstallCommand:
    """Post-installation setup for Toolbox."""

    @staticmethod
    def run():
        """Initialize Toolbox environment after installation."""
        from pathlib import Path
        import subprocess

        toolbox_home = Path.home() / ".toolbox"
        venv_path = toolbox_home / "venv"
        scripts_dir = Path.home() / ".toolbox_scripts"

        # Create directories
        toolbox_home.mkdir(parents=True, exist_ok=True)
        scripts_dir.mkdir(parents=True, exist_ok=True)

        # Create virtual environment if it doesn't exist
        if not venv_path.exists():
            print(f"\n[Toolbox Setup] Creating virtual environment at {venv_path}...")
            try:
                subprocess.run(
                    [sys.executable, "-m", "venv", str(venv_path)],
                    check=True
                )
                print(f"[Toolbox Setup] Virtual environment created successfully!")
            except subprocess.CalledProcessError as e:
                print(
                    f"[Toolbox Setup] Warning: Could not create venv: {e}",
                    file=sys.stderr
                )

        print(f"\n[Toolbox Setup] Setup complete!")
        print(f"[Toolbox Setup] Virtual environment: {venv_path}")
        print(f"[Toolbox Setup] Scripts directory: {scripts_dir}")
        print(f"[Toolbox Setup] Add your scripts to {scripts_dir} and run them with 'toolbox run <script-name>'")


setup(
    name="toolbox-cli",
    version=__version__,
    description="A lightweight CLI for managing and running scripts from ~/.toolbox_scripts/",
    long_description=long_description,
    long_description_content_type="text/markdown",
    author="Toolbox Contributors",
    url="https://github.com/altforunix/tobepushed",
    py_modules=["toolbox"],
    entry_points={
        "console_scripts": [
            "toolbox=toolbox:main",
        ],
    },
    install_requires=[
        "virtualenv>=20.0.0",
    ],
    python_requires=">=3.7",
    classifiers=[
        "Development Status :: 4 - Beta",
        "Intended Audience :: Developers",
        "Topic :: Software Development :: Libraries :: Python Modules",
        "License :: OSI Approved :: BSD License",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
    ],
    keywords="cli script manager virtualenv toolbox",
)
