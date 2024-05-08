from django import template

register = template.Library()

BAN_WORDS = ["редиска", "помидор", "огурец"]
CAPS_BAN_WORDS = [i[0].capitalize()+i[1:] for i in BAN_WORDS]


@register.filter()
def censor(sentence):
    for i in sentence.split():
        if "!" in i or "?" in i:
            i = i[0:-1]
        if i in BAN_WORDS or i in CAPS_BAN_WORDS:
            new_word = i[0] + (len(i[1:]) * "*")
            sentence = sentence.replace(i, new_word)
    return sentence
