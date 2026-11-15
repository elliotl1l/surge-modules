# Surge Modules (Sanitized & Energy-Optimized)

适用于 Surge iOS / Mac 的高能效净化模块集合。

- **消灭 TCP RST 重发风暴**：将 `[Rule]` 内所有裸 `REJECT` 精准替换为 `REJECT-DROP`，避免基带与 Wi-Fi 芯片持续处于高功耗重试状态；
- **剥离冗余日志与磁盘 I/O**：对于高频刷帖应用（如小红书），剥离巨量 `console.log` 与无谓的闪存持久化存储，将 JS 引擎唤醒次数压缩 80% 以上。

---

## 订阅安装链接 (Surge)

### 1. 高德地图 (AutoNavi)
- **Surge 安装链接**:
  `https://raw.githubusercontent.com/elliotl1l/surge-modules/main/AutoNavi.sgmodule`

### 2. 微博去广告&净化
- **Surge 安装链接**:
  `https://raw.githubusercontent.com/elliotl1l/surge-modules/main/weibo.sgmodule`

### 3. 小红书 (纯净去广告·低功耗专版)
- **特点**：专注去广告（开屏/信息流赞助/带货卡片/直播卡片/搜索推广/营销弹窗）。打开笔记、看大图、看视频、刷评论区 **零脚本挂载（0 CPU / 0 I/O）**，告别高频刷帖发热掉电。
- **Surge 安装链接**:
  `https://raw.githubusercontent.com/elliotl1l/surge-modules/main/xiaohongshu.sgmodule`

### 4. 豆瓣 (精简去广告)
- **特点**：移除豆瓣开屏与信息流广告，放行 `erebor.douban.com` 保证 Web JSSDK、动态鉴权与微信内置浏览器正常打开，仅在 URL Rewrite 精准过滤广告计数。
- **Surge 安装链接**:
  `https://raw.githubusercontent.com/elliotl1l/surge-modules/main/Douban.sgmodule`

---

## 维护机制

- **高德、微博、豆瓣**：每月 1 号由 GitHub Actions 自动从上游同步更新并清洗规则；
- **小红书**：由本地维护高能效纯净脚本 `scripts/xiaohongshu.js` 与模块配置。
