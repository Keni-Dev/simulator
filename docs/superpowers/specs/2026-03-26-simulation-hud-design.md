# Simulation HUD Design

## Goal
Overlay a heads-up display on top of the full-screen R3F canvas showing live physics data and material selectors for both objects.

## Layout
Two side panels (left + right) overlaid on the canvas edges, with a small bottom-center readout for collision state and velocity. The canvas stays full-screen and interactive underneath.

```
┌─────────────────────────────────────────┐
│ ┌──────────┐               ┌──────────┐ │
│ │ OBJECT L │               │ OBJECT R │ │
│ │          │               │          │ │
│ │ material │               │ material │ │
│ │ buttons  │               │ buttons  │ │
│ │          │               │          │ │
│ │ charge   │               │ charge   │ │
│ │ meter    │               │ meter    │ │
│ │ value    │               │ value    │ │
│ └──────────┘               └──────────┘ │
│            ┌─────────────┐              │
│            │ ● COLLIDING │              │
│            │ v_rel: X.XX │              │
│            └─────────────┘              │
└─────────────────────────────────────────┘
```

## Components

### `SimulationHUD` (`src/components/hud/SimulationHUD.tsx`)
Absolute-positioned overlay covering the full viewport. `pointer-events: none` on the container so canvas interactions pass through. Renders `ChargePanel` (left) + `ChargePanel` (right) + `PhysicsReadout`.

### `ChargePanel` (`src/components/hud/ChargePanel.tsx`)
Props: `side: 'left' | 'right'`

Reads from store:
- `leftMaterial` / `rightMaterial` — current material
- `q1` / `q2` — current charge
- `setLeftMaterial` / `setRightMaterial` — material selector actions

Displays:
- **Label** — "OBJECT L" or "OBJECT R" in `--color-hud` green, mono font, small caps
- **Material selector** — one button per material from `MATERIALS` constant. Active material: green border + text. Inactive: dim. `pointer-events: auto` so clicks work.
- **Charge meter** — vertical bar. Height = `(|charge| / MAX_CHARGE) * 100%`. Color = `--color-positive` (#ff4444) when charge ≥ 0, `--color-negative` (#00ccff) when charge < 0. Contained in a fixed-height track with a center line at 0.
- **Charge value** — large mono number, e.g. `+47.23 μC`. Color matches meter.

### `PhysicsReadout` (`src/components/hud/PhysicsReadout.tsx`)
Reads from store: `isColliding`, `relativeVelocity`

Displays:
- Collision indicator: `● COLLIDING` (green) or `○ SEPARATED` (dim white). The `●` pulses with a CSS animation when colliding.
- Velocity: `v_rel  0.84 u/s` in mono font.
- Positioned bottom-center, small semi-transparent pill.

## Styling
- Panel background: `rgba(15, 15, 17, 0.75)` with `backdrop-filter: blur(8px)`
- Border: `1px solid rgba(0, 255, 0, 0.3)`
- Fonts: JetBrains Mono for numbers/labels, Inter for material names
- All via Tailwind utility classes + inline CSS variables where needed

## Integration
`SimulationCanvas.tsx` — the outer wrapper `div` already has `position` implied by full-screen sizing. Add `position: relative` explicitly, then render `<SimulationHUD />` as a sibling after `<Canvas>`.

## Data flow
All components subscribe to `useSimulationStore` directly via fine-grained selectors. No prop drilling.
