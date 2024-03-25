import wget
hash_url = "https://link.storjshare.io/s/jw43zc2rlwjv26ebnrkzyzzl24ya/model%2Fhash.txt?download=1"
try:
    with open("hash.txt", "r") as f:
        hash_old = f.read()
except:
    hash_old = 0
new = wget.download(hash_url)
with open(new, "r") as f:
    hash_new = f.read()
if hash_old != hash_new:
    url = "https://link.storjshare.io/s/jv57f7htl5khe5krqbcp7qnjk7pa/model%2Fdreamshaper_8.safetensors?download=1"
    filename = wget.download(url)
