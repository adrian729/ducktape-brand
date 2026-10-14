<p align="center">
  <picture>
    <source media="(prefers-color-scheme: dark)" srcset="assets/lockup-dark.svg">
    <img src="assets/lockup-light.svg" alt="ducktape" width="470">
  </picture>
</p>

Brand assets for the ducktape software projects. The mark combines the original selected tape artwork with the mallard duck. The tape pixels are preserved exactly outside the area covered by the duck.

## Use the assets

| Need | File |
| --- | --- |
| Master transparent artwork | [`source/mark.png`](source/mark.png) |
| Separate mallard cutout | [`source/duck-cutout.png`](source/duck-cutout.png) |
| Icon in SVG container | [`assets/mark.svg`](assets/mark.svg) |
| Square favicon | [`assets/favicon.svg`](assets/favicon.svg) |
| Standalone lockup | [`assets/lockup-light.svg`](assets/lockup-light.svg), [`assets/lockup-dark.svg`](assets/lockup-dark.svg) |
| Project lockups | [`assets/product/`](assets/product/) |
| PNG icon exports, 32–1024 px | [`exports/png/`](exports/png/) |

Use the light lockup on light backgrounds and the dark lockup on dark backgrounds. Keep the mark's proportions and leave clear space around the torn tape end. The product repositories contain copies of the files used in their READMEs.

## Source and regeneration

[`source/mark.png`](source/mark.png) is the 1536 × 1024 transparent master. The SVGs embed that image; they are **not fully vector artwork**. The lockup lettering is outlined vector text, using Liberation Sans Bold from [`source/fonts/`](source/fonts/).

The composition uses [`concepts/raster-refinement.png`](concepts/raster-refinement.png) as the original tape and extracts only the duck from [`source/duck-reference.png`](source/duck-reference.png). [`scripts/compose.py`](scripts/compose.py) scales the duck uniformly, composites it into the original, and checks that every pixel outside [`source/duck-edit-mask.png`](source/duck-edit-mask.png) matches the original exactly. The reference images and composition recipe are retained so future exports do not require redrawing the tape.

```sh
uv sync --locked
uv run --locked python scripts/build.py
```

The build first regenerates and checks the composition, then writes the SVGs under `assets/` and PNG sizes under `exports/png/`. Commit source and generated files together.

## Color direction

The duck uses a green head, yellow bill, white neck ring, and brown chest, following the supplied mallard photo. The tape stays neutral gray so the duck remains the focal point.
