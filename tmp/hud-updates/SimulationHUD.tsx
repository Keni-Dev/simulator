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
