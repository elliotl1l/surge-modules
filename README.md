# Surge Modules (Sanitized & Energy-Optimized)

适用于 Surge iOS / Mac 的高能效净化模块集合。

- **四层决策矩阵能效优化**：严禁无脑将所有 `REJECT` 替换为 `REJECT-DROP`；纯三方广告/打点转 `REJECT-DROP` 迫退 SDK 休眠基带；APM 崩溃监控、系统日志、Push 推送、IM 聊天网关与 QUIC 协议严格保持 `REJECT`，杜绝 75 秒 TCP 握手挂死与推送延迟；
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

### 4. 豆瓣 (精简去广告·奶思原版逻辑)
- **特点**：遵循奶思原版开屏与推荐广告过滤规则，保证基础鉴权与动态页面稳定。
- **Surge 安装链接**:
  `https://raw.githubusercontent.com/elliotl1l/surge-modules/main/Douban.sgmodule`

---

## 维护机制

- **高德、微博、豆瓣**：每月 1 号由 GitHub Actions 自动从上游同步，并经由 `scripts/sync.py` 执行四层决策矩阵清洗规则；
- **小红书**：本地独立自研与维护轻量纯净脚本 `scripts/xiaohongshu.js` 与模块配置，不受上游污染。
