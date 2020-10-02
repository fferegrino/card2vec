import multiprocessing as mp
import os
import random
from typing import List

import numpy as np


def get_positive_samples(position: int, deck: np.array, window: int):
    examples = np.zeros((window * 2 + 1, 2), dtype=int)
    examples[:, 0] = deck[position]
    examples[:, 1] = deck[
        np.arange(position - window, position + window + 1) % len(deck)
    ]
    mask = np.ones(window * 2 + 1, dtype=bool)
    mask[window] = False
    return examples[mask]


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
    deck_copy = np.copy(deck)
    deck_size = len(deck_copy)
    window = window_size // 2
    window_examples = window * 2

    positive_examples = np.zeros((deck_size * shuffles * window_examples, 2), dtype=int)
    negative_examples = np.zeros((deck_size * shuffles * n_negatives, 2), dtype=int)

    for shuffle_id in range(shuffles):
        for position in range(deck_size):
            positive = get_positive_samples(position, deck_copy, window)
            positive_start = (
                shuffle_id * deck_size * window_examples + position * window_examples
            )
            positive_end = shuffle_id * deck_size * window_examples + (
                (position * window_examples) + window_examples
            )
            positive_examples[positive_start:positive_end, :] = positive
            negative = get_negative_samples(position, deck_copy, n_negatives, all_cards)
            negative_start = (
                shuffle_id * deck_size * n_negatives + position * n_negatives
            )
            negative_end = shuffle_id * deck_size * n_negatives + (
                (position * n_negatives) + n_negatives
            )
            negative_examples[negative_start:negative_end, :] = negative
        np.random.shuffle(deck_copy)
    return positive_examples, negative_examples


def generate_all_examples(
    decks: List[dict],
    window_size: int,
    n_negatives: int,
    shuffles: int,
):
    deck_arrays = []
    unique_cards = set()
    for deck in decks:
        deck_arrays.append(np.array(deck["main"] + deck["side"] + deck["extra"]))
        unique_cards.update(deck["main"] + deck["side"] + deck["extra"])
    all_cards = np.array(list(unique_cards))

    params = (
        (deck_array, window_size, n_negatives, shuffles, all_cards)
        for deck_array in deck_arrays
    )

    p = mp.Pool(2)
    all_examples = [
        get_examples_for_deck(*param) for param in params
    ]  # p.starmap(get_examples_for_deck, params)

    p.close()
    p.join()

    positives, negatives = zip(*all_examples)
    return np.concatenate(positives), np.concatenate(negatives)


def generate_batches(
    positive_examples: np.array,
    negative_examples: np.array,
    window_size: int,
    n_negatives: int,
):
    window = window_size // 2
    window_examples = window * 2
    for pos, neg in zip(
        range(0, positive_examples.shape[0], window_examples),
        range(0, negative_examples.shape[0], n_negatives),
    ):
        yield positive_examples[pos : pos + window_examples, :], negative_examples[
            neg : neg + n_negatives, :
        ]
