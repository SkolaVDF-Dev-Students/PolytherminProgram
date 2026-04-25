#!/bin/bash

# ============================
#  CONFIG
# ============================
DEVELOPER_MODE=false   # true = dev build
DIST_DIR="dist"

echo "--------------------------------------"
echo "   Welcome to the build script (Linux)"
echo "--------------------------------------"

# ============================
#  CHECK / INSTALL MPREMOTE
# ============================
if [ "$DEVELOPER_MODE" = false ]; then
    echo "[INFO] Kontroluji mpremote..."

    if ! command -v mpremote >/dev/null 2>&1; then
        echo "[INFO] mpremote nenalezen – instaluji..."
        pip install mpremote || {
            echo "[ERROR] Instalace mpremote selhala."
            exit 1
        }
    else
        echo "[INFO] mpremote OK"
    fi
else
    echo "[DEV MODE] Přeskakuji kontrolu mpremote."
fi

# ============================
#  PREPARE DIST
# ============================
echo "[INFO] Čistím a vytvářím složku $DIST_DIR..."
rm -rf "$DIST_DIR"
mkdir "$DIST_DIR"

echo "[INFO] Kopíruji main.py a libs..."
cp ./main.py "$DIST_DIR"/
cp -r ./libs "$DIST_DIR"/

# ============================
#  VERSIONING
# ============================
if [ "$DEVELOPER_MODE" = true ]; then
    echo "[DEV MODE] Zapisuji verzi: dev"
    echo "dev" > "$DIST_DIR/version.txt"
else
    read -p "Zadej verzi buildu (např. 1.0.0): " VERSION
    echo "[INFO] Verze: $VERSION"
    echo "$VERSION" > "$DIST_DIR/version.txt"
fi

# ============================
#  CREATE ZIP (ONLY OFFICIAL)
# ============================
if [ "$DEVELOPER_MODE" = false ]; then
    echo "[INFO] Vytvářím dist.zip..."
    rm -f dist.zip
    zip -r dist.zip "$DIST_DIR" >/dev/null
fi

# ============================
#  RUN MPREMOTE
# ============================
cd "$DIST_DIR" || exit 1

echo "[INFO] Upload přes mpremote..."
python -m mpremote connect auto fs cp -r . :

echo "[INFO] Hotovo!"
