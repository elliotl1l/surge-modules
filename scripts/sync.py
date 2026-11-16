import re, urllib.request, os, sys

# 1. 明确模块分类
# UPSTREAM_MODULES: 从社区上游同步并进行“四层决策矩阵”净化
UPSTREAM_MODULES = {
    "AutoNavi.sgmodule": "https://raw.githubusercontent.com/fmz200/wool_scripts/main/Surge/module/split/partG/AutoNavi.sgmodule",
    "weibo.sgmodule": "https://raw.githubusercontent.com/fmz200/wool_scripts/main/Surge/module/weibo.module",
}

# SELF_MAINTAINED_MODULES: 本地自研独立维护，严禁被上游抓取覆盖
SELF_MAINTAINED_MODULES = [
    "xiaohongshu.sgmodule",
]

def apply_decision_matrix(line, name):
    """
    根据四层决策矩阵精准定策，坚决消灭盲目 REJECT -> REJECT-DROP 的一刀切逻辑：
    - Tier 2 (QUIC): 强制 REJECT (ICMP Port Unreachable 瞬时降级 TCP，防 3 秒卡死)
    - Tier 3 (APM/日志): 强制 REJECT (TCP RST 0ms 释放 Socket，防连接池排队挂死)
    - Tier 4 (Push/IM/核心通信/URL-REGEX): 强制 REJECT (防 75s 长连接超时与推送延时)
    - Tier 1 (纯广告/三方广告联盟 SDK): 转 REJECT-DROP (逼退 SDK 重试，基带即刻休眠)
    """
    stripped = line.strip()
    if not stripped or stripped.startswith("#"):
        return line

    # 1. QUIC 探测降级（第二层）：必须 REJECT
    if "PROTOCOL,QUIC" in line:
        return line.replace(",REJECT-DROP", ",REJECT")

    # 2. 核心通信、推送网关、IM 聊天通道、主域名 URL-REGEX（第四层）：严禁 DROP！
    # 典型：gw5.push.mcp.weibo.cn, dp.im.weibo.cn, api-cloudim.api.weibo.com, api.weibo.cn
    tier4_patterns = [
        "push", ".im.", "cloudim", "api.weibo.cn", "URL-REGEX",
        "ynuf.aliapp.org", "alibabachengdun", "page.amap.com"
    ]
    if any(k in line for k in tier4_patterns):
        return re.sub(r",REJECT-DROP\b", ",REJECT", line)

    # 4. APM 崩溃监控、系统与应用日志、云同步（第三层）：必须 REJECT，0ms 释放连接池！
    # 典型：logs.amap.com, dualstack-logs.amap.com, icloud-amap.com, datacollection
    # 注：小红书 apm-native 遭遇 REJECT 会陷入高频重试风暴，改走置顶 DIRECT 放行，不归入此处
    tier3_patterns = [
        "logs.amap.com", "icloud-amap.com", "datacollection"
    ]
    if any(k in line for k in tier3_patterns):
        return re.sub(r",REJECT-DROP\b", ",REJECT", line)

    # 5. 纯商业广告、追踪打点、开屏预载（第一层）：转 REJECT-DROP
    # 此时剩下的规则均为纯广告域名（如 biz.weibo.com, adimg, zymo, alitui, optimus-ads 等）
    if re.search(r",REJECT(\b|$)", line) and not re.search(r"REJECT-(DROP|NO-DROP|200|TINYGIF)", line):
        return re.sub(r",REJECT\b", ",REJECT-DROP", line)

    return line

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

        # 2. 规则层应用四层决策矩阵
        if in_rule:
            line = apply_decision_matrix(line, name)
                
        out.append(line)

    if not has_raw_url:
        # 在头部插入 raw-url
        insert_idx = 1
        for i, l in enumerate(out):
            if l.startswith("#!name="):
                insert_idx = i + 1
                break
        out.insert(insert_idx, f"#!raw-url=https://raw.githubusercontent.com/elliotl1l/surge-modules/main/{name}")
        
    result = "\n".join(out) + "\n"

    # 健全性断言：防上游抓空或破损
    assert "[Rule]" in result or "[URL Rewrite]" in result or "[Map Local]" in result, f"Sanity check failed for {name}"
    assert len(result) > 200, f"Sanity check failed for {name}: content too short"

    return result

def main():
    repo_root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    modules_dir = os.path.join(repo_root, "modules")
    os.makedirs(modules_dir, exist_ok=True)
    
    for name, url in UPSTREAM_MODULES.items():
        print(f"Syncing {name} from {url}...")
        try:
            cleaned = sanitize(name, url)
            with open(os.path.join(modules_dir, name), "w", encoding="utf-8") as f:
                f.write(cleaned)
            with open(os.path.join(repo_root, name), "w", encoding="utf-8") as f:
                f.write(cleaned)
            print(f"Successfully sanitized {name}")
        except Exception as e:
            print(f"Error syncing {name}: {e}")
            sys.exit(1)

if __name__ == "__main__":
    main()
