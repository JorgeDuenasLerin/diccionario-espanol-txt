#!/bin/bash

# By: @hasecilu

if [ ${PWD##*/} = "diccionario-espanol-txt" ]
then
	mkdir -pv length

	FILENAME="0_palabras_todas.txt"
	LINES=$(cat $FILENAME)

	COUNTER=0

	for LINE in $LINES
	do
		if [ ${#LINE} -lt 10 ]
		then
			echo $LINE >> ./length/0${#LINE}.txt
		else
			echo $LINE >> ./length/${#LINE}.txt		# time:    7.01s user    2.54s system  99% cpu     9.595 total
			# echo $LINE | tee -a ./length/${#LINE}.txt	# time: 1263.37s user 3400.90s system 131% cpu 58:60.00  total
		fi
		
		COUNTER=$((COUNTER+1))
	done
	
	wc -l ./length/*
else
	echo "Go to the diccioanrio-espanol-folder"
fi

