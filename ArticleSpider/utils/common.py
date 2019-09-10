import hashlib

def get_md5(url):
    # 在python3中，需要判断url是否是字符串，如果是的话需要将字符进行utf-8转换
    if isinstance(url,str):
        url = url.encode("utf-8")
    m = hashlib.md5()
    m.update(url)
    return m.hexdigest()

if __name__ == "__main__":
    # print(get_md5("http://jobbole.com"))
    # 报错 TypeError: Unicode-objects must be encoded before hashing
    # 在python3中会报错  因为所有python3将所有的字符都变成了unicode了
    print (get_md5("http://jobbole.com".encode("utf-8")))

