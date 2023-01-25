from enum import Enum

class HTMLTAG(Enum):
    TD = 1,
    DIV = 2,
    IMG = 3

def Return(tag):
    return tag.name.lower()