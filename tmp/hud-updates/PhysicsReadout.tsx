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
        pointerEvents: 'none',
      }}
    >
      {/* Glassmorphic pill */}
      <div
        style={{
          background: 'rgba(255, 255, 255, 0.04)',
          backdropFilter: 'blur(16px) saturate(150%)',
          WebkitBackdropFilter: 'blur(16px) saturate(150%)',
          borderRadius: 24,
          border: '1px solid rgba(255, 255, 255, 0.08)',
          boxShadow: '0 8px 32px rgba(0, 0, 0, 0.3), inset 0 1px 0 rgba(255, 255, 255, 0.05)',
          padding: '12px 24px',
          display: 'flex',
          alignItems: 'center',
          gap: 24,
        }}
      >
        {/* Status indicator */}
        <div style={{ display: 'flex', alignItems: 'center', gap: 10 }}>
          <div
            style={{
              width: 8,
              height: 8,
              borderRadius: '50%',
              background: isColliding ? '#22d3ee' : 'rgba(255, 255, 255, 0.2)',
              boxShadow: isColliding 
                ? '0 0 12px #22d3ee, 0 0 24px rgba(34, 211, 238, 0.4)' 
                : 'none',
              transition: 'all 0.2s ease',
              animation: isColliding ? 'contact-pulse 1.2s ease-in-out infinite' : 'none',
              color: '#22d3ee',
            }}
          />
          <span
            style={{
              fontFamily: 'Inter, -apple-system, sans-serif',
              fontSize: 12,
              fontWeight: 500,
              letterSpacing: '0.02em',
              color: isColliding ? 'rgba(255, 255, 255, 0.9)' : 'rgba(255, 255, 255, 0.4)',
              transition: 'all 0.2s ease',
            }}
          >
            {isColliding ? 'Contact' : 'Separated'}
          </span>
        </div>

        {/* Divider */}
        <div
          style={{
            width: 1,
            height: 16,
            background: 'rgba(255, 255, 255, 0.1)',
          }}
        />

        {/* Velocity readout */}
        <div style={{ display: 'flex', alignItems: 'baseline', gap: 8 }}>
          <span
            style={{
              fontFamily: 'Inter, -apple-system, sans-serif',
              fontSize: 11,
              fontWeight: 500,
              letterSpacing: '0.05em',
              color: 'rgba(255, 255, 255, 0.4)',
              textTransform: 'uppercase',
            }}
          >
            Vel
          </span>
          <span
            style={{
              fontFamily: "'Space Mono', monospace",
              fontSize: 16,
              fontWeight: 700,
              color: relativeVelocity > 0.5 
                ? 'rgba(255, 255, 255, 0.9)' 
                : 'rgba(255, 255, 255, 0.4)',
              fontVariantNumeric: 'tabular-nums',
              transition: 'all 0.2s ease',
            }}
          >
            {relativeVelocity.toFixed(2)}
          </span>
          <span
            style={{
              fontFamily: 'Inter, -apple-system, sans-serif',
              fontSize: 10,
              fontWeight: 500,
              color: 'rgba(255, 255, 255, 0.35)',
            }}
          >
            u/s
          </span>
        </div>
      </div>
    </div>
  )
}
