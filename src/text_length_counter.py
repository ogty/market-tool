import unicodedata


def text_length_counter(text: str) -> int:
    count = 0
    for char in text:
        if unicodedata.east_asian_width(char) in "FWA":
            count += 2
        else:
            count += 1
    return count
