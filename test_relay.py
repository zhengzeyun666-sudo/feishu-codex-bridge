import json
import stat
import tempfile
import unittest
from pathlib import Path

import relay


class RelayTest(unittest.TestCase):
    def test_writes_private_jsonl(self):
        env = {
            "CC_HOOK_SESSION_KEY": "feishu:chat:user",
            "CC_HOOK_CONTENT": "你好",
            "CC_HOOK_USER_ID": "ou_test",
            "CC_HOOK_PLATFORM": "feishu",
            "CC_HOOK_PROJECT": "demo",
        }

        with tempfile.TemporaryDirectory() as tmp:
            inbox = Path(tmp) / ".cc-connect" / "inbox.jsonl"
            relay.append_message(inbox, relay.message_from_env(env, now=lambda: 1.0))

            record = json.loads(inbox.read_text(encoding="utf-8"))
            self.assertEqual(record["session_key"], "feishu:chat:user")
            self.assertEqual(record["content"], "你好")
            self.assertEqual(stat.S_IMODE(inbox.stat().st_mode), 0o600)
            self.assertEqual(stat.S_IMODE(inbox.parent.stat().st_mode), 0o700)

    def test_rejects_message_without_session_key(self):
        with self.assertRaisesRegex(ValueError, "CC_HOOK_SESSION_KEY"):
            relay.message_from_env({}, now=lambda: 1.0)


if __name__ == "__main__":
    unittest.main()
