"""Export the original orbital animation with transparency as a compact APNG.

Requires Pillow, NumPy, and SciPy. Run from the website repository root:
    python3 scripts/render_satellite_orbit.py

The original GIF is the source of every foreground pixel. Satellite position,
rotation, radiation effects, Earth texture, frame order, and timing are retained.
"""
from pathlib import Path

import numpy as np
from PIL import Image, ImageSequence
from scipy import ndimage

ROOT = Path(__file__).resolve().parents[1]
SOURCE = ROOT / "artwork" / "orbiting_chip.gif"
OUTPUT = ROOT / "assets" / "earth_satellite.png"
TRANSPARENT = 255


def read_source():
    with Image.open(SOURCE) as image:
        frames, durations = [], []
        for frame in ImageSequence.Iterator(image):
            frames.append(np.asarray(frame.convert("RGB")))
            durations.append(frame.info.get("duration", 50))
    return np.stack(frames), durations


def foreground_masks(frames):
    # The sky is static. A temporal median recovers it even where the satellite
    # passes; the unchanged Earth is retained separately as its original disk.
    background = np.median(frames[::4], axis=0).astype(np.int16)
    height, width = frames.shape[1:3]
    y, x = np.ogrid[:height, :width]
    earth = (x - width / 2) ** 2 + (y - height / 2) ** 2 <= 120 ** 2
    for frame in frames:
        difference = np.max(np.abs(frame.astype(np.int16) - background), axis=2)
        moving = ndimage.binary_closing((difference >= 12) & ~earth, structure=np.ones((3, 3)))
        labels, _ = ndimage.label(moving)
        sizes = np.bincount(labels.ravel())
        sizes[0] = 0
        if not sizes.any():
            raise ValueError("Could not locate the original satellite")
        cy, cx = ndimage.center_of_mass(labels == sizes.argmax())
        # Keep the satellite and its nearby original radiation effects; discard
        # isolated sky noise. Fill enclosed solar cells and the opaque chip bus.
        nearby = (x - cx) ** 2 + (y - cy) ** 2 < 125 ** 2
        moving = ndimage.binary_fill_holes(moving & nearby)
        yield earth | moving


def main():
    source, durations = read_source()
    palette = Image.fromarray(source[0]).quantize(colors=255, method=Image.Quantize.MEDIANCUT)
    frames = []
    for rgb, mask in zip(source, foreground_masks(source)):
        frame = Image.fromarray(rgb).quantize(palette=palette, dither=Image.Dither.NONE)
        # PNG must explicitly include the reserved transparent palette slot;
        # GIF padded short palettes automatically, but PNG does not.
        colors = frame.getpalette()
        frame.putpalette(colors + [0] * (768 - len(colors)))
        frame.paste(TRANSPARENT, mask=Image.fromarray((~mask * 255).astype(np.uint8)))
        frame.info["transparency"] = TRANSPARENT
        frames.append(frame)
    # APNG stores only changed rectangles and can replace pixels with transparency.
    # The static Earth is stored once, without a setup frame or satellite trails.
    # SOURCE blending replaces each rectangle, including its transparent pixels.
    frames[0].save(OUTPUT, save_all=True, append_images=frames[1:], duration=durations,
                   loop=0, transparency=TRANSPARENT, disposal=0, blend=0,
                   compress_level=9, optimize=True)
    print(f"Rendered {OUTPUT}: {len(frames)} original frames, {sum(durations) / 1000:g} seconds, {OUTPUT.stat().st_size:,} bytes")


if __name__ == "__main__":
    main()
