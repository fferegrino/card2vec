import json
from pathlib import Path

from card2vec.feature_extraction.data_reading import read_cards


def test_read_cards(fixtures_dir):
    expected = json.load(Path(fixtures_dir, "read", "cards.json").open())
    expected["int_to_card"] = {int(k): v for k, v in expected["int_to_card"].items()}
    actual = read_cards(Path(fixtures_dir, "raw"))
    assert expected == actual
