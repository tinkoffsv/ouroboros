# Ouroboros VPS Deployment

Quick setup guide for deploying Ouroboros on a VPS.

## Quick Start

```bash
# 1. Clone repository
git clone https://github.com/tinkoffsv/ouroboros.git
cd ouroboros

# 2. Run installation script
./install_vps.sh

# 3. Edit credentials (if not done before)
nano .env

# 4. Restart service
systemctl --user restart ouroboros.service
```

## Prerequisites

- Linux VPS (Ubuntu 20.04+ recommended)
- Python 3.10+
- Internet connection
- Telegram bot token
- API keys (OpenRouter, etc.)

## Configuration

Edit `.env` file with your credentials:

- `GITHUB_TOKEN` - GitHub personal access token
- `TELEGRAM_BOT_TOKEN` - Telegram bot token from @BotFather
- `OPENROUTER_API_KEY` - OpenRouter API key
- `TOTAL_BUDGET` - Maximum spend limit in USD

## Management

### Service Control

```bash
# Start
systemctl --user start ouroboros.service

# Stop
systemctl --user stop ouroboros.service

# Restart
systemctl --user restart ouroboros.service

# Status
systemctl --user status ouroboros.service

# View logs
journalctl --user -u ouroboros.service -f
```

### Data Location

All persistent data stored in `~/ouroboros_data/`:
- `state/` - Runtime state
- `logs/` - Application logs
- `memory/` - Agent memory
- `index/` - Code indexes
- `locks/` - Lock files
- `archive/` - Archived data

## Manual Setup

If you prefer manual installation:

```bash
# 1. Install mise
curl https://mise.run | sh
export PATH="$HOME/.local/bin:$PATH"

# 2. Copy environment template
cp .env.example .env
nano .env  # Edit with your credentials

# 3. Install Python and dependencies
mise install
mise exec -- pip install -r requirements.txt
mise exec -- playwright install

# 4. Create data directory
mkdir -p ~/ouroboros_data/{state,logs,memory,index,locks,archive}

# 5. Install systemd service
mkdir -p ~/.config/systemd/user
cp ouroboros.service ~/.config/systemd/user/
systemctl --user daemon-reload
systemctl --user enable ouroboros.service
systemctl --user start ouroboros.service
```

## Troubleshooting

### Service won't start
```bash
journalctl --user -u ouroboros.service -n 50
```

### Missing dependencies
```bash
cd ~/ouroboros
mise exec -- pip install -r requirements.txt --upgrade
```

### Reset state
```bash
systemctl --user stop ouroboros.service
rm -rf ~/ouroboros_data/state/*
systemctl --user start ouroboros.service
```

## Differences from Colab

- No Google Drive mount (uses local filesystem)
- Environment variables via `.env` file
- Systemd service management
- mise for Python version management
- Direct filesystem paths instead of `/content/`
