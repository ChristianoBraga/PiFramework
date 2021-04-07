#!/bin/bash
if [ $# -eq 0 ]
then
    echo "Use: test.sh n" ;
    echo "Parameter n is the number of the state to be printed, counting backwards." ;
    exit 1 ;
fi
for i in examples/*.imp2 ; do
    echo === ;
    echo $i ;
    echo ===;
    python3 imp2.py -f $i --last $1 -s --out ;
done
