#                                                           -*- Python -*-
#    ast -- a simple abstract-syntax-tree class
#    Copyright (C) 2001  Eric S. Tiedemann <est@hyperreal.org>
#
#    This program is free software; you can redistribute it and/or modify
#    it under the terms of the GNU General Public License as published by
#    the Free Software Foundation; either version 2 of the License, or
#    (at your option) any later version.
#
#    This program is distributed in the hope that it will be useful,
#    but WITHOUT ANY WARRANTY; without even the implied warranty of
#    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#    GNU General Public License for more details.
#
#    You should have received a copy of the GNU General Public License
#    along with this program; if not, write to the Free Software
#    Foundation, Inc., 59 Temple Place, Suite 330, Boston, MA  02111-1307  USA
#

class ast:
    def __init__(self, type, kids):
        self.type = type
        self.kids = kids

    def __getitem__(self, i):
        return self.kids[i]
    
    def __str__(self, indent=0):
        s = ' ' * indent
        s += self.type
        for k in self.kids:
            if isinstance(k, ast):
                s1 = k.__str__(indent + 1)
            else:
                s1 = (' ' * (indent + 1)) + str(k)
            s += "\n"
            s += s1
        return s
