dnl Process this file with autoconf to produce a configure script.

AC_CONFIG_MACRO_DIRS([m4])

AC_INIT(configure.ac)
AC_CANONICAL_HOST

AM_PROG_LIBTOOL

AM_INIT_AUTOMAKE(biab, 0.1.0)

AC_PROG_INSTALL
AC_PROG_MAKE_SET

AC_PATH_PROG(PYTHON, python)
AC_PYTHON_REQUIRE(2.0)

AC_PATH_PROG(BISON, bison)

if test ! "$BISON"
then AC_ERROR([biab requires bison])
fi

BIAB_BISON_VERSION=1.28
AC_BISON_VERSION

if test "$BISON_VERSION" != "$BIAB_BISON_VERSION"
then AC_MSG_WARN([biab is only known to work with bison $BIAB_BISON_VERSION, which $BISON is not])
fi

AC_OUTPUT(Makefile setup.py biab.sh biab/parse.py)
