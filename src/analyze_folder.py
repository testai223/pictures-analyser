"""
Run YOLO detections over all images in a folder and save annotated outputs plus a CSV summary.

Example:
    python -m venv .venv && source .venv/bin/activate
    pip install -r requirements.txt
    python -m src.analyze_folder --input assets/raw_images --output runs/demo --model yolov8n.pt --conf 0.25
"""

from __future__ import annotations

import argparse
import csv
from pathlib import Path
from typing import Iterable, List

from ultralytics import YOLO

ImagePath = Path


def list_images(folder: Path) -> List[ImagePath]:
    """Return all image paths inside the folder (non-recursive)."""
    exts = {".jpg", ".jpeg", ".png", ".bmp", ".gif", ".tif", ".tiff"}
    return sorted([p for p in folder.iterdir() if p.suffix.lower() in exts and p.is_file()])


def write_summary_csv(rows: Iterable[dict], destination: Path) -> None:
    """Write detection rows to a CSV file."""
    fieldnames = ["image", "label", "confidence", "x1", "y1", "x2", "y2"]
    with destination.open("w", newline="", encoding="utf-8") as csvfile:
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
        writer.writeheader()
        for row in rows:
            writer.writerow(row)


def run_inference(
    model_path: Path,
    input_dir: Path,
    output_dir: Path,
    conf: float = 0.25,
    imgsz: int = 640,
) -> None:
    """Run YOLO on every image in input_dir and save annotated images plus a CSV."""
    if not input_dir.exists():
        raise FileNotFoundError(f"Input directory does not exist: {input_dir}")

    images = list_images(input_dir)
    if not images:
        raise ValueError(f"No images found in {input_dir}")

    output_dir.mkdir(parents=True, exist_ok=True)
    annotated_dir = output_dir / "annotated"
    annotated_dir.mkdir(exist_ok=True)

    model = YOLO(str(model_path))
    summary_rows = []

    for image_path in images:
        results = model(
            source=str(image_path),
            conf=conf,
            imgsz=imgsz,
            verbose=False,
        )
        for result in results:
            out_path = annotated_dir / image_path.name
            result.save(filename=str(out_path))

            names = result.names
            boxes = getattr(result, "boxes", None)
            if boxes is None or boxes.data.size(0) == 0:
                summary_rows.append(
                    {
                        "image": image_path.name,
                        "label": "no-detections",
                        "confidence": "",
                        "x1": "",
                        "y1": "",
                        "x2": "",
                        "y2": "",
                    }
                )
                continue

            for box in boxes:
                cls_id = int(box.cls.item())
                label = names.get(cls_id, str(cls_id))
                confidence = float(box.conf.item()) if box.conf is not None else ""
                x1, y1, x2, y2 = [round(float(coord), 2) for coord in box.xyxy[0].tolist()]
                summary_rows.append(
                    {
                        "image": image_path.name,
                        "label": label,
                        "confidence": confidence,
                        "x1": x1,
                        "y1": y1,
                        "x2": x2,
                        "y2": y2,
                    }
                )

    write_summary_csv(summary_rows, output_dir / "summary.csv")
    print(f"Processed {len(images)} images. Annotated images: {annotated_dir}. Summary: {output_dir / 'summary.csv'}")


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description="Run YOLO detections on all images in a folder.")
    parser.add_argument("--input", type=Path, required=True, help="Folder containing images to analyze.")
    parser.add_argument("--output", type=Path, required=True, help="Folder to write annotated images and summary.csv.")
    parser.add_argument(
        "--model",
        type=Path,
        default=Path("yolov8n.pt"),
        help="YOLO model path or alias (default: yolov8n.pt; downloads if not present).",
    )
    parser.add_argument("--conf", type=float, default=0.25, help="Confidence threshold (default: 0.25).")
    parser.add_argument("--imgsz", type=int, default=640, help="Inference image size (default: 640).")
    return parser


def main() -> None:
    args = build_parser().parse_args()
    run_inference(
        model_path=args.model,
        input_dir=args.input,
        output_dir=args.output,
        conf=args.conf,
        imgsz=args.imgsz,
    )


if __name__ == "__main__":
    main()
