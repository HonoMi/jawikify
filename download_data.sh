#!/bin/bash

mkdir -p data/
cd data/

for filename in "linker.model" "list-Name20161220.txt" "master06_candidates.kct" "master06_content_mecab_annotated.idf.kch" "master06_content.kch" "md.full" "word_ids.tsv"; do
    url="http://www.cl.ecei.tohoku.ac.jp/~matsuda/jawikify_data/"$filename
    if [ ! -e "$filename" ]; then
        echo "download $url ..."
        wget $url
    fi
done
