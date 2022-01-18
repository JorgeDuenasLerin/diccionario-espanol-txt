#ª/bin/bash

LETRAS=('a' 'b' 'c' 'd' 'e' 'f' 'g' 'h' 'i' 'j' 'k' 'l' 'm' 'n' 'ñ' 'o' 'p' 'q' 'r' 's' 't' 'u' 'v' 'w' 'x' 'y' 'z')

cat palabras_todas.txt | grep -v '.*-$' | grep -v ^- | sort | uniq > 0_palabras_todas.txt
cat palabras_todas.txt | grep '.*-$' | sort | uniq > 0_prefijos.txt
cat palabras_todas.txt | grep ^- | sort | uniq > 0_subfijos.txt
rm palabras_todas.txt

for l in "${LETRAS[@]}"; do
  cat 0_palabras_todas.txt | grep ^$l > palabras_$l.txt
done
