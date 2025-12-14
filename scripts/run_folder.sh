#!/usr/bin/env bash
set -euo pipefail

# Simple wrapper to run YOLO across a folder.
# Usage: scripts/run_folder.sh [input_dir] [output_dir] [model_path]

INPUT_DIR="${1:-assets/raw_images}"
OUTPUT_DIR="${2:-runs/demo}"
MODEL_PATH="${3:-yolov8n.pt}"
CONF="${CONF:-0.25}"
IMGSZ="${IMGSZ:-640}"

# Create venv and install dependencies if missing.
if [[ ! -x ".venv/bin/python" ]]; then
  echo "Creating virtualenv in .venv/..."
  python3 -m venv .venv
  echo "Installing dependencies..."
  .venv/bin/pip install -r requirements.txt
fi

.venv/bin/python -m src.analyze_folder \
  --input "$INPUT_DIR" \
  --output "$OUTPUT_DIR" \
  --model "$MODEL_PATH" \
  --conf "$CONF" \
  --imgsz "$IMGSZ"
