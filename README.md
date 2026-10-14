<p align="center">
  <picture>
    <source media="(prefers-color-scheme: dark)" srcset="assets/lockup-dark.svg">
    <img src="assets/lockup-light.svg" alt="ducktape" width="470">
  </picture>
</p>

Canonical logo assets for the ducktape software projects. The mark is a duck peeking through a roll of duct tape. All SVG exports contain vector paths; the text in the lockups is outlined so it does not depend on a font installed by the viewer.

## Use the assets

| Need | File |
| --- | --- |
| Main icon | [`assets/mark-color.svg`](assets/mark-color.svg) |
| Icon at 64 px or smaller | [`assets/mark-small.svg`](assets/mark-small.svg) |
| Black-and-white icon | [`assets/mark-mono.svg`](assets/mark-mono.svg) |
| Square SVG favicon | [`assets/favicon.svg`](assets/favicon.svg) |
| Standalone name and mark | [`assets/lockup-light.svg`](assets/lockup-light.svg), [`assets/lockup-dark.svg`](assets/lockup-dark.svg) |
| Project name and mark | [`assets/product/`](assets/product/) |
| PNG icons, 32–1024 px | [`exports/png/`](exports/png/) |

Use the light lockup on light backgrounds and the dark lockup on dark backgrounds. Keep the mark's proportions and leave clear space around its torn tape end. The small icon omits fine rings and the nostril so the duck remains visible at small sizes.

The product repositories keep copies of the assets used in their READMEs. This repository is the source for edits and new exports.

## Source and regeneration

[`source/mark.svg`](source/mark.svg) is the editable vector master. The selected sketch and its raster refinement are preserved in [`concepts/`](concepts/) for reference. The wordmark uses outlined Liberation Sans Bold, with the font and its license in [`source/fonts/`](source/fonts/).

```sh
uv sync --locked
uv run --locked python scripts/build.py
```

The build writes the SVGs under `assets/` and transparent PNGs under `exports/png/`. Commit source and generated files together when the mark changes.

## Colors

| Part | Hex |
| --- | --- |
| Ink | `#1B1D20` |
| Tape | `#BFC1C4` |
| Tape side | `#83878B` |
| Bill | `#F6C82C` |
| Dark-background wordmark | `#F4F4F2` |
