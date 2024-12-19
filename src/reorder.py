import time
import argparse
import pickle
import pyuca
import urllib.request

collator = pyuca.Collator("src/allkeys.txt")

palabras = []

with open("data/0_palabras_todas.txt", 'r') as f:
    for line in f:
        palabras.append (line.strip())

palabras = sorted(list(set(palabras)), key=collator.sort_key)

with open("data/0_palabras_todas_sorted.txt", 'w') as f:
    for palabra in palabras:
        f.write(palabra + '\n')
