#                                                            -*- Python -*-
#    scanopt  -  scans *selected* options out of an arg list
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

"""
Derived (via cut-and-paste) from getopt.
This scans specified arguments out of args, skipping over options it
doesn't know about.
This should probably be a mode for getopt.
"""
class ScanoptError(Exception):
    opt = ''
    msg = ''
    def __init__(self, msg, opt):
        self.msg = msg
        self.opt = opt
        Exception.__init__(self, msg, opt)

    def __str__(self):
        return self.msg

def scanopt(args, longopts):
    opts = []
    newargs = []
    
    while args:
        arg = args[0]
        if arg == '--':
            newargs += args[1:]
            break
        if arg.startswith('--'):
            flag, opts, args = do_longs(opts, arg[2:], longopts, args[1:])
            if not flag:
                newargs.append(arg)
        else:
            newargs.append(arg)
            args = args[1:]

    return opts, newargs

def do_longs(opts, opt, longopts, args):
    try:
        i = opt.index('=')
    except ValueError:
        optarg = None
    else:
        opt, optarg = opt[:i], opt[i+1:]

    has_arg, opt = long_has_args(opt, longopts)

    if opt:
        if has_arg:
            if optarg is None:
                if not args:
                    raise ScanoptError('option --%s requires argument' % opt, opt)
                optarg, args = args[0], args[1:]
        elif optarg:
            raise ScanoptError('option --%s must not have an argument' % opt, opt)
        opts.append(('--' + opt, optarg or ''))
        return 1, opts, args
    else:
        return 0, opts, args

# Return:
#   has_arg?
#   full option name (0 if we don't know about this option)
def long_has_args(opt, longopts):
    possibilities = [o for o in longopts if o.startswith(opt)]
    if not possibilities:
        return 0, 0
    if opt in possibilities:
        return 0, opt
    elif opt + '=' in possibilities:
        return 1, opt
    else:
        return 0, 0
