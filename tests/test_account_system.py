import json
import tempfile
from pathlib import Path

from account_system import login_account, register_account


def test_registration_and_login_persist_to_file() -> None:
    with tempfile.TemporaryDirectory() as tmp_dir:
        account_file = Path(tmp_dir) / "accounts.json"

        ok, result = register_account("Ada", "secret123", account_file=account_file)
        assert ok is True
        assert result["username"] == "Ada"
        assert result["coins"] == 100

        ok, login_result = login_account("Ada", "secret123", account_file=account_file)
        assert ok is True
        assert login_result["username"] == "Ada"

        stored = json.loads(account_file.read_text(encoding="utf-8"))
        assert stored["Ada"]["username"] == "Ada"
