#!/usr/bin/env python
# -*- coding: utf-8 -*-
from __future__ import print_function
from __future__ import unicode_literals
import argparse
import tempfile
import json
from sanic import Sanic
from sanic import response
from honoka_utility import util
from pdb import set_trace

app = Sanic()


def get_args():
    parser = argparse.ArgumentParser()
    parser.add_argument('--port', '-p', type=int, default=8000)
    args = parser.parse_args()
    return args


def format_jawikify_result(result_json):
    ner_results = result_json['ner']
    ret_json = {'result': []}
    for sentence, extracted_in_sent, linked_in_sent in zip(ner_results['sentences'], ner_results['extracted'], ner_results['linked']):
        ret_json['result'].append({
            'sentence': sentence,
            'extracted': [{'surface': extracted[0], 'class': extracted[1]} for extracted in extracted_in_sent],
            'linked': [linked for linked in linked_in_sent],
        })
    return ret_json


@app.route('/link', methods=['POST'])
async def classify(request):
    '''
        input: {
            "query": [
                {
                    "sentence": "角刈りにパイソン柄のセットアップ、目元には怪しいサングラスをした謎の男性が、「ペンパイナッポーアッポーペン」と、テクノ調の曲で歌い踊る約１分間の動画が世界を席巻している。"
                    "extracted": [
                        {"surface": "サングラス"},
                        {"surface": "ペンパイナッポーアッポーペン"}, 
                    ],
                    "offset": []
                },
                ...
            ]
        }
        output: jawikifyと同じ。
    '''
    ''' 中間表現
        {
            "ner"{
            "sentences": [
                "hoge",
                "fuga",
            ],
            "extraceted":[
                "サングラス", "日本"
            ]
            "offsets": []
            }
        }
    '''
    rows = request.json['query']
    ner_input_json = {'ner': {}}
    ner_input_json['ner']['sentences'] = [row['sentence'] for row in rows]
    ner_input_json['ner']['extracted'] = [
        [
            [named_entity['surface'], 'UserInput']
            for named_entity in row['extracted']
        ]
        for row in rows
    ]
    ner_input_json['ner']['offsets'] = [row.get('offset', 0) for row in rows]

    ner_input_file = tempfile.mktemp()
    with open(ner_input_file, 'w') as f:
        f.write(json.dumps(ner_input_json))

    cmd = 'cat ' + ner_input_file + ' | bash ./jawikify.link'
    out, err = util.exec_shell_cmd(cmd)
    ret_json = format_jawikify_result(json.loads(out))
    ret_json['query'] = request.json['query']
    return response.json(ret_json)


@app.route('/jawikify', methods=['POST'])
async def jawikify(request):
    '''
        input: {
            "query": [
                {"sentence": "角刈りにパイソン柄のセットアップ、目元には怪しいサングラスをした謎の男性が、「ペンパイナッポーアッポーペン」と、テクノ調の曲で歌い踊る約１分間の動画が世界を席巻している。"},
                {"sentence": "マクドナルドやスターバックスコーヒーといった外資大手外食.."},
                ..
            ]
        }

        output: {
            "result": [
                {
                    "sentence": "サッカーのワールドカップ（W杯）へ調整を続ける⽇本代表は..",
                    "extracted": [
                        {"surface": "サングラス", "class": "Product"},
                        {"surface": "ペンパイナッポーアッポーペン", "class": "Product"},
                    ],
                    "linked": [
                        {
                            "surface": "サングラス",
                            "title": "サングラス",
                            "score": "0.2176E1"
                        },
                        {
                            "surface": "ペンパイナッポーアッポーペン",
                            "title": null,
                            "score": 0
                        }
                    ],
                },
            ]
        }
    '''
    sentences = [row['sentence'] for row in request.json.get('query', [])]
    text = '\n'.join(sentences)
    input_text_file = tempfile.mktemp()
    with open(input_text_file, 'w') as f:
        f.write(text)

    cmd = 'cat ' + input_text_file + ' | bash ./jawikify'
    out, err = util.exec_shell_cmd(cmd)
    ret_json = format_jawikify_result(json.loads(out))
    ret_json['query'] = request.json['query']
    return response.json(ret_json)


if __name__ == '__main__':
    args = get_args()
    app.run(host='0.0.0.0', port=args.port)
