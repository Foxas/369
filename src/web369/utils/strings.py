# encoding: utf-8;

import unicodedata
import re
import string


def unicode_to_ascii(s, errors="ignore"):
    u"""
    >>> unicode_to_ascii(u'„Ąžėęūšųį“')
    'Azeeusui'
    """
    s = unicode(s)
    return unicodedata.normalize("NFKD", s).encode('ascii', errors)


def word_list(text):
    u"""
    Return list of words in string. To get unique list of words use::

    >>> print word_list(u" „vienas“ du, \\u0161ienas!")
    [u'vienas', u'du', u'\\u0161ienas']
    """
    return re.findall('\w+', text, flags=re.U)


def text_split(text):
    u"""
    Slit text into list of words and non-word

    >>> print text_split(u"„vienas“ du, \\u0161ienas!")
    [u'\\u201e', u'vienas', u'\\u201c ', u'du', u', ', u'\\u0161ienas', u'!']
    """
    return re.findall(r'\w+|\W+', text, flags=re.U)


def count_words(text, match=None):
    """
    Returns a list of (word, count) pairs.

    >>> count_words("a a b c")
    [('a', 2), ('c', 1), ('b', 1)]
    >>> count_words("a a b c", match="[ab]+")
    [('a', 2), ('b', 1)]
    """
    words = word_list(text)
    unique_words = set(words)
    return [(word, words.count(word))
            for word in unique_words
            if match == None or re.match(match, word)]


def highlight_words(text, words, formatting="<strong>%s</strong>"):
    u"""
    >>> text = u"Geri vyrai geroi girioi Gerą girą gerai gėrė. "
    >>> print highlight_words(text, ['gera', 'gere'], "<%s>")
    Geri vyrai geroi girioi <Gerą> girą gerai <gėrė>. 
    >>> print highlight_words(text, [], "<%s>")
    Geri vyrai geroi girioi Gerą girą gerai gėrė. 
    >>> print highlight_words(text, ['nnn'], "<%s>")
    Geri vyrai geroi girioi Gerą girą gerai gėrė. 
    >>> text = u"„Geri“ vyrai geroi girioi „Gerą“ girą gerai gėrė"
    >>> print highlight_words(text, ['gera', 'gere'], "<%s>")
    „Geri“ vyrai geroi girioi „<Gerą>“ girą gerai <gėrė>
    >>> print highlight_words(text, "one two free".split(), "<%s>")
    „Geri“ vyrai geroi girioi „Gerą“ girą gerai gėrė
    """
    text = text_split(text)
    for index, word in enumerate(text):
        if unicode_to_ascii(word).lower() in words:
            text[index] = formatting % word
    return ''.join(text)
