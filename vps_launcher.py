# ============================
# Ouroboros — VPS Runtime Launcher
# ============================
# VPS-adapted launcher: env-based config, local filesystem storage.
# Heavy logic lives in supervisor/ package.

import logging
import os, sys, json, time, uuid, pathlib, subprocess, datetime, threading, queue as _queue_mod
from typing import Any, Dict, List, Optional, Set, Tuple

log = logging.getLogger(__name__)

# ----------------------------
# 0) Load environment variables
# ----------------------------
from dotenv import load_dotenv
load_dotenv()

# ----------------------------
# 0.1) Install launcher deps (if needed)
# ----------------------------
def install_launcher_deps() -> None:
    subprocess.run(
        [sys.executable, "-m", "pip", "install", "-q", "openai>=1.0.0", "requests"],
        check=True,
    )

# Only install if running in a fresh environment
try:
    import openai
    import requests
except ImportError:
    install_launcher_deps()

def ensure_claude_code_cli() -> bool:
    """Best-effort install of Claude Code CLI for Anthropic-powered code edits."""
    local_bin = str(pathlib.Path.home() / ".local" / "bin")
    if local_bin not in os.environ.get("PATH", ""):
        os.environ["PATH"] = f"{local_bin}:{os.environ.get('PATH', '')}"

    has_cli = subprocess.run(["bash", "-lc", "command -v claude >/dev/null 2>&1"], check=False).returncode == 0
    if has_cli:
        return True

    subprocess.run(["bash", "-lc", "curl -fsSL https://claude.ai/install.sh | bash"], check=False)
    has_cli = subprocess.run(["bash", "-lc", "command -v claude >/dev/null 2>&1"], check=False).returncode == 0
    if has_cli:
        return True

    subprocess.run(["bash", "-lc", "command -v npm >/dev/null 2>&1 && npm install -g @anthropic-ai/claude-code"], check=False)
    has_cli = subprocess.run(["bash", "-lc", "command -v claude >/dev/null 2>&1"], check=False).returncode == 0
    return has_cli

# ----------------------------
# 0.2) provide apply_patch shim
# ----------------------------
from ouroboros.llm import DEFAULT_LIGHT_MODEL

def install_apply_patch_user():
    """Install apply_patch to user's local bin (VPS-safe, no root needed)."""
    import pathlib
    
    user_bin = pathlib.Path.home() / ".local" / "bin"
    apply_patch_path = user_bin / "apply_patch"
    
    # Read the apply_patch code from the module
    from ouroboros.apply_patch import APPLY_PATCH_CODE
    
    try:
        user_bin.mkdir(parents=True, exist_ok=True)
        apply_patch_path.write_text(APPLY_PATCH_CODE, encoding="utf-8")
        apply_patch_path.chmod(0o755)
    except Exception as e:
        log.warning(f"Failed to install apply_patch to {apply_patch_path}: {e}")

install_apply_patch_user()

# ----------------------------
# 1) Environment-based config
# ----------------------------
def get_env(name: str, default: Optional[str] = None, required: bool = False) -> Optional[str]:
    """Get environment variable with optional default and validation."""
    v = os.environ.get(name, default)
    if required:
        assert v is not None and str(v).strip() != "", f"Missing required environment variable: {name}"
    return v

def _parse_int_cfg(raw: Optional[str], default: int, minimum: int = 0) -> int:
    try:
        val = int(str(raw))
    except Exception:
        val = default
    return max(minimum, val)

# Required secrets
OPENROUTER_API_KEY = get_env("OPENROUTER_API_KEY", required=True)
TELEGRAM_BOT_TOKEN = get_env("TELEGRAM_BOT_TOKEN", required=True)
TOTAL_BUDGET_DEFAULT = get_env("TOTAL_BUDGET", required=True)
GITHUB_TOKEN = get_env("GITHUB_TOKEN", required=True)

# Robust TOTAL_BUDGET parsing
try:
    import re
    _raw_budget = str(TOTAL_BUDGET_DEFAULT or "")
    _clean_budget = re.sub(r'[^0-9.\-]', '', _raw_budget)
    TOTAL_BUDGET_LIMIT = float(_clean_budget) if _clean_budget else 0.0
    if _raw_budget.strip() != _clean_budget:
        log.warning(f"TOTAL_BUDGET cleaned: {_raw_budget!r} → {TOTAL_BUDGET_LIMIT}")
except Exception as e:
    log.warning(f"Failed to parse TOTAL_BUDGET ({TOTAL_BUDGET_DEFAULT!r}): {e}")
    TOTAL_BUDGET_LIMIT = 0.0

# Optional secrets
OPENAI_API_KEY = get_env("OPENAI_API_KEY", default="")
ANTHROPIC_API_KEY = get_env("ANTHROPIC_API_KEY", default="")
TELEGRAM_BOT_TOKEN_ARCHITECT = get_env("TELEGRAM_BOT_TOKEN_ARCHITECT", required=True) # Added for architect bot

# GitHub config
GITHUB_USER = get_env("GITHUB_USER", required=True)
GITHUB_REPO = get_env("GITHUB_REPO", required=True)

# Infrastructure config
MAX_WORKERS = int(get_env("OUROBOROS_MAX_WORKERS", default="5") or "5")
MODEL_MAIN = get_env("OUROBOROS_MODEL", default="anthropic/claude-sonnet-4.6")
MODEL_CODE = get_env("OUROBOROS_MODEL_CODE", default="anthropic/claude-sonnet-4.6")
MODEL_LIGHT = get_env("OUROBOROS_MODEL_LIGHT", default=DEFAULT_LIGHT_MODEL)

BUDGET_REPORT_EVERY_MESSAGES = 10
SOFT_TIMEOUT_SEC = max(60, int(get_env("OUROBOROS_SOFT_TIMEOUT_SEC", default="600") or "600"))
HARD_TIMEOUT_SEC = max(120, int(get_env("OUROBOROS_HARD_TIMEOUT_SEC", default="1800") or "1800"))
DIAG_HEARTBEAT_SEC = _parse_int_cfg(
    get_env("OUROBOROS_DIAG_HEARTBEAT_SEC", default="30"),
    default=30,
    minimum=0,
)
DIAG_SLOW_CYCLE_SEC = _parse_int_cfg(
    get_env("OUROBOROS_DIAG_SLOW_CYCLE_SEC", default="20"),
    default=20,
    minimum=0,
)

# Set environment variables for subprocesses
# ... (existing code)
if str(ANTHROPIC_API_KEY or "").strip():
    ensure_claude_code_cli()

# ----------------------------
# 2) VPS Filesystem Setup
# ----------------------------
# ... (existing code)

# ----------------------------
# 3) Git constants
# ----------------------------
# ... (existing code)

# ----------------------------
# 4) Initialize supervisor modules (modified for dual-bot)
# ----------------------------
# ... (existing imports)

# Initialize both Telegram clients
from supervisor.telegram import init as telegram_init, TelegramClient, send_with_budget, log_chat
TG_OWNER = TelegramClient(str(TELEGRAM_BOT_TOKEN))
TG_ARCHITECT = TelegramClient(str(TELEGRAM_BOT_TOKEN_ARCHITECT))
telegram_init(
    drive_root=DRIVE_ROOT,
    total_budget_limit=TOTAL_BUDGET_LIMIT,
    budget_report_every=BUDGET_REPORT_EVERY_MESSAGES,
    tg_client=TG_OWNER,
)

# ... (existing initialization)

# ----------------------------
# 5) Bootstrap repo
# ----------------------------
# ... (existing code)

# ----------------------------
# 6) Start workers
# ----------------------------
# ... (existing code)

# ----------------------------
# 6.1) Auto-resume after restart
# ----------------------------
# ... (existing code)

# ----------------------------
# 6.2) Direct-mode watchdog
# ----------------------------
# ... (existing code)

# ----------------------------
# 6.3) Background consciousness
# ----------------------------
# ... (existing code)

# ----------------------------
# 7) Main loop
# ----------------------------
# ... (existing imports and context)

def _safe_qsize(q: Any) -> int:
    try:
        return int(q.qsize())
    except Exception:
        return -1


def _handle_supervisor_command(text: str, chat_id: int, tg_offset: int = 0):
    # ... (existing code)

# Main poll loop
while True:
    try:
        st = load_state()
        
        # Initialize architect offset if not exists
        if "tg_offset_architect" not in st:
            st["tg_offset_architect"] = 0
            save_state(st)
            
        # Get updates for owner bot
        try:
            owner_updates = TG_OWNER.get_updates(offset=st["tg_offset"], limit=100)
        except Exception as e:
            log.error(f"Failed to get owner updates: {e}")
            time.sleep(5)
            continue

        # Get updates for architect bot
        try:
            architect_updates = TG_ARCHITECT.get_updates(offset=st["tg_offset_architect"], limit=100)
        except Exception as e:
            log.error(f"Failed to get architect updates: {e}")
            architect_updates = []

        # Store new offsets after processing
        new_owner_offset = st["tg_offset"]
        new_architect_offset = st["tg_offset_architect"]

        # Process owner messages
        for update in owner_updates:
            message = update.get("message") or update.get("edited_message")
            if message:
                chat_id = message["chat"]["id"]
                text = message.get("text", "___no_text___")
                
                # Log the message
                append_jsonl(DRIVE_ROOT / "logs" / "chat.jsonl", {
                    "ts": datetime.datetime.now(datetime.timezone.utc).isoformat(),
                    "direction": "in",
                    "chat_id": chat_id,
                    "text": text,
                    "update_id": update["update_id"],
                })
                
                # Process supervisor commands
                cmd_note = _handle_supervisor_command(text, chat_id, update["update_id"])
                if text.strip().startswith("/") and cmd_note is True:
                    new_owner_offset = max(new_owner_offset, update["update_id"] + 1)
                    continue
                
                # Update offset
                new_owner_offset = max(new_owner_offset, update["update_id"] + 1)
                
                # Enqueue as owner task
                enqueue_task({
                    "type": "chat",
                    "text": text,
                    "chat_id": chat_id,
                    "task_id": str(uuid.uuid4())
                })

        # Process architect messages
        for update in architect_updates:
            message = update.get("message") or update.get("edited_message")
            if message:
                # Extract architect message details
                chat_id = message["chat"]["id"]
                text = message.get("text", "___no_text___")

                # Log the architect message
                append_jsonl(DRIVE_ROOT / "logs" / "architect_chat.jsonl", {
                    "ts": datetime.datetime.now(datetime.timezone.utc).isoformat(),
                    "direction": "in",
                    "chat_id": chat_id,
                    "text": text,
                    "update_id": update["update_id"],
                })

                # Create and enqueue task with architect context
                task_id = str(uuid.uuid4())
                enqueue_task(
                    {
                        "type": "architect_chat",
                        "text": text,
                        "chat_id": chat_id,
                        "task_id": task_id,
                        "_architect_context": True,
                    }
                )
                
                # Update architect offset
                new_architect_offset = max(new_architect_offset, update["update_id"] + 1)

        # Save updated offsets
        if new_owner_offset > st["tg_offset"]:
            st["tg_offset"] = new_owner_offset
        if new_architect_offset > st["tg_offset_architect"]:
            st["tg_offset_architect"] = new_architect_offset
        
        if new_owner_offset > st["tg_offset"] or new_architect_offset > st["tg_offset_architect"]:
            save_state(st)

    except Exception as e:
        log.error(f"Error in main loop: {e}")
        time.sleep(5)
