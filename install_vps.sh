#!/bin/bash
set -e

echo "====================================="
echo "Ouroboros VPS Installation Script"
echo "====================================="
echo ""

# Colors
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
RED='\033[0;31m'
NC='\033[0m'

# Get script directory
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
cd "$SCRIPT_DIR"

echo -e "${GREEN}[1/8]${NC} Checking mise installation..."
if ! command -v mise &> /dev/null; then
    echo -e "${YELLOW}mise not found. Installing mise...${NC}"
    curl https://mise.run | sh
    export PATH="$HOME/.local/bin:$PATH"
    echo 'export PATH="$HOME/.local/bin:$PATH"' >> ~/.bashrc
    
    if ! command -v mise &> /dev/null; then
        echo -e "${RED}Failed to install mise. Please install manually: https://mise.jdx.dev${NC}"
        exit 1
    fi
else
    echo -e "${GREEN}✓ mise is already installed${NC}"
fi

echo ""
echo -e "${GREEN}[2/8]${NC} Setting up environment file..."
if [ ! -f ".env" ]; then
    echo -e "${YELLOW}Creating .env from .env.example...${NC}"
    cp .env.example .env
    echo -e "${YELLOW}⚠️  IMPORTANT: Edit .env file with your actual credentials!${NC}"
    echo -e "${YELLOW}   Run: nano .env${NC}"
else
    echo -e "${GREEN}✓ .env file already exists${NC}"
fi

echo ""
echo -e "${GREEN}[3/8]${NC} Installing Python via mise..."
mise install

echo ""
echo -e "${GREEN}[4/8]${NC} Installing Python dependencies..."
mise exec -- pip install -r requirements.txt

echo ""
echo -e "${GREEN}[5/8]${NC} Installing Playwright browsers..."
mise exec -- playwright install

echo ""
echo -e "${GREEN}[6/8]${NC} Creating data directory..."
DATA_DIR="$HOME/ouroboros_data"
mkdir -p "$DATA_DIR"/{state,logs,memory,index,locks,archive}
echo -e "${GREEN}✓ Created $DATA_DIR${NC}"

echo ""
echo -e "${GREEN}[7/8]${NC} Installing systemd service..."
SERVICE_FILE="$SCRIPT_DIR/ouroboros.service"
SYSTEMD_USER_DIR="$HOME/.config/systemd/user"

if [ -f "$SERVICE_FILE" ]; then
    mkdir -p "$SYSTEMD_USER_DIR"
    cp "$SERVICE_FILE" "$SYSTEMD_USER_DIR/ouroboros.service"
    
    systemctl --user daemon-reload
    systemctl --user enable ouroboros.service
    echo -e "${GREEN}✓ Systemd service installed and enabled${NC}"
else
    echo -e "${RED}✗ Service file not found: $SERVICE_FILE${NC}"
    exit 1
fi

echo ""
echo -e "${GREEN}[8/8]${NC} Starting Ouroboros service..."
systemctl --user start ouroboros.service

echo ""
echo -e "${GREEN}====================================="
echo "Installation Complete!"
echo "=====================================${NC}"
echo ""
echo "Next steps:"
echo "  1. Edit credentials: ${YELLOW}nano .env${NC}"
echo "  2. Restart service: ${YELLOW}systemctl --user restart ouroboros.service${NC}"
echo ""
echo "Useful commands:"
echo "  • View status:  ${YELLOW}systemctl --user status ouroboros.service${NC}"
echo "  • View logs:    ${YELLOW}journalctl --user -u ouroboros.service -f${NC}"
echo "  • Stop service: ${YELLOW}systemctl --user stop ouroboros.service${NC}"
echo "  • Restart:      ${YELLOW}systemctl --user restart ouroboros.service${NC}"
echo ""
echo "Data location: ${YELLOW}$DATA_DIR${NC}"
echo ""
