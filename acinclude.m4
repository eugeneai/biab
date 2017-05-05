AC_DEFUN([AC_PYTHON_REQUIRE],
  [AC_MSG_CHECKING([for python >= $1])
   if test ! "$PYTHON"; then AC_ERROR([no python found!]); fi
[PYTHON_VERSION=`$PYTHON -c "
import sys
print sys.version[:3]"`
PYTHON_VERSION_GE=`$PYTHON -c "
import sys
print (sys.version[:3] >= '$1')"`]
if test "$PYTHON_VERSION_GE" = '0'
then AC_ERROR([python $PYTHON_VERSION found])
else AC_MSG_RESULT([python $PYTHON_VERSION])
fi
])

AC_DEFUN([AC_BISON_VERSION], [
AC_MSG_CHECKING([bison version])
[BISON_VERSION=`$BISON --version|sed -e 's/[^0-9.]*//'`]
AC_MSG_RESULT([$BISON_VERSION])
])

AC_DEFUN([AC_DEVELOPER_SANITY], [
AC_MSG_CHECKING([whether developer was sane])
AC_MSG_RESULT([well..continuing anyway])
])
