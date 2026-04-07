# Collision Detection Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Implement per-frame AABB collision detection between the two material meshes, writing `isColliding` and `relativeVelocity` into the simulation store every frame.

**Architecture:** A module-level mesh registry holds refs to both `THREE.Group` objects. `MaterialMesh` registers its group on mount and deregisters on unmount. A `useFrame` hook reads both groups, computes world-space AABBs, checks overlap, calculates relative velocity from stored previous positions, and calls `setCollisionState` on the store.

**Tech Stack:** React Three Fiber (`useFrame`), Three.js (`THREE.Box3`, `THREE.Vector3`, `THREE.Group`), Zustand simulation store, TypeScript.

> **No test runner is configured** — verification steps are manual: open the dev server, add a temporary `console.log`, and confirm store values in DevTools.

---

## File Map

| Action | Path |
|--------|------|
| Create | `tribosim/src/features/physics/utils/mesh-registry.ts` |
| Create | `tribosim/src/features/physics/utils/collision.ts` |
| Create | `tribosim/src/features/physics/hooks/use-collision-detection.ts` |
| Create | `tribosim/src/features/physics/index.ts` |
| Modify | `tribosim/src/features/simulation/components/MaterialMesh.tsx` |
| Modify | `tribosim/src/features/simulation/components/Scene.tsx` |

---

### Task 1: Mesh Registry

**Files:**
- Create: `tribosim/src/features/physics/utils/mesh-registry.ts`

The registry is a plain module-level `Map`. No React context needed — there is exactly one left and one right mesh in the scene.

- [ ] **Step 1: Create the registry file**

```typescript
// tribosim/src/features/physics/utils/mesh-registry.ts
import * as THREE from 'three'

type MeshSide = 'left' | 'right'

const registry = new Map<MeshSide, THREE.Group>()

export function registerMesh(side: MeshSide, group: THREE.Group): void {
  registry.set(side, group)
}

export function unregisterMesh(side: MeshSide): void {
  registry.delete(side)
}

export function getMesh(side: MeshSide): THREE.Group | undefined {
  return registry.get(side)
}
```

- [ ] **Step 2: Commit**

```bash
cd tribosim
git add src/features/physics/utils/mesh-registry.ts
git commit -m "feat(physics): add mesh registry for collision detection"
```

---

### Task 2: Collision Utility Functions

**Files:**
- Create: `tribosim/src/features/physics/utils/collision.ts`

Pure functions — no React, no side effects, easy to reason about and replace.

- [ ] **Step 1: Create the collision utilities file**

```typescript
// tribosim/src/features/physics/utils/collision.ts
import * as THREE from 'three'

/**
 * Returns a world-space AABB for the given group/mesh.
 * setFromObject traverses all children and accounts for world matrix
 * (position, rotation, scale), so the box is in world coordinates.
 */
export function computeBoundingBox(group: THREE.Group): THREE.Box3 {
  return new THREE.Box3().setFromObject(group)
}

/**
 * Returns true if boxA and boxB overlap in all three axes.
 * Uses Three.js's built-in intersectsBox check.
 */
export function checkAABBCollision(boxA: THREE.Box3, boxB: THREE.Box3): boolean {
  return boxA.intersectsBox(boxB)
}

/**
 * Returns the minimum penetration depth across all three axes.
 * Returns 0 if the boxes do not overlap.
 * Useful for scaling charge transfer rate by collision intensity.
 */
export function calculateOverlapDepth(boxA: THREE.Box3, boxB: THREE.Box3): number {
  const overlapX = Math.min(boxA.max.x, boxB.max.x) - Math.max(boxA.min.x, boxB.min.x)
  const overlapY = Math.min(boxA.max.y, boxB.max.y) - Math.max(boxA.min.y, boxB.min.y)
  const overlapZ = Math.min(boxA.max.z, boxB.max.z) - Math.max(boxA.min.z, boxB.min.z)

  if (overlapX <= 0 || overlapY <= 0 || overlapZ <= 0) return 0
  return Math.min(overlapX, overlapY, overlapZ)
}

/**
 * Computes the scalar magnitude of the relative velocity between two objects.
 * velocityA = (posA - prevPosA) / deltaTime
 * velocityB = (posB - prevPosB) / deltaTime
 * returns |velocityA - velocityB| in world-units per second
 *
 * This is v_rel in the triboelectric equation.
 */
export function calculateRelativeVelocity(
  posA: THREE.Vector3,
  prevPosA: THREE.Vector3,
  posB: THREE.Vector3,
  prevPosB: THREE.Vector3,
  deltaTime: number,
): number {
  if (deltaTime <= 0) return 0

  const velA = new THREE.Vector3().subVectors(posA, prevPosA).divideScalar(deltaTime)
  const velB = new THREE.Vector3().subVectors(posB, prevPosB).divideScalar(deltaTime)

  return new THREE.Vector3().subVectors(velA, velB).length()
}
```

- [ ] **Step 2: Commit**

```bash
git add src/features/physics/utils/collision.ts
git commit -m "feat(physics): add AABB collision utility functions"
```

---

### Task 3: Collision Detection Hook

**Files:**
- Create: `tribosim/src/features/physics/hooks/use-collision-detection.ts`

This hook runs inside the R3F render loop. It reads both groups from the registry, computes their bounding boxes, checks overlap, and writes to the store. Previous positions are stored in `useRef` so velocity can be computed across frames.

- [ ] **Step 1: Create the hook file**

```typescript
// tribosim/src/features/physics/hooks/use-collision-detection.ts
'use client'

import { useRef } from 'react'
import { useFrame } from '@react-three/fiber'
import * as THREE from 'three'
import { useSimulationStore } from '@/stores/simulation-store'
import { getMesh } from '../utils/mesh-registry'
import {
  computeBoundingBox,
  checkAABBCollision,
  calculateRelativeVelocity,
} from '../utils/collision'

export function useCollisionDetection(): void {
  const prevPosLeft = useRef(new THREE.Vector3())
  const prevPosRight = useRef(new THREE.Vector3())
  const setCollisionState = useSimulationStore((s) => s.setCollisionState)

  useFrame((_, delta) => {
    const leftGroup = getMesh('left')
    const rightGroup = getMesh('right')

    if (!leftGroup || !rightGroup) return

    const posLeft = leftGroup.position.clone()
    const posRight = rightGroup.position.clone()

    const boxLeft = computeBoundingBox(leftGroup)
    const boxRight = computeBoundingBox(rightGroup)

    const colliding = checkAABBCollision(boxLeft, boxRight)

    if (colliding) {
      const relVel = calculateRelativeVelocity(
        posLeft,
        prevPosLeft.current,
        posRight,
        prevPosRight.current,
        delta,
      )
      setCollisionState(true, relVel)
    } else {
      setCollisionState(false, 0)
    }

    // Store positions for next frame's velocity computation
    prevPosLeft.current.copy(posLeft)
    prevPosRight.current.copy(posRight)
  })
}
```

- [ ] **Step 2: Commit**

```bash
git add src/features/physics/hooks/use-collision-detection.ts
git commit -m "feat(physics): add useCollisionDetection hook"
```

---

### Task 4: Barrel Export

**Files:**
- Create: `tribosim/src/features/physics/index.ts`

- [ ] **Step 1: Create the barrel export**

```typescript
// tribosim/src/features/physics/index.ts
export { useCollisionDetection } from './hooks/use-collision-detection'
export {
  computeBoundingBox,
  checkAABBCollision,
  calculateOverlapDepth,
  calculateRelativeVelocity,
} from './utils/collision'
export { registerMesh, unregisterMesh, getMesh } from './utils/mesh-registry'
```

- [ ] **Step 2: Commit**

```bash
git add src/features/physics/index.ts
git commit -m "feat(physics): add barrel export for physics feature"
```

---

### Task 5: Register Meshes in MaterialMesh

**Files:**
- Modify: `tribosim/src/features/simulation/components/MaterialMesh.tsx`

Add `useEffect` to register the `groupRef` on mount and deregister on unmount. The registry import comes directly from the utils file (not the barrel) to avoid a circular dependency risk.

- [ ] **Step 1: Open the file and add the import and useEffect**

Current top of file (lines 1–9):
```typescript
'use client'

import { useRef } from 'react'
import { useFrame } from '@react-three/fiber'
import * as THREE from 'three'
import { PHYSICS_CONSTANTS } from '@/constants'
import type { Material } from '@/types'
import { MaterialType } from '@/types'
import { useSimulationStore } from '@/stores/simulation-store'
```

Replace with:
```typescript
'use client'

import { useRef, useEffect } from 'react'
import { useFrame } from '@react-three/fiber'
import * as THREE from 'three'
import { PHYSICS_CONSTANTS } from '@/constants'
import type { Material } from '@/types'
import { MaterialType } from '@/types'
import { useSimulationStore } from '@/stores/simulation-store'
import { registerMesh, unregisterMesh } from '@/features/physics/utils/mesh-registry'
```

- [ ] **Step 2: Add the registration effect inside the component**

After the existing `const groupRef = useRef<THREE.Group>(null)` line, add:

```typescript
  useEffect(() => {
    if (groupRef.current) {
      registerMesh(side, groupRef.current)
    }
    return () => {
      unregisterMesh(side)
    }
  }, [side])
```

- [ ] **Step 3: Verify the full file looks correct**

The complete `MaterialMesh.tsx` should be:

```typescript
'use client'

import { useRef, useEffect } from 'react'
import { useFrame } from '@react-three/fiber'
import * as THREE from 'three'
import { PHYSICS_CONSTANTS } from '@/constants'
import type { Material } from '@/types'
import { MaterialType } from '@/types'
import { useSimulationStore } from '@/stores/simulation-store'
import { registerMesh, unregisterMesh } from '@/features/physics/utils/mesh-registry'

interface MaterialMeshProps {
  side: 'left' | 'right'
  material: Material
  /** Fallback position used before hand-tracking initialises */
  defaultPosition: [number, number, number]
}

export function MaterialMesh({ side, material, defaultPosition }: MaterialMeshProps) {
  const groupRef = useRef<THREE.Group>(null)

  useEffect(() => {
    if (groupRef.current) {
      registerMesh(side, groupRef.current)
    }
    return () => {
      unregisterMesh(side)
    }
  }, [side])

  // Fine-grained subscriptions — each selector is independent
  const charge = useSimulationStore((s) => (side === 'left' ? s.q1 : s.q2))

  const isInsulator = material.type === MaterialType.Insulator

  // Material properties driven by physical type
  const metalness = isInsulator ? 0.1 : 0.8
  const roughness = isInsulator ? 0.7 : 0.2

  // Emissive glow: red for positive charge, cyan for negative, black at 0
  const intensity = Math.abs(charge) / PHYSICS_CONSTANTS.MAX_CHARGE
  const emissiveColor = intensity > 0 ? (charge >= 0 ? '#ff4444' : '#00ccff') : '#000000'

  // ─── Smooth interpolation toward store position ──────────
  useFrame(() => {
    const group = groupRef.current
    if (!group) return

    const pos = useSimulationStore.getState()
    const target = side === 'left' ? pos.leftPosition : pos.rightPosition

    group.position.lerp(
      new THREE.Vector3(target[0], target[1], target[2]),
      0.2,
    )
  })

  return (
    <group ref={groupRef} position={defaultPosition}>
      <mesh castShadow receiveShadow>
        <boxGeometry args={[1, 1, 1]} />
        <meshStandardMaterial
          color={material.color}
          emissive={emissiveColor}
          emissiveIntensity={intensity}
          metalness={metalness}
          roughness={roughness}
        />
      </mesh>
    </group>
  )
}
```

- [ ] **Step 4: Commit**

```bash
git add src/features/simulation/components/MaterialMesh.tsx
git commit -m "feat(physics): register MaterialMesh groups in mesh registry"
```

---

### Task 6: Wire Up Hook in Scene

**Files:**
- Modify: `tribosim/src/features/simulation/components/Scene.tsx`

Add the `useCollisionDetection()` call alongside the other interaction hooks.

- [ ] **Step 1: Add the import**

After the existing imports, add:
```typescript
import { useCollisionDetection } from '@/features/physics'
```

- [ ] **Step 2: Call the hook inside the Scene component**

After the existing `usePanInteraction()` call, add:
```typescript
  useCollisionDetection()
```

- [ ] **Step 3: Verify the full file looks correct**

```typescript
'use client'

import { OrbitControls } from '@react-three/drei'
import { MATERIALS, SCENE_CONSTANTS } from '@/constants'
import { useSimulationStore } from '@/stores/simulation-store'
import { MaterialMesh } from './MaterialMesh'
import { useGrabInteraction } from '@/features/hand-tracking/hooks/use-grab-interaction'
import { useZoomInteraction } from '@/features/hand-tracking/hooks/use-zoom-interaction'
import { usePanInteraction } from '@/features/hand-tracking/hooks/use-pan-interaction'
import { useCollisionDetection } from '@/features/physics'

export function Scene() {
  const leftMaterial = useSimulationStore((s) => s.leftMaterial)
  const rightMaterial = useSimulationStore((s) => s.rightMaterial)
  const isZooming = useSimulationStore((s) => s.isZooming)
  const isPanning = useSimulationStore((s) => s.isPanning)

  // Hand-to-object interaction hooks (run inside R3F context)
  useGrabInteraction()
  useZoomInteraction()
  usePanInteraction()
  useCollisionDetection()

  return (
    <>
      {/* Lighting rig */}
      <ambientLight intensity={0.3} />
      <pointLight
        position={[0, 5, 5]}
        intensity={1.0}
        color="#ffffff"
      />
      {/* Rim / backlight — slight cool tint */}
      <pointLight
        position={[0, 2, -3]}
        intensity={0.5}
        color="#4488ff"
      />

      {/* Material objects */}
      <MaterialMesh
        side="left"
        material={leftMaterial ?? MATERIALS[0]!}
        defaultPosition={[
          SCENE_CONSTANTS.LEFT_SPAWN_POSITION.x,
          SCENE_CONSTANTS.LEFT_SPAWN_POSITION.y,
          SCENE_CONSTANTS.LEFT_SPAWN_POSITION.z,
        ]}
      />
      <MaterialMesh
        side="right"
        material={rightMaterial ?? MATERIALS[1]!}
        defaultPosition={[
          SCENE_CONSTANTS.RIGHT_SPAWN_POSITION.x,
          SCENE_CONSTANTS.RIGHT_SPAWN_POSITION.y,
          SCENE_CONSTANTS.RIGHT_SPAWN_POSITION.z,
        ]}
      />

      {/* OrbitControls — makeDefault exposes it via useThree for pan hook */}
      <OrbitControls
        makeDefault
        enablePan={!isPanning}
        enableZoom={!isZooming}
        enableRotate={!isPanning}
      />
    </>
  )
}
```

- [ ] **Step 4: Commit**

```bash
git add src/features/simulation/components/Scene.tsx
git commit -m "feat(physics): wire up collision detection in Scene"
```

---

### Task 7: Manual Verification

No test runner is configured — verify in the browser.

- [ ] **Step 1: Start the dev server**

```bash
cd tribosim
npm run dev
```

Open `http://localhost:3000`.

- [ ] **Step 2: Add a temporary console log to the hook**

In `use-collision-detection.ts`, inside `useFrame`, after the `setCollisionState` calls, add:

```typescript
    if (process.env.NODE_ENV === 'development') {
      console.log('[collision]', { colliding, relVel: colliding ? undefined : 0 })
    }
```

- [ ] **Step 3: Verify all checklist items from the spec**

Open browser DevTools → Console. Filter by `[collision]`.

| Check | Expected |
|-------|----------|
| Objects visually overlapping | `colliding: true` appears in console |
| Objects moved apart | `colliding: false` |
| Objects overlapping AND hands moving | `relativeVelocity > 0` in store (check via Zustand DevTools or log) |
| Objects overlapping, hands still | `relativeVelocity ≈ 0` |
| Frame rate while overlapping | Still smooth (~60 fps — no stuttering) |
| Objects visually apart but `colliding: true` | Should NOT happen — if it does, see troubleshooting table in spec |

- [ ] **Step 4: Remove the temporary console log**

Delete the `console.log` block added in Step 2.

- [ ] **Step 5: Final commit**

```bash
git add src/features/physics/hooks/use-collision-detection.ts
git commit -m "chore: remove debug logging from collision detection hook"
```
