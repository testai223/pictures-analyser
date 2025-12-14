# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Commands

### Environment Setup
```bash
python -m venv .venv && source .venv/bin/activate
pip install -r requirements.txt
```

### Running the Application
```bash
# Primary CLI command
python -m src.analyze_folder --input assets/raw_images --output runs/demo --model yolov8n.pt --conf 0.25 --imgsz 640

# Convenience script wrapper
scripts/run_folder.sh [input_dir] [output_dir] [model_path]
```

### Testing
```bash
pytest  # Once tests are added to tests/ directory
```

### Code Quality (when configured)
```bash
ruff check .    # Lint
ruff format .   # Format
```

## Architecture

### Core Components
- **`src/analyze_folder.py`**: Main CLI entry point that runs YOLO object detection across all images in a folder
- **Input Processing**: Supports `.jpg`, `.png`, `.bmp`, `.gif`, `.tif` image formats
- **Output Generation**: Creates annotated images with bounding boxes and a CSV summary of detections

### Data Flow
1. Load YOLO model (downloads `yolov8n.pt` on first run if not present)
2. Scan input directory for supported image formats
3. Run inference on each image with configurable confidence threshold and image size
4. Save annotated images to `output_dir/annotated/`
5. Generate `summary.csv` with detection data: `image,label,confidence,x1,y1,x2,y2`

### Project Structure
- `src/`: Implementation code with clear subfolders per feature
- `assets/`: Input images and fixtures (keep large files out of repo)
- `runs/`: Default output location (not tracked by git)
- `tests/`: Automated tests mirroring `src/` layout
- `scripts/`: One-off tools and wrappers

### Dependencies
- **ultralytics**: YOLO model framework (v8.1.0+)
- **opencv-python**: Image processing (v4.8.1.78+)

## Development Notes

### Module Organization
- Use `python -m src.<module>` for consistent import resolution
- Keep modules focused; extract shared helpers into `src/utils/`
- Use explicit type hints on public functions

### Testing Strategy
- Store small image fixtures in `tests/fixtures/`
- Generate larger test images at runtime
- Include integration tests for CLI argument parsing
- Add regression tests for any bug fixes

### Output Format
- Images with no detections show `"no-detections"` in CSV
- Bounding boxes use `x1,y1,x2,y2` coordinate format
- Confidence scores rounded to reasonable precision