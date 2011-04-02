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


def count_words(text, match=None):
    """
    Returns a list of (word, value) pairs.

    >>> count_words("a a b c")
    [('a', 2), ('c', 1), ('b', 1)]
    >>> count_words("a a b c", match="[ab]+")
    [('a', 2), ('b', 1)]
    """
    word_list = split_words(text)
    unique_split_words = set(word_list)
    return [(word, word_list.count(word))
            for word in unique_split_words
            if match == None or re.match(match, word)]


def find_all(s, sub):
    if not sub:
        return []
    positions = []
    i = s.find(sub)
    while i != -1:
        positions.append(i)
        i = s.find(sub, i + len(sub))
    return positions


def highlight_ranges(s, ranges, formatting="<strong>%s</strong"):
    """
    >>> highlight_ranges("0123456789", [(2, 5), (2, 6), (8,9), (9, 10)], "<%s>")
    '01<2345>67<89>'
    >>> highlight_ranges("0123", [])
    '0123'
    """
    if not ranges:
        return s
    last_end = 0
    last_start = 0
    splitted = []
    for start, end in ranges:
        if last_end and start <= last_end:
            splitted.pop()
            start = last_start
        else:
            splitted.append(s[last_end:start])
        splitted.append(s[start:end])
        last_start = start
        last_end = end
    splitted.append(s[end:])
    return ''.join([ (formatting % x if i % 2 == 1 else x)
                     for i, x in enumerate(splitted) ])


def highlight_query(s, query, formatting="<strong>%s</strong>"):
    u"""
    >>> text = u"Geri vyrai geroi girioi Gerą girą gerai gėrė"
    >>> print highlight_query(text, "gera gere", "<%s>")
    Geri vyrai geroi girioi <Gerą> girą <gera>i <gėrė>
    >>> print highlight_query(text, "")
    Geri vyrai geroi girioi Gerą girą gerai gėrė
    >>> print highlight_query(text, "nnn")
    Geri vyrai geroi girioi Gerą girą gerai gėrė
    >>> text = u"Geri vyrai geroi girioi „Gerą“ girą gerai gėrė"
    >>> print highlight_query(text, "gera gere", "<%s>")
    Geri vyrai geroi girioi „<Gerą>“ girą <gera>i <gėrė>
    """
    unwanted_chars = u'[„“]'
    clean = lambda c: re.sub(unwanted_chars, ' ', c)
    norm_s = unicode_to_ascii( clean(s) ).lower()
    norm_query = unicode_to_ascii( clean(query) ).lower()
    if len(norm_s) < len(s):
        # we need to keep equal char length, however python does not support
        # normalization of some characters, like lithuanian-quotes.
        norm_s = s.lower()
        norm_query = query.lower()

    ranges = []
    for word in set(split_words(norm_query)):
        ranges.extend([ ( i, i+len(word) )
                        for i in find_all(norm_s, word) ])
    return highlight_ranges(s, ranges, formatting)
