# Change Log

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](http://keepachangelog.com/)
and this project adheres to [Semantic Versioning](http://semver.org/).


## [In Development] - Unreleased


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
