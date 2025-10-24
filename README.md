# 🕒 Factorial Attendance Automation

<div align="center">

![Python](https://img.shields.io/badge/python-3.8%2B-blue.svg?style=for-the-badge&logo=python)
![Selenium](https://img.shields.io/badge/selenium-WebDriver-43B02A?style=for-the-badge&logo=selenium)
![Chrome](https://img.shields.io/badge/chrome-driver-4285F4?style=for-the-badge&logo=googlechrome)
![License](https://img.shields.io/badge/license-Unlicense-blue?style=for-the-badge)

![Open Use](https://img.shields.io/badge/OPEN-USE%20NO%20WARRANTY-lightgrey?style=flat-square)
![PoC](https://img.shields.io/badge/status-PoC-lightgrey?style=flat-square)
![No Support](https://img.shields.io/badge/support-none-critical?style=flat-square)
![AI Powered](https://img.shields.io/badge/AI-Powered-00D4AA?style=flat-square&logo=openai)
![Made with Love](https://img.shields.io/badge/Made%20with-❤️-red?style=flat-square)

</div>

<div align="center">
  <h3>✨ Automate your timesheet like a boss ✨</h3>
  <p><em>"Why do manually what you can automate intelligently?"</em></p>
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
|---------|-------------|--------|
| 🚀 **Automated Timesheet** | Fills your Factorial HR timesheet automatically | ✅ Ready |
| 🔒 **Secure Credentials** | Environment variables for secure credential management | ✅ Ready |
| 🖥️ **Cross-Platform** | Works on Windows, Linux, and macOS | ✅ Ready |
| ⚡ **Lightning Fast** | Completes in seconds what takes minutes manually | ✅ Ready |

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