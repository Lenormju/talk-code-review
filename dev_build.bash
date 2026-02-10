#!/bin/bash
set -euo pipefail

mkdir -p public
uv tool run 'mkslides<2.0' \
    serve \
    --config-file 'mkslides_config.yml' \
    --strict \
    --open \
    'slides/slides.md'
