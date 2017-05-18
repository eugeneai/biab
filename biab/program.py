#                                                            -*- Python -*-
#    program  -  a generic program framework
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

# TODO
# test exit
# make profiling handle exit
# parameterize error output stream more
# handle usage and help
# report verbosity/quiet conflicts
# handle rc/environment/option values

import sys as _sys
from . import scanopt as _scanopt
import profile as _profile
from . import prof as _prof


class _myprofile(_profile.Profile):
    """
    A variant of profile.Profile whose run() method takes global and
    local dict arguments.
    """

    def __init__(self):
        _profile.Profile.__init__(self)

    def run(self, cmd, globals, locals):
        """
        run(cmd, globals, locals)
        Just like profile.Profile.run() except it takes global and
        local dict arguments as well.
        """
        return self.runctx(cmd, globals, locals)


class _Exit(Exception):
    def __init__(self, rc):
        Exception.__init__(self, rc)
        self.rc = rc

    def __int__(self):
        return self.rc


class program:
    def __init__(self):
        self.profilep = 0
        self.profp = 0
        self.debug = 0
        self.verbosity = 1
        self.stderr = _sys.stderr

    def carp(self, msg):
        self.stderr.write(msg)
        self.stderr.flush()

    def info(self, msg):
        self.stderr.write(msg)
        self.stderr.flush()

    def exit(self, rc):
        raise _Exit(rc)

    def die(self, msg):
        self.stderr.write(msg)
        self.stderr.flush()

        self.exit(1)

    def open(self, file, mode='r'):
        try:
            return open(file, mode)
        except IOError as e:
            self.die("Problem %s `%s': %s\n"
                     % ((mode == 'r' and 'reading' or 'writing'),
                        file, e))

    def run(self, args=None):
        if args is None:
            args = _sys.argv
        self.name = args[0]
        # print args

        opts, args = _scanopt.scanopt(_sys.argv[1:],
                                      [
            'prof',
            'profile',
            'debug=',
            'verbosity=',
            'quiet=',
        ])

        for opt, val in opts:
            if opt == '--profile':
                self.profilep = 1
            if opt == '--prof':
                self.profp = 1
            elif opt == '--debug':
                self.debug = int(val)
            elif opt == '--verbosity':
                self.verbosity = int(val)
            elif opt == '--quiet':
                self.verbosity = 0

        # this is a cell instead of a simple variable so we can get a
        # value in it during profiling (the dict returned by locals
        # does not contain our actual mutable local bindings)
        rc = [0]

        try:
            if self.profilep:
                statsfile = self.name + 'stats'
                pr = _myprofile()
                pr = pr.run('rc[0] = self.main(args)', globals(), locals())
                pr.dump_stats(statsfile)
                import pstats
                p = pstats.Stats(statsfile)
                p.sort_stats('cumulative').print_stats(20)
                p.sort_stats('time').print_stats(20)
            elif self.profp:
                p = _prof.prof()
                p.runctx('rc[0] = self.main(args)', globals(), locals())
                p.line_report()
                p.func_report()
            else:
                rc[0] = self.main(args)
        except _Exit as e:
            rc[0] = int(e)

        if rc[0] is None:
            rc[0] = 0

        _sys.exit(rc[0])


if __name__ == '__main__':
    class myprog(program):
        def __init__(self):
            program.__init__(self)
            self.name = 'myprog'

        def main(self, args):
            print(args)
            return 23

    p = myprog()
    p.run()
