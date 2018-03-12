#!/bin/bash
MAUDE=/Users/cbraga/Applications/Maude-2/maude.darwin64
IMP_DIR=/Users/cbraga/Dropbox/BPLC/examples/imp
if [ "$TERM_PROGRAM" = "iTerm.app" ] ;
then
  ./imgcat ./img/imp.jpg
fi
while [ "$1" != "" ]; do
  $MAUDE -no-banner $IMP_DIR/maude/imp.maude "$1"
  shift
done
