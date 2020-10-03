import json
import time
from pathlib import Path

import numpy as np

from card2vec.feature_extraction.data_reading import read_cards, read_decks
from card2vec.feature_extraction.examples import generate_all_examples


def generate_training(
    input_path: Path,
    ouput_path: Path,
    shuffles: int,
    window_size: int,
    negative_samples: int,
):
    file_name = f"data_shuffles-{shuffles}__window_size-{window_size}__negative_samples-{negative_samples}"

    cards_info = read_cards(input_path)
    decks = read_decks(
        input_path,
        variants=cards_info["variants"],
        card_to_int=cards_info["card_to_int"],
    )

    t0 = time.time()
    positives, negatives = generate_all_examples(
        decks, window_size, negative_samples, shuffles
    )
    t1 = time.time()

    np.savez_compressed(
        Path(ouput_path, file_name), positives=positives, negatives=negatives
    )
    with open(Path(ouput_path, f"{file_name}.json"), "w") as writable:
        json.dump(
            {
                "time": t1 - t0,
                "decks": len(decks),
                "window_size": window_size,
                "negative_samples": negative_samples,
                "shuffles": shuffles,
                "positives": len(positives),
                "negatives": len(negatives),
            },
            writable,
        )


def generate_training_multiple(input_path, output_path):
    values = [
        (3, 5, 5),
        (4, 5, 5),
        (4, 7, 7),
        (4, 9, 7),
        (3, 9, 9),
    ]

    for shuffles, window_size, negative_samples in values:
        generate_training(
            input_path, output_path, shuffles, window_size, negative_samples
        )
