require 'json'

while line = gets()
  o = JSON.load(line)
  o['ner'].delete("mecab")
  o['ner'].delete("features")
  o['ner'].delete("chunk")
  o['ner'].delete("gold2")
  puts o.to_json
end

