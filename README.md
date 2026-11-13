# Surge Modules (Sanitized & Auto-Synced)

每月 1 号由 GitHub Actions 自动从上游作者（fmz200）拉取最新模块，将 `[Rule]` 内可能引发移动端 TCP RST 死循环重试的裸 `REJECT` 精准替换为 `REJECT-DROP`，同时 100% 完整保留原作者的 `[Map Local]`、`[URL Rewrite]` 与 `[MITM]` 核心去广告逻辑。

## 订阅链接 (Surge)

### 1. 高德地图 (AutoNavi)
* **Surge 安装链接**:
  ```text
  https://raw.githubusercontent.com/elliotl1l/surge-modules/main/AutoNavi.sgmodule
  ```

### 2. 微博去广告&净化
* **Surge 安装链接**:
  ```text
  https://raw.githubusercontent.com/elliotl1l/surge-modules/main/weibo.sgmodule
  ```

## 维护机制
* **定时任务**: 每月 1 号 00:00 UTC 自动检测并同步；
* **按需触发**: 支持在 GitHub Actions 页面随时手动触发立即同步。
