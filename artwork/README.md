# Artwork sources and archive

This repository owns the artwork formerly stored in both profile repositories'
`assets_readme/` directories. Both profile READMEs retain their eleven referenced
SVG contact and profile icons; their unused artwork is preserved here once per
unique file. The two source repositories contained identical copies of all eight
unused assets, so no differing variants needed separate archive filenames.

## Runtime assets

- `../assets/earth_satellite.png` is the original transparent APNG, unchanged:
  720 × 420 pixels, 144 frames at 50 ms each, looping every 7.2 seconds, and
  530,362 bytes. It retains the satellite, rotation, orbit, radiation, and Earth.
- `../assets/earth_satellite_still.png` is a standalone RGBA PNG decoded from the
  APNG's first frame, with identical pixels and transparency. It contains one
  frame and can be used as a static fallback.
- `../assets/chip_radiation_logo.png` is the canonical transparent logo. The two
  former `Logo_Chip_Radiation_Transparent.png` copies were byte-identical to this
  existing file and were removed without creating an archive duplicate.

## Animation source and renderer

`orbiting_chip.gif` is the unchanged original opaque orbital GIF (857,842 bytes).
The renderer now belongs to this website at
`../scripts/render_satellite_orbit.py`. With Pillow, NumPy, and SciPy installed,
rebuild the animation from the website repository root:

```bash
python3 scripts/render_satellite_orbit.py
```

The renderer removes the static sky using a temporal median and preserves the
original Earth disk and moving foreground. Its indexed palette reserves a
transparent slot. APNG changed rectangles use SOURCE blending so old satellite
pixels become transparent while the static Earth remains. Frame order and timing
come from the source GIF.

After rebuilding the animation, regenerate its static fallback from the website
repository root:

```bash
python3 - <<'PY'
from PIL import Image

with Image.open('assets/earth_satellite.png') as animation:
    animation.seek(0)
    animation.convert('RGBA').save(
        'assets/earth_satellite_still.png',
        format='PNG', optimize=True, compress_level=9,
    )
PY
```

## Legacy artwork and migration audit

`legacy/` preserves the unused black logo, full IEEE SVG, quantum tunneling
banner, radiation-hard chip image, and radiation-test animation. These files are
archival artwork rather than runtime dependencies. All migrated source bytes are
unchanged. The SHA-256 values below identify the unique originals from each
profile repository and their canonical destinations relative to this directory.

| Former filename in `assets_readme/` | Canonical destination | SHA-256 |
| --- | --- | --- |
| `Logo_Chip_Radiation_Blacked.png` | `legacy/Logo_Chip_Radiation_Blacked.png` | `3b6dfef47ea56d1f244f0b125c6f46f652570d81773b87d5b0c5cafa649d115c` |
| `Logo_Chip_Radiation_Transparent.png` | `../assets/chip_radiation_logo.png` | `2a5c10b50817280528084ad34e43a2d63038e326c979b57b1711cd4e19eca389` |
| `earth_satellite.png` | `../assets/earth_satellite.png` | `1b79fcbe19d2e7e1171aa728e603a3cce8955f5c8a04a6dc40447d499727c4ba` |
| `ieee_full.svg` | `legacy/ieee_full.svg` | `d6079c785269d3dd5fd06daadce5e3136df45623452772d7b164f1921e6f2629` |
| `orbiting_chip.gif` | `orbiting_chip.gif` | `69cb25acc50dff1f34da691867bf6399be0094ce87fb66afef1ab49f04f08d58` |
| `quantum_tunneling_banner.gif` | `legacy/quantum_tunneling_banner.gif` | `02172dd99463d4bddeb7764b07548e66fd01f557175cb71ac66b07d2c0672c34` |
| `rad_hard_chip.png` | `legacy/rad_hard_chip.png` | `12bf327034e23858cc13fb40a416c01d752c3be732a2da2f4192c720c54a4af0` |
| `radiation_test.gif` | `legacy/radiation_test.gif` | `3c5fd4c52ec11731d3f101ee4e9c90c5e04d07ff11b2ed8e87eabd78a6ebd2e8` |
