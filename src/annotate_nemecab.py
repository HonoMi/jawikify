#!/usr/bin/env python
# -*- coding: utf-8 -*-
from __future__ import print_function
from __future__ import unicode_literals

import copy
import sys
import json
from honoka_utility import util
import logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


def main():

    in_json = json.loads(sys.stdin.read())
    out_json = copy.deepcopy(in_json)
    # if 'nemecab' in out_json['ner']:
    #     # print(json.dumps(out_json, ensure_ascii=False, indent=4, sort_keys=True, separators=(',', ': ')))
    #     print(json.dumps(out_json))
    #     return

    nemecab = []
    for sentence in in_json['ner']['sentences']:
        mecab_result, err = util.exec_shell_cmd('echo " ' + sentence + '" | mecab')
        nemecab.append(mecab_result.rstrip('\n'))
    out_json['ner']['nemecab'] = nemecab
    print(json.dumps(out_json))
    # print(json.dumps(out_json, ensure_ascii=False, indent=4, sort_keys=True, separators=(',', ': ')))
    return


if __name__ == '__main__':
    main()
