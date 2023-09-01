# Change Log

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](http://keepachangelog.com/)
and this project adheres to [Semantic Versioning](http://semver.org/).

## \[In Development\] - Unreleased

## \[1.1.0\] - 2023-09-01

### Added

- Korean translation

## \[1.0.1\] - 2023-08-31

This version is purely to push changes in the README to Pypi.

### Fixed

- Some little whoopsies in README

## \[1.0.0\] - 2023-08-31

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
> very first time, feel free to happiely ignore this section.

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

## \[0.0.1-alpha.14\] - 2023-08-28

Hopefully the last one before official release …

### Added

- Fleet composition scan as intel type

### Changed

- Moved template designation to `SUPPORTED_INTEL_TYPES` constant
- Translation files updated

## \[0.0.1-alpha.13\] - 2023-08-25

### Added

- `fetchAjaxData` function introduced to our JS framework

## \[0.0.1-alpha.12\] - 2023-08-24

### Added

- Upwell structures on grid to D-Scan result page
- Deployables on grid to D-Scan result page
- Pos / Pos Modules on grid to D-Scan result page
- Destination system to Ansiblex Jump Gate in D-Scan

### Changed

- Chat list parser re-enabled. See Warning in [README.md](README.md) (=> Settings).

## \[0.0.1-alpha.11\] - 2023-08-23

### Changed

- Sticky highlight in D-Scan tables re-introduced
- "On grid" detection for Upwell structures improved
- Only show a D-Scan table when there is actual data available

## \[0.0.1-alpha.10\] - 2023-08-22

### Added

- Unique relation between scan and scan section in the database table
- Detection of Upwell structures that are on grid on D-Scans (No UI for it yet, though)

### Fixed

- Return empty jSon when no data for ajax call
- Empty scan sections will no longer be stored in the database

### Removed

- Nonsensical exclude clause

## \[0.0.1-alpha.9\] - 2023-08-22

### Changed

- On grid detection for D-Scans improved
- Ship parser refactored
- JS for highlighting in D-Scan result tables improved
- Sticky highlight in D-Scan tables removed for the time being for being faulty

## \[0.0.1-alpha.8\] - 2023-08-15

### Changed

- Hard disabling the chat list parser for now

## \[0.0.1-alpha.7\] - 2023-08-13

### Fixed

- Bootstrap CSS fix (Sounds weird, but it is what it is …)
- Make D-Scan regex less greedy

### Changed

- Order admin list by creation date descending
- Reduced the size of the saved jSon data

## \[0.0.1-alpha.6\] - 2023-08-12

### Changed

- Django admin page finished
- Modal verbose names
- Admin descriptions are now translatable

## \[0.0.1-alpha.5\] - 2023-08-12

### Fixed

- Dealing with re-used character names from biomassed characters years ago

### Changed

- Use the `EveCharacter` model functions to generate character portraits and alliance-
  and corp logos

## \[0.0.1-alpha.4\] - 2023-08-11

### Changed

- Moved regex patterns to their own dedicated constant `REGEX_PATTERN`
- Clearer error messages
- Constant `SUPPORTED_INTEL_TYPES` extended
- pre-commit config cleaned up
- Pre-load command renamed

## \[0.0.1-alpha.3\] - 2023-08-11

### Changed

- Raise exceptions instead of returning `None` for our parser
- Deactivate no yet implemented module (fleet composition) by default

## \[0.0.1-alpha.2\] - 2023-08-10

### Added

- Command to pre-load Eve data

## \[0.0.1-alpha.1\] - 2023-08-10

### Added

- Chat Scan Module
- D-Scan Module
