# 飞书连接 cc-connect 与 Codex

这是一个轻量桥接示例：cc-connect 接收飞书消息，`relay.py` 再把消息写入本地 `inbox.jsonl`，供正在运行的 Codex 桌面版任务读取和处理。

> 当前是“消息交接”，不是无人值守的桌面版远程控制。Codex 桌面版需要有一个正在运行的任务主动读取 inbox；本仓库不包含常驻轮询器，也不会自行触发桌面操作。

## 能做什么

- 飞书消息通过 cc-connect 的 WebSocket 长连接进入本机
- cc-connect 的 Codex CLI agent 处理普通对话
- Hook 将消息写入权限为 `0600` 的 JSONL 队列
- 活跃的 Codex 桌面版任务可读取队列，并通过 `cc-connect send` 回传消息或文件

```text
飞书 → cc-connect → message.received Hook → inbox.jsonl
                                              ↓ 主动读取
飞书 ← cc-connect send ← Codex CLI / Codex 桌面版任务
```

## 快速开始

最低要求：Codex 桌面版、Node.js 18+、Python 3、飞书账号。

```bash
npm install -g cc-connect
git clone https://github.com/zhengzeyun666-sudo/feishu-codex-bridge.git
cd feishu-codex-bridge

mkdir -p ~/.cc-connect
cp relay.py ~/.cc-connect/
cp config.toml.template ~/.cc-connect/config.toml
chmod 700 ~/.cc-connect
chmod 600 ~/.cc-connect/config.toml
chmod +x ~/.cc-connect/relay.py
```

编辑 `~/.cc-connect/config.toml`，替换 App ID、App Secret、工作目录和飞书 Open ID，然后运行：

```bash
cc-connect --config ~/.cc-connect/config.toml
```

完整的飞书权限、事件订阅、验证和排障步骤见 [SKILL.md](SKILL.md)。

## 安全默认值

模板默认采用以下边界：

- `allow_from` 只允许指定飞书 Open ID，不使用 `*`
- `admin_from` 位于 `[[projects]]` 层级，仅允许指定用户执行特权命令
- Codex 使用 `suggest`（只读沙箱），不使用会绕过审批和沙箱的 `yolo`
- `work_dir` 指向单个工作区，不直接暴露整个用户目录

首次不知道 Open ID 时，可临时把 `allow_from` 设为 `*`，只发送 `/whoami` 获取 ID；随后立即改回具体 ID 并重启 cc-connect。

## 本地验证

```bash
python3 -m unittest -v
python3 -m py_compile relay.py
```

## 文件说明

| 文件 | 用途 |
|---|---|
| `SKILL.md` | 完整配置与排障指南 |
| `config.toml.template` | 安全默认的 cc-connect 配置模板 |
| `relay.py` | 将 Hook 消息追加到本地 JSONL 队列 |
| `test_relay.py` | 中继脚本的最小回归测试 |
| `LICENSE` | MIT |

## 已知限制

- Hook 会无条件接收符合 cc-connect 平台权限配置的消息，无法按消息内容分流
- CLI agent 和桌面版任务可能同时回复同一条消息
- 桌面版任务不运行或未读取 inbox 时，消息只会留在本地队列
- 第三方模型和 Provider 由 cc-connect/Codex CLI 配置决定，不是本仓库提供的能力
