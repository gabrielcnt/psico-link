import re
import unicodedata


def slug_treatment(text: str) -> str:

    text = text.strip()

    normalized = unicodedata.normalize("NFD", text)

    remove_accents = "".join(
        char for char in normalized if unicodedata.category(char) != "Mn"
    )

    text_lower = remove_accents.lower()

    replace_spaces = text_lower.replace(" ", "-")

    remove_invalid_characters = re.sub("[^a-z0-9-]", "", replace_spaces)

    hifens_duplicate = re.sub(r"-{2,}", "-", remove_invalid_characters)

    slug = hifens_duplicate.strip("-")

    return slug



def crp_treatment_to_slug(crp: str) -> str:
    text = crp.strip()

    crp = text.replace("/", "")

    return crp

print(slug_treatment(" --gâbriEl--@   & VieírA--   "))

print(crp_treatment_to_slug("65/87954"))