### Abstract
- ConceptNetは常識(common-sense knowledge)に関する知識を集めたもの．
- conceptnet-lite ライブラリを用いてConceptNetから，指定言語のトリプルを取得する

- outputs/ 以下に抽出済みトリプルのjsonlを配置
    ```
    outputs/triples_ja.jsonl  日本語(ja)
    outputs/triples_en.jsonl  英語(en)
    ```
    - jsonlに含まれるトリプルについてのlicense: ConceptNetのlicense: `CC-BY-SA-4.0`に従う．
        - [URL](https://github.com/commonsense/conceptnet5/wiki/Copying-and-sharing-ConceptNet)


### Setup & Run
- install library
``$ pip install conceptnet-lite``

- build ConceptNet database
- 以下のコマンドを実行することで，ConceptNet (ConceptNet-5.7) databaseがDL, 構築される．

    ```python
    import conceptnet_lite

    conceptnet_lite.connect("/path/to/conceptnet.db")
    ```

- 指定言語(en, ja)のトリプルを取得する
    - step1 指定言語のトリプル(重複あり)の取得
        - extract_triples.py main_ge_all_triples()で抽出対象言語を指定
            ```python
            def main_get_all_triples():
                ...
                # lang = 'ja'
                lang = 'en'
                ...
            ```

        - 次の関数を実行. extract_triples.py - main_get_all_triples
        - 以下の構造のjsonlが得られる

            ```json
            {"start": "at", "relation": "antonym", "end": "マニュアル", "dataset": "/d/wiktionary/en", "license": "cc:by-sa/4.0", "weight": 1.0}
            {"start": "at", "relation": "synonym", "end": "オートマチック", "dataset": "/d/wiktionary/en", "license": "cc:by-sa/4.0", "weight": 1.0}
            ...
            ```
   
    - step2 step1で得られたトリプルから重複を除く
        - 次の関数を実行. extract_triples.py - main_get_deduplicated_triples()



- TEST Env
    ```
    OS: macOS
    python 3.11.3
    conceptnet-lite 0.2.0
    ```

### References
- https://github.com/ldtoolkit/conceptnet-lite
