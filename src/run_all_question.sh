#!/bin/bash

while read line 
do
	echo $line | python3 prototype.py 
done < questions.txt
