import random
from typing import List

import numpy as np


def get_positive_samples(position: int, deck: np.array, window: int):
    examples = np.zeros((window * 2 + 1, 2), dtype=int)
    examples[:, 0] = deck[position]
    examples[:, 1] = deck[
        np.arange(position - window, position + window + 1) % len(deck)
    ]
    return examples[examples[:, 0] != examples[:, 1]]


def get_negative_samples(
    position: int, deck: np.array, n_negatives: int, all_cards: np.array
):
    examples = np.full((n_negatives, 2), deck[position], dtype=int)
    negative_samples = np.random.choice(all_cards, n_negatives)
    examples[:, 1] = negative_samples
    return examples


def get_examples_for_deck(
    deck: np.array,
    window_size: int,
    n_negatives: int,
    shuffles: int,
    all_cards: np.array,
):
    examples = []
    deck_copy = np.copy(deck)
    window = window_size // 2
    for shuffle_id in range(shuffles):
        for position in range(len(deck_copy)):
            examples.append(
                (
                    get_positive_samples(position, deck_copy, window),
                    get_negative_samples(position, deck_copy, n_negatives, all_cards),
                )
            )
    return examples


def generate_all_examples(
    decks: List[np.array], window_size: int, n_negatives: int, shuffles: int, n_jobs=-1
):

    pass