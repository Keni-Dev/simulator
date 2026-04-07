Project Specification: 3D Triboelectric "Friction" Simulator

1. Project Overview

Title: 3D Triboelectricity & Conservation of Charge Simulator

Core Concept: An interactive 3D web application where users manipulate virtual materials using webcam hand-tracking. By physically rubbing materials together in front of the camera, users visually generate, transfer, and ground electrostatic charges.

Academic Scope: Strictly adheres to Foundations of Electrostatics 1.1 (Properties of Charge), 1.3 (Conservation of Charges), and 1.6 (Kinds of Materials: Conductors vs. Insulators).

Primary Objective: To visually and mathematically prove that the net charge in a closed system remains zero ($0\mu C$) during triboelectric charging, and to demonstrate why insulators hold charge while conductors dissipate it.

2. Technical Architecture

Frontend UI & State Management: React built with TypeScript. Strict typing will be crucial for managing the complex state of 3D coordinates, physics values, and material properties without dropping frames.

3D Rendering Engine: Three.js (via @react-three/fiber for seamless React integration). Used to render 3D meshes of the materials (e.g., a glass rod, a silk cloth, a copper pipe) anchored dynamically to the user's tracked hands.

Computer Vision: Google MediaPipe (Hands solution). Captures real-time $x, y, z$ coordinates of the palms to calculate velocity and collision data directly in the browser.

Styling: Tailwind CSS for a sleek, modern floating HUD (Heads-Up Display) overlay.

3. Core Physics Mechanics

A. The Triboelectric Pseudo-Equation

Instead of a pre-baked animation, charge transfer will be calculated dynamically based on the user's physical effort. The simulation runs on a physics loop using this continuous pseudo-equation for charge transfer per frame:

$\Delta q = k \cdot v_{rel} \cdot \Delta t \cdot (T_A - T_B)$

$\Delta q$: Charge transferred in the current frame.

$k$: A hardcoded friction scaling coefficient to tune the math for visual gameplay and responsiveness.

$v_{rel}$: The relative velocity of the left hand and right hand while their 3D bounding boxes are intersecting.

$\Delta t$: Time elapsed since the last frame (delta time) to ensure frame-rate independence.

$T_A, T_B$: The "Triboelectric Index" of Material A and Material B. (e.g., Glass = +5, Silk = -3. The larger the absolute difference, the faster the charge transfers).

B. Material Behaviors (Insulators vs. Conductors)

Insulators (e.g., Glass, Rubber, Silk, Fur): When these are rubbed together, the calculated $\Delta q$ accumulates on the 3D objects. A visual aura (e.g., red for positive, blue for negative) scales in intensity around the meshes based on total charge.

Conductors (e.g., Copper, Aluminum): If a user selects a conductor, the triboelectric charging pseudo-equation still triggers. However, because the virtual object is "held" by the user's virtual hand, it grounds instantly to the human body. The charge variable for the conductor is hardcoded to force a rapid discharge back to $0\mu C$, accompanied by a visual "grounding spark" flowing down the user's arm.

4. 3D Environment & UI Design

The Canvas: A dark, minimalist 3D environment to ensure the glowing electron particles and UI elements contrast heavily and pop out to the user.

Hand Mapping: Invisible 3D bounding boxes are dynamically anchored to the center of the user's tracked palms. When a material is selected via the UI, its 3D mesh becomes a child of this bounding box.

Visual Effects (VFX): * When $v_{rel}$ is high and the bounding boxes intersect, a particle system spawns glowing spheres representing electrons.

Particles flow directionally from the material with the higher triboelectric index to the lower one.

The HUD (Heads-Up Display): Fixed to the top of the screen to constantly prove the core physics laws. It includes:

Left Hand Object Charge ($q_1$) in $\mu C$.

Right Hand Object Charge ($q_2$) in $\mu C$.

System Net Charge ($q_{net} = q_1 + q_2$): This metric is the absolute core of the simulator. It must visually remain locked at exactly $0\mu C$ to definitively prove the Law of Conservation of Charge.
