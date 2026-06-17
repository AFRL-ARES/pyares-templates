# PyAres Templates

A collection of templates to make it easy to get started creating modular, portable, and reusable PyAres services.

## Overview

This repository contains starter templates for building various components of the [PyAres](https://github.com/AFRL-ARES/PyAres) ecosystem. PyAres requires Python version 3.10 or newer. Because ARES OS can require multiple projects operating in tandem, these templates are designed to help you structure your code to avoid dependency conflicts and ensure your services remain portable across different host computers and laboratory environments.

## Available Templates

### 1. Planner (simple) (`pyares-template-planner-simple`)

This is a template for a simple, single-file PyAres planner service. This approach is best for getting started with PyAres or if your planning protocol is relatively simple and doesn't require a lot of custom logic that isn't already abstracted away by external libraries.

### 2. Planner 
*Coming soon*

### 3. Analyzer (simple) (`pyares-template-analyzer-simple`)

This provides a simple, single-file PyAres Analyzer service. It is ideal for basic analysis protocols that do not require sprawling logic across multiple files.

### 5. Analyzer (`pyares-template-analyzer`)

This template is intended for more complex code that cannot be cleanly defined in a single file. It is structured as a self-contained Python module that can be installed into your Python path using `pip` (e.g., via `pip install -e .`). This package-based approach helps keep code redistributable, handles external dependencies gracefully, and organizes code into sub-modules and support functions.

### 5. Device (simple) (`pyares-template-device-simple`)

A template for a simple, single-file PyAres device service. Device services communicate with real-world hardware, this template utilizes `pyserial` to establish a connection to an example device running on an Arduino Uno microcontroller.

* **Arduino Example:** This template also includes a basic sketch for an Arduino Uno that initializes serial communication at 9600 baud and configures the onboard LED. The sketch demonstrates how to process device states and commands, such as toggling the LED, reading voltage from a pin, and parsing custom user values.

### 6. Device
*Coming Soon*

## Sharing Your Code
Our goal is to create an ecosystem of PyAres users sharing open source code and collaborating on the development of new services to accelerate the pace of autnomous experimtation system development and avoid duplicated work. If you have developed a new service or feature that you would like to share with the community, please consider submitting a pull request to our [PyAres Directory](https://github.com/AFRL-ARES/pyares-directory) and we will consider it for inclusion.

## Getting Started & Environment Management

The complexity of scientific code can vary widely. To minimize dependency conflicts, it is highly recommended that each service be run in its own dedicated Python environment.

### Option A: Using Anaconda / Miniconda / Miniforge

1. **Create the environment:**
```bash
conda create -n pyares_env python=3.10 pip 

```

2. **Activate the environment:**
```bash
conda activate pyares_env

```

3. **Install dependencies:** Navigate to the specific template directory and run:
```bash
pip install -r requirements.txt

```

### Option B: Using Python venv

1. **Create the virtual environment:**
```bash
python3 -m venv pyares_env

```

2. **Activate the environment:**
* **Windows:** `.\pyares_env\Scripts\activate`
* **Linux/macOS:** `source pyares_env/bin/activate`

3. **Install dependencies:** Navigate to the specific template directory and run:
```bash
pip install -r requirements.txt

```

# Public Release:
**Distribution Statement A**. Approved for public release: distribution is unlimited. AFRL-2026-2820