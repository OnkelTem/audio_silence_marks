#!/usr/bin/env bash

file="$1"

[[ -f "$file" ]] || { echo "Cannot read input file: '$file'"; exit 1; }

jq '[.files[].marklist[].id] | length'  "$file"
