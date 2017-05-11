__all__ = ["biab", "parse", "lex", "token", "ast"]


def main():
    from biab.main import biab
    import sys
    return biab().run(sys.argv)
