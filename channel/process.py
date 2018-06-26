from .models import Tag


def tagprocess(tagtext):
    tagl = tagtext.replace(" ", "")
    taglist = tagl.split("#")
    taglist.remove('')

    TagR = []
    for tagitem in taglist:
        TagR.append(tagitem)

    return TagR
