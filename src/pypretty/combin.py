'''Document combinators.

Created on 4 août 2012

@author: fredo
'''

from pypretty.doc import empty, column, DocCat, line, soft_line, lbreak, \
                         soft_lbreak, group, text, nesting, nest

#==============================================================================
# Basic combinators
#==============================================================================


def happend(*args):
    '''Doc * Doc * ... -> Doc
    Concatenates argument (horizontaly)
    '''
    if not args:
        return empty()

    doc = args[-1]

    for arg in args[-2::-1]:
        doc = DocCat(arg, doc)

    return doc


def happend_with(sep, *args):
    '''Doc * Doc * Doc * ... -> Doc
    Concatenates the argument, each one separated
    by the sep document
    '''
    if not args:
        return empty()
    size = len(args)
    if size == 1:
        return args[0]
    # at least 2 arguments
    nargs = []
    count = 0
    for arg in args:
        nargs.append(arg)
        if count < size - 1:
            nargs.append(sep)
        count = count + 1
    return happend(*nargs)


def hsappend(*args):
    return happend_with(space(), *args)


def vappend(*args):
    return happend_with(line(), *args)


def vsappend(*args):
    return happend_with(soft_line(), *args)


def vbappend(*args):
    return happend_with(lbreak(), *args)


def vsbappend(*args):
    return happend_with(soft_lbreak(), *args)


#=============================================================================
# Fillers and alignments
#=============================================================================

def width(doc, fun):
    return column(lambda k1: happend(doc, \
                                     column(lambda k2: fun(k2 - k1))))


SPACE_CHARACTER = " "


def change_space_character(nspace):
    global SPACE_CHARACTER
    SPACE_CHARACTER = nspace


def space():
    return text(SPACE_CHARACTER)


def spaces(nb):
    assert(nb >= 0)
    # TODO: faster version ?
    msg = ""
    while nb > 0:
        msg += SPACE_CHARACTER
        nb = nb - 1
    return text(msg)


def extend(strng, nb_spaces):
    return strng + spaces(nb_spaces).text


def fill(nb_spaces, doc):
    '''Add extra spaces to rendered
    document to reach at least nb_spaces
    '''
    def f(n):
        if n > nb_spaces:
            return empty()
        else:
            return spaces(nb_spaces - n)
    return width(doc, f)


def fill_break(nb_spaces, doc):
    '''Add extra spaces to rendered
    document to reach at least nb_spaces, otherwise
    insert a line break
    '''
    def f(n):
        if n > nb_spaces:
            return nest(nb_spaces, lbreak())
        else:
            return spaces(nb_spaces - n)
    return width(doc, f)


def indent(nb, doc):
    return hang(nb, happend(spaces(nb), doc))


def hang(nb, doc):
    return align(nest(nb, doc))


def align(doc):
    return column(lambda k: nesting(lambda i: nest(k - i, doc)))
