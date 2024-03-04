import wget
hash_url = "hash_url"
with open("hash.txt", "r") as f
    hash_old = f.read()
new = wget.download(hash_url)
with open(new, "r") as f
    hash_new = f.read()
if hash_old != hash_new
    url = "url"
    filename = wget.download(url)
