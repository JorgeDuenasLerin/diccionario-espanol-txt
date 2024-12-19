import time
import argparse
import pickle
import pyuca
import urllib.request

parser = argparse.ArgumentParser(description='RAE Process data.')
parser.add_argument('--inputfile', metavar='outfile no extension', type=str, default="data/raw/allwords")
parser.add_argument('--outputfile', metavar='outputfile', type=str, default="data/allwords")
args = parser.parse_args()

def save_file(lista, file):
    with open(file, 'w') as f:
        for item in lista:
            f.write(item + '\n')


letras = ['a', 'á', 'b', 'c', 'd', 'e', 'é', 'f', 'g', 'h', 'i', 'í', 'j', 'k', 'l', 'm',
             'n', 'ñ', 'o', 'ó', 'p', 'q', 'r', 's', 't', 'u', 'ú', 'ü', 'v', 'w', 'x', 'y', 'z']


collator = pyuca.Collator("src/allkeys.txt")

palabras = []

for l in letras:
    with open(f"{args.inputfile}_{l}.pkl", 'rb') as f:
        words = pickle.load(f)
        keys = words.keys()
        palabras += keys



palabras = sorted(list(set(palabras)), key=collator.sort_key)

#paraborrar = ["(impersonal:", "(solo", ")"]
#for borrar in paraborrar:
#    palabras.remove(borrar)


save_file(palabras, f"{args.outputfile}.txt")

"-", ""

"""




longitudes = {}

for palabra in palabras:
    longitud = len(palabra)
    if longitud in longitudes:
        longitudes[longitud] += palabra
    else:
        longitudes[longitud] = [palabra]

for longitud in longitudes:
    longitudes[longitud] = sorted(longitudes[longitud], key=collator.sort_key)

"""
