#=============================================================================
#;;
#;;  a pretty-printer for Python
#;;  Copyright (C) 2012 -  Frederic Peschanski
#;;
#;;  This is a Lua then a Python Port of the following:
#;;
#;;  a pretty-printer for PLT-Scheme
#;;  Copyright (C) 2005 - 2008 David Herman
#
#;;  Portions based on PPrint.hs - a pretty-printer for Haskell
#;;  Copyright 2000, Daan Leijen. All rights reserved.
#;;  See COPYING.HASKELL for accompanying license.
#;;
#;;  Portions based on pprint.m - a pretty-printer for Mercury
#;;  Copyright (C) 2000-2002 The University of Melbourne
#;;  Written by Ralph Becket
#;;  See COPYING for accompanying license.
#;;
#;;  This library is free software; you can redistribute it and/or modify it
#;;  under the terms of the GNU Lesser General Public License as published by
#;;  the Free Software Foundation; either version 2.1 of the License, or (at
#;;  your option) any later version.
#;;
#;;  This library is distributed in the hope that it will be useful, but WITHOUT
#;;  ANY WARRANTY; without even the implied warranty of MERCHANTABILITY or
#;;  FITNESS FOR A PARTICULAR PURPOSE.  See the GNU Lesser General Public
#;;  License for more details.
#;;
#;;  You should have received a copy of the GNU Lesser General Public License
#;;  along with this library; if not, write to the Free Software Foundation,
#;;  Inc., 59 Temple Place, Suite 330, Boston, MA 02111-1307 USA
#;;
#;; =============================================================================

from pypretty.combin import happend, vappend, nest, text,\
                            hsappend, fill, align, vbappend,\
                            fill_break, group

from pypretty.layout import pprint
