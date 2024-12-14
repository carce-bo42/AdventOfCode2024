#!/bin/bash

declare -i i=0
while [[ $((i)) -le 100000 ]]; do
	python solution2.py $i
	i=$((i+1))
	echo "processing $i seconds" 
done
