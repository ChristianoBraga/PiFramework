#!/bin/bash

MAUDE="/Users/cbraga/Applications/Maude-2/maude.darwin64"
IMP_DIR="/Users/cbraga/Dropbox/BPLC/BPLC/examples/imp/"

if [ "$TERM_PROGRAM" = "iTerm.app" ] ;
then
  ./imgcat ./img/imp.jpg
fi
  
if [ "$1" != "" ]; then
   $MAUDE -no-banner $IMP_DIR/imp.maude "$1"
else
   $MAUDE -no-banner $IMP_DIR/imp.maude
fi
