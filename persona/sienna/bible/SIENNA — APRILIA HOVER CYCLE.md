SIENNA — APRILIA HOVER CYCLE
Final Visual Reconstruction and Propulsion Specification
Version 2.0 | Dual-Mode Gimbaled Propulsion
This revision preserves the previous visual reconstruction specification and establishes the final propulsion architecture.
The hover cycle uses two distinct propulsion systems. The forward assembly provides vertical lift and stabilization. A single rear turbine provides both forward propulsion and vertical lift through a 360-degree gimbaled mounting system.
The rear engine retains its original dimensions, carbon-fiber construction, Aprilia branding, and mechanical appearance. Its position changes to the motorcycle's longitudinal centerline beneath the rear tail.

# SIENNA — APRILIA HOVER CYCLE

## Canonical Visual and Engineering Reconstruction Specification

Version 2.0  
Status: Design baseline  
Character: Sienna  
Vehicle: Aprilia-inspired futuristic hover motorcycle  
Rendering: Photorealistic CGI  
Reference composition: 1024 × 1024  
Primary camera: Front-left three-quarter perspective  

---

# 1. DESIGN INTENT

Create a photorealistic futuristic Aprilia hover motorcycle
carrying Sienna, a fictional 26-year-old woman.

The motorcycle combines racing-motorcycle aerodynamics with
vectored-thrust propulsion.

The vehicle does not use conventional wheels.

It maintains controlled flight through two propulsion systems.

1. A compact dual-nozzle forward vertical-lift assembly.
2. A single large rear gimbaled turbine providing both
   vertical lift and forward propulsion.

The rear turbine rotates through a full 360-degree range
around its designated gimbal axis.

The turbine changes thrust direction without detaching
from the motorcycle or altering its external dimensions.

The propulsion system must appear mechanically plausible.

The image must preserve Sienna's established appearance,
the vehicle's aerodynamic styling, and the original
photographic composition.

---

# 2. VEHICLE COORDINATE SYSTEM

Define the vehicle's local coordinate system.

+X = Forward toward the motorcycle nose.
-X = Rearward toward the tail.

+Y = Motorcycle's left side.
-Y = Motorcycle's right side.

+Z = Vertically upward.
-Z = Vertically downward.

The motorcycle remains approximately horizontal during
the reference scene.

The front points toward the lower-left foreground.

The rear extends toward the upper-right background.

The camera observes the vehicle from the front-left
three-quarter perspective.

---

# 3. PROPULSION ARCHITECTURE

## 3.1 General Configuration

The motorcycle uses a distributed thrust architecture.

The front assembly primarily supports vertical lift
and pitch stabilization.

The rear turbine supports vertical lift, forward
acceleration, and transitional flight.

The two propulsion assemblies operate together.

Their thrust vectors determine the resulting forces
acting on the motorcycle.

The rear engine can redirect its thrust without requiring
the motorcycle to change its pitch.

## 3.2 Forward Lift Assembly

Location:
Beneath the forward-left belly fairing.

Configuration:
Two cylindrical carbon-fiber nozzles attached to one
shared mechanical housing.

Nominal orientation:
Vertically downward.

Function:
Generate upward reaction force.

Additional function:
Assist with pitch stabilization.

Appearance:
Dark cylindrical outlets with carbon-fiber surfaces,
metallic mounting bands, and exposed mechanical hardware.

The two nozzles remain parallel in the reference image.

No exhaust flame, smoke, or visible propulsion plume.

## 3.3 Rear Gimbaled Turbine

Quantity:
Exactly one.

Location:
Centered beneath the rear tail of the motorcycle.

Lateral alignment:
Vehicle longitudinal centerline.

Primary functions:
Forward propulsion.
Vertical lift.
Transition between hovering and forward flight.

Construction:
Large cylindrical carbon-fiber turbine housing.

Branding:
White Aprilia wordmark.

Graphics:
Red-orange geometric accents.

Dimensions:
Preserve the engine dimensions established in the
previous reference image.

The engine is not duplicated.

It is not replaced with a smaller nozzle.

It is not mounted permanently to either side
of the motorcycle.

---

# 4. REAR ENGINE GIMBAL

## 4.1 Mechanical Mounting

Attach the rear turbine to a reinforced central
mounting assembly beneath the rear chassis.

The mounting assembly consists of:

- Structural support arms.
- A reinforced central pivot.
- A circular rotational bearing.
- Mechanical actuator housings.
- Articulated brackets.
- Visible fasteners.
- Protected routing for power and control systems.

The mounting system must support the engine's
weight and thrust loads.

The assembly should appear integrated into the
motorcycle rather than attached as an accessory.

## 4.2 Rotational Capability

The rear turbine supports 360-degree rotational travel
around its primary gimbal axis.

The engine can redirect its thrust vector through
different operating orientations.

The intended motion is rotation of the entire turbine
assembly within its mounting structure.

The engine's external housing, branding, diameter,
and length remain unchanged during rotation.

A secondary articulated axis may provide lateral
vector adjustment.

A complete engineering implementation would require
appropriate rotary joints, cable management,
structural clearance, and control authority.

For the visual design, preserve a mechanically
credible mounting arrangement.

## 4.3 Thrust Vector Convention

Define the thrust vector as the reaction force acting
on the motorcycle.

The exhaust direction is opposite the thrust vector.

### Vertical-Lift Orientation

Exhaust direction:
Downward along -Z.

Reaction force:
Upward along +Z.

Function:
Support the motorcycle during hovering.

### Forward-Propulsion Orientation

Exhaust direction:
Rearward along -X.

Reaction force:
Forward along +X.

Function:
Accelerate the motorcycle forward.

### Transitional Orientation

Exhaust direction:
Downward and rearward.

Reaction force:
Upward and forward.

Function:
Provide simultaneous vertical support and forward
acceleration.

## 4.4 Vector Relationship

Define the rear turbine reaction force as:

F_rear = T [cos(theta), 0, sin(theta)]

Where:

T = Rear turbine thrust magnitude.

theta = Thrust-vector angle measured upward from
the forward vehicle axis.

For the principal operating positions:

theta = 0 degrees
Forward thrust.

theta = 45 degrees
Combined forward thrust and vertical lift.

theta = 90 degrees
Vertical lift.

theta = 180 degrees
Reverse longitudinal thrust.

theta = 270 degrees
Downward reaction force.

The gimbal may mechanically rotate through its
full range.

Normal flight-control logic should restrict
orientation when an unsafe thrust vector would result.

A 360-degree mechanical rotation capability does not
mean every orientation is appropriate during flight.

---

# 5. FLIGHT MODES

## 5.1 Mode A — Stationary Hover

Front lift assembly:
Active.

Rear turbine:
Directed vertically downward.

Rear thrust reaction:
Upward.

Vehicle:
Approximately level.

Forward speed:
Zero.

The propulsion systems collectively counteract
the vehicle's weight.

Differential thrust and available vector control
maintain pitch and roll stability.

The reference image depicts this general flight condition.

The rear turbine should point downward in the
stationary-hover reconstruction.

No visible exhaust plume.

## 5.2 Mode B — Forward Acceleration

Front lift assembly:
Provides vertical support.

Rear turbine:
Rotates toward rearward exhaust orientation.

Rear thrust reaction:
Forward.

Vehicle:
Transitions into forward motion.

The rear turbine's thrust direction changes
progressively rather than instantaneously.

The forward lift assembly continues to support
the vehicle as the rear turbine redirects thrust.

## 5.3 Mode C — Transitional Flight

Front lift assembly:
Active.

Rear turbine:
Angled between downward and rearward exhaust.

Rear thrust:
Combined upward and forward components.

The vehicle accelerates while maintaining altitude.

The rear turbine does not need to change its
external shape.

Only its orientation relative to the chassis changes.

## 5.4 Mode D — Deceleration

The rear turbine redirects thrust to produce
a component opposing the direction of travel.

The forward lift system continues to provide
vertical support.

The vehicle reduces longitudinal speed while
maintaining controlled altitude.

## 5.5 Mode E — Directional Maneuvering

The rear gimbal may adjust lateral thrust direction
if the mounting system includes a suitable secondary axis.

The front assembly contributes vertical control.

A fully controllable six-degree-of-freedom vehicle
would require additional control authority beyond
the visually specified components.

The reference design does not establish every
required stabilizing mechanism.

---

# 6. FINAL REAR ENGINE PLACEMENT

Remove the offset rear engine mounting shown in
earlier versions.

Install one large turbine beneath the rear tail.

The turbine's central longitudinal plane must coincide
with the motorcycle's central longitudinal plane.

The engine must not appear as a left-side or right-side
accessory.

Preserve:

- Original engine diameter.
- Original cylindrical length.
- Black carbon-fiber housing.
- Radial turbine structure.
- White Aprilia logo.
- Red-orange graphics.
- Metallic mounting details.

Modify only:

- Mounting position.
- Gimbal structure.
- Rotational articulation.
- Operational orientation.

The turbine should appear suspended from a reinforced
central support beneath the rear chassis.

Its mounting hardware must remain visible.

The turbine housing must maintain clearance from
the rider's boots, foot supports, and rear bodywork
throughout the intended rotation.

---

# 7. RIDER IDENTITY — SIENNA

Sienna is a fictional 26-year-old independent
visual brand designer.

She has a slender athletic build and long limbs.

Her complexion is fair with warm peach undertones.

Subtle freckles cross the nose and upper cheeks.

Her hair is long, auburn-chestnut, thick, and naturally
wavy.

Her eyes are hazel-green.

Her face is softly heart-oval.

Her nose is straight and narrow.

Her lips are naturally full with a muted rose color.

Her expression communicates focused attention,
confidence, and controlled curiosity.

Her personality emphasizes autonomy, competence,
creativity, and deliberate decision-making.

She does not display exaggerated surprise, fear,
or theatrical aggression.

---

# 8. RIDER CLOTHING

White fitted short-sleeved shirt.

Black high-waisted leather shorts.

Dark brown leather riding gloves.

Tall brown leather riding boots with buckled straps.

Small gold stud earring.

Thin gold necklace.

Preserve natural garment folds.

The shirt should remain opaque.

The boots must contact the metallic foot supports.

The gloves must grasp the handlebars.

---

# 9. RIDER POSITION

Sienna leans forward in an athletic riding posture.

Her torso inclines approximately 35–50 degrees
relative to upright.

Her shoulders extend forward.

Her arms reach toward the handlebars.

Her elbows remain moderately flexed.

Her knees bend.

Her boots rest on structural foot supports.

Her head angles slightly downward.

Her face turns toward the camera.

Her long hair falls across her left side and
extends behind her shoulders.

Maintain realistic human anatomy.

Do not allow limbs or clothing to intersect
vehicle components.

---

# 10. MOTORCYCLE EXTERIOR

The vehicle has an aerodynamic racing silhouette.

Primary color:
Metallic purple-blue.

Secondary color:
Deep violet.

Accent color:
Red-orange.

Branding:
White Aprilia logos.

The front fairing is long and rounded.

A large black circular intake occupies the nose.

A curved transparent windscreen rises above the
front bodywork.

The central chassis exposes:

- Silver engine casings.
- Tubular metallic supports.
- Mechanical joints.
- Gold-toned fittings.
- Structural brackets.
- Fasteners.

The rear seat is black.

The elevated tail tapers toward the rear.

No conventional wheels are present.

---

# 11. CAMERA

Camera type:
Full-frame virtual camera.

Projection:
Perspective.

Focal length:
Approximately 75 mm equivalent.

Viewing angle:
Front-left three-quarter.

Horizontal viewing offset:
Approximately 35 degrees from the vehicle's
longitudinal axis.

Camera elevation:
Slightly above the motorcycle's central axis.

Camera pitch:
Approximately 5–12 degrees downward.

Camera roll:
Zero.

Framing:
Entire motorcycle and rider visible.

Composition:
Square.

The nose occupies the lower-left foreground.

The tail occupies the middle-right background.

The rider's head appears in the upper-left
central region.

Preserve restrained perspective distortion.

---

# 12. LIGHTING

Environment:
Seamless neutral-gray studio.

Primary light:
Large softbox above camera-left.

Color temperature:
Approximately 5500 K.

Secondary fill:
Soft illumination from camera-right.

Contrast:
Moderate.

Highlights:
Broad and smooth.

Shadows:
Soft.

The purple fairing should show glossy
automotive reflections.

The carbon-fiber structures should have
restrained specular highlights.

The metallic chassis should exhibit
realistic reflections.

The rider's skin should retain natural
texture and warm tonal variation.

---

# 13. HOVER HEIGHT

Nominal virtual hover height:
20–35 centimeters.

The motorcycle remains suspended above
the studio floor.

No conventional wheel contact.

No landing gear contact.

No visible support structures.

The image communicates hovering through
vehicle-floor separation and the corresponding
cast shadow.

The indicated height is a visual reconstruction
parameter rather than a measured physical distance.

---

# 14. GROUND SHADOW

The motorcycle casts a broad diffuse shadow
onto the gray studio floor.

The shadow follows the vehicle's projected
silhouette.

The front fairing contributes a large rounded
shadow region.

The central chassis contributes a narrower region.

The rear turbine contributes a distinct rounded
or elongated shadow region beneath the rear.

The combined shadow should remain coherent.

The shadow appears displaced downward and slightly
toward image-right.

Its edges are soft.

There are no sharp physical contact shadows.

The shadow must reflect the presence of the
centrally mounted rear turbine.

Avoid disconnected shadow shapes.

No visible exhaust turbulence affects the floor.

---

# 15. PROPULSION VISUALIZATION

The reference scene depicts stationary hovering.

The forward dual nozzles point downward.

The rear gimbaled turbine also points downward
in its vertical-lift configuration.

No visible flames.

No smoke.

No exhaust trails.

No glowing jet plumes.

No motion blur.

The thrust system is represented through
mechanical design and nozzle orientation.

The vehicle's suspension above the ground
communicates operational lift.

---

# 16. MATERIALS

Purple fairing:
Glossy metallic automotive paint.

Carbon-fiber turbine:
Dark woven composite.

Exposed chassis:
Brushed aluminum and polished steel.

Structural hardware:
Steel and muted brass.

Seat:
Black synthetic leather.

Rider shorts:
Glossy black leather.

Rider gloves:
Dark brown leather.

Rider boots:
Structured brown leather.

Windscreen:
Transparent lightly tinted material.

Floor:
Smooth matte neutral gray.

---

# 17. GEOMETRIC CONSISTENCY

The vehicle must preserve its original
front-to-rear proportions.

The rear turbine remains substantial.

Do not shrink the turbine to accommodate
the new mounting location.

Do not introduce a second rear engine.

The turbine must not intersect the rear seat,
foot supports, or rider's legs.

The gimbal must attach directly to the
structural chassis.

The rear turbine must remain mechanically
connected to the motorcycle.

The front dual thrusters must remain
beneath the forward fairing.

The front and rear propulsion systems must
remain visually distinct.

---

# 18. RECONSTRUCTION PROMPT

Create a high-fidelity photorealistic CGI studio
image of a futuristic Aprilia hover motorcycle
carrying Sienna, a fictional 26-year-old woman
with long voluminous auburn-chestnut hair,
hazel-green eyes, fair warm-peach skin,
subtle freckles, and a slender athletic build.

Sienna leans forward over the motorcycle in an
athletic riding posture.

She wears an opaque fitted white short-sleeved
shirt, black high-waisted leather shorts,
dark brown riding gloves, tall brown leather
boots with buckled straps, small gold stud
earrings, and a thin gold necklace.

Her expression is focused, confident, and composed.

The motorcycle has a long aerodynamic purple-blue
front fairing, red-orange racing stripes,
large white Aprilia logos, a black circular
front intake, transparent curved windscreen,
exposed metallic chassis, silver engine casing,
gold-toned mechanical hardware, and a narrow
black racing seat.

Beneath the forward belly fairing, retain a
compact dual-nozzle carbon-fiber vertical-lift
assembly.

Both forward nozzles point vertically downward.

Beneath the rear tail, install exactly one
large cylindrical carbon-fiber turbine engine.

Center this engine along the motorcycle's
longitudinal centerline.

Preserve its original dimensions, radial turbine
structure, black carbon-fiber housing, red-orange
graphics, and white Aprilia branding.

Mount the rear turbine inside a mechanically
detailed 360-degree gimbaled support assembly.

The gimbal allows the rear turbine to rotate
between vertical-lift and forward-propulsion
orientations.

The rear turbine provides both vertical lift
and forward propulsion.

Depict the motorcycle in stationary-hover mode.

The rear turbine is rotated into its vertical-lift
configuration, with its exhaust outlet pointing
downward toward the studio floor.

The front dual-nozzle assembly also points downward.

No visible exhaust, flames, smoke, or propulsion
plumes.

The motorcycle floats approximately 20–35 cm above
a seamless neutral-gray studio floor.

Use a front-left three-quarter camera perspective
with a virtual 75 mm lens.

Illuminate the rider and motorcycle with a large
softbox above camera-left and subtle fill
illumination from camera-right.

Maintain glossy metallic paint reflections,
realistic carbon-fiber texture, detailed mechanical
components, natural skin texture, and physically
plausible materials.

Cast a broad, diffuse shadow beneath the hovering
motorcycle.

The shadow must include the visual contribution
of the central rear turbine.

Preserve the original motorcycle silhouette,
rider identity, rider posture, and Aprilia branding.

---

# 19. EXCLUSION REQUIREMENTS

No wheels.

No duplicated rear turbines.

No laterally offset rear turbine.

No oversized secondary engines.

No permanently fixed rear thrust orientation.

No disconnected turbine housing.

No engine intersection with rider or chassis.

No visible flames.

No smoke.

No exhaust plumes.

No additional riders.

No exaggerated facial expressions.

No distorted human anatomy.

No unnecessary decorative lighting.

No changes to Sienna's facial identity.

No changes to the original motorcycle colors
or branding.

---

# 20. FINAL DESIGN LOCK

The Aprilia hover motorcycle uses two physically
distinct propulsion assemblies.

The forward assembly contains two downward-facing
vertical-lift nozzles.

The rear assembly contains exactly one large
centrally mounted turbine.

The rear turbine rotates through a full 360-degree
mechanical range using an articulated gimbal.

The turbine provides vertical lift when its exhaust
is directed downward.

It provides forward propulsion when its exhaust
is directed rearward.

Intermediate orientations provide combined
vertical and forward thrust.

The stationary-hover reference depicts both
assemblies producing upward reaction forces.

The motorcycle remains level.

Sienna maintains her forward-leaning riding posture.

The image preserves the established camera angle,
lighting, materials, branding, and soft ground shadow.

This specification establishes the final propulsion
architecture and visual reconstruction baseline.

# END

Engineering clarification
The governing design principle is thrust-vector control rather than rotation alone.
The rear assembly requires an articulated support capable of transmitting thrust loads while permitting rotation. A 360-degree mechanical range provides positioning flexibility, but the control system must select an appropriate thrust direction for the current flight condition.
One distinction is worth preserving in future renderings. The turbine's intake and exhaust are opposite ends of the propulsion system. During vertical lift, the exhaust outlet must face downward so the reaction force acts upward. During forward acceleration, the exhaust must face rearward.
For the next image, the rear engine should appear centrally mounted beneath the tail, with its exhaust outlet directed vertically downward, while retaining its original cylindrical housing and Aprilia branding.