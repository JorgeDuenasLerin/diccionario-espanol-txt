#!/usr/bin/env python3

# Desarrollado por Jorge Dueñas Lerín

from urllib.parse   import quote
from urllib.request import Request, urlopen
from lxml import etree

import time
import argparse
import pickle

from helpers import get_xtree, try_conjugacion, try_plural, try_me_siento_con_suerte, url_list, skip


parser = argparse.ArgumentParser(description='RAE Downloader.')
parser.add_argument('--ix', metavar='ix', type=int, required=True, help='Start with this letter index')
parser.add_argument('--conjugaciones', action='store_true')
parser.add_argument('--skip-conjugaciones', dest='conjugaciones', action='store_false')
parser.set_defaults(conjugaciones=True)
parser.add_argument('--plurals', default=True)
parser.add_argument('--outfile', metavar='outfile no extension', type=str, default="data/allwords")
args = parser.parse_args()


letras = ['a', 'á', 'b', 'c', 'd', 'e', 'é', 'f', 'g', 'h', 'i', 'í', 'j', 'k', 'l', 'm',
             'n', 'ñ', 'o', 'ó', 'p', 'q', 'r', 's', 't', 'u', 'ú', 'ü', 'v', 'w', 'x', 'y', 'z']
#letras = ['s', 'i', 'í']
letras_count = len(letras)
start = letras[args.ix]
print(f"Running with {args.ix}/{letras_count}: {start}")
start_with = [start]
dict_dump = {}


while len(start_with) != 0:
    palabra_start_with = start_with.pop(0)
    
    if(palabra_start_with in ['app', 'docs', 'js']): # RAE servers do not like this
        continue
    
    try_me_siento_con_suerte(palabra_start_with, dict_dump)

    tree = get_xtree(url_list, palabra_start_with)
    res = tree.xpath('//*[@id="resultados"]/*/div[@class="n1"]/a/@title')

    # Se repiten palabras. Cuando por ejemplo aba tiene más de 30 y se exapande
    # abaa, abab, etc... las primeras palabras no aparecen: aba
    for pal in res:
        pal_clean = pal[skip:]
        pal_list = []

        if ", " not in pal_clean:
            pal_list.append(pal_clean)
        else:
            pal_clean = pal_clean.split(", ")
            for pal_clean_multi in pal_clean:
                pal_list.append(pal_clean_multi)
        
        for pal_ix in pal_list:
            print(pal_ix)
            dict_dump[pal_ix] = pal_ix
            if args.conjugaciones:
                try_conjugacion(pal_ix, dict_dump)
            # try_plural(pal_ix, dict_dump)
            
    

    if(len(res)>30):
        print("!" * 80)
        print("EXAPEND: " + palabra_start_with)
        expand = [palabra_start_with + l for l in letras]
        start_with = expand + start_with


pickle.dump(dict_dump, open(f"{args.outfile}_{start}.pkl", "wb"))
