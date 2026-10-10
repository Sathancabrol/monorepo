#!/usr/bin/env bash
cd "$(dirname "$0")"
echo "Playground Bone → http://127.0.0.1:8765"
python3 -m http.server 8765
