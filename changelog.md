# Changelog

All notable changes to this project will be documented in this file.

The format is based on "Keep a Changelog" (https://keepachangelog.com/en/1.0.0/)
and follows Semantic Versioning (https://semver.org/).

Sections:
- Unreleased — changes that are being prepared for the next release.
- Added, Changed, Deprecated, Removed, Fixed, Security — categories for changes.

---

## [Unreleased]
- (No unreleased changes at time of v3.0.0 release.)

---

## [3.0.0] - 2026-08-27
Major release: refactor and packaging milestone. This release reorganizes the project as an installable Python package, introduces CI and tests, improves documentation, and renames a small set of core functions (breaking API). These changes are intended to make MW‑Gui easier to install, test, and contribute to.

### Added
- Packaging: added pyproject.toml, setup.cfg, and MANIFEST.in — project is now pip-installable and produces sdist/wheel distributions.
- Console entry point `mw-gui` to launch the GUI after installation.
- Example resources bundled and packaged: molecule example files, water catalog, and metal list (examples accessible from the package or repo `exemple/` and `molecules/` directories).
- README quickstart with a minimal runnable example that completes in ~10 minutes.
- CHANGELOG.md (this file), CITATION.cff, and a skeleton CHANGELOG maintenance workflow.
- CONTRIBUTING.md and CODE_OF_CONDUCT.md to facilitate community contributions.
- Issue & PR templates and a dedicated "community interest" issue template for tester feedback.
- Basic GitHub Actions CI workflow that runs tests, lint, and builds the package on PRs.
- Unit tests and a smoke test for core utilities (core/xyz2inp, core/electrode_generator, core/generate_electrode_coords).
- Logging (using Python logging module) for core modules and improved error messages for common file I/O problems.
- A small release-ready example runner script to create reproducible test runs in CI.

### Changed
- Project layout and distribution: code packaged under the project package name (mw_gui_builder by default) and resources included in package data for installation.
- Core utilities renamed for clarity (breaking changes; aliases provided for backward compatibility where possible — see Migration notes):
  - `formate_lines` → `format_lines`
  - `mw_file_writting` → `mw_file_writing`
  - `mw_writting` → `mw_writing`
- Replaced ad-hoc print() debugging with structured logging in core modules (improves diagnosability in tests and CI).
- README updated with install and test instructions; example use cases documented in `exemple/` tutorials.
- Bundled third-party fftool retained but treated as a packaged convenience script with clear attribution and license note.

### Deprecated
- Old non-standard function names remain as deprecated aliases for one release cycle; they will be removed in the next major release (v4.x) unless otherwise requested.

### Removed
- (No removals beyond the above renames; deprecated aliases remain for transition.)

### Fixed
- Improved input validation and parsing robustness across core modules (fewer silent failures on malformed .xyz/.els files).
- Deterministic behavior for box-size detection and electrode insertion edge cases.
- Several small bugfixes surfaced by unit tests and community smoke tests.

### Security
- No security-related changes in this release.

### Notes
- This release is considered a breaking change relative to earlier versions due to API renames and packaging reorganization — see Migration / Upgrade notes below.

---

## [0.1.0] - 2025-06-30
Initial public release.

### Added
- Core GUI application:
  - Box generation tools (gui/box_generator.py)
  - XYZ → MetalWalls .inp converter (gui/converter.py + core/xyz2inp.py)
  - Electrode generator GUI and core routines (gui/electrode_builder.py, core/electrode_generator.py, core/generate_electrode_coords.py)
  - Parameter generator GUI and parameter writer (gui/parameter_generator.py, core/parameter_writer.py)
- Example cases in `exemple/` demonstrating workflows:
  - Water_Graphene
  - Ionic_Liquids_Platinum
  - Alkaline_HER_Platinum
- Distributed molecule files and resource tables (molecules/, ressources/).
- Bundled third-party fftool script (core/fftool) with license and attribution.

---

## Migration / Upgrade notes (important)
Because v3.0.0 reorganizes the codebase and renames several core functions, please follow these steps when upgrading from older versions:

1. Install the new package (recommended):
   - pip install --upgrade mw-gui
   - or from source: python -m pip install -e .

2. If your scripts import or call older function names, update them:
   - Replace occurrences:
     - `formate_lines(...)`  → `format_lines(...)`
     - `mw_file_writting(...)` → `mw_file_writing(...)`
     - `mw_writting(...)` → `mw_writing(...)`
   - For compatibility, v3.0.0 ships aliases so old calls should still work but will raise DeprecationWarnings; plan to update before v4.0.0.

3. If you relied on in-repo invocation paths (for example `core/fftool` run directly from repo root), the recommended approach is:
   - Install the package and run the CLI `mw-gui`, or
   - Use the packaged scripts via the installed package path (see README for examples).

4. Resource file locations:
   - Example and resource files are now included as package data. Consult README to discover installed resource paths, or access bundled resources via package resource APIs.

5. If you have continuous integration or automation that expects the old layout, update it to import from the package name (default: `mw_gui_builder`) or to run `mw-gui`.

---

## How to use this changelog and release process
- While developing:
  - Add every notable user-visible change to the Unreleased section under the appropriate category (Added / Changed / Fixed / Deprecated / Removed / Security).
- When releasing:
  1. Move Unreleased entries under a new version heading with version number and date.
  2. Set the version according to semantic versioning.
  3. Update CITATION.cff and README if required.
  4. Create a Git tag (e.g., `v3.0.0`) and a GitHub release pointing to this changelog entry.
  5. (Recommended) Link GitHub release to Zenodo to mint a DOI for the release.

### Example entry format
- Added:
  - Add XYZ converter with bohr conversion utility (core/xyz2inp.py) ([#17](https://github.com/julwolff/MW-Gui-Builder/pull/17))
- Fixed:
  - Fix parsing of electrode atom counts in header lines (core/electrode_generator.py) ([#19](https://github.com/julwolff/MW-Gui-Builder/issues/19))

---

## Guidelines for contributors / PR authors
- When opening a PR that contains user-visible changes:
  - Add a brief bullet to the Unreleased section under the appropriate category.
  - Use concise, descriptive bullet points. Prefer one bullet per distinct change.
  - Include links to relevant PRs or issues where helpful.
- The release manager (maintainer) should:
  - Ensure Unreleased items are moved to the release section when cutting a release.
  - Set the release date and version according to semantic versioning and project policies.

---

## Automation (optional recommendations)
- Consider adding a release script or GitHub Action to:
  - Validate that the changelog Unreleased section is empty after release.
  - Automatically generate a draft release body from Unreleased notes and PR links.
  - Validate that CITATION.cff and version metadata match the release tag.

---

