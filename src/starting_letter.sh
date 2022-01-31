#!/bin/bash

# By: @hasecilu, some lines were extracted from spliter.sh file

if [ ${PWD##*/} = "diccionario-espanol-txt" ]
then
	mkdir -pv starting_letter
	LETRAS=('a' 'b' 'c' 'd' 'e' 'f' 'g' 'h' 'i' 'j' 'k' 'l' 'm' 'n' 'ñ' 'o' 'p' 'q' 'r' 's' 't' 'u' 'v' 'w' 'x' 'y' 'z')

	for l in "${LETRAS[@]}"; do
		cat 0_palabras_todas.txt | grep ^$l > starting_letter/$l.txt
	done

	wc -l starting_letter/*
else
	echo "Go to the diccionario-espanol-txt folder"
fi

