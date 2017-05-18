from biab.main import biab
import os
import os.path
import importlib
import sys

biab = biab()
DIR = os.path.join(os.getcwd(), "tests")


def example(filename):
    return os.path.abspath(os.path.join(DIR, filename))


def bcompile(modulename):
    ex = modulename + ".bb"
    ex = example(ex)
    biab.process(ex)
    if DIR not in sys.path:
        sys.path.append(DIR)
    return importlib.import_module(modulename)


class TestBasic(object):

    def setUp(self):
        pass

    def test_C(self):
        rc = bcompile("ANSI-C-grammar")
        assert rc
