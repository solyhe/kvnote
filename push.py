#!/usr/bin/env python3
"""推送内容到 KV Note。
用法:
  python kvnote.py <key> "一段文本"     # 直接推文本
  python kvnote.py <key> <文件>         # 文件存在则读文件
  type x.txt | python kvnote.py <key>    # 从标准输入读
读取: https://txt.cn66.dpdns.org/<key>
"""
import io, json, os, sys, urllib.request

PUSH = "https://txt.cn66.dpdns.org/set?token=changeme"

def push(key, value):
    req = urllib.request.Request(
        PUSH,
        data=json.dumps({"key": key, "value": value}).encode(),
        headers={"content-type": "application/json",
                 "User-Agent": "curl/8.5.0"})  # 无 UA 会被 Cloudflare 403
    opener = urllib.request.build_opener(urllib.request.ProxyHandler({}))  # 绕过环境代理
    return opener.open(req, timeout=30).read().decode()

if __name__ == "__main__":
    if len(sys.argv) < 2:
        sys.exit(__doc__)
    key = sys.argv[1]
    if len(sys.argv) > 2:
        arg = " ".join(sys.argv[2:])
        if len(sys.argv) == 3 and os.path.isfile(arg):
            value = open(arg, encoding="utf-8").read()
        else:
            value = arg
    else:
        value = io.TextIOWrapper(sys.stdin.buffer, encoding="utf-8").read()
    print(key, push(key, value).strip())
