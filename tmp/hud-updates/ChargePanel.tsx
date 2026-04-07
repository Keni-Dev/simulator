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
  const chargeColor = isPositive ? '#f87171' : '#22d3ee'
  const meterFill = Math.min((Math.abs(charge) / PHYSICS_CONSTANTS.MAX_CHARGE) * 100, 100)
  const sign = charge > 0 ? '+' : charge < 0 ? '−' : ''
  const isActive = Math.abs(charge) > 0.5

  return (
    <div
      style={{
        position: 'absolute',
        top: 24,
        ...(side === 'left' ? { left: 24 } : { right: 24 }),
        width: 180,
        pointerEvents: 'none',
      }}
    >
      {/* Glassmorphic panel */}
      <div
        style={{
          background: 'rgba(255, 255, 255, 0.04)',
          backdropFilter: 'blur(16px) saturate(150%)',
          WebkitBackdropFilter: 'blur(16px) saturate(150%)',
          borderRadius: 16,
          border: '1px solid rgba(255, 255, 255, 0.08)',
          boxShadow: '0 8px 32px rgba(0, 0, 0, 0.3), inset 0 1px 0 rgba(255, 255, 255, 0.05)',
          overflow: 'hidden',
        }}
      >
        {/* Header */}
        <div
          style={{
            padding: '14px 16px 12px',
            borderBottom: '1px solid rgba(255, 255, 255, 0.06)',
            display: 'flex',
            alignItems: 'center',
            justifyContent: 'space-between',
          }}
        >
          <span
            style={{
              fontFamily: 'Inter, -apple-system, sans-serif',
              fontSize: 11,
              fontWeight: 500,
              letterSpacing: '0.08em',
              color: 'rgba(255, 255, 255, 0.5)',
              textTransform: 'uppercase',
            }}
          >
            Object {side === 'left' ? 'A' : 'B'}
          </span>
          <span
            style={{
              width: 6,
              height: 6,
              borderRadius: '50%',
              background: isActive ? chargeColor : 'rgba(255, 255, 255, 0.2)',
              boxShadow: isActive ? `0 0 8px ${chargeColor}` : 'none',
              transition: 'all 0.2s ease',
            }}
          />
        </div>

        {/* Content */}
        <div style={{ padding: 16 }}>
          {/* Material selector */}
          <div style={{ marginBottom: 16, pointerEvents: 'auto' }}>
            <div
              style={{
                fontFamily: 'Inter, -apple-system, sans-serif',
                fontSize: 10,
                fontWeight: 500,
                letterSpacing: '0.1em',
                color: 'rgba(255, 255, 255, 0.35)',
                marginBottom: 10,
                textTransform: 'uppercase',
              }}
            >
              Material
            </div>
            <div style={{ display: 'flex', flexDirection: 'column', gap: 4 }}>
              {MATERIALS.map((m) => {
                const isSelected = material.id === m.id
                return (
                  <button
                    key={m.id}
                    onClick={() => setMaterial(m)}
                    style={{
                      background: isSelected
                        ? 'rgba(255, 255, 255, 0.08)'
                        : 'rgba(255, 255, 255, 0.02)',
                      border: 'none',
                      borderRadius: 8,
                      padding: '10px 12px',
                      fontFamily: 'Inter, -apple-system, sans-serif',
                      fontSize: 13,
                      fontWeight: isSelected ? 500 : 400,
                      color: isSelected ? 'rgba(255, 255, 255, 0.9)' : 'rgba(255, 255, 255, 0.5)',
                      cursor: 'pointer',
                      textAlign: 'left',
                      transition: 'all 0.15s ease',
                      display: 'flex',
                      alignItems: 'center',
                      gap: 10,
                    }}
                  >
                    <span
                      style={{
                        width: 8,
                        height: 8,
                        borderRadius: 4,
                        backgroundColor: m.color,
                        boxShadow: isSelected ? `0 0 8px ${m.color}` : 'none',
                        transition: 'box-shadow 0.15s ease',
                      }}
                    />
                    {m.name}
                  </button>
                )
              })}
            </div>
          </div>

          {/* Charge meter section */}
          <div
            style={{
              background: 'rgba(0, 0, 0, 0.25)',
              borderRadius: 12,
              padding: 14,
            }}
          >
            <div
              style={{
                fontFamily: 'Inter, -apple-system, sans-serif',
                fontSize: 10,
                fontWeight: 500,
                letterSpacing: '0.1em',
                color: 'rgba(255, 255, 255, 0.35)',
                marginBottom: 12,
                textTransform: 'uppercase',
              }}
            >
              Charge
            </div>

            {/* Meter + value layout */}
            <div style={{ display: 'flex', gap: 14, alignItems: 'center' }}>
              {/* Vertical bar meter */}
              <div
                style={{
                  width: 8,
                  height: 72,
                  background: 'rgba(255, 255, 255, 0.06)',
                  borderRadius: 4,
                  position: 'relative',
                  overflow: 'hidden',
                  flexShrink: 0,
                }}
              >
                {/* Center line */}
                <div
                  style={{
                    position: 'absolute',
                    top: '50%',
                    left: 0,
                    right: 0,
                    height: 1,
                    background: 'rgba(255, 255, 255, 0.15)',
                  }}
                />
                {/* Fill bar */}
                <div
                  style={{
                    position: 'absolute',
                    left: 1,
                    right: 1,
                    height: `${meterFill / 2}%`,
                    ...(isPositive 
                      ? { bottom: '50%' } 
                      : { top: '50%' }
                    ),
                    background: chargeColor,
                    borderRadius: 3,
                    transition: 'height 0.12s ease-out',
                    boxShadow: isActive ? `0 0 12px ${chargeColor}` : 'none',
                  }}
                />
              </div>

              {/* Digital readout */}
              <div style={{ flex: 1 }}>
                <div
                  style={{
                    fontFamily: "'Space Mono', monospace",
                    fontSize: 28,
                    fontWeight: 700,
                    color: Math.abs(charge) < 0.1 ? 'rgba(255, 255, 255, 0.25)' : chargeColor,
                    lineHeight: 1,
                    fontVariantNumeric: 'tabular-nums',
                    transition: 'color 0.15s ease',
                    textShadow: isActive ? `0 0 20px ${chargeColor}` : 'none',
                  }}
                >
                  {sign}{Math.abs(charge).toFixed(1)}
                </div>
                <div
                  style={{
                    fontFamily: 'Inter, -apple-system, sans-serif',
                    fontSize: 11,
                    color: 'rgba(255, 255, 255, 0.4)',
                    marginTop: 4,
                    fontWeight: 500,
                  }}
                >
                  μC
                </div>
                
                {/* Polarity pills */}
                <div
                  style={{
                    marginTop: 10,
                    display: 'flex',
                    gap: 6,
                  }}
                >
                  <span 
                    style={{ 
                      fontFamily: 'Inter, -apple-system, sans-serif',
                      fontSize: 9,
                      fontWeight: 500,
                      letterSpacing: '0.05em',
                      padding: '3px 6px',
                      borderRadius: 4,
                      background: isPositive && isActive 
                        ? 'rgba(248, 113, 113, 0.15)' 
                        : 'rgba(255, 255, 255, 0.04)',
                      color: isPositive && isActive 
                        ? '#f87171' 
                        : 'rgba(255, 255, 255, 0.3)',
                      transition: 'all 0.15s ease',
                    }}
                  >
                    +
                  </span>
                  <span 
                    style={{ 
                      fontFamily: 'Inter, -apple-system, sans-serif',
                      fontSize: 9,
                      fontWeight: 500,
                      letterSpacing: '0.05em',
                      padding: '3px 6px',
                      borderRadius: 4,
                      background: !isPositive && isActive 
                        ? 'rgba(34, 211, 238, 0.15)' 
                        : 'rgba(255, 255, 255, 0.04)',
                      color: !isPositive && isActive 
                        ? '#22d3ee' 
                        : 'rgba(255, 255, 255, 0.3)',
                      transition: 'all 0.15s ease',
                    }}
                  >
                    −
                  </span>
                </div>
              </div>
            </div>
          </div>
        </div>
      </div>
    </div>
  )
}
