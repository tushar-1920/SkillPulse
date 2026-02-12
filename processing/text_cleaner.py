# text_cleaner.py

import re
import html


def clean_text(text: str) -> str:
    if not isinstance(text, str) or not text:
        return ""

    # convert html entities
    text = html.unescape(text)

    # lowercase
    text = text.lower()

    # remove html tags
    text = re.sub(r"<.*?>", " ", text)

    # remove urls
    text = re.sub(r"http\S+|www\S+", " ", text)

    # keep only letters and numbers
    text = re.sub(r"[^a-z0-9\s]", " ", text)

    # remove extra spaces
    text = re.sub(r"\s+", " ", text).strip()

    return text


if __name__ == "__main__":
    import pandas as pd

    # read raw scraped jobs
    df = pd.read_csv("data/raw_jobs.csv")

    # clean descriptions
    df["cleaned_description"] = df["description"].apply(clean_text)

    # save processed file
    df.to_csv("data/processed_jobs.csv", index=False)

    print("Processed rows:", len(df))
