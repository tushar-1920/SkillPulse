# skill_normalizer.py

import pandas as pd
from pathlib import Path


# Canonical mapping
NORMALIZATION_MAP = {
    "sklearn": "scikit-learn",
    "scikit learn": "scikit-learn",

    "ml": "machine learning",
    "machine-learning": "machine learning",

    "dl": "deep learning",
    "deep-learning": "deep learning",

    "nlp": "natural language processing",

    "postgres": "postgresql",

    "js": "javascript",

    "py": "python"
}


def normalize_skill(skill: str) -> str:
    if not isinstance(skill, str):
        return ""

    s = skill.strip().lower()

    # direct mapping
    if s in NORMALIZATION_MAP:
        return NORMALIZATION_MAP[s]

    return s


def normalize_dataframe(df, skill_column="skill"):
    df["normalized_skill"] = df[skill_column].apply(normalize_skill)
    return df


if __name__ == "__main__":

    BASE_DIR = Path(__file__).resolve().parent.parent

    input_path = BASE_DIR / "data" / "extracted_skills.csv"
    output_path = BASE_DIR / "data" / "normalized_skills.csv"

    print("Loading extracted skills...")

    df = pd.read_csv(input_path)

    df = normalize_dataframe(df, skill_column="skill")

    df.to_csv(output_path, index=False)

    print("Rows:", len(df))
    print("Saved normalized skills to:", output_path)
