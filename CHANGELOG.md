# Change Log

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](http://keepachangelog.com/)
and this project adheres to [Semantic Versioning](http://semver.org/).


## [In Development] - Unreleased

### Changed

- Chat list parser re-enabled. See Warning in [README.md](README.md).


## [0.0.1-alpha.11] - 2023-08-23

### Changed

- Sticky highlight in D-Scan tables re-introduced
- "On grid" detection for Upwell structures improved
- Only show a D-Scan table when there is actual data available


## [0.0.1-alpha.10] - 2023-08-22

### Fixed

- Return empty jSon when no data for ajax call
- Empty scan sections will no longer be stored in the database

### Added

- Unique relation between scan and scan section in the database table
- Detection of Upwell structures that are on grid on D-Scans (No UI for it yet, though)

### Removed

- Nonsensical exclude clause


## [0.0.1-alpha.9] - 2023-08-22

### Changed

- On grid detection for D-Scans improved
- Ship parser refactored
- JS for highlighting in D-Scan result tables improved
- Sticky highlight in D-Scan tables removed for the time being for being faulty


## [0.0.1-alpha.8] - 2023-08-15

### Changed

- Hard disabling the chat list parser for now


## [0.0.1-alpha.7] - 2023-08-13

### Fixed

- Bootstrap CSS fix (Sounds weird, but it is what it is …)
- Make D-Scan regex less greedy

### Changed

- Order admin list by creation date descending
- Reduced the size of the saved jSon data


## [0.0.1-alpha.6] - 2023-08-12

### Changed

- Django admin page finished
- Modal verbose names
- Admin descriptions are now translatable


## [0.0.1-alpha.5] - 2023-08-12

### Fixed

- Dealing with re-used character names from biomassed characters years ago

### Changed

- Use the `EveCharacter` model functions to generate character portraits and alliance-
  and corp logos


## [0.0.1-alpha.4] - 2023-08-11

### Changed

- Moved regex patterns to their own dedicated constant `REGEX_PATTERN`
- Clearer error messages
- Constant `SUPPORTED_INTEL_TYPES` extended
- pre-commit config cleaned up
- Pre-load command renamed


## [0.0.1-alpha.3] - 2023-08-11

### Changed

- Raise exceptions instead of returning `None` for our parser
- Deactivate no yet implemented module (fleet composition) by default


## [0.0.1-alpha.2] - 2023-08-10

### Added

- Command to pre-load Eve data


## [0.0.1-alpha.1] - 2023-08-10

### Added

- Chat Scan Module
- D-Scan Module
