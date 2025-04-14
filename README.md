# AA Intel Tool<a name="aa-intel-tool"></a>

[![Badge: Version]][aa intel tool on pypi]
[![Badge: License]][aa intel tool license]
[![Badge: Supported Python Versions]][aa intel tool on pypi]
[![Badge: Supported Django Versions]][aa intel tool on pypi]
![Badge: pre-commit]
[![Badge: pre-commit.ci status]][pre-commit.ci status]
[![Badge: Code Style: black]][black code formatter documentation]
[![Badge: Support Discord]][support discord]
[![Badge: Automated Tests]][automated tests on github]
[![Badge: Code Coverage]][aa intel tool on codecov]
[![Badge: Translation Status]][weblate engage]
[![Badge: Contributor Covenant]][code of conduct]

[![Badge: Buy me a coffee]][ppfeufer on ko-fi]

D-Scans and more in [Alliance Auth].

______________________________________________________________________

<!-- mdformat-toc start --slug=github --maxlevel=6 --minlevel=2 -->

- [Overview](#overview)
  - [Features](#features)
  - [Screenshots](#screenshots)
    - [Chat Scan](#chat-scan)
    - [D-Scan](#d-scan)
    - [Fleet Composition](#fleet-composition)
- [Installation](#installation)
  - [Step 1: Install the Package](#step-1-install-the-package)
  - [Step 2: Configure Alliance Auth](#step-2-configure-alliance-auth)
    - [Add the App to Alliance Auth](#add-the-app-to-alliance-auth)
    - [Add the Scheduled Task](#add-the-scheduled-task)
    - [(Optional) Allow Public Views](#optional-allow-public-views)
  - [Step 4: Preload Eve Universe Data](#step-4-preload-eve-universe-data)
  - [Step 5: Finalizing the Installation](#step-5-finalizing-the-installation)
  - [Step 6: Update Your Webserver Configuration](#step-6-update-your-webserver-configuration)
    - [Apache 2](#apache-2)
    - [Nginx](#nginx)
- [Settings](#settings)
- [Changelog](#changelog)
- [Translation Status](#translation-status)
- [Contributing](#contributing)

<!-- mdformat-toc end -->

______________________________________________________________________

## Overview<a name="overview"></a>

### Features<a name="features"></a>

The following modules can be enabled or disabled.
See [Settings](#settings) section for details.

- Chat scan module (Disabled by default due to its possible high number of ESI calls)
- D-Scan module

### Screenshots<a name="screenshots"></a>

#### Chat Scan<a name="chat-scan"></a>

![Image: Chat Scan Module]

#### D-Scan<a name="d-scan"></a>

![Image: D-Scan Module]

#### Fleet Composition<a name="fleet-composition"></a>

![Image: Fleet Composition Module]

## Installation<a name="installation"></a>

> [!NOTE]
>
> **AA Intel Tool >= 2.0.0 needs at least Alliance Auth v4.0.0!**
>
> Please make sure to update your Alliance Auth instance _before_ you install this
> module or update to the latest version, otherwise an update to Alliance Auth will
> be pulled in unsupervised.
>
> The last version compatible with Alliance Auth v3 is `1.2.0`.

**Important**: Please make sure you meet all preconditions before you proceed:

- AA Intel Tool is a plugin for [Alliance Auth]. If you don't have Alliance Auth running
  already, please install it first before proceeding. (see the official
  [Alliance Auth installation guide] for details)
- AA Intel Tool needs [Eve Universe] to function. Please make sure it is installed,
  before continuing.

### Step 1: Install the Package<a name="step-1-install-the-package"></a>

Make sure you're in the virtual environment (venv) of your Alliance Auth
installation Then install the latest release directly from PyPi.

```shell
pip install aa-intel-tool
```

### Step 2: Configure Alliance Auth<a name="step-2-configure-alliance-auth"></a>

#### Add the App to Alliance Auth<a name="add-the-app-to-alliance-auth"></a>

This is fairly simple, configure your AA settings (`local.py`) as follows:

Add `eveuniverse` (if not already done so for a different app) and `aa_intel_tool` to
the list of `INSTALLED_APPS`.

```python
# Add any additional apps to this list.
INSTALLED_APPS += [
    "eveuniverse",
    "aa_intel_tool",  # https://github.com/ppfeufer/aa-intel-tool
]
```

#### Add the Scheduled Task<a name="add-the-scheduled-task"></a>

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

#### (Optional) Allow Public Views<a name="optional-allow-public-views"></a>

This app supports AA's feature of public views. To allow this feature, please add
`"aa_intel_tool",` to the list of `APPS_WITH_PUBLIC_VIEWS` in your `local.py`:

```python
# By default, apps are prevented from having public views for security reasons.
# To allow specific apps to have public views, add them to APPS_WITH_PUBLIC_VIEWS
#   » The format is the same as in INSTALLED_APPS
#   » The app developer must also explicitly allow public views for their app
APPS_WITH_PUBLIC_VIEWS = [
    "aa_intel_tool",  # https://github.com/ppfeufer/aa-intel-tool
]
```

> [!NOTE]
>
> If you don't have a list for `APPS_WITH_PUBLIC_VIEWS` yet, then add the whole
> block from here. This feature has been added in Alliance Auth v3.6.0 so you
> might not yet have this list in your `local.py`.

### Step 4: Preload Eve Universe Data<a name="step-4-preload-eve-universe-data"></a>

AA Intel Tool utilizes the EveUniverse module, so it doesn't need to ask ESI for ship
information. To set this up, you now need to run the following command.

```shell
python manage.py aa_intel_tool_load_eve_types
```

### Step 5: Finalizing the Installation<a name="step-5-finalizing-the-installation"></a>

Run static files collection and migrations.

```shell
python manage.py collectstatic
python manage.py migrate
```

Restart your supervisor services for Auth.

### Step 6: Update Your Webserver Configuration<a name="step-6-update-your-webserver-configuration"></a>

By default, webservers have a timout of about 30 seconds for requests. So we have to
tweak that a little bit, since parsing intel data can take a while, and we don't want
the webserver to spoil our fun, right?

#### Apache 2<a name="apache-2"></a>

Open your vhost configuration and add the following 2 lines right after the
`ProxyPreserveHost On` directive:

```apache
ProxyTimeout 600
Timeout      600
```

Restart your Apache2 service.

#### Nginx<a name="nginx"></a>

Open your vhost configuration and add the following lines inside the `location / {`
directive:

```nginx
proxy_connect_timeout 600;
proxy_read_timeout    600;
proxy_send_timeout    600;
send_timeout          600;
```

Restart your Nginx service.

## Settings<a name="settings"></a>

To customize the app, the following settings are available and can be made in
your `local.py`.

> [!WARNING]
>
> Enable the chat scan module at your own risk. This module has the potential to
> generate a huge number of ESI calls, which CCP might not be too happy about.

| Name                              | Description                                                                                                                             | Default |
| :-------------------------------- | :-------------------------------------------------------------------------------------------------------------------------------------- | :------ |
| INTELTOOL_ENABLE_MODULE_CHATSCAN  | Enable or disable the chat scan module.                                                                                                 | False   |
| INTELTOOL_ENABLE_MODULE_DSCAN     | Enable or disable the d-scan module.                                                                                                    | True    |
| INTELTOOL_ENABLE_MODULE_FLEETCOMP | Enable or disable the fleet composition module.                                                                                         | True    |
| INTELTOOL_SCAN_RETENTION_TIME     | Set the time in days for how long the scans will be kept in the database. Set to 0 to keep scans indefinitely.                          | 30      |
| INTELTOOL_CHATSCAN_MAX_PILOTS     | Set the limit of pilots for chat scans, since these can take quite a long time to process. Set to 0 to disable.                         | 500     |
| INTELTOOL_DSCAN_GRID_SIZE         | Set the grid size for D-Scans.<br/>This defines the size of the grid in km in which ships and structures are considered to be "on grid" | 10000   |

> [!NOTE]
>
> **A word about the chat scan limitations:**
>
> It is advised to keep the `INTELTOOL_CHATSCAN_MAX_PILOTS` to a sane number. Large
> chat scans can take quite some time to parse and from a certain number of pilots, the
> bottleneck might be your browser refusing to render the results page.
> (Source: Trust me, bro …)

## Changelog<a name="changelog"></a>

See [CHANGELOG.md]

## Translation Status<a name="translation-status"></a>

[![Translation status](https://weblate.ppfeufer.de/widget/alliance-auth-apps/aa-intel-tool/multi-auto.svg)](https://weblate.ppfeufer.de/engage/alliance-auth-apps/)

Do you want to help translate this app into your language or improve the existing
translation? - [Join our team of translators][weblate engage]!

## Contributing<a name="contributing"></a>

Do you want to contribute to this project? That's cool!

Please make sure to read the [Contribution Guidelines].\
(I promise, it's not much, just some basics)

<!-- Inline Links -->

[aa intel tool license]: https://github.com/ppfeufer/aa-intel-tool/blob/master/LICENSE
[aa intel tool on codecov]: https://codecov.io/gh/ppfeufer/aa-intel-tool
[aa intel tool on pypi]: https://pypi.org/project/aa-intel-tool/
[alliance auth]: https://gitlab.com/allianceauth/allianceauth "Alliance Auth on GitLab"
[alliance auth installation guide]: https://allianceauth.readthedocs.io/en/latest/installation/allianceauth.html
[automated tests on github]: https://github.com/ppfeufer/aa-intel-tool/actions/workflows/automated-checks.yml
[badge: automated tests]: https://github.com/ppfeufer/aa-intel-tool/actions/workflows/automated-checks.yml/badge.svg "Automated Tests"
[badge: buy me a coffee]: https://ko-fi.com/img/githubbutton_sm.svg "Buy Me a Coffee!"
[badge: code coverage]: https://codecov.io/gh/ppfeufer/aa-intel-tool/branch/master/graph/badge.svg "Code Coverage"
[badge: code style: black]: https://img.shields.io/badge/code%20style-black-000000.svg "Code Style: black"
[badge: contributor covenant]: https://img.shields.io/badge/Contributor%20Covenant-2.1-4baaaa.svg "Contributor Covenant"
[badge: license]: https://img.shields.io/github/license/ppfeufer/aa-intel-tool "License"
[badge: pre-commit]: https://img.shields.io/badge/pre--commit-enabled-brightgreen?logo=pre-commit&logoColor=white "pre-commit"
[badge: pre-commit.ci status]: https://results.pre-commit.ci/badge/github/ppfeufer/aa-intel-tool/master.svg "pre-commit.ci status"
[badge: support discord]: https://img.shields.io/discord/790364535294132234?label=discord "Support Discord"
[badge: supported django versions]: https://img.shields.io/pypi/djversions/aa-intel-tool?label=django "Supported Django Versions"
[badge: supported python versions]: https://img.shields.io/pypi/pyversions/aa-intel-tool "Supported Python Versions"
[badge: translation status]: https://weblate.ppfeufer.de/widget/alliance-auth-apps/aa-intel-tool/svg-badge.svg "Translation Status"
[badge: version]: https://img.shields.io/pypi/v/aa-intel-tool?label=release "Version"
[black code formatter documentation]: http://black.readthedocs.io/en/latest/
[changelog.md]: https://github.com/ppfeufer/aa-intel-tool/blob/master/CHANGELOG.md
[code of conduct]: https://github.com/ppfeufer/aa-intel-tool/blob/master/CODE_OF_CONDUCT.md
[contribution guidelines]: https://github.com/ppfeufer/aa-intel-tool/blob/master/CONTRIBUTING.md "Contribution Guidelines"
[eve universe]: https://gitlab.com/ErikKalkoken/django-eveuniverse "Eve Universe"
[image: chat scan module]: https://raw.githubusercontent.com/ppfeufer/aa-intel-tool/master/docs/images/presentation/chat-scan.jpg "Chat Scan Module"
[image: d-scan module]: https://raw.githubusercontent.com/ppfeufer/aa-intel-tool/master/docs/images/presentation/d-scan.jpg "D-Scan Module"
[image: fleet composition module]: https://raw.githubusercontent.com/ppfeufer/aa-intel-tool/master/docs/images/presentation/fleet-composition.jpg "Fleet Composition Module"
[ppfeufer on ko-fi]: https://ko-fi.com/ppfeufer "Buy Me a Coffee!"
[pre-commit.ci status]: https://results.pre-commit.ci/latest/github/ppfeufer/aa-intel-tool/master "pre-commit.ci"
[support discord]: https://discord.gg/zmh52wnfvM "Alliance Auth Community Apps Support Discord"
[weblate engage]: https://weblate.ppfeufer.de/engage/alliance-auth-apps/ "Weblate Translations"
