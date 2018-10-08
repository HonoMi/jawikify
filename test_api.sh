#!/usr/bin/env zsh

PORT=8079

echo '\n== jawikify'
curl -d '{"query": [
            {"sentence": "スズキのバイクを買った。"},
            {"sentence": "角刈りにパイソン柄のセットアップ、目元には怪しいサングラスをした謎の男性が、「ペンパイナッポーアッポーペン」と、テクノ調の曲で歌い踊る約１分間の動画が世界を席巻している。"}
        ]}' localhost:$PORT/jawikify | jq
