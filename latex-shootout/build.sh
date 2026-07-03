#!/bin/sh
# Build the memoir shootout chapter with TinyTeX.
set -e
cd "$(dirname "$0")"
TEXBIN="$HOME/Library/TinyTeX/bin/universal-darwin"
mkdir -p build
"$TEXBIN/latexmk" -pdf -interaction=nonstopmode -output-directory=build giza-memoir.tex
echo "→ build/giza-memoir.pdf"
