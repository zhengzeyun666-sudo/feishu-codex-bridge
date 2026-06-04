#!/usr/bin/env python3
"""
cc-connect Hook 中继脚本
================================
被 cc-connect 的 message.received hook 调用。
将飞书消息写入 inbox.jsonl，供 Codex 桌面版轮询处理。

环境变量（由 cc-connect 注入）：
  CC_HOOK_USER_ID     - 用户 open_id
  CC_HOOK_USER_NAME   - 用户名称
  CC_HOOK_CONTENT     - 消息正文
  CC_HOOK_SESSION_KEY - 会话标识，用于 cc-connect send 回复
  CC_HOOK_PLATFORM    - 平台（feishu）
  CC_HOOK_PROJECT     - 项目名
  CC_HOOK_EVENT       - 事件类型（message.received）
  CC_HOOK_TIMESTAMP   - 时间戳

部署：
  1. 复制到 ~/.cc-connect/relay.py
  2. chmod +x ~/.cc-connect/relay.py
  3. 在 cc-connect config.toml 的 [[hooks]] 中引用
"""
import os
import json
import time

INBOX_FILE = os.path.expanduser("~/.cc-connect/inbox.jsonl")


def main():
    msg = {
        "timestamp": time.time(),
        "user_id": os.environ.get("CC_HOOK_USER_ID", ""),
        "user_name": os.environ.get("CC_HOOK_USER_NAME", ""),
        "content": os.environ.get("CC_HOOK_CONTENT", ""),
        "session_key": os.environ.get("CC_HOOK_SESSION_KEY", ""),
        "platform": os.environ.get("CC_HOOK_PLATFORM", ""),
        "project": os.environ.get("CC_HOOK_PROJECT", ""),
        "status": "pending",
    }

    with open(INBOX_FILE, "a", encoding="utf-8") as f:
        f.write(json.dumps(msg, ensure_ascii=False) + "\n")

    print(f"relay ok: {msg['user_name']} → inbox")


if __name__ == "__main__":
    main()
