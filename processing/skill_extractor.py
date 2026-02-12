# skill_extractor.py
# skill_extractor.py

import pandas as pd
from pathlib import Path


def load_skill_dictionary(path):
    skills = []

    with open(path, "r", encoding="utf-8") as f:
        for line in f:
            s = line.strip().lower()
            if s:
                skills.append(s)

    return skills


def extract_skills_from_text(text, skill_list):
    found = set()

    if not isinstance(text, str):
        return []

    text = text.lower()

    for skill in skill_list:
        # simple whole word / phrase match
        if skill in text:
            found.add(skill)

    return list(found)


def extract_skills_dataframe(df, text_column, skill_list):
    all_skills = []

    for idx, row in df.iterrows():
        skills = extract_skills_from_text(row[text_column], skill_list)

        for skill in skills:
            all_skills.append({
                "job_id": idx,
                "skill": skill
            })

    return pd.DataFrame(all_skills)


if __name__ == "__main__":

    BASE_DIR = Path(__file__).resolve().parent.parent

    input_path = BASE_DIR / "data" / "processed_jobs.csv"
    skill_path = BASE_DIR / "data" / "skills_master.txt"
    output_path = BASE_DIR / "data" / "extracted_skills.csv"

    print("Loading data...")

    df = pd.read_csv(input_path)

    skills_master = load_skill_dictionary(skill_path)

    print("Total skills in dictionary:", len(skills_master))

    extracted_df = extract_skills_dataframe(
        df,
        text_column="cleaned_description",
        skill_list=skills_master
    )

    extracted_df.to_csv(output_path, index=False)

    print("Extracted skill rows:", len(extracted_df))
    print("Saved to:", output_path)
