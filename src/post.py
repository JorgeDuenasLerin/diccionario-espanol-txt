import time
import argparse
import pickle
import pyuca
import urllib.request

parser = argparse.ArgumentParser(description='RAE Process data.')
parser.add_argument('--inputfile', metavar='outfile no extension', type=str, default="data/allwords")
parser.add_argument('--outputfile', metavar='outputfile', type=str, default="data/allwords.txt")
args = parser.parse_args()


letras = ['a', 'á', 'b', 'c', 'd', 'e', 'é', 'f', 'g', 'h', 'i', 'í', 'j', 'k', 'l', 'm',
             'n', 'ñ', 'o', 'ó', 'p', 'q', 'r', 's', 't', 'u', 'ú', 'ü', 'v', 'w', 'x', 'y', 'z']

collator = pyuca.Collator()


palabras = []

for l in letras:
    with open(f"{args.inputfile}_{l}.pkl", 'rb') as f:
        words = pickle.load(f)
        keys = words.keys()
        palabras += keys


palabras = sorted(list(set(palabras)), key=collator.getSortKey)


with open(args.outputfile, 'w') as f:
    for palabra in palabras:
        f.write(palabra + '\n')



