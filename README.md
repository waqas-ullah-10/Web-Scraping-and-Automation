# Web-Scraping-and-Automation

## Overview

This repository contains two Python automation scripts developed to demonstrate core web scraping and task automation concepts: a headline scraper for Hacker News and a directory-based file organizer. Each script can be executed as a single run or configured to execute on a recurring schedule.

## Contents

1. [Requirements](#requirements)
2. [Installation](#installation)
3. [Script Descriptions](#script-descriptions)
4. [Usage](#usage)
5. [Automated Scheduling](#automated-scheduling)
6. [Repository Structure](#repository-structure)
7. [Concepts Demonstrated](#concepts-demonstrated)
8. [License](#license)

## Requirements

- Python 3.8 or later
- Internet access (for the scraper script)
- Dependencies listed in `requirements.txt`

## Installation

Clone the repository and install the required dependencies:

```bash
git clone https://github.com/waqas-ullah-10/Web-Scraping-and-Automation.git
cd Web-Scraping-and-Automation
pip install -r requirements.txt
```

## Script Descriptions

### news_scraper.py

Retrieves the current front-page listings from Hacker News. The script issues an HTTP GET request to the site, parses the returned HTML using BeautifulSoup4, and extracts the following fields for each listed story:

- Rank
- Title
- URL
- Point count
- Author
- Comment count

Extracted data is written to a timestamped CSV file within a `scraped_data` directory, created automatically on first execution.

### file_organizer.py

This Python script automates file organization by sorting files into folders based on their extensions. It scans a specified directory, creates category folders if needed, and moves each file to its appropriate location. The script also prevents duplicate file names by automatically renaming files when necessary. It demonstrates practical use of Python modules such as `pathlib` and `shutil` for file system automation.


## Usage

### News Scraper

| Command | Description |
|---|---|
| `python news_scraper.py` | Scrapes the top 30 stories once |
| `python news_scraper.py --limit 50` | Scrapes a specified number of stories |
| `python news_scraper.py --schedule 60` | Repeats the scrape at the specified interval, in minutes |

### File Organizer

| Command | Description |
|---|---|
| `python file_organizer.py <directory>` | Organizes the specified directory |
| `python file_organizer.py <directory> --dry-run` | Displays intended changes without executing them |
| `python file_organizer.py <directory> --schedule 30` | Repeats the operation at the specified interval, in minutes |

## Automated Scheduling

Each script includes an internal scheduling mechanism (via the `schedule` library) that requires the process to remain running. For persistent automation independent of an active terminal session, system-level schedulers are recommended.

**Windows (Task Scheduler):**

Configure a new task with the trigger of your choice, setting the action to execute `python.exe` with the script path and target directory as arguments.

## Repository Structure

```
.
├── news_scraper.py
├── file_organizer.py
├── requirements.txt
├── scraped_data/
└── README.md
```

## Concepts Demonstrated

- HTTP request handling
- HTML parsing and CSS selector-based data extraction
- File system manipulation and path handling
- Command-line argument parsing
- Scheduled task execution

## License

Distributed under the MIT License. See `LICENSE` for details.
