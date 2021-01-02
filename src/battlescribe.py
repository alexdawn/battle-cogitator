import requests
from itertools import chain
from collections import namedtuple
import logging
import os
from copy import deepcopy
from io import StringIO

from lxml import etree
from pprint import pprint
from IPython.core.display import display, HTML

CURR_DIR = os.getcwd()
URL = 'https://api.github.com/repos/BSData/wh40k/contents/'
CONTENT_URL = 'https://raw.githubusercontent.com/BSData/wh40k/master/'
GAME_SCHEMA = os.path.join(CURR_DIR, 'notebooks/battlescribe/game_schema.xsd')
CAT_SCHEMA = os.path.join(CURR_DIR, 'notebooks/battlescribe/catelogue_schema.xsd')
CACHE = os.path.join(CURR_DIR, 'notebooks/battlescribe/cache')


def get_cache_if_possible(filename):
    """Try and load filename from CACHE path, otherwise load from CONTENT_URL"""
    pathname = os.path.join(CACHE, filename)
    if not os.path.isfile(pathname):
        path = CONTENT_URL + filename
        text = requests.get(path).content
        if not os.path.exists(CACHE):
            os.makedirs(CACHE)
        with open(pathname, 'wb') as f:
            f.write(text)
    else:
        with open(pathname, 'rb') as f:
            text = f.read()
    return text


def convert_catalogue(catalogue):
    name, ext = catalogue.split(".")
    if ext == 'cat':
        print(name)
        path = os.path.join(CONTENT_URL, catalogue)
        r = requests.get(path)
        cat = etree.fromstring(
            get_cache_if_possible(catalogue),
            etree.XMLParser(
                remove_blank_text=True, schema = catelogue_schema
            )
        )
        # warn about cat links at the moment do nothing about them
        link = cat.xpath("//cat:catalogueLink", namespaces=namespaces)
        for x in link:
            logging.warning("{} has catalogue Link to {}".format(
                name, x.xpath('@name')
                ))
        # merge main cat into gst, TODO do for all the needed links
        base_copy = deepcopy(base)
        for x in cat:
            base_copy.append(x)
        # escape things which are not valid json (done here as not so easy in XSLT 1.0)
        for x in base_copy.xpath(
            "//cat:*|//gc:*", namespaces=namespaces):
            if x.text:
                x.text = x.text.replace('\\', '\\\\').replace('"', '\\"').replace('\r', '\\r').replace('\n', '\\n')
        with open(os.path.join(CURR_DIR, "./notebooks/battlescribe/catelogue to_json.xslt"), "r") as f:
            xslt_root = etree.XML(f.read())
        transform = etree.XSLT(xslt_root)
        result_tree = transform(base_copy)
        with open(os.path.join(CURR_DIR, "./notebooks/battlescribe/outputs/{}.json".format(name)), "w") as f:
            f.write(str(result_tree))


if __name__ == '__main__':
    files = requests.get(URL).json()

    catalogues = []
    for file in files:
        if file['type'] == 'file' and file['name'][0] != '.':
            catalogues.append(file['name'])

    with open(GAME_SCHEMA, 'rb') as fh:
        game_schema = etree.XMLSchema(etree.fromstring(fh.read()))
    with open(CAT_SCHEMA, 'rb') as fh:
        catelogue_schema = etree.XMLSchema(etree.fromstring(fh.read()))

    base = etree.fromstring(
        get_cache_if_possible('Warhammer 40,000.gst'),
        etree.XMLParser(
            remove_blank_text=True, schema = game_schema
        )
    )

    namespaces = {
        'gc': 'http://www.battlescribe.net/schema/gameSystemSchema',
        'cat': 'http://www.battlescribe.net/schema/catalogueSchema'
    }

    if not os.path.exists(os.path.join(CURR_DIR, './notebooks/battlescribe/outputs')):
        os.mkdir(os.path.join(CURR_DIR, './notebooks/battlescribe/outputs'))

for catalogue in catalogues:
    convert_catalogue(catalogue)
# a very lazy multicore implementation, lxml is pretty processor heavy
# from multiprocessing import Pool
# pool = Pool()
# pool.map(convert_catalogue, catalogues)
# pool.close()
# pool.join()
