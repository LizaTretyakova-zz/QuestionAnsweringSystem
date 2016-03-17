#!/bin/bash

while read line 
do
	echo $line | python prototype.py 
done < questions.txt
