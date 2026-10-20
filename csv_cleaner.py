
import csv
from pathlib import Path


def clean_csv(input_file):
    input_path = Path(input_file)

    if not input_path.is_file():
        print("Error: CSV file nahi mili.")
        return

    output_path = input_path.with_name(
        input_path.stem + "_cleaned.csv"
    )

    try:
        with input_path.open(
            "r", newline="", encoding="utf-8-sig"
        ) as file:
            reader = csv.reader(file)
            rows = list(reader)

        if not rows:
            print("CSV file khaali hai.")
            return

        header = rows[0]
        original_rows = rows[1:]

        # Completely blank rows remove karo
        nonblank_rows = [
            row for row in original_rows
            if any(value.strip() for value in row)
        ]

        blank_removed = len(original_rows) - len(nonblank_rows)

        # Duplicate rows remove karo, order same rakho
        unique_rows = []
        seen = set()

        for row in nonblank_rows:
            row_key = tuple(value.strip() for value in row)

            if row_key not in seen:
                seen.add(row_key)
                unique_rows.append(row_key)

        duplicates_removed = len(nonblank_rows) - len(unique_rows)

        # Cleaned data ko new file mein save karo
        with output_path.open(
            "w", newline="", encoding="utf-8"
        ) as file:
            writer = csv.writer(file)
            writer.writerow(header)
            writer.writerows(unique_rows)

        print("\nCSV Cleaning Complete!")
        print(f"Original data rows: {len(original_rows)}")
        print(f"Blank rows removed: {blank_removed}")
        print(f"Duplicate rows removed: {duplicates_removed}")
        print(f"Clean rows remaining: {len(unique_rows)}")
        print(f"Saved file: {output_path}")

    except (OSError, csv.Error) as error:
        print(f"Error: {error}")


def main():
    file_path = input("CSV file ka path enter karo: ").strip()
    file_path = file_path.strip('"')
    clean_csv(file_path)


if __name__ == "__main__":
    main()
