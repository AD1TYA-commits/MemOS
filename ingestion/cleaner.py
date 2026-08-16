import re

def clean_text(text):
    text = text.replace("\xa0", " ")
    text = re.sub(r"[ \t]+"," ",text)
    text = re.sub(r"\n{3,}"," ",text)
    return text.strip()