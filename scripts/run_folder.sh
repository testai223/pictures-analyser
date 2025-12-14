#!/usr/bin/env bash
set -euo pipefail

# Simple wrapper to run YOLO across a folder.
# Usage: scripts/run_folder.sh [input_dir] [output_dir] [model_path]

INPUT_DIR="${1:-assets/raw_images}"
OUTPUT_DIR="${2:-runs/demo}"
MODEL_PATH="${3:-yolov8n.pt}"
CONF="${CONF:-0.25}"
IMGSZ="${IMGSZ:-640}"

if [[ ! -x ".venv/bin/python" ]]; then
  echo "Missing virtualenv at .venv/. Create it with: python3 -m venv .venv && source .venv/bin/activate && pip install -r requirements.txt" >&2
  exit 1
fi

.venv/bin/python -m src.analyze_folder \
  --input "$INPUT_DIR" \
  --output "$OUTPUT_DIR" \
  --model "$MODEL_PATH" \
  --conf "$CONF" \
  --imgsz "$IMGSZ"
