# Triboelectric Engine Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Implement the triboelectric charge transfer equation so rubbing two materials together builds up charge on both objects, visible through their emissive glow.

**Architecture:** Pure math functions in `triboelectric-engine.ts` compute Δq each frame. A `usePhysicsLoop` hook reads collision state from the store, calls those functions, and writes new charge values directly via `useSimulationStore.setState` to guarantee charge conservation. Scene wires in the hook after collision detection.

**Tech Stack:** React Three Fiber (`useFrame`), Zustand (direct `setState`), TypeScript. No test runner — verification is manual via browser console.

---

## File Map

| Action | Path |
|--------|------|
| Create | `tribosim/src/features/physics/utils/triboelectric-engine.ts` |
| Create | `tribosim/src/features/physics/hooks/use-physics-loop.ts` |
| Modify | `tribosim/src/features/physics/index.ts` |
| Modify | `tribosim/src/features/simulation/components/Scene.tsx` |

## Key Constants (already in codebase)

```typescript
// src/constants/index.ts
PHYSICS_CONSTANTS.MAX_CHARGE       // 100 μC
PHYSICS_CONSTANTS.GROUNDING_RATE   // 50 μC/s
PHYSICS_CONSTANTS.CHARGE_PRECISION // 2 decimal places

getFrictionCoefficient(idA: string, idB: string): number  // already exists
```

```typescript
// src/types/index.ts
MaterialType.Insulator // 'insulator'
MaterialType.Conductor // 'conductor'
Material.triboIndex    // number (e.g. Glass=25, Rubber=-70)
Material.id            // string (e.g. 'glass', 'rubber')
Material.type          // MaterialType
```

---

### Task 1: Triboelectric Engine Utility Functions

**Files:**
- Create: `tribosim/src/features/physics/utils/triboelectric-engine.ts`

All pure functions — no React, no side effects.

- [ ] **Step 1: Create the file**

```typescript
// tribosim/src/features/physics/utils/triboelectric-engine.ts
import { getFrictionCoefficient as lookupFrictionCoefficient } from '@/constants'
import type { Material } from '@/types'
import { MaterialType } from '@/types'
import { PHYSICS_CONSTANTS } from '@/constants'

/**
 * Scales the raw triboelectric index difference to keep charge transfer
 * in a visually meaningful range (0–10 μC/s at moderate rubbing speed).
 * Tune this if charge builds too fast or too slow.
 */
const TRIBO_NORMALIZATION_FACTOR = 0.01

/**
 * Returns the friction coefficient k for a material pair.
 * Returns 0 for same-material pairs (no charge transfer).
 * Falls back to 0.3 for unknown pairs.
 */
export function getFrictionCoefficient(materialA: Material, materialB: Material): number {
  if (materialA.id === materialB.id) return 0
  return lookupFrictionCoefficient(materialA.id, materialB.id) ?? 0.3
}

/**
 * Implements Δq = k · v_rel · Δt · (T_A - T_B) · TRIBO_NORMALIZATION_FACTOR
 *
 * Positive deltaQ means material A becomes more positive (loses electrons to B).
 * Returns deltaQ in μC.
 */
export function calculateChargeTransfer(params: {
  frictionCoefficient: number
  relativeVelocity: number
  deltaTime: number
  triboIndexA: number
  triboIndexB: number
}): number {
  const { frictionCoefficient, relativeVelocity, deltaTime, triboIndexA, triboIndexB } = params
  return (
    frictionCoefficient *
    relativeVelocity *
    deltaTime *
    (triboIndexA - triboIndexB) *
    TRIBO_NORMALIZATION_FACTOR
  )
}

/**
 * Applies deltaQ with strict charge conservation.
 * newQ2 = -(newQ1) — not q2 - deltaQ — to prevent floating-point drift.
 * Clamps both charges to ±maxCharge. Rounds to CHARGE_PRECISION decimal places.
 */
export function applyChargeTransfer(
  q1: number,
  _q2: number,
  deltaQ: number,
  maxCharge: number,
): { newQ1: number; newQ2: number } {
  const precision = PHYSICS_CONSTANTS.CHARGE_PRECISION
  const factor = 10 ** precision

  const rawQ1 = q1 + deltaQ
  const clampedQ1 = Math.max(-maxCharge, Math.min(maxCharge, rawQ1))
  const newQ1 = Math.round(clampedQ1 * factor) / factor

  // Enforce conservation: newQ2 is always the mirror of newQ1
  const newQ2 = Math.round(-newQ1 * factor) / factor

  return { newQ1, newQ2 }
}

/**
 * Exponential discharge toward 0 (conductor grounding to human body).
 * Snaps to exactly 0 if within 0.01 μC to prevent infinite decay.
 */
export function applyGroundingEffect(
  charge: number,
  groundingRate: number,
  deltaTime: number,
): number {
  const decayed = charge * Math.exp(-groundingRate * deltaTime)
  return Math.abs(decayed) < 0.01 ? 0 : decayed
}

/**
 * Returns true if charge conservation holds within tolerance.
 * Only meaningful for insulator pairs (conductor grounding is implicit).
 */
export function isConservationMaintained(q1: number, q2: number, tolerance: number): boolean {
  return Math.abs(q1 + q2) <= tolerance
}
```

---

### Task 2: Physics Loop Hook

**Files:**
- Create: `tribosim/src/features/physics/hooks/use-physics-loop.ts`

Reads collision state every frame, applies the triboelectric engine, writes new charges directly to the Zustand store via `setState` (not the `updateCharges` action) to guarantee conservation.

- [ ] **Step 1: Create the file**

```typescript
// tribosim/src/features/physics/hooks/use-physics-loop.ts
'use client'

import { useFrame } from '@react-three/fiber'
import { useSimulationStore } from '@/stores/simulation-store'
import { PHYSICS_CONSTANTS } from '@/constants'
import { MaterialType } from '@/types'
import {
  getFrictionCoefficient,
  calculateChargeTransfer,
  applyChargeTransfer,
  applyGroundingEffect,
  isConservationMaintained,
} from '../utils/triboelectric-engine'

const CONSERVATION_TOLERANCE = 0.001

export function usePhysicsLoop(): void {
  useFrame((_, delta) => {
    const state = useSimulationStore.getState()
    const {
      isColliding,
      relativeVelocity,
      leftMaterial,
      rightMaterial,
      q1,
      q2,
    } = state

    if (!isColliding || relativeVelocity <= 0) return

    const k = getFrictionCoefficient(leftMaterial, rightMaterial)
    if (k === 0) return // same material — no charge transfer

    const deltaQ = calculateChargeTransfer({
      frictionCoefficient: k,
      relativeVelocity,
      deltaTime: delta,
      triboIndexA: leftMaterial.triboIndex,
      triboIndexB: rightMaterial.triboIndex,
    })

    const leftIsConductor = leftMaterial.type === MaterialType.Conductor
    const rightIsConductor = rightMaterial.type === MaterialType.Conductor

    if (!leftIsConductor && !rightIsConductor) {
      // Both insulators: conserved charge transfer
      const { newQ1, newQ2 } = applyChargeTransfer(q1, q2, deltaQ, PHYSICS_CONSTANTS.MAX_CHARGE)
      useSimulationStore.setState({ q1: newQ1, q2: newQ2 })

      if (!isConservationMaintained(newQ1, newQ2, CONSERVATION_TOLERANCE)) {
        console.warn('[physics] Conservation violated:', newQ1, newQ2, 'sum:', newQ1 + newQ2)
      }
    } else if (!leftIsConductor && rightIsConductor) {
      // Left = insulator, Right = conductor
      // Insulator charges up; conductor immediately grounds
      const precision = 10 ** PHYSICS_CONSTANTS.CHARGE_PRECISION
      const newQ1 = Math.round(
        Math.max(-PHYSICS_CONSTANTS.MAX_CHARGE, Math.min(PHYSICS_CONSTANTS.MAX_CHARGE, q1 + deltaQ)) * precision,
      ) / precision
      const newQ2 = applyGroundingEffect(q2, PHYSICS_CONSTANTS.GROUNDING_RATE, delta)
      useSimulationStore.setState({ q1: newQ1, q2: newQ2 })
    } else if (leftIsConductor && !rightIsConductor) {
      // Left = conductor, Right = insulator
      const precision = 10 ** PHYSICS_CONSTANTS.CHARGE_PRECISION
      const newQ1 = applyGroundingEffect(q1, PHYSICS_CONSTANTS.GROUNDING_RATE, delta)
      const newQ2 = Math.round(
        Math.max(-PHYSICS_CONSTANTS.MAX_CHARGE, Math.min(PHYSICS_CONSTANTS.MAX_CHARGE, q2 - deltaQ)) * precision,
      ) / precision
      useSimulationStore.setState({ q1: newQ1, q2: newQ2 })
    } else {
      // Both conductors: ground both
      const newQ1 = applyGroundingEffect(q1, PHYSICS_CONSTANTS.GROUNDING_RATE, delta)
      const newQ2 = applyGroundingEffect(q2, PHYSICS_CONSTANTS.GROUNDING_RATE, delta)
      useSimulationStore.setState({ q1: newQ1, q2: newQ2 })
    }
  })
}
```

---

### Task 3: Wire Up — Barrel Export + Scene

**Files:**
- Modify: `tribosim/src/features/physics/index.ts`
- Modify: `tribosim/src/features/simulation/components/Scene.tsx`

- [ ] **Step 1: Update the barrel export**

Replace the entire contents of `tribosim/src/features/physics/index.ts` with:

```typescript
export { useCollisionDetection } from './hooks/use-collision-detection'
export { usePhysicsLoop } from './hooks/use-physics-loop'
export {
  computeBoundingBox,
  checkAABBCollision,
  calculateOverlapDepth,
  calculateRelativeVelocity,
} from './utils/collision'
export { registerMesh, unregisterMesh, getMesh } from './utils/mesh-registry'
export {
  getFrictionCoefficient,
  calculateChargeTransfer,
  applyChargeTransfer,
  applyGroundingEffect,
  isConservationMaintained,
} from './utils/triboelectric-engine'
```

- [ ] **Step 2: Add `usePhysicsLoop` to Scene**

In `tribosim/src/features/simulation/components/Scene.tsx`:

Replace the existing physics import line (which currently only imports `useCollisionDetection`) with:
```typescript
import { useCollisionDetection, usePhysicsLoop } from '@/features/physics'
```

Add call inside the `Scene` component body, after `useCollisionDetection()`:
```typescript
  usePhysicsLoop()
```

The hook call order matters: collision detection writes `isColliding` and `relativeVelocity`, then the physics loop reads them on the same frame.

---

### Task 4: Manual Verification

- [ ] **Step 1: Start the dev server**

```bash
cd tribosim
npm run dev
```

Open `http://localhost:3000`.

- [ ] **Step 2: Add a temporary charge logger**

In `tribosim/src/features/physics/hooks/use-physics-loop.ts`, inside `useFrame`, at the very end (after all `setState` calls), add:

```typescript
    const { q1: newQ1val, q2: newQ2val } = useSimulationStore.getState()
    if (Math.abs(newQ1val) > 0.01) {
      console.log('[physics] q1:', newQ1val.toFixed(2), 'q2:', newQ2val.toFixed(2), 'sum:', (newQ1val + newQ2val).toFixed(4))
    }
```

- [ ] **Step 3: Verify the checklist**

Open DevTools Console. Filter by `[physics]`.

| Check | How to verify |
|-------|---------------|
| Glass + Silk rubbing → q1 changes | See `[physics]` logs while overlapping and moving hands |
| `q1 + q2 = 0.0000` at all times | Check `sum:` in console — must stay near 0 |
| Faster rubbing = faster charge | Move hands faster; watch charge accumulate quicker |
| Stop rubbing → charges hold | Overlap objects but keep hands still; charges stop changing |
| Copper vs Glass → Copper stays ~0 | Select Copper material on one side; rub against Glass |
| Charges cap at ±100 μC | Keep rubbing; watch values stop at 100.00 / -100.00 |
| Same materials → no charge | Set both sides to Glass; rub; no `[physics]` logs appear |

- [ ] **Step 4: Tune normalization if needed**

If charges build too fast: reduce `TRIBO_NORMALIZATION_FACTOR` in `triboelectric-engine.ts` (try `0.001`)
If charges build too slow: increase it (try `0.05`)

- [ ] **Step 5: Remove the temporary console log**

Delete the `console.log` block added in Step 2.
