# Is It Down Alert

Validates if webpages are online on a predefined interval. Sends email alerts from gmail account if a page is down. Quick and simple deployment using Docker container.

## Table of Contents
- [Is It Down Alert](#is-it-down-alert)
  - [Table of Contents](#table-of-contents)
  - [Features](#features)
  - [Requirements](#requirements)
  - [Installation and Setup](#installation-and-setup)
    - [Setting up a Gmail account to use as Sender](#setting-up-a-gmail-account-to-use-as-sender)
    - [Setting up the project](#setting-up-the-project)
    - [Removing Docker container](#removing-docker-container)
  - [Email Alert Example](#email-alert-example)
## Features

* Sends request to website periodically;
* Current time intervals allowed:
  * every x minutes;
  * every x hours;
  * every x days;
* Abstracts crontab job creation.
* User chooses which websites to check as well as the interval for each one by populating *webpages.yaml*
* If an http request does not return an expected response status code, an email is sent to a specified email address.
* Dockerized allowing easy and fast deployment on any system running docker.

## Requirements

* <a href="https://docs.docker.com/get-docker/">Docker</a>
* <a href="https://docs.docker.com/compose/install/">Docker Compose</a>

## Installation and Setup

### Setting up a Gmail account to use as Sender

**Important:** Due to security reasons, create a new Gmail account to use as sender. Avoid using this account for other purposes.

After creating a Gmail account, an App Password needs to be created. 

1. 2-Step Verification must be enabled on *Google account settings > Security*

2. Create an **App Password**:

<p align="center">
<img src="docs/images/security_settings.jpg" width=90% />
</p>

On *Select app* chose *Other (Custom name)* and chose any name.
Save the password for later use in project parameters.

<p align="center">
<img src="docs/images/app_password.png" width=70% />
</p>

### Setting up the project

1. Clone the repository:

```bash
$ git clone https://github.com/tngaspar/isitdown-alert.git
```

2. Create `.env` file in project root folder with the following parameters:
```toml
SENDER_EMAIL=<Sender Gmail created = example@gmail.com>
APP_PASSWORD=<App Password created for Gmail Account>
RECEIVER_EMAIL=<Email that Receives Alerts = example@something.com>
TIME_ZONE=<Timezone for Email Timestamps. Example: Europe/Amsterdam>
```
Find a list of availbable timezones [here](https://pypi.org/project/pytz/).

3. Edit `webpages.yaml` and add all the webpages to check as well as the corresponding time intervals. This file already contains 2 examples and instruction on how to configure it.

4. Build and run the container:

```bash
$ docker-compose build  # Builds the container
$ docker-compose up -d  # Runs the container
```
Check if the container is running with the command `docker ps`.

That's it. The email alerts should now be activated. 

Before deploying final webpage list, I would recommend using an unreacheble URL with a small interval to check if emails are being sent. 

In a future release, I intend to add a way to track sucessfull requests to verify that all is up and running and keep an history of websites' downtimes.

### Removing Docker container

```bash
$ docker-compose stop  # Stops the container
$ docker-compose rm  # Removes the container
```

## Email Alert Example

Emails sent when website is unreacheble have the following format:

<p align="center">
<img src="docs/images/email_alert_example.png" width=90% />
</p>

<p align="right">(<a href="#top">back to top</a>)</p>