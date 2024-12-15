#!/bin/bash

declare -i i=0
while [[ $((i)) -le 10000 ]]; do
	python solution2.py $i
	i=$((i+1))
done
