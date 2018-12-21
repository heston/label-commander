from titlecase import titlecase


def process(text):
    filtered_text = text
    for f in filters:
        filtered_text = f(filtered_text)
    return filtered_text


def lower_case(text):
    return text.lower()


def amp(text):
    return text.replace(' and ', ' & ')


def apos(text):
    return text.replace(" ' ", "'")


filters = [
    lower_case,
    amp,
    apos,
    titlecase,
]
