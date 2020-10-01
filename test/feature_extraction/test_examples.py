import random
from unittest.mock import ANY, patch

import numpy as np
import pytest

from card2vec.feature_extraction.examples import (
    get_examples_for_deck,
    get_negative_samples,
    get_positive_samples,
)


@pytest.fixture
def seed():
    random.seed(42)
    np.random.seed(42)
    yield


@pytest.fixture()
def all_cards():
    return np.arange(0, 1000)


@pytest.mark.parametrize(
    ["position", "deck", "window", "expected"],
    [
        # fmt: off
    (
            0,
            np.arange(10, 20),
            2,
            np.array([
                [10., 18.],
                [10., 19.],
                [10., 11.],
                [10., 12.]
            ])
    ),
    (
            5,
            np.arange(1, 11),
            4,
            np.array([
                [6., 2.],
                [6., 3.],
                [6., 4.],
                [6., 5.],
                [6., 7.],
                [6., 8.],
                [6., 9.],
                [6., 10.]
            ])
    ),
    (
            9,
            np.arange(10, 20),
            2,
            np.array([
                [19., 17.],
                [19., 18.],
                [19., 10.],
                [19., 11.]
            ])
    )
        # fmt: on
    ],
)
def test_get_positive_samples(position, deck, window, expected):
    actual = get_positive_samples(position, deck, window)
    assert np.allclose(actual, expected)


@pytest.mark.parametrize(
    ["position", "n_negatives", "expected"],
    [
        # fmt: off
    (
        0,
        10,
        np.array([
            [0, 102],
            [0, 435],
            [0, 860],
            [0, 270],
            [0, 106],
            [0, 71],
            [0, 700],
            [0, 20],
            [0, 614],
            [0, 121]
          ])
    ),
    (
        0,
        2,
        np.array([
            [0, 102],
            [0, 435]
          ])
    ),
        # fmt: on
    ],
)
def test_get_negative_samples(seed, all_cards, position, n_negatives, expected):
    deck = np.arange(0, 10)
    actual = get_negative_samples(position, deck, n_negatives, all_cards)
    assert np.allclose(actual, expected)


@pytest.mark.parametrize(
    ["n_negatives", "window_size", "shuffles"], [(2, 5, 1), (10, 15, 4)]
)
def test_get_examples_for_deck(all_cards, n_negatives, window_size, shuffles):
    deck_size = 4
    deck = np.arange(0, deck_size)

    with patch(
        "card2vec.feature_extraction.examples.get_negative_samples"
    ) as neg_samples_patch, patch(
        "card2vec.feature_extraction.examples.get_positive_samples"
    ) as pos_samples_patch:

        actual = get_examples_for_deck(
            deck, window_size, n_negatives, shuffles, all_cards
        )

    neg_samples_patch.assert_called_with(ANY, ANY, n_negatives, all_cards)
    pos_samples_patch.assert_called_with(ANY, ANY, window_size // 2)
    assert len(actual) == shuffles * deck_size
