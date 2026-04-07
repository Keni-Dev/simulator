# Glassmorphism HUD Implementation

## Overview

This update transforms the TriboSim HUD from an amber/industrial aesthetic to a modern **glassmorphism** design with:

- **Frosted glass panels** with `backdrop-filter: blur(16px)`
- **Inter font** for clean, readable UI text
- **Subtle animations** for active states
- **High contrast** text on translucent backgrounds

## Design Tokens

```css
--hud-glass-bg: rgba(255, 255, 255, 0.04)
--hud-glass-border: rgba(255, 255, 255, 0.08)
--hud-blur: 16px
--color-positive: #f87171 (red-400)
--color-negative: #22d3ee (cyan-400)
```

## Files Changed

| File | Changes |
|------|---------|
| `globals.css` | Added glassmorphism CSS variables and animations |
| `ChargePanel.tsx` | Redesigned with glass effect, Inter font, rounded corners |
| `PhysicsReadout.tsx` | Glassmorphic pill with subtle glow effects |
| `SimulationHUD.tsx` | No changes (container only) |

## How to Apply

Run the following command:

```bash
cd /Users/keni/Documents/SKUL/pisiks/tmp/hud-updates
./apply-hud.sh
```

This will:
1. Fix file permissions (requires sudo password)
2. Copy all updated files to `tribosim/src/`

## Visual Preview

### ChargePanel (Left/Right)
- Translucent panel at top corners
- Material selector with hover states
- Vertical charge meter with glow
- Digital readout with polarity indicators

### PhysicsReadout (Bottom Center)
- Pill-shaped status bar
- Contact indicator with pulse animation
- Velocity display

## Technical Notes

- Uses `backdrop-filter` with `saturate(150%)` for enhanced glass effect
- All animations respect user's motion preferences via CSS
- Maintains `pointer-events: none` on overlay, `auto` on interactive elements
- Performance-optimized with minimal blur radius (16px)
