#!/bin/sh

aclocal
libtoolize -f

AUTOMAKE_DIRECTORIES=.

rm -f config.cache
autoconf
