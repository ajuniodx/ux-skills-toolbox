---
name: tv-motion
description: Use when designing or reviewing animations and micro-interactions for TV interfaces (Android TV, Google TV, Fire TV, launchers, widget dashboards) navigated by remote/D-pad, especially on low-end Android TV / Fire TV devices (1–2 GB RAM).
---
# Motion for TV (10-foot UI)

## Principles
1. **Focus is the primary animation.** Users only know where they are through focus. Every focusable item needs a visible focus state within 1 frame (never wait for an animation to finish).
2. **Animation never blocks the D-pad.** Remote input has priority; if the user presses again, interrupt and move to the new target.
3. **Short and predictable.** At ~3 m (10 ft), large slow movements are tiring; tiny ones disappear.
4. **Weak hardware rules.** Design for a stable 30 fps on a low-end 1 GB device; 60 fps is a bonus.

## Tokens (defaults)
| Use | Duration | Easing |
|---|---|---|
| Focus in (scale/elevation/border) | 120–150 ms | ease-out (FastOutSlowIn / cubic-bezier(0.2,0,0,1)) |
| Focus out | 90–120 ms | ease-in |
| Row/grid scroll to focused item | 200–250 ms | ease-in-out |
| Screen/panel enter | 250–300 ms | ease-out, fade + offset ≤ 48 dp |
| Screen exit (Back) | 180–220 ms | ease-in |
| Widget data update | 150–200 ms crossfade | linear/ease |
| Overlay/notification | in 250 ms, out 200 ms | ease-out/in |

- Focus scale: **1.05–1.10** (cards), never > 1.15. Combine with a 2–4 dp border/highlight and slight elevation.
- Offsets in multiples of 8 dp. No bounce/elastic, heavy parallax or animated blur.

## Performance rules (low-end devices)
- Animate only **transform and opacity** (scale, translation, alpha). Avoid animating size/layout, large shadows, blur and gradients.
- At most **1 continuous animation** on screen (e.g. a clock or ticker). Widgets update via crossfade, never a grid re-layout.
- Pre-sized images; never decode large images during an animation.
- No looping video/Lottie behind the home screen; Lottie only for occasional, lightweight moments.
- Long-press/fast scroll: disable intermediate animations and jump directly (focus throttle ~1 item per 80–100 ms).
- Test with Android's "Animator duration scale" at 1x and 0x; the UI must work with animations off.

## Implementation
- **Jetpack Compose for TV** (preferred): `androidx.tv.material3` (Card/Surface with `scale`, `border`, `glow` per focus state), `animateFloatAsState`/`updateTransition` with `tween(150, easing = FastOutSlowInEasing)`, `Modifier.graphicsLayer { scaleX = s; scaleY = s }` (not `size`). Lists with `LazyRow/LazyColumn` + `BringIntoViewSpec` for scroll-to-focus.
- **Views/Leanback**: `FocusHighlight` / `View.animate().scaleX().scaleY().setDuration(150)`; `hardwareAccelerated=true`.
- **Web (dashboard in WebView/kiosk)**: `transform`/`opacity` with `will-change` only on the focused item; `:focus-visible` with a 150 ms transition; respect `prefers-reduced-motion`.
- Centralize tokens in one file (`Motion.kt` / `motion.css`) and use only those.

## Review checklist
- [ ] Focus visible immediately on every item, including with animations off
- [ ] No navigation animation > 300 ms; the D-pad never waits
- [ ] Only transform/opacity animated; ≤ 1 continuous animation
- [ ] Back always has a clear, fast exit
- [ ] Tested on a real low-end device (not just an emulator), holding the D-pad for 3 s on a grid
- [ ] Readable at 3 m: contrast ≥ 4.5:1, body text ≥ 24 sp, 5% safe-area margins (overscan)
