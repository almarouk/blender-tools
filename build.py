#!/usr/bin/env python3
"""
Simple Blender Extension Builder

Usage:
    python build.py validate    - Validate extension
    python build.py build       - Build extension
    python build.py install     - Install extension locally

Setup:
    1. Copy .env.example to .env
    2. Set BLENDER_PATH in .env to your Blender executable path
"""

import os
import sys
import subprocess
from pathlib import Path


def load_env():
    """Load environment variables from .env file"""
    env_path = Path(".env")
    if env_path.exists():
        with open(env_path) as f:
            for line in f:
                line = line.strip()
                if line and not line.startswith("#") and "=" in line:
                    key, value = line.split("=", 1)
                    os.environ[key.strip()] = value.strip()


def get_blender_path():
    """Get Blender executable path from environment"""
    blender_path = os.environ.get("BLENDER_PATH")
    if not blender_path:
        print("❌ Error: BLENDER_PATH not set")
        print("💡 Copy .env.example to .env and set BLENDER_PATH")
        return None

    if not os.path.exists(blender_path):
        print(f"❌ Error: Blender not found at {blender_path}")
        return None

    return blender_path


def run_command(cmd: list[str], description: str) -> bool:
    """Run a Blender command"""
    print(f"� {description}...")
    try:
        result = subprocess.run(cmd, check=True, capture_output=True, text=True)
        print(result.stdout)
        print(f"✅ {description} completed")
        return True
    except subprocess.CalledProcessError as e:
        print(f"❌ {description} failed")
        if e.stderr:
            print(e.stderr)
        return False


def main():
    load_env()

    if len(sys.argv) != 2 or sys.argv[1] not in ["validate", "build", "install"]:
        print(__doc__)
        return

    command = sys.argv[1]
    blender_path = get_blender_path()
    if not blender_path:
        return

    print(f"Using Blender: {blender_path}")

    if command == "validate":
        run_command([blender_path, "--command", "extension", "validate"], "Validation")

    elif command == "build":
        if run_command(
            [blender_path, "--command", "extension", "validate"], "Validation"
        ):
            if run_command([blender_path, "--command", "extension", "build"], "Build"):
                # Find built file
                zip_files = list(Path(".").glob("*.zip"))
                if zip_files:
                    latest = max(zip_files, key=os.path.getmtime)
                    print(f"📦 Built: {latest}")

    elif command == "install":
        zip_files = list(Path(".").glob("*.zip"))
        if not zip_files:
            print("❌ No .zip file found. Run 'build' first.")
            return

        latest = max(zip_files, key=os.path.getmtime)
        cmd = [
            blender_path,
            "--command",
            "extension",
            "install-file",
            "--repo",
            "user_default",
            "--enable",
            str(latest),
        ]
        run_command(cmd, f"Installing {latest}")


if __name__ == "__main__":
    main()
