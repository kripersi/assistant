from config import COMMANDS_JSON
from assistant.utils import read_json


def match_command(text):
    text = text.lower()
    commands = read_json(COMMANDS_JSON)

    for action, variants in commands.items():
        if isinstance(variants, dict):
            for key, synonyms in variants.items():
                if any(word in text for word in synonyms):
                    return action, key, variants
        elif isinstance(variants, list):
            if any(word in text for word in variants):
                return action, None, variants
    return None, None, None
