import requests
from itertools import chain
from functools import partial
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

namespaces = {
    'gc': 'http://www.battlescribe.net/schema/gameSystemSchema',
    'cat': 'http://www.battlescribe.net/schema/catalogueSchema'
}


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


def escape_to_safe_json(x):
    """Because XSLT has limited replacement functions, it is done here in python first"""
    return x.replace('\\', '\\\\').replace('"', '\\"').replace('\r', '\\r').replace('\n', '\\n')


def load_cat_file_to_dom(catalogue):
    return etree.fromstring(
            get_cache_if_possible(catalogue),
            etree.XMLParser(
                remove_blank_text=True, schema = catelogue_schema
            )
        )

def convert_catalogue(game_system, catalogue):
    name, ext = catalogue.split(".")
    if ext == 'cat':
        print(name)
        path = os.path.join(CONTENT_URL, catalogue)
        r = requests.get(path)
        cat = load_cat_file_to_dom(catalogue)

        # Catalogues can link to other catalogues
        extra_cats = {}
        for x in cat.xpath("//cat:catalogueLink", namespaces=namespaces):
            assert x.attrib['type'] == 'catalogue', "Catalogue link has type which is not a catalogue {}".format(x.attrib)
            extra_cats[x.attrib['name']] = {
                'dom': load_cat_file_to_dom(x.attrib['name'] + '.cat'),
                'import_root': True if x.attrib['importRootEntries'] == 'true' else False
            }

        # merge main cat into gst, not certain but I think import root entries
        # is to mark if to import selection Entries or not
        base_copy = deepcopy(game_system)
        for x in cat:
            base_copy.append(x)
        for cat_name, c in extra_cats.items():
            print("Adding {} to DOM".format(cat_name))
            for x in c['dom']:
                if c['import_root'] or x.tag.split('}')[1] != 'entryLinks':
                    base_copy.append(x)
                else:
                    print("didn't copy entryLinks")
        # escape things which are not valid json (done here as not so easy in XSLT 1.0)
        for x in base_copy.xpath(
            "//cat:*|//gc:*", namespaces=namespaces):
            if x.text:
                x.text = escape_to_safe_json(x.text)
            for k, v in x.attrib.items():
                x.attrib[k] = escape_to_safe_json(v)
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

    base_game = etree.fromstring(
        get_cache_if_possible('Warhammer 40,000.gst'),
        etree.XMLParser(remove_blank_text=True, schema=game_schema)
    )

    if not os.path.exists(os.path.join(CURR_DIR, './notebooks/battlescribe/outputs')):
        os.mkdir(os.path.join(CURR_DIR, './notebooks/battlescribe/outputs'))

    for catalogue in catalogues:
        convert_catalogue(base_game, catalogue)
    # a very lazy multicore implementation, lxml is pretty processor heavy
    # from multiprocessing import Pool
    # pool = Pool()
    # pool.map(partial(convert_catalogue, base_game), catalogues)
    # pool.close()
    # pool.join()
