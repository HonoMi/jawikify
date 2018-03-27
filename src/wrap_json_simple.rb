require 'json'

ret = {
  "ner" => {
    "sentences" => [],
    "offsets" => []
  }
}
while line = gets()
  line = line.encode(
  'utf-16',
  'utf-8',
  :invalid => :replace,
  :undef => :replace
  ).encode('utf-8')
  ret["ner"]["sentences"] << line.chomp
end
puts JSON.dump(ret)
