#                                                            -*- Python -*-
#    prof  -  a line-oriented profiler
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
#
# NB: the last line executed in the run isn not counted
#   however, doing so would probably hurt accuracy rather than help it
# nice headers
# nice formatting
# extension module for _tracer
# dist

import sys as _sys
import time as _time

class _tracer:
  def __init__(self):
    self.counts = {}
    self.lastline = None
    
  def tb(self, f, t, a):
    #print f, t, a
    tm = _time.time()
    if t == 'line':
      file = f.f_code.co_filename
      func = f.f_code.co_name
      line = f.f_lineno
      if self.lastline:
        dt = tm - self.lasttime
        k = (self.lastfile, self.lastfunc, self.lastline)
        c = self.counts.setdefault(k, 0)
        self.counts[k] += dt
      self.lastfile = file
      self.lastfunc = func
      self.lastline = line
    self.lasttime = _time.time()
    return self.tb

class prof:
  def __init__(self):
    self.funcs = None
    self.total = None

  def run(self, code):
    import __main__
    dict = __main__.__dict__
    self.runctx(code, dict, dict)

  def runctx(self, code, gs, ls):
    tb = _tracer()
    self.oldtrace = _sys.settrace(tb.tb)
    exec(code, gs, ls)
    _sys.settrace(self.oldtrace)
    self.counts = tb.counts

  def __item2str(self, i):
    pt = 100.0 * i[1] / self.total
    pf = 100.0 * i[1] / self.funcs[self.__fkey(i)]
    return "\"%s\", line %d: %s()  %g  %.2f%%  %.2f%%" \
           % (i[0][0], i[0][2], i[0][1], i[1], pf, pt)

  def __fkey(self, i):
    return i[0][0] + ':' + i[0][1] + '()'

  def __init_stats(self):
    if self.funcs == None:
      self.funcs = {}
      self.total = 0
      items = self.counts.items()
      for i in items:
        self.total += i[1]
        fkey = self.__fkey(i)
        v = self.funcs.setdefault(fkey, 0)
        self.funcs[fkey] += i[1]

  def cmp(self, a, b):
    d = b[1] - a[1]
    if d < 0: return -1
    elif d == 0: return 0
    else: return 1

  def line_report(self, n=20):
    print self.line_report_str()

  def line_report_str(self, n=20):
    self.__init_stats()

    s = ''
    s += "total time = %g\n\n" % (self.total,)

    items = self.counts.items()
    items.sort(self.cmp)
    i = 0
    for it in items:
      if i == n: break
      s += self.__item2str(it) + "\n"
      i += 1
    return s

  def func_report(self, n=20):
    print self.func_report_str()

  def func_report_str(self, n=20):
    self.__init_stats()

    s = ''
    s += "total time = %g\n\n" % (self.total,)

    items = self.funcs.items()
    items.sort(self.cmp)
    i = 0
    for it in items:
      if i == n: break
      pt = 100.0 * it[1] / self.total
      s += "%s  %g  %.2f%%\n" % (it[0], it[1], pt)
      i += 1
    return s
    
if __name__ == '__main__':
  def bar(n):
    while n > 0:
      n -= 1

  p = prof()
  p.run("bar(10000)")
  p.line_report()
  p.func_report()
