# 飞书直连 Codex 桌面版

> 通过 cc-connect + Hook 中继，将飞书机器人对接 Codex 桌面版，实现远程对话、收发文件、操控电脑。

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
