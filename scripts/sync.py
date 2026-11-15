import re, urllib.request, os

MODULES = {
    "AutoNavi.sgmodule": "https://raw.githubusercontent.com/fmz200/wool_scripts/main/Surge/module/split/partG/AutoNavi.sgmodule",
    "weibo.sgmodule": "https://raw.githubusercontent.com/fmz200/wool_scripts/main/Surge/module/weibo.module",
    "Douban.sgmodule": "https://raw.githubusercontent.com/fmz200/wool_scripts/main/Surge/module/split/partD/Douban.sgmodule",
}

def sanitize(name, url):
    req = urllib.request.Request(url, headers={"User-Agent": "Mozilla/5.0"})
    content = urllib.request.urlopen(req, timeout=15).read().decode("utf-8")
    lines = content.splitlines()
    in_rule = False
    in_rewrite = False
    has_raw_url = False
    out = []
    
    for line in lines:
        stripped = line.strip()
        if stripped.startswith("["):
            in_rule = (stripped == "[Rule]")
            in_rewrite = (stripped == "[URL Rewrite]")
            out.append(line)
            continue
            
        # 0. 规范化 raw-url 永远指向用户私有仓库，确保模块自动更新不脱离真值源
        if stripped.startswith("#!raw-url="):
            line = f"#!raw-url=https://raw.githubusercontent.com/elliotl1l/surge-modules/main/{name}"
            has_raw_url = True
            out.append(line)
            continue

        # 1. 过滤 AutoNavi 致命破坏规则
        if name == "AutoNavi.sgmodule":
            # 剔除导致打车/顺风车挂死的初始化域名与 H5 页面容器
            if re.search(r",(apiinit|aboard\.apilocate|page)\.amap\.com,", line):
                continue
            # 修复将所有增值业务(打车/顺风车)一刀切拦截的粗暴规则
            if in_rewrite and re.search(r"\^https\?:\\/\\/m5\\.amap\\.com\\/ws\\/valueadded\\/ - reject", line):
                line = "^https?:\\/\\/m5\\.amap\\.com\\/ws\\/valueadded\\/alimama\\/splash_screen - reject"

        # 2. 过滤 Douban 摧毁 JSSDK/鉴权的整域拦截
        if name == "Douban.sgmodule":
            if in_rule and re.search(r"DOMAIN-SUFFIX,erebor\.douban\.com", line):
                continue

        # 3. 移动端规则转换：广告拦截转 REJECT-DROP，但严禁将 QUIC / APM 转为 DROP
        if in_rule:
            if "PROTOCOL,QUIC" in line or "apm-native" in line:
                if ",REJECT-DROP" in line:
                    line = line.replace(",REJECT-DROP", ",REJECT")
            elif re.search(r",REJECT(\b|$)", line) and not re.search(r"REJECT-(DROP|NO-DROP|200|TINYGIF)", line):
                line = re.sub(r",REJECT\b", ",REJECT-DROP", line)
                
        out.append(line)

    if not has_raw_url:
        # 在头部插入 raw-url
        insert_idx = 1
        for i, l in enumerate(out):
            if l.startswith("#!name="):
                insert_idx = i + 1
                break
        out.insert(insert_idx, f"#!raw-url=https://raw.githubusercontent.com/elliotl1l/surge-modules/main/{name}")
        
    return "\n".join(out) + "\n"

def main():
    os.makedirs("modules", exist_ok=True)
    for name, url in MODULES.items():
        print(f"Syncing {name} from {url}...")
        try:
            cleaned = sanitize(name, url)
            with open(f"modules/{name}", "w", encoding="utf-8") as f:
                f.write(cleaned)
            with open(name, "w", encoding="utf-8") as f:
                f.write(cleaned)
            print(f"Successfully sanitized {name}")
        except Exception as e:
            print(f"Error syncing {name}: {e}")

if __name__ == "__main__":
    main()
