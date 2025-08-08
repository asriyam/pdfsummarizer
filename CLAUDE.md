# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

This is a Python-based PDF summarizer that uses the Anthropic Claude API. The project is in early development with a single main module.

## Architecture

- `summarizer.py` - Main application module that imports the Anthropic library for AI-powered summarization
- Uses a virtual environment (`venv/`) for Python dependencies
- Currently minimal structure with room for expansion

## Development Setup

The project uses a Python virtual environment. To work with dependencies:

```bash
# Activate virtual environment (Windows)
venv\Scripts\activate

# Activate virtual environment (Unix/MacOS)
source venv/bin/activate

# Install dependencies (when requirements file exists)
pip install -r requirements.txt
```

## Dependencies

- `anthropic` - Claude API client library for AI summarization functionality

## Notes

- No formal dependency management file (requirements.txt, pyproject.toml) exists yet
- Project structure suggests a single-file application that could be expanded into modules
- Virtual environment is already set up but may need dependency installation