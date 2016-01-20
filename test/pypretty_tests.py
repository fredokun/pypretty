'''Tests for the pretty printer

Created on 5 août 2012

@author: F. Peschanski
'''

import sys
sys.path.append("../src/")

from pypretty import vappend, nest, text, pprint, happend, group,\
                     hsappend, vbappend, fill, fill_break, align


def example_doc_1():
    '''First example from scheme pprint lib'''
    return vappend(nest(4, vappend(text("while (true) {"),
                                   text("f();"),
                                   nest(4, vappend(text("if (done())"),
                                                   text("exit();"))))),
                   text("}"))


def example_doc_2():
    '''Second example from scheme pprint library'''
    return hsappend(text('let'),
                    align(vbappend(hsappend(fill(6, text('empty')),
                                            text('::'),
                                            text('Doc')),
                                   hsappend(fill(6, text('next')),
                                            text('::'),
                                            text('Int -> Doc -> Doc')),
                                   hsappend(fill(6, text('linebreak')),
                                            text('::'),
                                            text('Doc')))))


def example_doc_2bis():
    '''Second example from scheme pprint library, second varian'''
    return hsappend(text('let'),
                    align(vbappend(hsappend(fill_break(6, text('empty')),
                                            text('::'),
                                            text('Doc')),
                                   hsappend(fill_break(6, text('next')),
                                            text('::'),
                                            text('Int -> Doc -> Doc')),
                                   hsappend(fill_break(6, text('linebreak')),
                                            text('::'),
                                            text('Doc')))))


def example_doc_3():
    '''A simple group example'''
    return happend(hsappend(text('public'), text('void'), text('mymethod')),
                   text('('),
                   align(group(vappend(
                happend(text('Type1'), text(' '), text('arg1'), text(',')),
                happend(text('Type2'), text(' '), text('arg2'), text(',')),
                happend(text('Type3'), text(' '), text('arg3'), text(',')),
                happend(text('Type4'), text(' '), text('arg4'))))),
                   text(')'),
                   text(';'))

if __name__ == "__main__":
    print("Example 1:")
    print("----------")
    doc = example_doc_1()
    strng = pprint(doc)
    print(strng)
    print()

    print("Example 2:")
    print("----------")
    doc = example_doc_2()
    strng = pprint(doc)
    print(strng)
    print()

    print("Example 2bis:")
    print("----------")
    doc = example_doc_2bis()
    strng = pprint(doc)
    print(strng)
    print()

    print("Example 3:")
    print("---------")
    doc = example_doc_3()
    strng = pprint(doc)
    print(strng)
    print()

    print("Example 3bis:")
    print("-------------")
    doc = example_doc_3()
    strng = pprint(doc, width=60)
    print(strng)
    print()
