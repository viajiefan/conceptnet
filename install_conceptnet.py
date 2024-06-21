# -*- coding: utf-8 -*-

import re
import conceptnet_lite

# 指定path にdbがあるか確認．なければnetからDLし, build
conceptnet_lite.connect('./conceptnet.db')

from conceptnet_lite import Label, edges_for



# ja_pattern = re.compile(r'[ぁ-ん]+|[ァ-ヴー]+|[一-龠]+')
ja_pattern = re.compile(r'^[ぁ-んァ-ヶーｱ-ﾝﾞﾟ一-龠]*$')   # 長音ー含む

def print_word_concepts(w):
    """ """
    w_concepts = Label.get(text=w, language='ja').concepts
    print(f'{w} concepts: {len(w_concepts)}')
    for c in w_concepts:
        print("Concept:", c.__dict__)
        print("    Concept URI:", c.uri)
        print("    Concept text:", c.text)



def get_concept_in_out(c):
    """個別 conceptに対して, in, outを個別に取得
    Args:
        c: concept
    """
    if c.edges_out:
        # print(f"Edges out:")
        for e in c.edges_out:
            if re.search(ja_pattern, e.end.text):
                # print(f"[{e.__dict__}] -> r: {e.relation.name} {e.end.text}")   # detail
                print(f"-> r: {e.relation.name} {e.end.text}")  # simple
            else:
                # print(f"xxx -> r: {e.relation.name} {e.end.text}")
                continue

    if c.edges_in:
        # print(f"Edges in:")
        for e in c.edges_in:
            if re.search(ja_pattern, e.start.text):
                # print(f"[{e.__dict__}] {e.start.text} r: {e.relation.name} ->")   # detail
                print(f'{e.start.text} r: {e.relation.name} ->')    # simple
            else:
                # print(f"xxx {e.start.text} r: {e.relation.name} ->")
                continue

def get_all_concepts_in_out(w_concepts):
    for c in w_concepts:
        # print(f"Concept text: {c.text}")
        get_concept_in_out(c)
    

def test_edges_for(same_language=False):
    # w = '猫'
    w = '数学'
    
    w_concepts = Label.get(text=w, language='ja').concepts
    for e in edges_for(w_concepts, same_language=same_language):
        print(e.start.text, "::", e.end.text, "|", e.relation.name)

def get_all_concepts_in_out_word():
    # w = '猫'
    w = '数学'
    w_concepts = Label.get(text=w, language='ja').concepts
    get_all_concepts_in_out(w_concepts)


if __name__ == "__main__":
    SAME_LANGUAGE = True
    # test_edges_for(SAME_LANGUAGE)    # 組み込み関数 edge_for
    get_all_concepts_in_out_word()