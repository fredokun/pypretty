'''Document representation

Created on 4 août 2012

@author: fredo
'''

#==============================================================================
# Document representation
#==============================================================================


class Doc:
    @property
    def isnil(self):
        return False

    @property
    def iscat(self):
        return False

    @property
    def isnest(self):
        return False

    @property
    def islabel(self):
        return False

    @property
    def ismarkup(self):
        return False

    @property
    def isline(self):
        return False

    @property
    def isgroup(self):
        return False

    @property
    def istext(self):
        return False

    @property
    def iscolumn(self):
        return False

    @property
    def isnesting(self):
        return False

    def flatten(self):
        raise NotImplemented("Abstract method")


class DocNil(Doc):
    def __init__(self):
        pass

    @property
    def isnil(self):
        return True

    def flatten(self):
        return DocNil()

    def __repr__(self):
        return "Nil"


class DocCat(Doc):
    def __init__(self, left, right):
        assert(isinstance(left, Doc))
        assert(isinstance(right, Doc))
        self.__left = left
        self.__right = right

    @property
    def iscat(self):
        return True

    @property
    def left(self):
        return self.__left

    @property
    def right(self):
        return self.__right

    def flatten(self):
        return DocCat(self.__left.flatten(), self.__right.flatten())

    def __repr__(self):
        return "Cat(" + repr(self.left) + ", " \
            + repr(self.right) + ")"


class DocNest(Doc):
    def __init__(self, depth, doc):
        self.__depth = depth
        self.__doc = doc

    @property
    def isnest(self):
        return True

    @property
    def depth(self):
        return self.__depth

    @property
    def doc(self):
        return self.__doc

    def flatten(self):
        return self.__doc.flatten()

    def __repr__(self):
        return "Nest(" + repr(self.depth) + ", " \
            + repr(self.doc) + ")"


class DocLabel(Doc):
    def __init__(self, label, doc):
        self.__label = label
        self.__doc = doc

    @property
    def islabel(self):
        return True

    @property
    def label(self):
        return self.__label

    @property
    def doc(self):
        return self.__doc

    def flatten(self):
        return self.__doc.flatten()

    def __repr__(self):
        return "Label(" + repr(self.depth) + ", " \
            + repr(self.doc) + ")"


class DocMarkup(Doc):
    def __init__(self, fmarkup, doc):
        self.__fmarkup = fmarkup
        self.__doc = doc

    @property
    def ismarkup(self):
        return True

    @property
    def fmarkup(self):
        return self.__fmarkup

    @property
    def doc(self):
        return self.__doc

    def flatten(self):
        return DocMarkup(self.__fmarkup, self.__doc.flatten())

    def __repr__(self):
        return "Markup(" + repr(self.fmarkup) + ", " \
            + repr(self.doc) + ")"


class DocText(Doc):
    def __init__(self, text):
        assert(isinstance(text, str))
        self.__text = text

    @property
    def istext(self):
        return True

    @property
    def text(self):
        return self.__text

    def flatten(self):
        return DocText(self.__text)

    def __repr__(self):
        return "Text(" + repr(self.text) + ")"


class DocLine(Doc):
    def __init__(self, breakp):
        self.__breakp = breakp

    @property
    def isline(self):
        return True

    @property
    def breakp(self):
        return self.__breakp

    def flatten(self):
        if self.__breakp:
            return DocNil()
        else:
            return DocText(' ')

    def __repr__(self):
        return "Line(" + repr(self.breakp) + ")"


class DocGroup(Doc):
    def __init__(self, doc):
        self.__doc = doc

    @property
    def isgroup(self):
        return True

    @property
    def doc(self):
        return self.__doc

    def flatten(self):
        return self.__doc.flatten()

    def __repr__(self):
        return "Group(" + repr(self.doc) + ")"


class DocColumn(Doc):
    def __init__(self, fcolumn):
        self.__fcolumn = fcolumn

    @property
    def iscolumn(self):
        return True

    @property
    def fcolumn(self):
        return self.__fcolumn

    def flatten(self):
        return DocColumn(lambda doc: self.__fcolumn(doc).flatten())

    def __repr__(self):
        return "Column(" + repr(self.fcolumn) + ")"


class DocNesting(Doc):
    def __init__(self, fnesting):
        self.__fnesting = fnesting

    @property
    def isnesting(self):
        return True

    @property
    def fnesting(self):
        return self.__fnesting

    def flatten(self):
        return DocNesting(lambda doc: self.__fnesting(doc).flatten())

    def __repr__(self):
        return "Nesting(" + repr(self.fnesting) + ")"


#==============================================================================
# Primitives
#==============================================================================

def empty():
    return DocNil()


def nest(i, x):
    return DocNest(i, x)


def text(s):
    return DocText(s)


def label(l, d):
    return DocLabel(l, d)


def markup(f, d):
    return DocMarkup(f, d)


def column(f):
    return DocColumn(f)


def nesting(f):
    return DocNesting(f)


def group(x):
    return DocGroup(x)


def char(c):
    if c == "\n":
        return line()
    else:
        return text(str(c))


def line():
    return DocLine(False)


def lbreak():
    return DocLine(True)


def soft_line():
    return group(line())


def soft_lbreak():
    return group(lbreak())


#==============================================================================
# Document flattening
#==============================================================================

def flatten(doc):
    return doc.flatten()
