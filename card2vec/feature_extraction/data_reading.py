import csv
from pathlib import Path


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

    return {
        "card_by_id": card_by_id,
        "card_to_int": card_to_int,
        "int_to_card": int_to_card,
    }
