#!/bin/bash
for i in examples/*.imp2 ; do echo === ; echo $i ; echo ===; python3 imp2.py -f $i --last 2 -s --out ; done
