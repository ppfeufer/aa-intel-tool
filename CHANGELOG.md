# Change Log

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](http://keepachangelog.com/)
and this project adheres to [Semantic Versioning](http://semver.org/).

<!--
GitHub MD Syntax:
https://docs.github.com/en/get-started/writing-on-github/getting-started-with-writing-and-formatting-on-github/basic-writing-and-formatting-syntax

Highlighting:
https://docs.github.com/assets/cb-41128/mw-1440/images/help/writing/alerts-rendered.webp

> [!NOTE]
> Highlights information that users should take into account, even when skimming.

> [!IMPORTANT]
> Crucial information necessary for users to succeed.

> [!WARNING]
> Critical content demanding immediate user attention due to potential risks.
-->

## [In Development] - Unreleased

<!--
Section Order:

### Added
### Fixed
### Changed
### Deprecated
### Removed
### Security
-->

### Changed

- Tooltip JS function simplified

## [2.8.0] - 2025-08-14

### Changed

- Use AA framework JS functions
- Minimum requirements
  - Alliance Auth >= 4.9.0

## [2.7.2] - 2025-08-05

### Changed

- Translations updated

## [2.7.1] - 2025-07-08

### Added

- Default/Fallback exception message for `ParserError`

### Changed

- Cast some translated strings to `str` to avoid potential issues
- Translations updated

### Removed

- Unused constants

## [2.7.0] - 2025-06-03

### Changed

- Translations updated

### Removed

- Redundant header from public page
- Cache breaker for static files. Doesn't work as expected with `django-sri`.

## [2.6.3] - 2025-05-05

### Change

- Improve "Unaffiliated / No Alliance" panel in chat list scan, to bring the visual in line with the rest of the panels
- Number of JS events reduced to improve JS performance
- Translations updated

## [2.6.2] - 2025-04-09

### Added

- More tests

### Fixed

- Spelling (It's EVE time, not Eve time)

### Changed

- Python code refactored/optmized
- JavaScript code refactored/optmized
  - HTML markup for the result tables is now unified

## [2.6.1] - 2025-03-07

### Changed

- Improve templatetag code
- Use DataTables native translations instead of our own

## [2.6.0] - 2025-01-31

### Changed

- Use `django-sri` for sri hashes
- Minimum requirements
  - Alliance Auth >= 4.6.0

## [2.5.3] - 2025-01-13

### Added

- Integrity hashes for static CSS and JS files

### Fixed

- Escaping translation strings to fix potential issues with French and Italian translations
- Search field positioning in the DataTables
- Sticky behaviour in fleet composition details tables

### Changed

- Set user agent according to MDN guidelines
- Better JS options merge

## [2.5.2] - 2024-12-14

### Added

- Python 3.13 to the test matrix

### Changed

- Translations updated

## [2.5.1] - 2024-11-01

### Changed

- Ukrainian translation improved

## [2.5.0] - 2024-09-16

### Changed

- Dependencies updated
  - `allianceauth`>=4.3.1
- French translation improved
- German translation improved
- Japanese translation improved
- Lingua codes updated to match Alliance Auth v4.3.1

## [2.4.0] - 2024-07-27

### Added

- Prepared Czech translation for when Alliance Auth supports it

### Changed

- Chinese translation improved
- French translation improved

## [2.3.0] - 2024-06-30

### Added

- Bootstrap tooltips to the scan result tables

### Changed

- French translation updated

## [2.2.0] - 2024-06-23

### Added

- `autofocus` attribute to textarea, so the form field is focused on page load

### Fixed

- "Interesting on grid" section is now properly hidden when no data is available

### Changed

- Refactored `fleetcomp.parser` to reduce complexity and improve readability

### Removed

- Support for Python 3.8 and Python 3.9

## [2.1.1] - 2024-05-16

### Changed

- Translations updated

## [2.1.0] - 2024-04-21

### Added

- Total mass to ship class tables

### Fixed

- zKillboard Link for corporations in scan results (Fixing #81)
- Ship with cosmic sig-like name makes parsing fail (Fixing #82)

## [2.0.0] - 2024-03-16

> [!NOTE]
>
> **This version needs at least Alliance Auth v4.0.0!**
>
> Please make sure to update your Alliance Auth instance **before**
> you install this version, otherwise, an update to Alliance Auth will
> be pulled in unsupervised.

### Added

- Compatibility to Alliance Auth v4
  - Bootstrap 5
  - Django 4.2

### Changed

- JS modernized
- CSS modernizes
- Templates changed to Bootstrap 5
- Translations improved

### Removed

- Compatibility to Alliance Auth v3

## [2.0.0-beta.1] - 2024-02-18

> [!NOTE]
>
> **This version needs at least Alliance Auth v4.0.0b1!**
>
> Please make sure to update your Alliance Auth instance **before**
> you install this version, otherwise, an update to Alliance Auth will
> be pulled in unsupervised.

### Added

- Compatibility to Alliance Auth v4
  - Bootstrap 5
  - Django 4.2

### Changed

- JS modernized
- CSS modernizes
- Templates changed to Bootstrap 5
- Translations improved

### Removed

- Compatibility to Alliance Auth v3

## [1.2.0] - 2023-10-04

> [!NOTE]
>
> **This is the last version compatible with Alliance Auth v3.**

### Added

- Support for lazy loading images, which should speed up the page load on larger scans

### Changed

- JS modernized
- Translations improved
  - Korean
  - Russian
  - Spanish

## [1.1.3] - 2023-09-26

### Fixed

- Capitalization for translatable strings

### Changed

- Translations updated

### Removed

- Unused Python file

## [1.1.2] - 2023-09-14

### Fixed

- Wrongfully triggered sticky highlight when clicking on a link in a result table row

### Change

- Use `bulk_create` on save action to create the scan data sections instead of saving
  each section individually
- JS compressed

## [1.1.1] - 2023-09-02

### Changed

- Korean translation improved

## [1.1.0] - 2023-09-01

### Added

- Korean translation

## [1.0.1] - 2023-08-31

This version is purely to push changes in the README to Pypi.

### Fixed

- Some little whoopsies in README

## [1.0.0] - 2023-08-31

**First Public Release**

### Added

- MySQL script to drop the DB tables

### Fixed

- Pilots in fleet count on fleet composition result page
- Missing semicolons in JavaScripts
- JS function attribute name
- Translations cleaned up

### Changed

- Migrations from Alpha-versions reset

### Update Instructions for Updating From an Alpha-Version

> **Note**
>
> If you have installed one of the Alpa-Versions before, make sure to follow these
> instructions **before** you update to this version. If you install this app for the
> very first time, feel free to happily ignore this section.

#### Remove the Migrations and DB Tables

During the alpha phase a number of DB migrations accumulated, which is, for obvious
reasons, not ideal for the first public version to have. So, they need to be reset.
This will happen in 2 steps.

##### From Django

Run the following command in your virtual environment:

```shell
python manage.py migrate aa_intel_tool zero --fake
```

This will remove the migration information from Django.

##### From Your MySQL Database

Now you need to remove the DB tables. This needs to be done to make sure the new
migration runs without issues. Don't worry, this is not hard at all, I've prepared a
little something for you.

All you need to do is, log in to your MySQL server from your console. and select the
Alliance Auth DB.

Log in:

```shell
mysql -h localhost -u allianceserver -p
```

Switch to the `alliance_auth` DB:

```mysql
USE alliance_auth;
```

Now copy/paste the following:

```mysql
SET FOREIGN_KEY_CHECKS=0;
DROP TABLE IF EXISTS aa_intel_tool_scandata;
DROP TABLE IF EXISTS aa_intel_tool_scan;
SET FOREIGN_KEY_CHECKS=1;
```

Once done, exit out of your MySQL server and run the update as usual.

## [0.0.1-alpha.14] - 2023-08-28

Hopefully the last one before official release …

### Added

- Fleet composition scan as intel type

### Changed

- Moved template designation to `SUPPORTED_INTEL_TYPES` constant
- Translation files updated

## [0.0.1-alpha.13] - 2023-08-25

### Added

- `fetchAjaxData` function introduced to our JS framework

## [0.0.1-alpha.12] - 2023-08-24

### Added

- Upwell structures on grid to D-Scan result page
- Deployables on grid to D-Scan result page
- Pos / Pos Modules on grid to D-Scan result page
- Destination system to Ansiblex Jump Gate in D-Scan

### Changed

- Chat list parser re-enabled. See Warning in [README.md](https://github.com/ppfeufer/aa-intel-tool/blob/master/README.md#settings) (=> Settings).

## [0.0.1-alpha.11] - 2023-08-23

### Changed

- Sticky highlight in D-Scan tables re-introduced
- "On grid" detection for Upwell structures improved
- Only show a D-Scan table when there is actual data available

## [0.0.1-alpha.10] - 2023-08-22

### Added

- Unique relation between scan and scan section in the database table
- Detection of Upwell structures that are on grid on D-Scans (No UI for it yet, though)

### Fixed

- Return empty jSon when no data for ajax call
- Empty scan sections will no longer be stored in the database

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
