"""Load the cleaned reviews and prepare tokenized train/val/test splits."""

import pandas as pd
from datasets import Dataset, DatasetDict
from sklearn.model_selection import train_test_split
from transformers import PreTrainedTokenizerBase

from src.sentiment.config import (
    LABEL2ID,
    MAX_SEQUENCE_LENGTH,
    RANDOM_SEED,
    TRAIN_FRACTION,
    VAL_FRACTION,
)


def load_cleaned_reviews(path: str) -> pd.DataFrame:
    """Load the cleaned reviews dataset and keep only text + sentiment label.

    Args:
        path: Path to the cleaned reviews parquet file.

    Returns:
        DataFrame with `text` and `label` (integer-encoded sentiment) columns.
    """
    df = pd.read_parquet(path, columns=["reviews.text", "sentiment"])
    df = df.rename(columns={"reviews.text": "text"})
    df["label"] = df["sentiment"].map(LABEL2ID)
    return df[["text", "label"]]


def split_dataset(df: pd.DataFrame) -> tuple[pd.DataFrame, pd.DataFrame, pd.DataFrame]:
    """Split reviews into stratified train/validation/test sets.

    Stratifying on `label` keeps the (heavily imbalanced) sentiment
    proportions consistent across all three splits.

    Args:
        df: DataFrame with `text` and `label` columns.

    Returns:
        Tuple of (train_df, val_df, test_df).
    """
    train_df, holdout_df = train_test_split(
        df,
        train_size=TRAIN_FRACTION,
        stratify=df["label"],
        random_state=RANDOM_SEED,
    )
    val_relative_size = VAL_FRACTION / (1 - TRAIN_FRACTION)
    val_df, test_df = train_test_split(
        holdout_df,
        train_size=val_relative_size,
        stratify=holdout_df["label"],
        random_state=RANDOM_SEED,
    )
    return train_df, val_df, test_df


def build_dataset_dict(train_df: pd.DataFrame, val_df: pd.DataFrame, test_df: pd.DataFrame) -> DatasetDict:
    """Wrap train/val/test DataFrames into a Hugging Face DatasetDict."""
    return DatasetDict(
        {
            "train": Dataset.from_pandas(train_df, preserve_index=False),
            "validation": Dataset.from_pandas(val_df, preserve_index=False),
            "test": Dataset.from_pandas(test_df, preserve_index=False),
        }
    )


def _tokenize_batch(batch: dict, tokenizer: PreTrainedTokenizerBase) -> dict:
    return tokenizer(
        batch["text"],
        truncation=True,
        max_length=MAX_SEQUENCE_LENGTH,
        padding="max_length",
    )


def tokenize_dataset_dict(dataset_dict: DatasetDict, tokenizer: PreTrainedTokenizerBase) -> DatasetDict:
    """Tokenize the `text` field of every split with truncation/padding."""
    return dataset_dict.map(
        lambda batch: _tokenize_batch(batch, tokenizer), batched=True, remove_columns=["text"]
    )


def tokenize_single_dataset(dataset: Dataset, tokenizer: PreTrainedTokenizerBase) -> Dataset:
    """Tokenize the `text` field of a single (non-split-dict) dataset."""
    return dataset.map(lambda batch: _tokenize_batch(batch, tokenizer), batched=True, remove_columns=["text"])
