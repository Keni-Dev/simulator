#!/bin/bash
# =============================================================
# Glassmorphism HUD Update Script
# Run: cd /Users/keni/Documents/SKUL/pisiks/tmp/hud-updates && ./apply-hud.sh
# =============================================================

set -e

SRC_DIR="/Users/keni/Documents/SKUL/pisiks/tribosim/src"
TMP_DIR="/Users/keni/Documents/SKUL/pisiks/tmp/hud-updates"

echo "🎨 Applying Glassmorphism HUD updates..."
echo ""

# Fix ownership first
echo "📁 Fixing file permissions..."
sudo chown -R $(whoami):staff "$SRC_DIR"

# Apply the files
echo "📝 Copying updated files..."
cp "$TMP_DIR/globals.css" "$SRC_DIR/app/globals.css"
cp "$TMP_DIR/ChargePanel.tsx" "$SRC_DIR/components/hud/ChargePanel.tsx"
cp "$TMP_DIR/PhysicsReadout.tsx" "$SRC_DIR/components/hud/PhysicsReadout.tsx"
cp "$TMP_DIR/SimulationHUD.tsx" "$SRC_DIR/components/hud/SimulationHUD.tsx"

echo ""
echo "✅ HUD files updated successfully!"
echo ""
echo "🚀 To test the changes, run:"
echo "   cd /Users/keni/Documents/SKUL/pisiks/tribosim && npm run dev"
echo ""
echo "📋 Changes applied:"
echo "   • globals.css - Added glassmorphism CSS variables & animations"  
echo "   • ChargePanel.tsx - Frosted glass panels with Inter font"
echo "   • PhysicsReadout.tsx - Glassmorphic status pill"
echo "   • SimulationHUD.tsx - Container component (unchanged)"
