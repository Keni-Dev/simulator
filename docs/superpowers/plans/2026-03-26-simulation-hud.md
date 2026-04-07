# Simulation HUD Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Add a HUD overlay on the full-screen canvas showing live charge data, material selectors, and collision state.

**Architecture:** Three focused components (`PhysicsReadout`, `ChargePanel`, `SimulationHUD`) rendered as an `position: absolute` overlay inside `SimulationCanvas`. Each component subscribes directly to `useSimulationStore` with fine-grained selectors. The overlay container has `pointer-events: none`; only material selector buttons have `pointer-events: auto`.

**Tech Stack:** React, Tailwind v4, Zustand, inline styles (CSS custom properties from `globals.css`), no test runner — verification is visual.

---

## File Map

| Action | Path |
|--------|------|
| Create | `tribosim/src/components/hud/PhysicsReadout.tsx` |
| Create | `tribosim/src/components/hud/ChargePanel.tsx` |
| Create | `tribosim/src/components/hud/SimulationHUD.tsx` |
| Modify | `tribosim/src/app/globals.css` |
| Modify | `tribosim/src/features/simulation/components/SimulationCanvas.tsx` |

## Key codebase facts

```typescript
// src/stores/simulation-store.ts — available selectors
s.q1, s.q2           // number — charge in μC
s.isColliding        // boolean
s.relativeVelocity   // number — world units/s
s.leftMaterial       // Material
s.rightMaterial      // Material
s.setLeftMaterial    // (material: Material) => void
s.setRightMaterial   // (material: Material) => void

// src/constants/index.ts
MATERIALS            // readonly Material[] — 5 items: glass, silk, fur, rubber, copper
PHYSICS_CONSTANTS.MAX_CHARGE  // 100

// src/app/globals.css — CSS custom properties
--color-hud: #00ff00
--color-positive: #ff4444
--color-negative: #00ccff
--bg-primary: #0f0f11
--font-mono: 'JetBrains Mono', monospace
--font-sans: 'Inter', sans-serif
```

---

### Task 1: PhysicsReadout + pulse keyframe

**Files:**
- Create: `tribosim/src/components/hud/PhysicsReadout.tsx`
- Modify: `tribosim/src/app/globals.css`

- [ ] **Step 1: Add pulse keyframe to globals.css**

Append to `tribosim/src/app/globals.css`:

```css
@keyframes hud-pulse {
  0%, 100% { opacity: 1; }
  50%       { opacity: 0.25; }
}
```

- [ ] **Step 2: Create PhysicsReadout**

```tsx
// tribosim/src/components/hud/PhysicsReadout.tsx
'use client'

import { useSimulationStore } from '@/stores/simulation-store'

export function PhysicsReadout() {
  const isColliding = useSimulationStore((s) => s.isColliding)
  const relativeVelocity = useSimulationStore((s) => s.relativeVelocity)

  return (
    <div
      style={{
        position: 'absolute',
        bottom: 24,
        left: '50%',
        transform: 'translateX(-50%)',
        background: 'rgba(15, 15, 17, 0.75)',
        backdropFilter: 'blur(8px)',
        border: '1px solid rgba(0, 255, 0, 0.3)',
        borderRadius: 8,
        padding: '8px 20px',
        display: 'flex',
        flexDirection: 'column',
        alignItems: 'center',
        gap: 4,
        pointerEvents: 'none',
        whiteSpace: 'nowrap',
      }}
    >
      {/* Collision indicator */}
      <div
        style={{
          display: 'flex',
          alignItems: 'center',
          gap: 8,
          fontFamily: 'var(--font-mono)',
          fontSize: 11,
          letterSpacing: 2,
          color: isColliding ? 'var(--color-hud)' : 'rgba(255,255,255,0.25)',
        }}
      >
        <span
          style={{
            animation: isColliding ? 'hud-pulse 1s ease-in-out infinite' : 'none',
          }}
        >
          {isColliding ? '●' : '○'}
        </span>
        {isColliding ? 'COLLIDING' : 'SEPARATED'}
      </div>

      {/* Velocity */}
      <div
        style={{
          fontFamily: 'var(--font-mono)',
          fontSize: 11,
          color: 'rgba(255,255,255,0.4)',
          letterSpacing: 1,
        }}
      >
        v_rel&nbsp;&nbsp;{relativeVelocity.toFixed(2)} u/s
      </div>
    </div>
  )
}
```

---

### Task 2: ChargePanel

**Files:**
- Create: `tribosim/src/components/hud/ChargePanel.tsx`

- [ ] **Step 1: Create ChargePanel**

```tsx
// tribosim/src/components/hud/ChargePanel.tsx
'use client'

import { useSimulationStore } from '@/stores/simulation-store'
import { MATERIALS, PHYSICS_CONSTANTS } from '@/constants'

interface ChargePanelProps {
  side: 'left' | 'right'
}

export function ChargePanel({ side }: ChargePanelProps) {
  const charge = useSimulationStore((s) => (side === 'left' ? s.q1 : s.q2))
  const material = useSimulationStore((s) =>
    side === 'left' ? s.leftMaterial : s.rightMaterial,
  )
  const setLeftMaterial = useSimulationStore((s) => s.setLeftMaterial)
  const setRightMaterial = useSimulationStore((s) => s.setRightMaterial)
  const setMaterial = side === 'left' ? setLeftMaterial : setRightMaterial

  const isPositive = charge >= 0
  const chargeColor = isPositive ? 'var(--color-positive)' : 'var(--color-negative)'
  const meterFill = `${(Math.abs(charge) / PHYSICS_CONSTANTS.MAX_CHARGE) * 50}%`
  const sign = charge > 0 ? '+' : ''

  return (
    <div
      style={{
        position: 'absolute',
        top: '50%',
        transform: 'translateY(-50%)',
        ...(side === 'left' ? { left: 16 } : { right: 16 }),
        width: 148,
        background: 'rgba(15, 15, 17, 0.75)',
        backdropFilter: 'blur(8px)',
        border: '1px solid rgba(0, 255, 0, 0.3)',
        borderRadius: 8,
        padding: 12,
        display: 'flex',
        flexDirection: 'column',
        gap: 10,
        pointerEvents: 'none',
      }}
    >
      {/* Label */}
      <div
        style={{
          fontFamily: 'var(--font-mono)',
          fontSize: 10,
          letterSpacing: 3,
          color: 'var(--color-hud)',
          textTransform: 'uppercase' as const,
        }}
      >
        OBJECT {side === 'left' ? 'L' : 'R'}
      </div>

      {/* Material selector */}
      <div
        style={{
          display: 'flex',
          flexDirection: 'column' as const,
          gap: 3,
          pointerEvents: 'auto',
        }}
      >
        {MATERIALS.map((m) => (
          <button
            key={m.id}
            onClick={() => setMaterial(m)}
            style={{
              background: 'transparent',
              border: `1px solid ${
                material.id === m.id
                  ? 'var(--color-hud)'
                  : 'rgba(255,255,255,0.12)'
              }`,
              borderRadius: 4,
              padding: '4px 8px',
              fontFamily: 'var(--font-sans)',
              fontSize: 11,
              color:
                material.id === m.id
                  ? 'var(--color-hud)'
                  : 'rgba(255,255,255,0.4)',
              cursor: 'pointer',
              textAlign: 'left' as const,
              transition: 'border-color 0.15s, color 0.15s',
            }}
          >
            {m.name}
          </button>
        ))}
      </div>

      {/* Charge display: meter + value */}
      <div style={{ display: 'flex', gap: 10, alignItems: 'center' }}>
        {/* Vertical meter track */}
        <div
          style={{
            width: 10,
            height: 80,
            background: 'rgba(255,255,255,0.08)',
            borderRadius: 5,
            position: 'relative' as const,
            overflow: 'hidden',
            flexShrink: 0,
          }}
        >
          {/* Zero line */}
          <div
            style={{
              position: 'absolute',
              top: '50%',
              left: 0,
              right: 0,
              height: 1,
              background: 'rgba(255,255,255,0.25)',
            }}
          />
          {/* Fill — grows up from center for positive, down for negative */}
          <div
            style={{
              position: 'absolute',
              left: 0,
              right: 0,
              height: meterFill,
              ...(isPositive ? { bottom: '50%' } : { top: '50%' }),
              background: chargeColor,
              borderRadius: 5,
              transition: 'height 0.08s linear, background 0.1s ease-out',
            }}
          />
        </div>

        {/* Numeric value */}
        <div
          style={{
            fontFamily: 'var(--font-mono)',
            color:
              Math.abs(charge) < 0.01 ? 'rgba(255,255,255,0.3)' : chargeColor,
            transition: 'color 0.1s ease-out',
          }}
        >
          <div style={{ fontSize: 15, fontWeight: 700, lineHeight: 1.2 }}>
            {sign}{charge.toFixed(2)}
          </div>
          <div style={{ fontSize: 10, opacity: 0.5, marginTop: 2 }}>μC</div>
        </div>
      </div>
    </div>
  )
}
```

---

### Task 3: SimulationHUD + SimulationCanvas integration

**Files:**
- Create: `tribosim/src/components/hud/SimulationHUD.tsx`
- Modify: `tribosim/src/features/simulation/components/SimulationCanvas.tsx`

- [ ] **Step 1: Create SimulationHUD**

```tsx
// tribosim/src/components/hud/SimulationHUD.tsx
'use client'

import { ChargePanel } from './ChargePanel'
import { PhysicsReadout } from './PhysicsReadout'

export function SimulationHUD() {
  return (
    <div
      style={{
        position: 'absolute',
        inset: 0,
        pointerEvents: 'none',
        zIndex: 10,
      }}
    >
      <ChargePanel side="left" />
      <ChargePanel side="right" />
      <PhysicsReadout />
    </div>
  )
}
```

- [ ] **Step 2: Integrate into SimulationCanvas**

Read `tribosim/src/features/simulation/components/SimulationCanvas.tsx` first. Then make two changes:

**Add the import** at the top (after the existing imports):
```tsx
import { SimulationHUD } from '@/components/hud/SimulationHUD'
```

**Update the outer wrapper div** — add `position: 'relative'` to its style, and add `<SimulationHUD />` after `</Suspense>`:

```tsx
    <div
      style={{
        position: 'relative',
        width: '100vw',
        height: '100vh',
        background: '#0f0f11',
        overflow: 'hidden',
      }}
    >
      <Suspense fallback={<CanvasLoader />}>
        <Canvas
          camera={{
            position: [
              CAMERA_DEFAULT_POSITION.x,
              CAMERA_DEFAULT_POSITION.y,
              CAMERA_DEFAULT_POSITION.z,
            ],
            fov: CAMERA_DEFAULT_FOV,
          }}
          gl={{
            antialias: true,
            alpha: false,
            powerPreference: 'high-performance',
          }}
          dpr={[1, 2]}
          style={{ width: '100%', height: '100%' }}
        >
          <Scene />
        </Canvas>
      </Suspense>
      <SimulationHUD />
    </div>
```

- [ ] **Step 3: Verify visually**

Run `npm run dev` in `tribosim/`. Open `http://localhost:3000`. Confirm:

| Check | Expected |
|-------|----------|
| Two side panels visible | Left panel on left edge, right panel on right edge, both vertically centered |
| Bottom readout visible | Small pill at bottom center showing ○ SEPARATED and v_rel |
| Material buttons work | Clicking a material name highlights it and changes the 3D object color |
| Charge meter animates | Rub objects together — meter fills red/cyan as charge builds |
| Collision indicator | Pulses green ● COLLIDING when objects overlap |
| Canvas still interactive | Hand tracking / OrbitControls still work — clicks on canvas pass through |
