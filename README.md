# 飞书直连 Codex 桌面版

这不是普通的飞书对话机器人。这是一个把 **Codex 桌面版的完整能力**搬到飞书上的桥接方案。

**你能做什么：**
- 🖥️ **操控桌面应用和文件** — 通过飞书自然语言让 Codex 打开 Chrome、编辑文档、读写文件
- 🌐 **浏览器操作** — 搜索网页、填表单，一句话搞定
- 📸 **截取画面** — 截取网页或桌面画面，以图片附件直接发回飞书
- 📎 **发送原始文件** — Excel、PPT、PDF、图片，以文件附件发回，不是纯文本
- 💰 **低成本运行** — 外接 DeepSeek v4 Pro 等第三方 API，不用官方模型也能跑

**它怎么工作的：**
飞书消息 → cc-connect (WebSocket) → Hook 中继 → Codex 桌面版处理 → 文件/消息原样返回飞书

Codex 桌面版具备浏览器控制、文档处理、桌面操控等插件能力，CLI 版没有这些。这个方案通过 inbox 中继让桌面版接管高级请求，CLI agent 处理日常对话。一句话：聊天能做的它做，聊天做不了的（发文件、操作电脑）它也做。

## 快速开始

详见 [SKILL.md](SKILL.md) — 完整配置指南（364 行，含架构图、安装方式、故障排查）。

## 文件说明

| 文件 | 用途 |
|------|------|
| `SKILL.md` | 完整配置文档 |
| `config.toml.template` | cc-connect 配置模板（TOML 格式，app_id/app_secret 分开写） |
| `relay.py` | Hook 中继脚本 |
| `LICENSE` | MIT |

## 一键安装

```bash
npm install -g cc-connect

# CLI 参数用「冒号」拼接 App ID 和 Secret（是 cc-connect 支持的简写格式，不同于 TOML 里的分开写法）
cc-connect feishu setup --project my-workspace --app cli_YOUR_APP_ID:YOUR_APP_SECRET
```

然后把 `relay.py` 放到 `~/.cc-connect/` 下，修改 `config.toml` 加上 `[[hooks]]` 即可。

## 最低要求

- Codex 桌面版
- Node.js >= 18
- Python 3
- 飞书账号
