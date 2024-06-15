from random import choice

from news.forms import BAD_WORDS

COMMENT_FORM = {
    "text": "new text",
}

COMMENT_BAD_WORDS = {
    "text": f"Какой-то текст, {choice(BAD_WORDS)}, еще текст"
}
