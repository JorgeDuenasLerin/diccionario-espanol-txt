# List of all spanish words. Source RAE

Work explained here:
https://duenaslerin.com/diccionario-palabras-espanol-en-texto-script/


Updated with RAE server in: 2022-05-11

## Run

Download all data from RAE

```
python3 src/rae_downloader.py
```

It generates the file ```data/palabras_todas.txt```

Split in diferent files
```
bash src/spliter.sh
```

Usage
```
usage: rae_downloader.py [-h] [--conjugaciones] [--skip-conjugaciones]

RAE Downloader.

optional arguments:
  -h, --help            show this help message and exit
  --conjugaciones
  --skip-conjugaciones
```

### Classify words by their length

The `0_palabras_todas.txt` file is needed.

Inside the `diccionario-espanol-txt` folder and running the `length.sh` file will create the `length` folder with the words classified by its length.

```
bash src/length.sh
```

### Classify words by their first letter

The `0_palabras_todas.txt` file is needed.


Due to the lack of `palabras_todas.txt` file (creating it will last so many hours) the `spliter.sh` file will not work. So this script works with the `0_palabras_todas.txt` file.

Inside the `diccionario-espanol-txt` folder and running the `starting_letter.sh` file will create the `starting_letter` folder with the words classified by the first letter.

```
bash src/starting_letter.sh
```


## Conjugaciones

primera: ababillarse
Dicho de un animal: Enfermar de la babilla.

última:
