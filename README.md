# lutop User Manual

## Introduction

Welcome to lutop (Lightweight System Monitor), a terminal-based system monitoring application inspired by Unix `top` command and designed using Python and curses library.

## Table of Contents

1. [Installation](#installation)
2. [Usage](#usage)
3. [Key Features](#key-features)
4. [Troubleshooting](#troubleshooting)
5. [Contributing](#contributing)
6. [License](#license)

## Installation

### Prerequisites

- Python 3.6 or above
- pip (Python package installer)
- curses (Python standard library for terminal handling)

### Install lutop

1. Clone the repository:

```bash
   git clone https://github.com/barkhayot/lutop.git
   cd lutop
```

2. Install dependencies:
```bash
pip install -r requirements.txt
```
## Usage
To start lutop, simply run the following command in your terminal:

```bash
python lutop.py
```
### Key Commands
- Quit: Press Ctrl + D to quit the application.
- Refresh: Data is automatically refreshed every second.
- Display Information
- CPU Usage: Displays usage of each CPU core with a progress bar.
- Memory Usage: Shows total, used, and free memory with a progress bar.
- Swap Usage: Shows total, used, and free swap memory with a progress bar.
- Top Processes: Displays top processes by memory usage.
### Key Features
- Real-time updates of system information.
- Color-coded progress bars for CPU and memory usage.
- Supports terminal resizing for dynamic layout adjustment.