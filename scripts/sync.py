import re, urllib.request, os

MODULES = {
    "AutoNavi.sgmodule": "https://raw.githubusercontent.com/fmz200/wool_scripts/main/Surge/module/split/partG/AutoNavi.sgmodule",
    "weibo.sgmodule": "https://raw.githubusercontent.com/fmz200/wool_scripts/main/Surge/module/weibo.module",
}

def sanitize(url):
    req = urllib.request.Request(url, headers={"User-Agent": "Mozilla/5.0"})
    content = urllib.request.urlopen(req, timeout=15).read().decode("utf-8")
    lines = content.splitlines()
    in_rule = False
    out = []
    for line in lines:
        if line.strip().startswith("["):
            in_rule = (line.strip() == "[Rule]")
        elif in_rule:
            if re.search(r",REJECT(\b|$)", line) and not re.search(r"REJECT-(DROP|NO-DROP|200|TINYGIF)", line):
                line = re.sub(r",REJECT\b", ",REJECT-DROP", line)
        out.append(line)
    return "\n".join(out) + "\n"

def main():
    os.makedirs("modules", exist_ok=True)
    for name, url in MODULES.items():
        print(f"Syncing {name} from {url}...")
        try:
            cleaned = sanitize(url)
            # Write to modules/ and root
            with open(f"modules/{name}", "w", encoding="utf-8") as f:
                f.write(cleaned)
            with open(name, "w", encoding="utf-8") as f:
                f.write(cleaned)
            print(f"Successfully sanitized {name}")
        except Exception as e:
            print(f"Error syncing {name}: {e}")

if __name__ == "__main__":
    main()
