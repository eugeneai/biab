from biab.main import biab
import os
import os.path
import importlib
import sys

biab = biab()
DIR = os.path.join(os.getcwd(), "tests")


def example(filename):
    return os.path.abspath(os.path.join(DIR, filename))


class TestBasic(object):

    def setUp(self):
        pass

    def test_C(self):
        ex1 = example("ANSI-C-grammar.bb")
        biab.process(ex1)
        if not DIR in sys.path:
            sys.path.append(DIR)
        mod = importlib.import_module("ANSI-C-grammar")
        assert mod
