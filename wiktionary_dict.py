#!/usr/bin/env python3

import bz2

from lxml import etree


def load_ontology(f):
    tree = etree.parse(f)
    results = tree.xpath('/OntoWiktionary[@lang="en"]/Concept/Lexicalization')

    wiki_dict = {}
    for r in results:
        lemma = r.attrib['lemma']
        pos = r.attrib['pos']
        sense = r.attrib['id'].split(":")[-1]
        if lemma not in wiki_dict:
            wiki_dict[lemma] = {}
        if pos not in wiki_dict[lemma]:
            wiki_dict[lemma][pos] = {}
        wiki_dict[lemma][pos][sense] = r.text
    return wiki_dict


def get_most_likely_definition(definitions, keywords):
    """

    :param definitions: An array of strings containing definitions.
    :param keywords: An array of strings containing the attribute and its adjectives.
    :return: String with first definition in definitions containing a keyword or the first definition.
    """

    # indexing starts at 1
    num_definitions = max(list(map(int, definitions.keys()))) + 1
    for keyword in keywords:
        for i in range(1, num_definitions):
            if definitions[str(i)] and keyword in definitions[str(i)]:
                return definitions[str(i)]
    return definitions["1"]

if __name__ == '__main__':

    wiki = load_ontology(bz2.open('./data/2011-08-01_OntoWiktionary_EN.xml.bz2'))

    while True:
        entry = input("\nEnter [word,POS] (POS must be N, A, V, or R) (EXIT to break): ")
        if entry == 'EXIT':
            break
        else:
            try:
                word = entry.split(",")[0]
                pos = entry.split(",")[1]
                if pos != "N" and pos != "A" and pos != "V" and pos != "R":
                    print("pos should be N, A, V, or R. Given:", pos)
                else:
                    try:
                        res = wiki[word][pos]["1"]
                        print(word + ":", res)
                    except KeyError:
                        print("entry not found")
            except IndexError:
                print("Invalid input:", entry)
