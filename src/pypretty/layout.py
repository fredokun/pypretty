'''Layout algorithm.

Created on 5 août 2012

@author: fredo
'''

from pypretty.combin import extend
from pypretty.doc import flatten


class SimpleDoc:
    def __init__(self):
        self._rest = None

    @property
    def isempty(self):
        return False

    @property
    def istext(self):
        return False

    @property
    def ispush(self):
        return False

    @property
    def ispop(self):
        return False

    @property
    def isline(self):
        return False

    @property
    def rest(self):
        return self._rest

    @rest.setter
    def rest(self, nrest):
        self._rest = nrest

    def __repr__(self):
        strng = self._child_repr()
        if self._rest:
            strng += repr(self._rest)
        else:
            strng += 'None'
        return strng + ')'

    def _child_repr(self):
        raise NotImplemented("Abstract method")


class SEmpty(SimpleDoc):
    def __init__(self):
        SimpleDoc.__init__(self)

    @property
    def isempty(self):
        return True

    @property
    def rest(self):
        raise NotImplemented("Rest not available for empty document")

    @rest.setter
    def rest(self, nrest):
        raise NotImplemented("Rest not available for empty document")

    def _child_repr(self):
        return 'SEmpty('


class SText(SimpleDoc):
    def __init__(self, text):
        SimpleDoc.__init__(self)
        self.__text = text

    @property
    def istext(self):
        return True

    @property
    def text(self):
        return self.__text

    def _child_repr(self):
        return "SText(" + repr(self.__text) + ','


class SPush(SimpleDoc):
    def __init__(self, fun):
        SimpleDoc.__init__(self)
        self.__fun = fun

    @property
    def ispush(self):
        return True

    @property
    def fun(self):
        return self.__fun

    def _child_repr(self):
        return "SPush(" + repr(self.__fun) + ","


class SPop(SimpleDoc):
    def __init__(self):
        SimpleDoc.__init__(self)

    @property
    def ispop(self):
        return True

    def _child_repr(self):
        return "SPop("


class SLine(SimpleDoc):
    def __init__(self, first):
        SimpleDoc.__init__(self)
        self.__first = first

    @property
    def isline(self):
        return True

    @property
    def first(self):
        return self.__first

    def _child_repr(self):
        return "SLine(" + repr(self.__first) + ","


def fst(tup):
    return tup[0]


def snd(tup):
    return tup[1]


def string_too_big(text, col, width):
    return (col + len(text)) > width


class Backtrack(Exception):
    pass


def best_layout(width, col, docs, alternate):

    root = None
    parent = None

    its_over = False
    while not its_over:
        current = None

        if not docs:
            current = SEmpty()
            its_over = True
        elif docs[0] == False:
            current = SPop()
            docs = docs[1:]
        elif snd(docs[0]).isnil:
            docs = docs[1:]
        elif snd(docs[0]).iscat:
            datum, cat = docs[0]
            docs = [(datum, cat.left), (datum, cat.right)] + docs[1:]
        elif snd(docs[0]).isnest:
            datum, nest = docs[0]
            docs = [(extend(datum, nest.depth), nest.doc)] + docs[1:]
        elif snd(docs[0]).islabel:
            datum, label = docs[0]
            docs = [(datum + label.label, label.doc)] + docs[1:]
        elif snd(docs[0]).ismarkup:
            datum, markup = docs[0]
            current = SPush(markup.fmarkup)
            docs = [(datum, markup.doc), False] + docs[1:]
        elif snd(docs[0]).isline:
            datum, _ = docs[0]
            current = SLine(datum)
            col = len(datum)
            docs = docs[1:]
        elif snd(docs[0]).isgroup:
            datum, group = docs[0]
            try:
                current = best_layout(width, col,
                                      [(datum, flatten(group.doc))] + docs[1:],
                                      True)
                its_over = True
            except Backtrack:
                docs = [(datum, group.doc)] + docs[1:]
        elif snd(docs[0]).istext:
            _, text = docs[0]
            if width > 0 and alternate \
            and string_too_big(text.text, col, width):
                raise Backtrack()
            else:
                current = SText(text.text)
                col += len(text.text)
                docs = docs[1:]
        elif snd(docs[0]).iscolumn:
            datum, column = docs[0]
            docs = [(datum, column.fcolumn(col))] + docs[1:]
        elif snd(docs[0]).isnesting:
            datum, nesting = docs[0]
            docs = [(datum, nesting.fnesting(len(datum)))] + docs[1:]

        else:
            raise NotImplemented("Unexpected document type (please report)")

        if current != None:
            # print('Current = ' + repr(current))
            if root == None:
                root = current
            if parent != None:
                parent.rest = current
            parent = current

    # end while

    return root


def layout(width, doc):
    return best_layout(width, 0, [("", doc)], False)

DEFAULT_PAGE_WIDTH = 80


def set_default_page_width(width):
    assert(width > 0)
    global DEFAULT_PAGE_WIDTH
    DEFAULT_PAGE_WIDTH = width


def sdoc_to_string(sdoc):
    if sdoc.isempty:
        return ""
    elif sdoc.istext:
        return sdoc.text + sdoc_to_string(sdoc.rest)
    elif sdoc.ispush:
        return sdoc_to_string(sdoc.rest)
    elif sdoc.ispop:
        return sdoc_to_string(sdoc.rest)
    elif sdoc.isline:
        return "\n" + sdoc.first + sdoc_to_string(sdoc.rest)
    else:
        raise NotImplemented("Unsupported simple document")


def pprint(doc, width=DEFAULT_PAGE_WIDTH):
    return sdoc_to_string(layout(width, doc))
