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


def split_words(text):
    """
    Return list of words in string. To get unique list of words use::

        unique_words = set( split_words(text) )
    """
    return re.sub('\W+', ' ', text).split(' ')


def highlight_query(text, query, formatting="<strong>%s</strong>"):
    u"""
    >>> text = u"Geri vyrai geroi girioi Gerą girą gerai gėrė"
    >>> print highlight_query(text, "gera gere", "<%s>")
    Geri vyrai geroi girioi <Gerą> girą gerai <gėrė>
    >>> print highlight_query(text, "")
    Geri vyrai geroi girioi Gerą girą gerai gėrė
    >>> print highlight_query(text, "nnn")
    Geri vyrai geroi girioi Gerą girą gerai gėrė
    >>> text = u"Geri vyrai geroi girioi „Gerą“ girą gerai gėrė"
    >>> print highlight_query(text, "gera gere", "<%s>")
    Geri vyrai geroi girioi „<Gerą>“ girą gerai <gėrė>
    """
    text = re.split(u'([ -@[-`{-~“-„]+)', text)
    words_to_highlight = split_words(unicode_to_ascii(query).lower())
    for index, word in enumerate(text):
        if unicode_to_ascii(word).lower() in words_to_highlight:
            text[index] = formatting % word
    return ''.join(text)
