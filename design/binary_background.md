# Original binary background

Source: [`src/binary_background.js`](../src/binary_background.js). Appearance and masking: [`src/site.css`](../src/site.css), specifically `#binary-field`, `.hero`, and `.hero::after`.

This is the original animation from the first published design, extracted from the former inline script. It is a decorative field of randomly generated `0` and `1` characters. It does not encode a document or display FPGA measurement data.

## Coordinate mapping

The canvas covers the hero section. Each vertical column stores a head position `y`, a speed, a tail length, and an array of binary characters. The glyph in a column is placed at:

```javascript
x = column_index * 22 + 7;
y = column_head_y - row_index * 22;
```

That gives a 22-pixel grid with a 7-pixel horizontal inset. Rows outside the canvas are skipped. On each drawing update, the column head moves down by its speed. Once the complete tail has left the canvas, the head restarts at `-22`.

## Drawing parameters

| Parameter | Original value |
| --- | --- |
| Grid spacing | 22 CSS pixels in both directions |
| Font | `11px Consolas, monospace` |
| Glyphs | Random `0` or `1` |
| Column count | `ceil(canvas_width / 22)` |
| Tail length | Random integer from 9 to 26 characters |
| Column speed | Random value from 1 to less than 3.5 pixels per drawing update |
| Character mutation | 13% chance per column per update; one random character is reassigned |
| Drawing interval | At least 65 ms between redraws, scheduled with `requestAnimationFrame` |
| Glyph RGB | `88, 166, 255`, the theme's `#58a6ff` blue |
| Leading alpha | `0.55` for every fourth column, `0.27` for others |
| Tail fade | Leading alpha multiplied by `1 - row_index / tail_length` |
| Canvas CSS opacity | `0.53`, with additional gradients behind the hero text |
| Resolution | Device pixel ratio, capped at 2 |

Each draw clears the old canvas and renders the full current state. The trails come from the stored rows and their opacity gradient. They are not smears left behind by earlier frames.

## Motion lifecycle

- A visitor's reduced-motion preference starts the background as a still frame.
- The pause/play control freezes or resumes the original canvas state.
- `IntersectionObserver` suspends drawing when the canvas is outside the viewport.
- `visibilitychange` suspends drawing while the browser tab is hidden.
- `ResizeObserver` resizes the canvas and recreates columns to fit the new dimensions.

The animation uses browser APIs and `Math.random()` only. There is no animation library, network connection, or binary image file required by the runtime.

## Regenerating the PNG

Start the local preview, then run:

```powershell
python scripts/export_assets.py
```

`design/exports/binary_background.png` is a frame exported directly from the canvas. It is a design reference; the website continues to run the JavaScript animation. Each regeneration can capture a different pattern because the original animation is intentionally random.
