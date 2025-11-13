#!/usr/bin/env python
"""Convenience script to run the game with proper environment."""
import subprocess
import sys

if __name__ == "__main__":
    # Run main.py with uv
    sys.exit(subprocess.call(["uv", "run", "python", "main.py"]))
