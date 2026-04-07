# Landing & Setup Screen — Dark Mode — Desktop

## Prompt

Design a premium web landing page for "TriboSim", a visual 3D triboelectricity and conservation of charge simulator, displayed in a minimal browser frame at 1440px.

**Overall Aesthetic:** Sci-Fi Lab meets minimalist educational tool. Think Vercel's monochrome discipline intersected with NASA mission control dashboards. The page breathes — a restrained dark palette with neon tech accents, and typography that commands scientific authority. This is NOT a generic AI layout; it's an immersive, precise instrument interface designed to build anticipation for a 3D experience.

**Background & Canvas:** Deep charcoal #0B0B0D for the entire page background. In the hero area, a soft gradient mesh floats in the center: a 600px blurred circle of neon cyan #00E5FF at 5% opacity, intersecting with a 500px blurred circle of neon red/orange #FF3D00 at 4% opacity, representing the duality of electrostatic charge. A subtle dot grid pattern: 1px dots in #2A2A2D, spaced 32px apart, covers the entire background.

**Navigation Bar (fixed, full-width, height 64px, z-index 50):**
Background: transparent with `backdrop-filter: blur(12px)` and a 1px bottom border in #2A2A2D. Max-width container 1240px, centered.
- Left: Logo — "TriboSim" in Inter Bold 20px #FFFFFF, with an atom or electron orbit icon (18px, outlined, #00E5FF) next to it.
- Center: Empty or minimalist "Ver 1.0" badge in JetBrains Mono 12px #888888.
- Right: A subtle "View on GitHub" ghost button in Inter Medium 14px #888888 (hover: #FFFFFF).

**Hero Section (centered, max-width 800px, padding 100px 0):**
- Headline: "Visualize the Flow of Charge." in Inter Black 64px, solid #FFFFFF, line-height 1.1, tight letter-spacing -1px.
- Subheadline: "An interactive 3D physics simulator for exploring triboelectricity and the conservation of charge. Use your webcam and bare hands to transfer electrons in real-time." in Inter Regular 18px #A1A1AA, max-width 600px, centered, margin-top 24px.
- Interaction Block (Camera Setup): A distinct central card, max-width 480px, background #121215, border 1px solid #2A2A2D, border-radius 12px, padding 32px, shadow 0 20px 40px rgba(0,0,0,0.5).
  - Inside Card Top: A camera icon (Lucide-style, stroke 1.5px, 24px, #00E5FF) and "Webcam Access Required" in Inter Semibold 16px #FFFFFF.
  - Inside Card Body: "TriboSim uses local device hand-tracking to anchor 3D materials to your palms. No video data is ever recorded or uploaded." in Inter Regular 14px #888888.
  - Primary button: "Enable Camera & Start" — background #00E5FF, text Inter Bold 14px #0B0B0D, height 48px, width 100%, border-radius 8px. Hover: background #00FFFF, intense glow shadow `0 0 20px rgba(0,229,255,0.4)`, transition 200ms ease.

**Instructions Panel (max-width 1000px, 3-col grid, gap 32px, margin-top 80px):**
Three clean cards explaining the workflow. Background #0F0F12, border 1px solid #1E1E22, border-radius 8px, padding 24px. Hover state: border color #2A2A2D, subtle shadow lift `0 10px 30px rgba(0,0,0,0.3)`.
- Card 1: "1. Select Materials" (Inter Semibold 16px #FFFFFF). "Choose an insulator and a conductor from the HUD." (Inter 14px #9CA3AF). Material icon.
- Card 2: "2. Generate Friction" (Inter Semibold 16px #FFFFFF). "Rub your hands together in front of the camera to strip electrons." (Inter 14px #9CA3AF). Hand icon.
- Card 3: "3. Verify Conservation" (Inter Semibold 16px #FFFFFF). "Observe the exact micro-Coulombs transferred while net charge remains zero." (Inter 14px #9CA3AF). Lightning icon.

**Footer (max-width 1240px, padding 40px 0 24px, border-top 1px solid #1E1E22, margin-top 100px):**
Layout: center-aligned minimal footer.
- Text: "Built for physics education. Entirely client-side." in Inter Regular 14px #52525B.
- Tech Stack Badges: Small inline tags (Next.js, Three.js, MediaPipe) in JetBrains Mono 12px #71717A, background #18181B, padding 4px 8px, border-radius 4px.

**Key Design Notes:**
- Highly scientific, precision-focused aesthetic, avoiding generic 'startup' friendliness.
- The glowing primary button against the deep charcoal background focuses user intent immediately on starting the simulation.
- Typography creates a clear hierarchy: Inter for readability and headings, JetBrains Mono reserved for technical/system hints.
- Interactive hover states should feel like turning on lab equipment (snappy, glowing).
- Uses neon cyan and orange/red as functional accents meant to map directly to the in-game charge particles (positive/negative).
