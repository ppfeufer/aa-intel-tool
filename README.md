# AA Intel Tool

[![Badge: Version]][AA Intel Tool on Pypi]
[![Badge: License]][AA Intel Tool License]
[![Badge: Supported Python Versions]][AA Intel Tool on Pypi]
[![Badge: Supported Django Versions]][AA Intel Tool on Pypi]
![Badge: pre-commit]
[![Badge: Code Style: black]][black code formatter documentation]
[![Badge: Support Discord]][Support Discord]
[![Badge: Automated Tests]][Automated Tests on GitHub]
[![Badge: Code Coverage]][AA Intel Tool on Codecov]
[![Badge: Contributor Covenant]][Code of Conduct]

[![Badge: Buy me a coffee]][ppfeufer on ko-fi]


D-Scans and more in [Alliance Auth].

---

<!-- TOC -->
* [AA Intel Tool](#aa-intel-tool)
  * [Overview](#overview)
    * [Features](#features)
    * [Screenshots](#screenshots)
  * [Installation](#installation)
    * [Step 1: Install the Package](#step-1-install-the-package)
    * [Step 2: Configure Alliance Auth](#step-2-configure-alliance-auth)
    * [Step 4: Finalizing the Installation](#step-4-finalizing-the-installation)
    * [Step 5: Update Your Webserver Configuration](#step-5-update-your-webserver-configuration)
      * [Apache 2](#apache-2)
      * [Nginx](#nginx)
  * [Settings](#settings)
  * [Changelog](#changelog)
  * [Contributing](#contributing)
<!-- TOC -->

---

## Overview

### Features

### Screenshots

## Installation

### Step 1: Install the Package

Make sure you're in the virtual environment (venv) of your Alliance Auth
installation Then install the latest release directly from PyPi.


### Step 2: Configure Alliance Auth

This is fairly simple, configure your AA settings (`local.py`) as follows:

- Add `aa_intel_tool` to the list of `INSTALLED_APPS`
  ```python
  # Add any additional apps to this list.
  INSTALLED_APPS += [
      "aa_intel_tool",  # https://github.com/ppfeufer/aa-intel-tool
  ]
  ```
- Add `aa_intel_tool` to the list of `APPS_WITH_PUBLIC_VIEWS` (Right below
  `INSTALLED_APPS`)
  ```python
  # By default, apps are prevented from having public views for security reasons.
  # To allow specific apps to have public views, add them to APPS_WITH_PUBLIC_VIEWS
  #   » The format is the same as in INSTALLED_APPS
  #   » The app developer must also explicitly allow public views for their app
  APPS_WITH_PUBLIC_VIEWS = [
      "aa_intel_tool",  # https://github.com/ppfeufer/aa-intel-tool
  ]
  ```
  > **Note**
  >
  > If you don't have a list for `APPS_WITH_PUBLIC_VIEWS` yet, then add the whole
  > block from here. This feature has been added in Alliance Auth v3.6.0 so you
  > might not yet have this list in your `local.py`.


### Step 4: Finalizing the Installation

Run static files collection and migrations.

```shell
python manage.py collectstatic
python manage.py migrate
```

Restart your supervisor services for Auth.


### Step 5: Update Your Webserver Configuration

By default, webservers have a timout of about 30 seconds for requests. So we have to
tweak that a little bit, since parsing intel data can take a while and we don't want
the webserver to spoil our fun, right?

#### Apache 2

Open your vhost configuration and add the following 2 lines right after the
`ProxyPreserveHost On` directive:

```apache
Timeout      600
ProxyTimeout 600
```

Restart your Apache2 service.

#### Nginx

Open your vhost configuration and add the following lines inside the `location / {`
directive:

```nginx
proxy_connect_timeout 600;
proxy_send_timeout    600;
proxy_read_timeout    600;
send_timeout          600;
```

Restart your Nginx service.


## Settings

To customize the module, the following settings are available and can be made in
your `local.py`.

| Name                          | Description                                                                                                      | Default |
|:------------------------------|:-----------------------------------------------------------------------------------------------------------------|:--------|
| INTELTOOL_SCAN_RETENTION_TIME | Sets the time in days for how long the scans will be kept in the database. Set to 0 to keep scans indefinitely.  | 30      |
| INTELTOOL_CHATSCAN_MAX_PILOTS | Sets the limit of pilots for chat scans, since these can take quite a long time to process. Set to 0 to disable. | 500     |


## Changelog

See [CHANGELOG.md]


## Contributing

Do you want to contribute to this project? That's cool!

Please make sure to read the [Contribution Guidelines]
(I promise, it's not much, just some basics)


<!-- Badges -->
[Badge: Version]: https://img.shields.io/pypi/v/aa-intel-tool?label=release "Version"
[Badge: License]: https://img.shields.io/github/license/ppfeufer/aa-intel-tool "License"
[Badge: Supported Python Versions]: https://img.shields.io/pypi/pyversions/aa-intel-tool "Supported Python Versions"
[Badge: Supported Django Versions]: https://img.shields.io/pypi/djversions/aa-intel-tool?label=django "Supported Django Versions"
[Badge: pre-commit]: https://img.shields.io/badge/pre--commit-enabled-brightgreen?logo=pre-commit&logoColor=white "pre-commit"
[Badge: Code Style: black]: https://img.shields.io/badge/code%20style-black-000000.svg "Code Style: black"
[Badge: Support Discord]: https://img.shields.io/discord/790364535294132234?label=discord "Support Discord"
[Badge: Automated Tests]: https://github.com/ppfeufer/aa-intel-tool/actions/workflows/automated-checks.yml/badge.svg "Automated Tests"
[Badge: Code Coverage]: https://codecov.io/gh/ppfeufer/aa-intel-tool/branch/master/graph/badge.svg "Code Coverage"
[Badge: Contributor Covenant]: https://img.shields.io/badge/Contributor%20Covenant-2.1-4baaaa.svg "Contributor Covenant"
[Badge: Buy me a coffee]: https://ko-fi.com/img/githubbutton_sm.svg "Buy me a coffee"

<!-- Hyperlinks -->
[Alliance Auth]: https://gitlab.com/allianceauth/allianceauth
[AA installation guide]: https://allianceauth.readthedocs.io/en/latest/installation/allianceauth.html
[CHANGELOG.md]: https://github.com/ppfeufer/aa-intel-tool/blob/master/CHANGELOG.md
[Contribution Guidelines]: https://github.com/ppfeufer/aa-intel-tool/blob/master/CONTRIBUTING.md
[AA Intel Tool on Pypi]: https://pypi.org/project/aa-intel-tool/
[AA Intel Tool on Codecov]: https://codecov.io/gh/ppfeufer/aa-intel-tool
[AA Intel Tool License]: https://github.com/ppfeufer/aa-intel-tool/blob/master/LICENSE
[black code formatter documentation]: http://black.readthedocs.io/en/latest/
[Support Discord]: https://discord.gg/zmh52wnfvM
[Automated Tests on GitHub]: https://github.com/ppfeufer/aa-intel-tool/actions/workflows/automated-checks.yml
[Code of Conduct]: https://github.com/ppfeufer/aa-intel-tool/blob/master/CODE_OF_CONDUCT.md
[ppfeufer on ko-fi]: https://ko-fi.com/ppfeufer
