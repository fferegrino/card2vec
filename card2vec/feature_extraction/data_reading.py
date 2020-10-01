import csv
import json
from pathlib import Path

import numpy as np


def read_cards(path: Path):
    card_by_id = dict()
    card_to_int = dict()
    int_to_card = dict()
    with open(Path(path, "yugioh-cards", "cards.csv")) as fp:
        reader = csv.DictReader(fp)
        for idx, card in enumerate(reader):
            card_by_id[card["id"]] = dict(card)
            card_to_int[card["id"]] = idx
            int_to_card[idx] = card["id"]

    with open(Path(path, "yugioh-cards", "variants.csv")) as fp:
        reader = csv.reader(fp)
        next(reader)
        variants = {row[0]: row[1] for row in reader}

    return {
        "card_by_id": card_by_id,
        "card_to_int": card_to_int,
        "int_to_card": int_to_card,
        "variants": variants,
    }


def read_decks(path: Path, variants: dict, card_to_int: dict):
    decks = []
    for jsonl in sorted(Path(path, "yugioh-decks").glob("**/*.jsonl")):
        for line in jsonl.open():
            deck_info = json.loads(line)
            if (
                "deck" in deck_info
                and "main" in deck_info["deck"]
                and len(deck_info["deck"]["main"])
            ):
                deck = {
                    "main": [
                        card_to_int[variants.get(card_id, card_id)]
                        for card_id in deck_info["deck"]["main"]
                        if variants.get(card_id, card_id) in card_to_int
                    ],
                    "side": [
                        card_to_int[variants.get(card_id, card_id)]
                        for card_id in deck_info["deck"].get("side", list())
                        if variants.get(card_id, card_id) in card_to_int
                    ],
                    "extra": [
                        card_to_int[variants.get(card_id, card_id)]
                        for card_id in deck_info["deck"].get("extra", list())
                        if variants.get(card_id, card_id) in card_to_int
                    ],
                }
                decks.append(deck)
    return decks
