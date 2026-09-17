"""
Experiment: Finding the Specific Hypothesis using the Find-S Algorithm
Dataset  : workload_data.csv
"""

import csv
import os

DATASET_NAME = "workload_data.csv"

print("Current folder:", os.getcwd())
print("Files:", os.listdir())


def create_default_dataset(filepath):
    """Create a small valid dataset if the expected CSV is missing."""
    rows = [
        ["Sky", "Temp", "Humidity", "Wind", "Water", "Forecast", "EnjoySport"],
        ["Sunny", "Warm", "Normal", "Strong", "Warm", "Same", "Yes"],
        ["Sunny", "Warm", "High", "Strong", "Warm", "Same", "Yes"],
        ["Rainy", "Cold", "High", "Strong", "Warm", "Change", "No"],
        ["Sunny", "Warm", "High", "Strong", "Cool", "Change", "Yes"],
    ]

    with open(filepath, "w", newline="") as f:
        writer = csv.writer(f)
        writer.writerows(rows)

    print(f"Created default dataset at: {filepath}")


def load_dataset(filepath):
    """
    1. Read the CSV file.
    2. Return two things:
       - attributes: list of attribute column names (excludes the target column)
       - rows: list of rows, each row = (list_of_attribute_values, target_label)
    """
    attributes = []
    rows = []

    with open(filepath, newline="") as f:
        reader = csv.reader(f)
        header = next(reader)

        # Last column is the target class, everything else is an attribute
        attributes = header[:-1]

        for line in reader:
            *attr_values, target = line
            rows.append((attr_values, target))

    return attributes, rows


def find_s(attributes, rows):
    """
    Implements the Find-S algorithm.
    - Initializes hypothesis to the most specific hypothesis ('phi' for every attribute).
    - Iterates over every row (prints hypothesis state after each row).
    - Only updates the hypothesis on POSITIVE ('Yes') instances.
    - Negative instances are ignored (hypothesis unchanged, but state still printed).
    """
    n = len(attributes)

    # Step 1: initialize hypothesis to the most specific hypothesis
    hypothesis = ["phi"] * n

    print("Initial hypothesis:")
    print(hypothesis)
    print("-" * 60)

    for i, (values, target) in enumerate(rows, start=1):
        print(f"Processing row {i}: {values} -> Target = {target}")

        if target == "Yes":
            # Positive instance: generalize the hypothesis
            if hypothesis == ["phi"] * n:
                # First positive instance seen: adopt it directly
                hypothesis = list(values)
            else:
                for j in range(n):
                    if hypothesis[j] != values[j]:
                        hypothesis[j] = "?"
                    # else: constraint already satisfied, do nothing
        else:
            # Negative instance: ignored, hypothesis unchanged
            print("  -> Negative instance, ignored.")

        print(f"Hypothesis after row {i}: {hypothesis}")
        print("-" * 60)

    return hypothesis


def main():
    script_dir = os.path.dirname(os.path.abspath(__file__))
    dataset_path = os.path.join(script_dir, DATASET_NAME)

    if not os.path.exists(dataset_path):
        create_default_dataset(dataset_path)

    attributes, rows = load_dataset(dataset_path)

    print("Attributes:", attributes)
    print("=" * 60)

    final_hypothesis = find_s(attributes, rows)

    print("Final Specific Hypothesis:")
    for attr, val in zip(attributes, final_hypothesis):
        print(f"  {attr}: {val}")


if __name__ == "__main__":
    main()