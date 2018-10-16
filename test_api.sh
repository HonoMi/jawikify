#!/usr/bin/env zsh

PORT=8079


# NER + linking
echo '\n== jawikify'
curl -H 'Content-Type:application/json'\
     -d '{"query": [
             {"sentence": "モーツァルトは有名なバイオリン奏者です。"},
             {"sentence": "東京オリンピックは有名なスポーツ大会です。"},
             {"sentence": "モーツァルト宿に入りました。"},
             {"sentence": "スズキのバイクを買った。"}
         ]}' localhost:$PORT/jawikify  | jq


# linking only.
echo '\n== jawikify.ner'
curl -H 'Content-Type:application/json'\
     -d '{"query": [
             {
                 "sentence": "モーツアルトは有名なバイオリン奏者です。",
                 "extracted": [
                    {"surface": "モーツァルト"},
                    {"surface": "バイオリン"}
                 ],
             },
             {
                 "sentence": "東京オリンピックは有名なスポーツ大会です。",
                 "extracted": [
                    {"surface": "オリンピック"}
                 ]
             }
         ]}' localhost:$PORT/link | jq
