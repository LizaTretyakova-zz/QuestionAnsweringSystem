#!/bin/bash

while read line 
do
	echo $line | python3 prototip.py 
done < questions.txt
