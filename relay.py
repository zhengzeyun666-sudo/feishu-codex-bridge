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
import json
import os
import time
from pathlib import Path

DEFAULT_INBOX_FILE = "~/.cc-connect/inbox.jsonl"


def message_from_env(env=os.environ, now=time.time):
    session_key = env.get("CC_HOOK_SESSION_KEY", "").strip()
    if not session_key:
        raise ValueError("CC_HOOK_SESSION_KEY is required")

    return {
        "timestamp": now(),
        "user_id": env.get("CC_HOOK_USER_ID", ""),
        "user_name": env.get("CC_HOOK_USER_NAME", ""),
        "content": env.get("CC_HOOK_CONTENT", ""),
        "session_key": session_key,
        "platform": env.get("CC_HOOK_PLATFORM", ""),
        "project": env.get("CC_HOOK_PROJECT", ""),
        "status": "pending",
    }


def append_message(path, msg):
    path = Path(path).expanduser()
    path.parent.mkdir(mode=0o700, parents=True, exist_ok=True)
    path.parent.chmod(0o700)

    flags = os.O_WRONLY | os.O_CREAT | os.O_APPEND
    if hasattr(os, "O_NOFOLLOW"):
        flags |= os.O_NOFOLLOW

    fd = os.open(path, flags, 0o600)
    os.fchmod(fd, 0o600)
    with os.fdopen(fd, "a", encoding="utf-8") as f:
        f.write(json.dumps(msg, ensure_ascii=False) + "\n")


def main():
    msg = message_from_env()
    append_message(os.environ.get("CC_RELAY_INBOX", DEFAULT_INBOX_FILE), msg)
    print("relay ok → inbox")


if __name__ == "__main__":
    main()
