import time
import argparse
import pickle

from lxml import etree
from urllib.parse   import quote
from urllib.request import Request, urlopen

"""
Cabeceras para la simulación de un navegador
"""
UA="Mozilla/5.0 (Windows NT 6.1; Win64; x64; rv:47.0) Gecko/20100101 Firefox/47.0"
url_list="https://dle.rae.es/{}/?m=31"
url_detail="https://dle.rae.es/{}"

"""
Usamos title por que el contenido en determinadas situaciones cambia:
https://dle.rae.es/abollado?m=31

<a data-cat="FETCH" data-acc="LISTA EMPIEZA POR" data-eti="abollado" title="Ir a la entrada abollado, abollada" href="/abollado">abollado<sup>1</sup>, da</a>
<a data-cat="FETCH" data-acc="LISTA EMPIEZA POR" data-eti="abollado" title="Ir a la entrada abollado" href="/abollado#07jAWsp">abollado<sup>2</sup></a>

"""
to_remove_from_title='Ir a la entrada '

skip = len(to_remove_from_title)


def get_xtree(url, param):
    tree = None
    attempt = 10
    while attempt > 0 and tree == None:
        try:
            req = Request(url.format(quote(param)), headers={'User-Agent': UA})
            webpage = urlopen(req, timeout=2)  # Set the timeout value to 10 seconds
            htmlparser = etree.HTMLParser()
            tree = etree.parse(webpage, htmlparser)
        except Exception as e:
            attempt -= 1
            print(str(e))
            time.sleep(10)

    return tree


def try_conjugacion(palabra, dict_dump):
    print("Intentamos conjugar " + palabra)
    tree = get_xtree(url_detail, palabra)
    contains_conjugacion = tree.xpath('//*[@id="resultados"]/*/a[@class="e2"]/@title')
    if len(contains_conjugacion) > 0:
        print("^" * 80)
        print(contains_conjugacion)
        # get all contant in tds
        conjugacion = tree.xpath('//div[@id="conjugacion"]//td//text()')
        conjugacion_clean = ' '.join(conjugacion).replace(', ', ' ').replace(' / ', ' ').split(' ')
        for conj in conjugacion_clean:
            if(conj!=''):
                print(conj)
                dict_dump[conj] = conj


def try_me_siento_con_suerte(palabra, dict_dump):
    # RAE por ejemplo al buscar si, devuelve psicolo, psiblabla, etc...
    # esta función prueba la cadena de caracteres en la url, la mayoría dará no pero alguna dará sí. Por ejemplo sí.
    # Ahora mismo sí, sí que aparece por la inclusión de las tildes en el lista inicial.
    # pero puede haber situaciones de palabras que no estén en la lista de resultado de búsqueda y que sean palabras.
    print("Intentamos suerte " + palabra)
    tree = get_xtree(url_detail, palabra)
    posible_palabra = tree.xpath('//*[@id="resultados"]/article/header/@title')
    print(posible_palabra)
    if len(posible_palabra) > 0:
        print("Aceptamos:" + palabra)
        dict_dump[palabra] = palabra
    else:
        print("Denegamos:" + palabra)


"""
Revisar bien con las reglas de https://www.rae.es/dpd/plural
"""
def formar_plural(palabra):
    plurales = []
    
    # Si la palabra termina en vocal átona o en -e tónica
    if palabra[-1] in ['a', 'e', 'i', 'o', 'u']:
        plurales.append(palabra + 's')
    
    # Si la palabra termina en -a o -o tónicas
    elif palabra[-1] in ['á', 'ó']:
        if palabra not in ['faralá', 'albalá', 'no']:
            plurales.append(palabra + 's')
        else:
            plurales.append(palabra + 'es')
    
    # Si la palabra termina en -i o -u tónicas
    elif palabra[-1] in ['í', 'ú']:
        plurales.append(palabra + 's')
        plurales.append(palabra + 'es')
    
    # Si la palabra termina en -y precedida de vocal
    elif palabra[-1] == 'y' and len(palabra)>1 and palabra[-2] in ['a', 'e', 'i', 'o', 'u']:
        plurales.append(palabra[:-1] + 'es')
        if palabra in ['gay', 'jersey', 'espray', 'yóquey']:
            plurales.append(palabra[:-1] + 's')
    
    # Si la palabra termina en -s o -x
    elif palabra[-1] in ['s', 'x']:
        if palabra[-2:] in ['ás', 'és', 'ís', 'ós', 'ús'] or palabra[-1] == 'x':
            plurales.append(palabra + 'es')
        else:
            plurales.append(palabra)  # invariable
    
    # Si la palabra termina en -l, -r, -n, -d, -z, -j
    elif palabra[-1] in ['l', 'r', 'n', 'd', 'z', 'j']:
        plurales.append(palabra + 'es')
    
    # Si la palabra termina en consonantes distintas de las anteriores
    elif palabra[-1] not in ['l', 'r', 'n', 'd', 'z', 'j', 's', 'x']:
        plurales.append(palabra + 's')
    
    return plurales

# Ejemplo de uso:
# palabra = "sofá"
# print(f"Formas posibles del plural de '{palabra}': {formar_plural(palabra)}")


def try_plural(palabra, dict_dump):
    print("Intentamos plural " + palabra)
    plural = formar_plural(palabra)
    for pl in plural:
        tree = get_xtree(url_detail, pl)
        posible_plural = tree.xpath('//*[@id="resultados"]/div[@class="otras"]/p/text()')
        if len(posible_plural) > 0 and pl in posible_plural[0]:
            print("Aceptamos:" + pl)
            dict_dump[pl] = pl
        else:
            # Puede ser una palabra: a -> plural as, es una palabra.
            # Aquí la denegamos. La recogeremos como palabra en otra parte del script
            print("Denegamos:" + pl)