#!/usr/bin/env python3
"""
Toolbox - A lightweight CLI for managing and running scripts from ~/.toolbox_scripts/
"""

import sys
import os
import subprocess
import argparse
from pathlib import Path

__version__ = "1.0.0"

TOOLBOX_HOME = Path.home() / ".toolbox"
VENV_PATH = TOOLBOX_HOME / "venv"
SCRIPTS_DIR = Path.home() / ".toolbox_scripts"
PYTHON_VENV = VENV_PATH / "bin" / "python"


def ensure_venv_exists():
    """Ensure the virtual environment exists and is initialized."""
    if not VENV_PATH.exists():
        print(f"Creating virtual environment at {VENV_PATH}...")
        subprocess.run([sys.executable, "-m", "venv", str(VENV_PATH)], check=True)
        print("Virtual environment created successfully.")


def ensure_scripts_dir_exists():
    """Ensure the scripts directory exists."""
    SCRIPTS_DIR.mkdir(parents=True, exist_ok=True)


def list_scripts():
    """List all scripts in ~/.toolbox_scripts/."""
    ensure_scripts_dir_exists()
    
    if not SCRIPTS_DIR.exists():
        print(f"Scripts directory not found at {SCRIPTS_DIR}")
        return
    
    scripts = sorted([f.name for f in SCRIPTS_DIR.glob("*.py")])
    
    if not scripts:
        print(f"No scripts found in {SCRIPTS_DIR}")
        return
    
    print(f"Scripts in {SCRIPTS_DIR}:")
    for script in scripts:
        print(f"  - {script}")


def run_script(script_name, args, use_venv=True):
    """Run a script from ~/.toolbox_scripts/."""
    ensure_scripts_dir_exists()
    ensure_venv_exists()
    
    script_path = SCRIPTS_DIR / f"{script_name}.py"
    
    if not script_path.exists():
        print(f"Error: Script '{script_name}.py' not found in {SCRIPTS_DIR}")
        sys.exit(1)
    
    if use_venv:
        if not PYTHON_VENV.exists():
            print(f"Error: Virtual environment not found at {VENV_PATH}")
            print("Run 'toolbox setup' to initialize the virtual environment.")
            sys.exit(1)
        cmd = [str(PYTHON_VENV), str(script_path)] + args
    else:
        cmd = [sys.executable, str(script_path)] + args
    
    try:
        result = subprocess.run(cmd, check=False)
        sys.exit(result.returncode)
    except KeyboardInterrupt:
        print("\nScript interrupted by user.")
        sys.exit(130)
    except Exception as e:
        print(f"Error running script: {e}")
        sys.exit(1)


def install_package(package_name):
    """Install a package into the virtual environment."""
    ensure_venv_exists()
    
    if not PYTHON_VENV.exists():
        print(f"Error: Virtual environment not found at {VENV_PATH}")
        sys.exit(1)
    
    pip_path = VENV_PATH / "bin" / "pip"
    
    print(f"Installing {package_name} into Toolbox virtual environment...")
    try:
        result = subprocess.run(
            [str(pip_path), "install", package_name],
            check=False
        )
        if result.returncode == 0:
            print(f"Successfully installed {package_name}")
        else:
            print(f"Failed to install {package_name}")
            sys.exit(1)
    except Exception as e:
        print(f"Error installing package: {e}")
        sys.exit(1)


def main():
    parser = argparse.ArgumentParser(
        description="Toolbox - Lightweight script manager and runner",
        prog="toolbox"
    )
    
    parser.add_argument(
        "--version",
        action="version",
        version=f"Toolbox {__version__}"
    )
    
    subparsers = parser.add_subparsers(dest="command", help="Available commands")
    
    # run command
    run_parser = subparsers.add_parser(
        "run",
        help="Run a script from ~/.toolbox_scripts/"
    )
    run_parser.add_argument("script", help="Script name without .py extension")
    run_parser.add_argument(
        "args",
        nargs=argparse.REMAINDER,
        help="Arguments to pass to the script"
    )
    run_parser.add_argument(
        "--no-venv",
        action="store_true",
        help="Run script with system Python instead of Toolbox venv"
    )
    
    # list command
    list_parser = subparsers.add_parser(
        "list",
        help="List all scripts in ~/.toolbox_scripts/"
    )
    
    # install command
    install_parser = subparsers.add_parser(
        "install",
        help="Install a package into Toolbox's virtual environment"
    )
    install_parser.add_argument(
        "package",
        help="Package name to install (supports pip syntax)"
    )
    
    # setup command (internal)
    setup_parser = subparsers.add_parser(
        "setup",
        help="Initialize Toolbox environment"
    )
    
    args = parser.parse_args()
    
    if not args.command:
        parser.print_help()
        sys.exit(0)
    
    if args.command == "run":
        # Extract --no-venv flag from remaining args if present
        use_venv = not args.no_venv
        script_args = [arg for arg in args.args if arg != "--no-venv"]
        run_script(args.script, script_args, use_venv=use_venv)
    
    elif args.command == "list":
        list_scripts()
    
    elif args.command == "install":
        install_package(args.package)
    
    elif args.command == "setup":
        ensure_venv_exists()
        ensure_scripts_dir_exists()
        print("Toolbox environment initialized successfully!")
        print(f"Virtual environment: {VENV_PATH}")
        print(f"Scripts directory: {SCRIPTS_DIR}")


if __name__ == "__main__":
    main()
