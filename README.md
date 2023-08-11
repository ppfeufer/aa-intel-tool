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
[![Badge: Translation Status]][Weblate Engage]
[![Badge: Contributor Covenant]][Code of Conduct]

[![Badge: Buy me a coffee]][ppfeufer on ko-fi]


D-Scans and more in [Alliance Auth].


---

<!-- TOC -->
* [AA Intel Tool](#aa-intel-tool)
  * [Overview](#overview)
    * [Features](#features)
    * [Screenshots](#screenshots)
      * [Chat Scan](#chat-scan)
      * [D-Scan](#d-scan)
  * [Installation](#installation)
    * [Step 1: Install the Package](#step-1-install-the-package)
    * [Step 2: Configure Alliance Auth](#step-2-configure-alliance-auth)
      * [Add the App to Alliance Auth](#add-the-app-to-alliance-auth)
      * [Add the Scheduled Task](#add-the-scheduled-task)
      * [(Optional) Allow Public Views](#optional-allow-public-views)
    * [Step 4: Preload Eve Universe Data](#step-4-preload-eve-universe-data)
    * [Step 5: Finalizing the Installation](#step-5-finalizing-the-installation)
    * [Step 6: Update Your Webserver Configuration](#step-6-update-your-webserver-configuration)
      * [Apache 2](#apache-2)
      * [Nginx](#nginx)
  * [Settings](#settings)
  * [Changelog](#changelog)
  * [Contributing](#contributing)
<!-- TOC -->

---


> **Warning**
>
> This app is still in active development and only available as an early alpha
> version. Do not install this app in your live environment. If you want to test
> this app, do so in a dedicated test environment. Don't come crying if you wreck
> your live environment.
>
> During the alpha phase, it is highly likely that the DB migrations will be reset a
> couple of times.
>
> Bugs and errors are expected during this time as well, so feel free to report them
> as early as possible, if you dare to test this app.
>
> Thank you!


## Overview

### Features

The following modules can be enabled or disabled.
See [Settings](#settings) section for details.

- Chat scan module (Disabled by default due to its possible high number of ESI calls)
- D-Scan module

### Screenshots

#### Chat Scan

![Image: Chat Scan Module]

#### D-Scan

![Image: D-Scan Module]

## Installation

**Important**: Please make sure you meet all preconditions before you proceed:

- AA Intel Tool is a plugin for [Alliance Auth]. If you don't have Alliance Auth running
  already, please install it first before proceeding. (see the official
  [Alliance Auth installation guide] for details)
- AA Intel Tool needs at least **Alliance Auth v3.6.1**. Please make sure to meet this
  condition _before_ installing this app, otherwise an update to Alliance Auth will
  be pulled in unsupervised.
- AA Intel Tool needs [Eve Universe] to function. Please make sure it is installed,
  before continuing.


### Step 1: Install the Package

Make sure you're in the virtual environment (venv) of your Alliance Auth
installation Then install the latest release directly from PyPi.

```shell
pip install aa-intel-tool
```


### Step 2: Configure Alliance Auth

#### Add the App to Alliance Auth

This is fairly simple, configure your AA settings (`local.py`) as follows:

- Add `eveuniverse` (if not already done so for a different app) and `aa_intel_tool` to
  the list of `INSTALLED_APPS`

  ```python
  # Add any additional apps to this list.
  INSTALLED_APPS += [
      "eveuniverse",
      "aa_intel_tool",  # https://github.com/ppfeufer/aa-intel-tool
  ]
  ```

#### Add the Scheduled Task

To remove old scans from your DB, add the following task.
The retention time can be adjusted through the `INTELTOOL_SCAN_RETENTION_TIME` setting.

```python
if "aa_intel_tool" in INSTALLED_APPS:
    # Run at 01:00 each day
    CELERYBEAT_SCHEDULE["AA Intel Tool :: Housekeeping"] = {
        "task": "aa_intel_tool.tasks.housekeeping",
        "schedule": crontab(minute="0", hour="1"),
    }
```

#### (Optional) Allow Public Views

This app supports AA's feature of public views, since time zones conversion is not
any mission-critical information. To allow users to view the time zone conversion page
without the need to log in, please add `"aa_intel_tool",` to the list of
`APPS_WITH_PUBLIC_VIEWS` in your `local.py`:

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


### Step 4: Preload Eve Universe Data

AA Intel Tool utilizes the EveUniverse module, so it doesn't need to ask ESI for ship
information. To set this up, you now need to run the following command.

```shell
python manage.py aa_intel_tool_load_ship_types
```


### Step 5: Finalizing the Installation

Run static files collection and migrations.

```shell
python manage.py collectstatic
python manage.py migrate
```

Restart your supervisor services for Auth.


### Step 6: Update Your Webserver Configuration

By default, webservers have a timout of about 30 seconds for requests. So we have to
tweak that a little bit, since parsing intel data can take a while, and we don't want
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

To customize the app, the following settings are available and can be made in
your `local.py`.

| Name                              | Description                                                                                                      | Default |
|:----------------------------------|:-----------------------------------------------------------------------------------------------------------------|:--------|
| INTELTOOL_ENABLE_MODULE_CHATSCAN  | Enable or disable the chat scan module.                                                                          | False   |
| INTELTOOL_ENABLE_MODULE_DSCAN     | Enable or disable the d-scan module.                                                                             | True    |
| INTELTOOL_ENABLE_MODULE_FLEETCOMP | Enable or disable the fleet composition module.                                                                  | True    |
| INTELTOOL_SCAN_RETENTION_TIME     | Sets the time in days for how long the scans will be kept in the database. Set to 0 to keep scans indefinitely.  | 30      |
| INTELTOOL_CHATSCAN_MAX_PILOTS     | Sets the limit of pilots for chat scans, since these can take quite a long time to process. Set to 0 to disable. | 500     |


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
[Badge: Translation Status]: https://weblate.ppfeufer.de/widgets/alliance-auth-apps/-/aa-intel-tool/svg-badge.svg "Translation Status"

<!-- Images -->
[Image: Chat Scan Module]: https://raw.githubusercontent.com/ppfeufer/aa-intel-tool/master/docs/images/chat-scan.jpg "Chat Scan Module"
[Image: D-Scan Module]: https://raw.githubusercontent.com/ppfeufer/aa-intel-tool/master/docs/images/d-scan.jpg "D-Scan Module"

<!-- Hyperlinks -->
[Alliance Auth]: https://gitlab.com/allianceauth/allianceauth
[Alliance Auth installation guide]: https://allianceauth.readthedocs.io/en/latest/installation/allianceauth.html
[Eve Universe]: https://gitlab.com/ErikKalkoken/django-eveuniverse "Eve Universe"
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
[Weblate Engage]: https://weblate.ppfeufer.de/engage/alliance-auth-apps/
