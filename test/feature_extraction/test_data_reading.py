import json
from pathlib import Path

from card2vec.feature_extraction.data_reading import read_cards, read_decks


def test_read_cards(fixtures_dir):
    expected = json.load(Path(fixtures_dir, "read", "cards.json").open())
    expected["int_to_card"] = {int(k): v for k, v in expected["int_to_card"].items()}
    actual = read_cards(Path(fixtures_dir, "raw"))
    assert expected == actual


def test_read_decks(fixtures_dir):
    expected = json.load(Path(fixtures_dir, "read", "decks.json").open())
    card_info = json.load(Path(fixtures_dir, "read", "cards.json").open())
    decks = read_decks(
        Path(fixtures_dir, "raw"),
        variants=card_info["variants"],
        card_to_int=card_info["card_to_int"],
    )
    assert decks == expected
