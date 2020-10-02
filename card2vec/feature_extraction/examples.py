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
    import pdb; pdb.set_trace()
    deck_copy = np.copy(deck)
    window = window_size // 2
    deck_size = len(deck_copy)
    window_examples = window_size - 1


    positive_examples = np.zeros((deck_size * shuffles * window_examples, 2))
    negative_examples = np.zeros((deck_size * shuffles * n_negatives, 2))

    for shuffle_id in range(shuffles):
        for position in range(deck_size):
            positive_start = shuffle_id * deck_size + position * window_examples
            positive_end = shuffle_id * deck_size + ((position * window_examples) + window_examples)
            positive = get_positive_samples(position, deck_copy, window)
            if positive.shape != positive_examples[positive_start:positive_end,:].shape:
                import pdb; pdb.set_trace()
                pass

            get_negative_samples(position, deck_copy, n_negatives, all_cards)
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
    all_examples =[get_examples_for_deck(*param) for param in params] #p.starmap(get_examples_for_deck, params)
    positives = []
    negatives = []
    p.close()
    p.join()
