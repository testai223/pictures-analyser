# Picture Analyser (YOLO)

Simple Python utility to run a YOLO model over every image in a folder, save annotated images, and produce a CSV of detections.

## Setup
- Python 3.9+ recommended.
- Create a virtual env and install deps:
  - `python -m venv .venv && source .venv/bin/activate`
  - `pip install -r requirements.txt`
- The default model is `yolov8n.pt`; the first run will download it if not present (network required). You can also pass a local `.pt` file.

## Usage
```
python -m src.analyze_folder --input assets/raw_images --output runs/demo --model yolov8n.pt --conf 0.25 --imgsz 640
```
- Shortcut wrapper (uses the same defaults): `scripts/run_folder.sh [input_dir] [output_dir] [model_path]`
- `--input`: folder containing images (`.jpg`, `.png`, `.bmp`, `.gif`, `.tif`).
- `--output`: target folder; creates `annotated/` with labeled images and `summary.csv` with bounding boxes.
- `--model`: YOLO model path or alias (any Ultralytics-compatible checkpoint).
- `--conf` / `--imgsz`: tweak thresholds and inference size.

## Output
- `runs/demo/annotated/<image>`: images with bounding boxes and labels drawn by YOLO.
- `runs/demo/summary.csv`: rows of detections with `image,label,confidence,x1,y1,x2,y2`. Images with no detections show `no-detections`.

## Project Layout
- `src/analyze_folder.py`: CLI entry point for running YOLO across a folder.
- `assets/`: optional place for sample or input images.
- `runs/`: suggested output location (not tracked by default).
- `tests/`: reserved for future automated tests.
