# Main Simulator HUD — Dark Mode — Desktop

## Prompt

Design a premium web dashboard/HUD for "TriboSim", a live 3D physics simulator, displayed in a full-screen browser frame at 1440px.

**Overall Aesthetic:** Immersive Scientific Heads-Up Display (HUD). Think SpaceX Crew Dragon interface meets high-end lab equipment. This is a full-screen, transparent UI overlay sitting on top of a 3D canvas. It relies on stark contrast, sharp edges, and monospace precision typography to convey real-time physics data. It is highly functional, minimal, and explicitly NOT a standard SaaS dashboard.

**Background & Canvas:** The background itself is the 3D rendering canvas. Since Stitch is 2D, represent the background as a very deep charcoal-to-black radial gradient (#111115 edge to #050508 center) with a subtle "vignette" effect. Place two floating, glowing abstract 3D-like shapes in the center (one glowing with neon blue particles #00E5FF, one glowing with neon red particles #FF3D00) to simulate the materials being held by the user. 

**Top Metrics Bar (HUD Header) (fixed top, full-width, padding 16px 24px, space-between):**
Floating 16px from the top edge, max-width 1392px, left/right margin auto.
- Left Block (System Status): "Camera Matrix: OK" with a pulsing green dot #10B981, and "60 FPS" in JetBrains Mono Medium 12px #A1A1AA.
- Center Block (Master Equation): A prominent glowing pill, background #0B0B0D with `backdrop-filter: blur(8px)`, border 1px solid #333333, border-radius 24px, padding 8px 24px, box-shadow `0 0 20px rgba(0,0,0,0.5)`. Text reads "Σq (Net Charge) = 0.00 µC" in JetBrains Mono Bold 18px. The "0.00 µC" part is colored perfectly white #FFFFFF, the rest is #A1A1AA.
- Right Block (Controls): Two ghost icon buttons (Lucide-style, 20px, #A1A1AA, hover #FFFFFF): Settings (cog), Fullscreen (expand).

**Left Hand HUD (absolute left, vertical center, width 280px, padding-left 32px):**
A floating telemetry panel tracking the left hand (Material A).
- Title: "MATERIAL A (LEFT)" in Inter Bold 12px, tracking 2px, #888888.
- Charge Readout: Large number "-14.25" in JetBrains Mono Light 48px #00E5FF (Neon Blue) with a subtle text-shadow `0 0 10px rgba(0,229,255,0.3)`. Sublabel "µC" to the right.
- Material Selector Dropdown: A dark button, background #121215, border 1px solid #2A2A2D, border-radius 6px, padding 12px 16px, width 100%, margin-top 16px. Reads "Teflon (Insulator)" in Inter Medium 14px #E4E4E7, with a chevron-down icon. Hover: border #00E5FF.
- Metric Row 1: "Tribo Index" - "Extremely Negative" (JetBrains Mono 12px #9CA3AF).
- Metric Row 2: "Ground State" - "Isolated" (JetBrains Mono 12px #9CA3AF).

**Right Hand HUD (absolute right, vertical center, width 280px, padding-right 32px):**
A floating telemetry panel tracking the right hand (Material B).
- Title: "MATERIAL B (RIGHT)" in Inter Bold 12px, tracking 2px, #888888.
- Charge Readout: Large number "+14.25" in JetBrains Mono Light 48px #FF3D00 (Neon Red) with text-shadow `0 0 10px rgba(255,61,0,0.3)`. Sublabel "µC" to the right.
- Material Selector Dropdown: Background #121215, border 1px solid #2A2A2D, border-radius 6px, padding 12px 16px, width 100%, margin-top 16px. Reads "Glass (Insulator)" in Inter Medium 14px #E4E4E7, with a chevron-down icon. Hover: border #FF3D00.
- Metric Row 1: "Tribo Index" - "Highly Positive" (JetBrains Mono 12px #9CA3AF).
- Metric Row 2: "Ground State" - "Isolated" (JetBrains Mono 12px #9CA3AF).

**Bottom Action Bar (absolute bottom, centered, margin-bottom 32px):**
- A contextual action button. Dark semi-transparent background #0B0B0D, border 1px solid #333333, text "Press [SPACE] to Ground / Discharge" in JetBrains Mono Medium 14px #D4D4D8. Padding 12px 24px, border-radius 8px.

**Key Design Notes:**
- UI must feel like an invisible layer of glass overlaid on reality/3D space, heavily utilizing `backdrop-filter: blur()`.
- Strict use of JetBrains Mono for all changing data values (numbers) to prevent layout jumping and reinforce the scientific instrument feel.
- Pure color association: Neon Cyan (#00E5FF) exclusively for negative charge elements, Neon Red (#FF3D00) exclusively for positive charge elements. Net Zero should be pure white.
- Symmetrical layout emphasizing the balance and conservation of charge (\$q_1 + q_2 = 0\$).
