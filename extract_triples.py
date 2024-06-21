# -*- coding: utf-8 -*-

import re
import json
import conceptnet_lite

conceptnet_lite.connect('./conceptnet.db')  # 指定path にdbがあるか確認．なければnetからDLし, build

from conceptnet_lite import Language

ja_pattern = re.compile(r'^[ぁ-んァ-ヶーｱ-ﾝﾞﾟ一-龠]*$')   # 長音ー含む

def get_concept_in_out_ja(c):
    """[Ja]個別 conceptに対して, in, outを個別に取得
    Args:
        c: concept
    """
    tuples = []
    if c.edges_out:
        # print(f"Edges out:")
        for e in c.edges_out:
            if re.search(ja_pattern, e.end.text):
                # print(f"[{e.__dict__}] -> r: {e.relation.name} {e.end.text}")   # detail
                # print(f"-> r: {e.relation.name} {e.end.text}")  # simple
                _etc_d = e.etc
                # print(f'e.etc {_etc_d}')
                etc_d = {'dataset': _etc_d.get('dataset', ''), 'license': _etc_d.get('license',''), 'weight': _etc_d.get('weight', '')}
                tuples.append((e.start.text, e.relation.name, e.end.text, etc_d))
            else:
                # print(f"xxx -> r: {e.relation.name} {e.end.text}")
                continue

    if c.edges_in:
        # print(f"Edges in:")
        for e in c.edges_in:
            if re.search(ja_pattern, e.start.text):
                # print(f"[{e.__dict__}] {e.start.text} r: {e.relation.name} ->")   # detail
                # print(f'{e.start.text} r: {e.relation.name} ->')    # simple
                _etc_d = e.etc
                # print(f'e.etc {_etc_d}')
                etc_d = {'dataset': _etc_d.get('dataset', ''), 'license': _etc_d.get('license',''), 'weight': _etc_d.get('weight', '')}
                tuples.append((e.start.text, e.relation.name, e.end.text, etc_d))
            else:
                # print(f"xxx {e.start.text} r: {e.relation.name} ->")
                continue
    return tuples

def get_concept_in_out_en(c):
    """[En]個別 conceptに対して, in, outを個別に取得"""
    tuples = []
    if c.edges_out:
        # print(f"Edges out:")
        for e in c.edges_out:
            # print(f"[{e.__dict__}] -> r: {e.relation.name} {e.end.text}")   # detail
            # print(f"-> r: {e.relation.name} {e.end.text}")  # simple
            _etc_d = e.etc
            # print(f'e.etc {_etc_d}')
            etc_d = {'dataset': _etc_d.get('dataset', ''), 'license': _etc_d.get('license',''), 'weight': _etc_d.get('weight', '')}
            tuples.append((e.start.text, e.relation.name, e.end.text, etc_d))

    if c.edges_in:
        # print(f"Edges in:")
        for e in c.edges_in:
            # print(f"[{e.__dict__}] {e.start.text} r: {e.relation.name} ->")   # detail
            # print(f'{e.start.text} r: {e.relation.name} ->')    # simple
            _etc_d = e.etc
            # print(f'e.etc {_etc_d}')
            etc_d = {'dataset': _etc_d.get('dataset', ''), 'license': _etc_d.get('license',''), 'weight': _etc_d.get('weight', '')}
            tuples.append((e.start.text, e.relation.name, e.end.text, etc_d))

    return tuples


def get_all_triples(lang='ja'):
    """
    triples (list[(list)]) : [ (start(str), relation(str), end(str), etc(dict: {'dataset', 'license', 'weight'}))]
    """
    triples = []
    langdata = Language.get(name=lang)
    print(f'langdata len: {len(langdata.labels)}')
    for i, l in enumerate(langdata.labels):       
        if i % 1000 == 0:
            print(f"{i} / {len(langdata.labels)}")
        _c_triples = []  # concepts triples
        for c in l.concepts:
            if lang == 'ja':
                _c_triples.extend(get_concept_in_out_ja(c))
            elif lang == 'en':
                _c_triples.extend(get_concept_in_out_en(c))
            else:
                print(f'TODO: lang {lang} not supported.')
                exit()
        triples.extend(_c_triples)
        # print(f'{_c_triples}')    # debug
        # if i == 2000:   # for TEST
            # return triples
    
    return triples


def rm_duplicates(triples):
    """tripleの重複なしリスト (start-relation-end) をkeyにして重複を除去"""
    clean_tripples = []
    s_r_e = set()   
    for t in triples:
        sre = (t['start'], t['relation'], t['end'])
        if sre not in s_r_e:
            clean_tripples.append(t)
            s_r_e.add(sre)

    return clean_tripples


def main_get_all_triples():
    """conceptnetから指定言語の全てのtriplesを取得し, jsonlで出力する
    Returns:
        all_triples.jsonl: {'start', 'relation', 'end', 'dataset', 'license', 'weight'}"""
    # lang = 'ja'
    lang = 'en'
    all_triples = get_all_triples(lang=lang)
    print(f"all_triples len: {len(all_triples)}")
    print(f'outputting all_triples.jsonl')
    with open('_all_triples.jsonl', 'w') as f:
        for i, t in enumerate(all_triples):
            if i % 1000 == 0:
                print(f"{i} / {len(all_triples)}")
            d = {'start': t[0], 'relation': t[1], 'end': t[2]}
            d.update(t[3])
            d_str = json.dumps(d, ensure_ascii=False)
            f.write(f'{d_str}\n')

def main_get_deduplicated_triples():
    """main_get_all_triples()で取得したトリプルから，トリプルの重複を除去"""
    # read jsonl
    tripleDict_list = []
    with open('_all_triples.jsonl', 'r') as f:
        for line in f:
            d = json.loads(line)
            tripleDict_list.append(d)
    print(f'read tripleDict_list len: {len(tripleDict_list)}')

    # deduplicate
    dedup_tripleDict_list = rm_duplicates(tripleDict_list)
    
    # output jsonl
    print(f'outputting dedup_triples.jsonl len: {len(dedup_tripleDict_list)} ({(len(dedup_tripleDict_list)/len(tripleDict_list)):.3f} % of original)')
    with open('triples.jsonl', 'w') as f:
        for i, d in enumerate(dedup_tripleDict_list):
            if i % 1000 == 0:
                print(f"{i} / {len(dedup_tripleDict_list)}")
            d_str = json.dumps(d, ensure_ascii=False)
            f.write(f'{d_str}\n')

if __name__ == "__main__":
    main_get_all_triples()    # step1
    # main_get_deduplicated_triples() # step2