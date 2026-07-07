import hashlib
import json
from datetime import datetime, timezone
from pathlib import Path

DEFAULT_ACCOUNT_FILE = Path(__file__).resolve().parent / "data" / "accounts.json"


def _now_iso() -> str:
    return datetime.now(timezone.utc).replace(microsecond=0).isoformat()


def _resolve_account_file(account_file=None) -> Path:
    return Path(account_file) if account_file else DEFAULT_ACCOUNT_FILE


def load_accounts(account_file=None) -> dict:
    path = _resolve_account_file(account_file)
    if not path.exists():
        return {}
    try:
        data = json.loads(path.read_text(encoding="utf-8"))
    except json.JSONDecodeError:
        return {}
    return data if isinstance(data, dict) else {}


def save_accounts(accounts, account_file=None) -> None:
    path = _resolve_account_file(account_file)
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(accounts, ensure_ascii=False, indent=2), encoding="utf-8")


def hash_password(password: str) -> str:
    return hashlib.sha256(password.encode("utf-8")).hexdigest()


def register_account(username: str, password: str, account_file=None) -> tuple[bool, str | dict]:
    clean_name = (username or "").strip()
    if not clean_name:
        return False, "Bitte einen Benutzernamen eingeben."
    if len(password or "") < 4:
        return False, "Das Passwort muss mindestens 4 Zeichen haben."

    accounts = load_accounts(account_file)
    if clean_name in accounts:
        return False, "Dieser Benutzername ist bereits vergeben."

    now = _now_iso()
    accounts[clean_name] = {
        "username": clean_name,
        "password_hash": hash_password(password),
        "coins": 100,
        "wins": 0,
        "created_at": now,
        "last_login": now,
        "store_unlocks": [],
    }
    save_accounts(accounts, account_file)
    return True, accounts[clean_name]


def login_account(username: str, password: str, account_file=None) -> tuple[bool, str | dict]:
    clean_name = (username or "").strip()
    accounts = load_accounts(account_file)
    account = accounts.get(clean_name)
    if not account:
        return False, "Ungültiger Benutzername oder Passwort."
    if account.get("password_hash") != hash_password(password):
        return False, "Ungültiger Benutzername oder Passwort."

    account["last_login"] = _now_iso()
    save_accounts(accounts, account_file)
    return True, account


def update_account(username: str, updates: dict, account_file=None) -> tuple[bool, str | dict]:
    accounts = load_accounts(account_file)
    account = accounts.get((username or "").strip())
    if not account:
        return False, "Account nicht gefunden."
    account.update(updates)
    save_accounts(accounts, account_file)
    return True, account
