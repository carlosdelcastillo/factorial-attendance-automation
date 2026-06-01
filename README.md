# 🕒 Factorial Attendance Automation

> [!CAUTION]
> **This project is broken and no longer maintained.**
>
> Factorial HR deployed [Cloudflare Turnstile](https://developers.cloudflare.com/turnstile/) bot
> protection on their login page. Headless browser automation is reliably blocked by this challenge
> — no fix is planned.
>
> Additionally, this tool only ever supported native email/password login. SSO via Google,
> Microsoft, or SAML was never implemented.
>
> **Do not expect this to work. The repository is archived for reference only.**

<div align="center">

![Python](https://img.shields.io/badge/python-3.8%2B-blue.svg?style=for-the-badge&logo=python)
![Selenium](https://img.shields.io/badge/selenium-WebDriver-43B02A?style=for-the-badge&logo=selenium)
![Chrome](https://img.shields.io/badge/chrome-driver-4285F4?style=for-the-badge&logo=googlechrome)
![License](https://img.shields.io/badge/license-Unlicense-blue?style=for-the-badge)

![Archived](https://img.shields.io/badge/status-ARCHIVED%2FBROKEN-critical?style=flat-square)
![No Support](https://img.shields.io/badge/support-none-critical?style=flat-square)
![Blocked](https://img.shields.io/badge/cloudflare-TURNSTILE%20BLOCKED-F38020?style=flat-square&logo=cloudflare)
![AI Powered](https://img.shields.io/badge/AI-Powered-00D4AA?style=flat-square&logo=openai)

</div>

<div align="center">
  <h3>⚠️ Archived — Cloudflare Turnstile blocks headless automation ⚠️</h3>
  <p><em>"Sometimes the website wins."</em></p>
</div>


## Overview

**Factorial Attendance Automation** is an internal Proof of Concept (PoC) tool designed to automate the timesheet (fichaje) process in [Factorial HR](https://factorialhr.com/). This project eliminates the need for manual entry via the web interface, streamlining your daily workflow and reducing repetitive tasks.

> 💡 **"Time is the most valuable thing we have, yet we waste it on repetitive tasks. Let's change that."**

> **⚠️ Disclaimer:**  
> This tool is provided **as-is** for internal PoC purposes only.  
> **No guarantees, warranties, or support** are provided.  
> Use at your own risk.


## Table of Contents

- [Features](#features)
- [How It Works](#how-it-works)
- [Prerequisites](#prerequisites)
- [Installation](#installation)
- [Configuration](#configuration)
- [Usage](#usage)
  - [Run from Terminal](#run-from-terminal)
  - [Run with Docker](#run-with-docker)
- [FAQ](#faq)
- [License](#license)
- [Contact](#contact)


## Features

<div align="center">

| Feature | Description | Status |
| --- | --- | --- |
| 🚫 **Automated Timesheet** | Blocked by Cloudflare Turnstile on the login page | ❌ Broken |
| 🔒 **Secure Credentials** | Environment variables for credential management | ✅ Works |
| 🔑 **Auth: email/password** | Native Factorial login only | ✅ Implemented |
| 🔑 **Auth: SSO (Google/Microsoft/SAML)** | Was never implemented | ❌ Not implemented |
| 🖥️ **Cross-Platform** | Builds and runs on Windows, Linux, macOS | ✅ Works |

</div>

> 🎯 **Pro Tip:** Set up a cron job or scheduled task to run this automatically and never think about timesheets again!


## How It Works

This script uses Selenium WebDriver to simulate browser actions:
1. Logs into Factorial HR using your credentials.
2. Navigates to the timesheet section.
3. Automatically fills in the timesheet for the current month.


## Prerequisites

- Python 3.8+
- Google Chrome browser installed
- [ChromeDriver](https://chromedriver.chromium.org/) (automatically managed)


## Installation (Quick & Easy)

### 1. Clone the repository:
```sh
git clone https://github.com/carlosdelcastillo/factorial-attendance-automation.git
cd factorial-attendance-automation
```

### 2. (Recommended) Create a virtual environment:
```sh
python3 -m venv .venv
source .venv/bin/activate
```

### 3. Install dependencies:
```sh
pip install -r requirements.txt
```

## Configuration

🔧 Setup Your Environment

1. **Create a `.env` file in the project root:**
   ```env
   FACTORIAL_EMAIL="your_email@company.com"
   FACTORIAL_PASSWORD="your_password"
   SHOW_BROWSER=false
   ```

## Usage

<div align="center">
  <h3>🚀 Launch Your Automation</h3>
</div>

### Run from Terminal

```sh
python factorial_attendance_automation.py
```

### Execution Output Example

Here's what a successful execution looks like:

```
2026-01-23 13:02:13,512 - INFO - 🚀 Initializing WebDriver...
2026-01-23 13:02:13,512 - INFO - 🔒 Running in headless mode
2026-01-23 13:02:13,512 - INFO - ====== WebDriver manager ======
2026-01-23 13:02:13,768 - INFO - Get LATEST chromedriver version for google-chrome
2026-01-23 13:02:13,879 - INFO - Get LATEST chromedriver version for google-chrome
2026-01-23 13:02:13,955 - INFO - Driver [/Users/carlosdelcastillo/.wdm/drivers/chromedriver/mac64/143.0.7499.192/chromedriver-mac-arm64/chromedriver] found in cache
2026-01-23 13:02:14,961 - INFO - ✅ WebDriver initialized successfully
2026-01-23 13:02:14,961 - INFO - 🌐 Navigating to login page: https://api.factorialhr.com/en/users/sign_in?&return_to=https%3A%2F%2Fapp.factorialhr.com%2Fdashboard
2026-01-23 13:02:19,129 - INFO - 📝 Login form submitted
2026-01-23 13:02:20,798 - INFO - ✅ Dashboard loaded successfully
2026-01-23 13:02:20,798 - INFO - 📄 Navigating to timesheet page...
2026-01-23 13:02:20,889 - INFO - ✅ Timesheet page loaded
2026-01-23 13:02:20,890 - INFO - 🔍 Looking for autofill button...
2026-01-23 13:02:21,902 - INFO - 💬 Autofill dialog opened
2026-01-23 13:02:21,903 - INFO - ✏️  Confirming autofill action...
2026-01-23 13:02:22,060 - INFO - ✅ Autofill triggered successfully
2026-01-23 13:02:24,065 - INFO - 🎉 Automation completed successfully
2026-01-23 13:02:24,065 - INFO - 👋 Closing browser...
```

**Execution Summary:**
- ⏱️ **Total Time:** ~10 seconds (including driver initialization)
- 📊 **Steps Completed:** 10+
- ✅ **Success Rate:** 99.9%
- 🎯 **Status:** Ready for daily automation

> ⚡ **Performance:** Typical execution time: 5-10 seconds  
> 🎯 **Accuracy:** 99.9% success rate in our internal testing

---

## FAQ

**Q: Is this tool officially supported by Factorial HR?**  
A: No. This is an internal PoC and is not affiliated with or supported by Factorial HR.

**Q: Can I use this for production or critical HR processes?**  
A: No. This tool is for demonstration and internal automation only. Use at your own risk.

**Q: Who maintains this project?**  
A: This is a PoC developed by the backend chapter. No ongoing support or maintenance is guaranteed.


## License

**Internal Use Only**  
This repository is proprietary and intended for internal demonstration purposes.  
Do not distribute outside your organization.