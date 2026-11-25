# Catalogue build and maintenance

The canonical catalogue is `parts/`; each `parts_source/<OOMP ID>/working.yaml`
supplies its metadata and geometry parameters. The existing project geometry
functions remain in `working_scad.py`. The refresh preserves the active catalogue,
including local geometry changes, and never scans archived or legacy folders.

## Rebuild

Install `requirements-catalogue.txt` in the project's configured Python environment.
The existing OOBB library must also be importable. OpenSCAD and Blender are required;
use `OPENSCAD_EXE` and `BLENDER_EXE` when they are not on PATH. Native projects retain
their `solidcraft/config.json` helper and Python configuration.

Run `python catalogue.py build` (or the project's make-all entry). All active source
records are merged synchronously, CAD is generated using the project's recipes,
STLs are exported with checked subprocess results, previews are completed, and only
then are READMEs/navigation generated and validated. A failed export or render
fails the build. OpenSCAD STLs remain enabled where they are the production source.
The timing-belt storage adapter uses its native recipe and avoids duplicate STL export.

Use `--filter <OOMP-ID-substring>` for a focused build; unchanged parts stay in the
catalogue. Use `--populate` explicitly to regenerate the source catalogue definitions.
Use `--native` to additionally run an available native adapter. Legacy Roboclick/
CorelDraw actions are opt-in with `--legacy-actions`; make-all does not launch desktop
automation by default. Existing labels and specialised examples are preserved.

`python catalogue.py render` refreshes previews and docs. `python catalogue.py docs`
refreshes documentation alone; `python catalogue.py verify` checks coverage, artifact
hashes, PNGs and generated local links. `python working_navigation.py` is compatible
with older navigation callers and also refreshes the printable STL at each taxonomy leaf.

## Documentation contract

The project README leads with the assembled basic connector. Its catalogue links each
wired variant to the canonical part README, browser guide and printable assembly book.
Every wired part and the project Assembly section use the same four steps from
`assembly.json`. Each part page retains its full OOMP ID and metadata. Manual text
outside the generation markers is preserved.

A printable taxonomy leaf contains `README.md`, `oomp_id.txt` and a byte-for-byte copy
of the canonical `3dpr.stl`. Other assets stay in the part folder.

## Rendering and validation

The vendored Blender worker uses the OOBB satin-teal, warm-background studio style
on actual STL geometry, with angled/top views and a measured envelope. It does not
invent details, alter holes or smooth away geometry. Raw views and logs stay under
ignored `build/`; final 1600×1000 sheets and a SHA256 manifest are published.
Cache identity includes geometry, renderer, Blender version, label and sheet code.
Both ASCII and binary STL are accepted. Purchased hardware records are not rendered.

## Connector assemblies

Install the published [OOMP electronic catalogue](https://github.com/oomlout/oomp_electronic_version_5)
as a sibling checkout or set `OOMP_ELECTRONIC_ROOT` to its location. The build reads
the prepared long headers, housings and socket contacts directly from that checkout.
Its STEP assets require the OpenCascade Python bindings in the requirements file.

~~~powershell
python catalogue.py render
python validate_wire_catalogue.py
~~~

To refresh one connector, add `--filter <part-id-fragment>` to the catalogue render.
To recompose assembly sheets and guides from existing Blender views, run
`python render_wire_catalogue.py --reuse --no-headers` followed by `python catalogue.py docs`.
The standalone renderer also supports updating the hardware catalogue with
`python render_wire_catalogue.py` from a full writable OOMP checkout.

Each wired variant has bare-print, prepared-header, exploded, seating and assembled
views. The book renderer uses the same four assembly steps and CAD views as the
README. It writes the A4 PDF and a standalone viewer under the canonical part's
`assembly/` directory. The viewer starts on the four-step page and embeds the
rendered PDF pages and their hardware links. GitHub Actions publishes the guides
to Pages when their files change on main.

The header dimensions, pin patterns and quantities are described in the
[assembly notes](presentation/wire_catalogue_notes.md).

## Storage and Git history

The initial refresh was explicitly authorised to replace history after verification.
Verified worktree archives, hash manifests and original Git bundles are retained
outside this checkout under `C:/gh/_repository_recovery/catalogue_refresh_2026-11-14/`.
They preserve old navigation-only material and uncommitted work. Ignored build and
dependency caches are local and excluded from the published tree.

Normal future updates use ordinary commits. Do not reset history on each build.
Any future reset must preserve current files, all relevant refs, dirty/index changes
and remote-only work, then validate the final tree. Create a parentless commit from
that reviewed tree and publish only with an explicit old-remote-SHA lease. Verify an
independent full clone before expiring old local reflogs or collecting objects.
Do not claim GitHub server storage is reclaimed simply because its branch changed.

[Refresh record](MAINTENANCE.md)
