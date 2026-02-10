#!/bin/bash
set -euo pipefail

mkdir -p public
uv tool run 'mkslides ~= 2.0' \
    build \
    --config-file 'mkslides_config.yml' \
    --site-dir 'public' \
    --strict

#xdg-open "file://$(pwd)/public/index.html"
