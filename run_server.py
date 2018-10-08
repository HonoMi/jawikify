#!/usr/bin/env python
# -*- coding: utf-8 -*-
from __future__ import print_function
from __future__ import unicode_literals
import argparse
import tempfile
import json
from sanic import Sanic
from sanic.response import json as sanic_json
from sanic.response import text as sanic_text
from honoka_utility import util

app = Sanic()


def get_args():
    parser = argparse.ArgumentParser()
    parser.add_argument('--port', '-p', type=int, default=8000)
    args = parser.parse_args()
    return args


@app.route('/jawikify', methods=['POST'])
async def classify(request):
    '''
        input: {
            'query': [
                {'sentence': '角刈りにパイソン柄のセットアップ、目元には怪しいサングラスをした謎の男性が、「ペンパイナッポーアッポーペン」と、テクノ調の曲で歌い踊る約１分間の動画が世界を席巻している。'},
                {'sentence': 'マクドナルドやスターバックスコーヒーといった外資大手外食..'},
                ..
            ]
        }

        output: {
            'result': [
                {
                    'sentence': 'サッカーのワールドカップ（W杯）へ調整を続ける⽇本代表は..',
                    'extracted': [
                        {"surface": "サングラス", "class": "Product"},
                        {"surface": "ペンパイナッポーアッポーペン", "class": "Product"},
                    ],
                    'linked': [
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

    cmd = 'cat ' + input_text_file + ' | ./jawikify'
    out, err = util.exec_shell_cmd(cmd)
    ner_results = json.loads(out)['ner']
    ret_json = {'result': []}
    for sentence, extracted_in_sent, linked_in_sent in zip(ner_results['sentences'], ner_results['extracted'], ner_results['linked']):
        ret_json['result'].append({
            'sentence': sentence,
            'extracted': [{'surface': extracted[0], 'class': extracted[1]} for extracted in extracted_in_sent],
            'linked': [linked for linked in linked_in_sent],
        })
    return sanic_text(ret_json)


if __name__ == '__main__':
    args = get_args()
    app.run(host='0.0.0.0', port=args.port)
