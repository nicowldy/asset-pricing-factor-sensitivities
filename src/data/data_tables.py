import os
import csv


def export_to_csv(data, filepath, headers, row_formatter):
    os.makedirs(os.path.dirname(filepath), exist_ok=True)
    with open(filepath, "w", newline="") as csvfile:
        writer = csv.writer(csvfile)
        writer.writerow(headers)
        for item in data:
            writer.writerow(row_formatter(item))


def export_processing_statistics(statistics, stats_filepath):
    headers = [
        "name",
        "raw_rows",
        "processed_rows",
        "raw_range",
        "processed_range",
        "dropped_cleaning",
        "dropped_intersection",
    ]

    def format_dataset_row(dataset):
        return [
            dataset["name"],
            dataset["raw_rows"],
            dataset.get("processed_rows"),
            dataset["raw_range"],
            dataset.get("processed_range"),
            dataset.get("dropped_cleaning"),
            dataset.get("dropped_intersection"),
        ]

    export_to_csv(
        statistics["datasets"].values(),
        stats_filepath,
        headers,
        format_dataset_row,
    )
