from __future__ import annotations

import csv
from pathlib import Path

JP_DIR = Path("jp")
OUTPUT_FILE = JP_DIR / "000_D365FO_UI_Menu_全体.csv"


def main() -> None:
    input_files = sorted(
        [p for p in JP_DIR.glob("*.csv") if p.name != OUTPUT_FILE.name],
        key=lambda p: p.name,
    )

    if not input_files:
        raise SystemExit("No CSV files found under jp/")

    header: list[str] | None = None
    rows: list[list[str]] = []

    for path in input_files:
        with path.open("r", encoding="utf-8-sig", newline="") as f:
            reader = csv.reader(f)
            file_header = next(reader, None)
            if not file_header:
                continue

            if header is None:
                header = ["SourceFile", *file_header]

            for row in reader:
                if not any(cell.strip() for cell in row):
                    continue
                rows.append([path.name, *row])

    if header is None:
        raise SystemExit("No headers found in CSV files")

    with OUTPUT_FILE.open("w", encoding="utf-8-sig", newline="") as f:
        writer = csv.writer(f)
        writer.writerow(header)
        writer.writerows(rows)

    print(f"Wrote {len(rows)} rows to {OUTPUT_FILE}")


if __name__ == "__main__":
    main()
