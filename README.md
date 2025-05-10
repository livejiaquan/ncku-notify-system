# NCKU OIA Announcement Crawler System

[English](README.md) | [繁體中文](README.zh-TW.md)

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Python 3.10](https://img.shields.io/badge/python-3.10-blue.svg)](https://www.python.org/downloads/release/python-3100/)
[![Selenium](https://img.shields.io/badge/Selenium-4.11.2-green.svg)](https://www.selenium.dev/)
[![Code style: black](https://img.shields.io/badge/code%20style-black-000000.svg)](https://github.com/psf/black)

Automatically crawls announcements from the NCKU Office of International Affairs website and sends notifications via email.

## Features

- Automatic crawling of latest NCKU OIA announcements
- Duplicate announcement filtering
- Email notification for new announcements
- Complete logging system
- Sensitive information management via configuration files

## Installation Requirements
```bash
pip install -r requirements.txt
```

## Conda Environment Setup
1. Create a new conda environment:
```bash
conda create -n ncku-notify python=3.10
conda activate ncku-notify
pip install -r requirements.txt
```

2. Export environment (for sharing):
```bash
conda env export > environment.yml
```

3. Import environment on another machine:
```bash
conda env create -f environment.yml
```

## Quick Start
You can use the provided shell script to run the crawler:

1. Make the script executable:
```bash
chmod +x run_crawler.sh
chmod +x run_today.sh
```

2. Run the script:
```bash
# To crawl all announcements:
./run_crawler.sh

# To crawl only today's announcements:
./run_crawler.sh --only-today
# Or use the dedicated script:
./run_today.sh
```

The script will:
- Automatically activate the conda environment
- Run the crawler
- Wait for user input before closing

## Configuration

1. Copy the configuration file example:
```bash
cp config/email_config.example.yaml config/email_config.yaml
```

2. Modify email settings in `email_config.yaml`:
- SMTP server information
- Sender's email and password
- Recipient's email

## Usage

Run the crawler:
```bash
python src/main.py
```

## Directory Structure
```
project_root/
├── config/                 # Configuration files
├── data/                   # Data storage
│   ├── announcements/      # Announcement storage
│   └── logs/              # Log files
├── src/                    # Source code
├── test/                   # Test files
└── experiments/           # Experimental features
```

## Important Notes

- Ensure `email_config.yaml` is not committed to version control
- Recommended to use Gmail app password instead of account password
- Recommended to run the crawler once per day to avoid frequent requests

## Author

- Author: LIM JIA QUAN
- Email: livejiaquan010313@gmail.com

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.