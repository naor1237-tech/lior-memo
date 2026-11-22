#!/bin/sh
# Builds a slim copy (no large mp4 except hero) for Netlify. Usage: sh deploy-netlify.sh <outdir>
set -e
OUT="$1"; rm -rf "$OUT"; mkdir -p "$OUT/media"
git archive HEAD | tar -x -C "$OUT"
find "$OUT/media" -name '*.mp4' ! -name 'hero.mp4' -delete
rm -f "$OUT/deploy-netlify.sh"
du -sh "$OUT"
