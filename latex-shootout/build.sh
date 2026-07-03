#!/bin/sh
# Thin wrapper — the real build is cross-platform Python.
cd "$(dirname "$0")" && exec python3 build.py
