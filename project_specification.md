# Project Specification: 3D Triboelectricity & Conservation of Charge Simulator

## 1. Executive Summary
- **Product:** 3D Triboelectric "Friction" Simulator — An interactive 3D web application where users manipulate virtual materials using webcam hand-tracking to visually generate, transfer, and ground electrostatic charges.
- **Problem:** Abstract physics concepts like triboelectricity and conservation of charge are difficult to visualize and internalize for college physics students through static textbook diagrams.
- **Solution:** A highly visual, interactive 3D simulator using real-time hand tracking ($v_{rel}$) to mathematically and visually prove that net charge in a closed system remains zero ($0\mu C$) during triboelectric charging, distinguishing between insulators and conductors.
- **Platform:** Web (Interactive 3D SPA)
- **Target Launch:** College project timeline (TBD)
- **Scope:** MVP / V1 (Complete functional simulator for standard materials)

direction using arorws

## 2. User Personas & Workflows
- **College Physics Student / Professor** — Primary User
  - **Primary goal:** To interactively observe and verify the Law of Conservation of Charge and understand the triboelectric series.
  - **Key workflow:** 
    1. Opens the web app (hosted on Vercel) on a MacBook (or similar hardware).
    2. Grants webcam permission for MediaPipe hand tracking.
    3. Selects two materials from the HUD UI (e.g., Glass and Silk), which spawn on the left and right sides of the 3D canvas.
    4. "Grabs" the virtual 3D meshes by positioning a hand over an object and pinching (thumb and index finger, with the other 3 fingers open) to move it.
    5. Rubs hands together; the app calculates relative velocity and visualizes electron transfer based on the triboelectric pseudo-equation.
    6. Observes the HUD updating charge values ($q_1$, $q_2$) while proving $q_{net} = 0\mu C$.
    7. Uses the zoom gesture (pinching thumb and index finger, with the other 3 fingers closed) to zoom in and out of the simulation. Releasing the pinch or opening the other 3 fingers cancels the zoom.
    8. Tests a conductor (e.g., Copper) to observe the grounding effect to the human body.
  - **Frequency:** Ad-hoc / per assignment.
  - **Pain points:** Struggling to intuitively grasp charge transfer rates, grounding, and conservation principles from 2D textbook problems.

## 3. Feature Specification

### MVP Features (Must Ship)
- **Webcam Hand-Tracking Integration**
  - Description: Real-time hand tracking using Google MediaPipe to detect finger states for object manipulation and zooming.
  - User story: "As a student, I want to grab and manipulate spawned 3D objects using precise hand gestures so the simulation feels physical and intuitive."
  - Inputs: User's webcam video feed to track 21 hand landmarks.
  - Outputs: Hand tracking maps pinch gestures (thumb + index pointing) to grab/move touching objects (if other 3 fingers are open), or to zoom the camera (if other 3 fingers are closed).
  - Business rules: Requires explicit camera permissions. Must calculate $v_{rel}$ (relative velocity) when bounding boxes intersect.
  - Edge cases: Hands go out of frame; multiple people in frame (limit to one user/two hands).

- **Dynamic Triboelectric Math Engine**
  - Description: Calculates charge transfer ($\Delta q$) per frame based on $\Delta q = k \cdot v_{rel} \cdot \Delta t \cdot (T_A - T_B)$.
  - User story: "As a user, I want the charge transfer to be proportional to how hard I rub the virtual materials."
  - Inputs: Delta time, hand velocities, material triboelectric indices, and specific material pair friction coefficient ($k$).
  - Outputs: Updated charge values $q_1$ and $q_2$ in $\mu C$.
  - Business rules: Sum of charges ($q_{net}$) must strictly equal 0 at all times for insulators.

- **Custom Friction Coefficients ($k$)**
  - Description: A predefined lookup table mapping the friction/resistance between specific pairs of materials (e.g., Glass and Silk transfer charge quickly, so they have a higher $k$).
  - User story: "As a student, I want different material combinations to physically feel different in how quickly they generate charge."
  - Inputs: The two actively selected materials.
  - Outputs: A scalar friction coefficient $k$ fed into the triboelectric math engine.
  - Business rules: Every pair of selectable materials must have a defined $k$ value in the configuration matrix.

- **3D Material Rendering & VFX**
  - Description: Rendering 3D meshes for selectable materials with particle effects for electron transfer.
  - User story: "As a user, I want to visually see electrons moving from the more positive to the more negative material."
  - Inputs: Current charge state, material types.
  - Outputs: Glowing auras (red/positive, blue/negative) and directional particle flow.
  - Business rules: Conductors instantly ground to $0\mu C$ with a "spark" effect; insulators accumulate charge.

- **Scientific HUD (Heads-Up Display)**
  - Description: A sleek, top-anchored overlay displaying real-time physics metrics.
  - User story: "As a user, I want to see the exact micro-Coulomb values to verify the conservation of charge."
  - Inputs: Data from the physics engine.
  - Outputs: Displays $q_1$, $q_2$, and $q_{net} = 0\mu C$.
  - Business rules: Cannot drop frames during high calculation periods. Must be highly contrasting against the 3D canvas.

- **Material Selector UI**
  - Description: UI to swap out the materials spawned on the left and right sides of the 3D environment.
  - User story: "As a user, I want to test different combinations of materials (e.g., Glass vs Silk, Rubber vs Fur)."
  - Inputs: Click events on UI elements.
  - Outputs: Spawns/changes the active 3D meshes on the left and right sides and updates the $T_A, T_B$ indices in the math engine.
  - Business rules: Must include at least 4 insulators and 1 conductor for the MVP.

### Future Considerations
- 3D models of specific physical experiments (e.g., charging an electroscope via induction).
- Saving recording sessions of experiments.
- Multi-user / multiplayer networked physics.

### Anti-Features (Explicitly Out of Scope)
- **Backend / Database:** No user authentication, saved states, or leaderboards needed. This is a purely client-side, ephemeral educational tool.
- **Mobile Support:** Hand tracking + 3D rendering is targeted for desktop/laptop webcams (e.g., MacBook M1). Mobile optimization is out of scope to avoid extreme performance constraints.

## 4. Technical Architecture

### Stack
| Layer | Technology | Justification |
|---|---|---|
| Frontend | Next.js (or Vite + React) + TypeScript | Fast client-side rendering; strict typing prevents math/state errors in the physics loop. |
| 3D Engine | Three.js + React Three Fiber (@react-three/drei) | Seamless integration of the 3D canvas with React state. Industry standard for web 3D. |
| Computer Vision | Google MediaPipe (Hands) | Runs entirely in the browser (client-side), low latency, no backend processing required. |
| Styling | Tailwind CSS | Rapid UI development for the HUD; clean, modern aesthetic. |
| State Management | Zustand | High-performance, non-blocking state updates for the continuous physics loop outside standard React render cycles. |
| Hosting | Vercel | Free, trivial deployment for Next.js/React apps with excellent edge performance. |

### System Architecture
The application runs entirely on the client side:
1. **Input Layer:** MediaPipe captures webcam frames $\rightarrow$ outputs hand landmark and gesture state data.
2. **Interaction & Physics Loop:** Reads gestures (grab vs zoom) $\rightarrow$ updates object positions or camera zoom. When grabbed objects collide and move, calculates $v_{rel}$ $\rightarrow$ applies triboelectric math $\rightarrow$ updates charge state in Zustand.
3. **Render Layer:** React Three Fiber reads state $\rightarrow$ updates camera zoom, mesh positions, and triggers particle systems if $\Delta q > 0$.
4. **UI Layer:** React DOM reads state $\rightarrow$ updates the HUD metrics overlay.

### Data Model (Key Entities)
- **Material**
  - Fields: `id` (string), `name` (string), `type` (enum 'insulator' \| 'conductor'), `triboIndex` (number), `modelPath` (string)
- **SimulationState**
  - Fields: `leftObj` (Material), `rightObj` (Material), `isZooming` (boolean), `q1` (number, $\mu C$), `q2` (number, $\mu C$), `isGrounding` (boolean)

## 5. Design Direction
- **Aesthetic:** Minimalist, "Sci-Fi Lab", Dark Mode. High contrast.
- **Color palette:** Background: Pitch black or very dark gray (`#0f0f11`). Positive Charge Aura: Neon Red/Orange. Negative Charge Aura: Neon Blue/Cyan. HUD text: Bright White (`#ffffff`) or Tech Green (`#00ff00`).
- **Typography:** Monospace fonts for numbers to simulate scientific instruments (e.g., `JetBrains Mono`, `Fira Code`). Clean sans-serif (e.g., `Inter`) for labels.
- **Themes:** Strictly Dark Mode (ensures 3D glowing particle effects pop out).
- **Responsive strategy:** Fixed desktop ratio or flexible fullscreen desktop. Mobile view triggers a "Please view on desktop" warning.

## 6. Security & Compliance
- **Security tier:** MVP / Client-Side Educational Tool.
- **Authentication:** None required.
- **Data handling:** Webcam data is processed 100% locally in the browser via MediaPipe. No video streams or images are sent to any server, preserving user privacy.

## 7. Infrastructure & DevOps
- **Environments:** Development (Local), Production (Vercel/GitHub Pages).
- **Deployment strategy:** GitHub pushes trigger Vercel auto-deployments.
- **Monitoring:** Optional simple analytics (Vercel Web Analytics) just to see page views.
- **Scaling considerations:** Entirely client-heavy processing (M1 chip handles this easily). Zero backend scaling concerns since there is no backend.

## 8. Project Phases & Milestones

| Phase | Focus | Duration | Key Deliverables |
|---|---|---|---|
| 0 | Project setup, Tooling, MVP 3D Canvas | TBD | Next.js/React repo, Tailwind, R3F blank canvas setup. |
| 1 | Computer Vision Integration | TBD | MediaPipe hand tracking working; detecting pinch+open fingers for grabbing spawned cubes, and pinch+closed fingers for zoom. |
| 2 | Physics Engine & State Logic | TBD | Collision detection, relative velocity math, charge transfer state working (logged to console/Zustand store). |
| 3 | VFX & 3D Assets | TBD | Replacing cubes with material models/shapes; adding glow auras, electron particles, and grounding sparks. |
| 4 | UI HUD & Integration | TBD | Overlay HUD with live numbers, material selection menu. |
| 5 | Performance Tuning & Polish | TBD | Optimizing frame rates, tweaking friction coefficient ($k$) for "fun factor". |

## 9. Open Questions & Risks
- **Risk:** MediaPipe hand tracking + React Three Fiber physics at 60fps might cause performance drops or thermal throttling on older laptops.
  - *Mitigation:* Cap particle counts; implement optional graphics quality toggle; offload physics to a regular requestAnimationFrame loop outside React if needed.
- **Risk:** Calculating accurate 3D bounding box intersections dynamically on fast-moving hands.
  - *Mitigation:* Use simplified sphere or AABB (Axis-Aligned Bounding Box) colliders around the palm instead of complex mesh colliders.
- **Question:** Do we need custom 3D models for the materials, or can we use basic geometries (cylinders for rods, planes for fabric) with high-res PBR textures to save time? (Recommending PBR textures on basic meshes for a school project MVP).

## 10. Success Metrics
- Performance: Maintains a stable 30-60 FPS on a standard MacBook Air M1 during maximum particle emission.
- Physics Validation: The HUD mathematically retains $q_{net} = 0 \mu C$ under all non-grounding intersection scenarios without floating-point drift accumulating over time.
- User Experience: The tracking feels snappy, and the electron transfer VFX clearly demonstrates the physics principle without verbal explanation.

## 11. Recommended Skills

| Phase | Skills | Purpose |
|---|---|---|
| Phase 0: Setup | `react-best-practices`, `frontend-dev-guidelines` | Establish a robust Next.js/React structure suitable for heavy state updates and canvas mounting. |
| Phase 1 & 2: 3D + CV | `3d-web-experience`, `research-engineer` | Implement Three.js/R3F performant canvas, integrate MediaPipe optimally, ensure physics and linear algebra math are rigorous. |
| Phase 3: VFX & Design | `ui-ux-pro-max`, `frontend-design`, `3d-web-experience` | Create the glowing particle systems, design the minimal Sci-Fi HUD, select typography. |
| Phase 4 & 5: Polish & Ops | `web-performance-optimization`, `vercel-deployment`, `systematic-debugging` | Profile the app to prevent frame drops, manage memory leaks from 3D object lifecycles, and deploy to Vercel perfectly. |
