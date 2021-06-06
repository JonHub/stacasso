# Changelog
All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [0.3.0] - 2021-06-06

Beta release of code.

- "Pretty print" renamed to `pprint( circuit )`
- Syntax highlighting (including pretty print) now powered by `highlight( circuit )` function, which exports highlighted strings as `.html`
- Ouput graphics as `.svg` now auto-scale to circuit size
- Added `setup.py`, so package can be installed using `pip install -e .`, and unintalled with `pip uninstall`
- Wavefunction states (up to four qubits) now be correctly unscrambled using `unscramble_wavefunction`.   (Order returned by `cirq.Simulator` is permutted.)
- The `illustrate( circuit )` function automatically draws the wavefunction evolution (works with up to four quibits.)

## [0.0.1] - 2021-05-10

Initial code release.

### Added
- README.md, CHANGELOG.md
- LICENSE (Apache 2.0)
- initial code in `/code` directory 
- initial `stacasso_introduction` jupyter Noteboook (also render notebook to `.html`)