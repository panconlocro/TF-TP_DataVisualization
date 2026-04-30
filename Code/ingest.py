"""Ingest the Steam games dataset from Kaggle Hub."""

# Install dependencies as needed:
# pip install kagglehub[pandas-datasets]
from __future__ import annotations

import argparse
import os
from pathlib import Path
from typing import Optional

import kagglehub
from kagglehub import KaggleDatasetAdapter


DEFAULT_DATASET = "fronkongames/steam-games-dataset"
DEFAULT_OUTPUT = Path("data") / "steam-games.csv"


def find_first_csv(dataset_dir: Path) -> Optional[Path]:
  for root, _, files in os.walk(dataset_dir):
    for name in files:
      if name.lower().endswith(".csv"):
        return Path(root) / name
  return None


def parse_args() -> argparse.Namespace:
  parser = argparse.ArgumentParser(description="Download and load a Kaggle dataset.")
  parser.add_argument("--dataset", default=DEFAULT_DATASET, help="Kaggle dataset slug")
  parser.add_argument(
    "--file",
    default="",
    help="File path inside the dataset (e.g. data.csv). If omitted, first CSV is used.",
  )
  parser.add_argument(
    "--out",
    default=str(DEFAULT_OUTPUT),
    help="Optional output CSV path. Use empty string to skip writing.",
  )
  return parser.parse_args()


def main() -> int:
  args = parse_args()

  dataset_dir = Path(kagglehub.dataset_download(args.dataset))
  file_path = args.file

  if not file_path:
    first_csv = find_first_csv(dataset_dir)
    if first_csv is None:
      raise FileNotFoundError(f"No CSV files found in {dataset_dir}")
    file_path = os.path.relpath(first_csv, dataset_dir)

  df = kagglehub.load_dataset(
    KaggleDatasetAdapter.PANDAS,
    args.dataset,
    file_path,
    # Provide any additional arguments like sql_query or pandas_kwargs:
    # https://github.com/Kaggle/kagglehub/blob/main/README.md#kaggledatasetadapterpandas
  )


  if args.out:
    output_path = Path(args.out)
    output_path.parent.mkdir(parents=True, exist_ok=True)
    df.to_csv(output_path, index=False)
    print(f"Saved dataset to: {output_path}")

  return 0


if __name__ == "__main__":
  raise SystemExit(main())