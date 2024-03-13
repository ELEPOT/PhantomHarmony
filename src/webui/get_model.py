import wget
hash_url = "download.elepot.dev/hash.txt"
try:
    with open("hash.txt", "r") as f:
        hash_old = f.read()
except:
    hash_old = 0
new = wget.download(hash_url)
with open(new, "r") as f:
    hash_new = f.read()
if hash_old != hash_new:
    url = "url"
    filename = wget.download(url)
