# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

This project creates a sample SQLite database with acoustic engineering data for development and testing purposes. It generates realistic acoustic project data including test results, materials, equipment specifications, and project communications that can be used for database iteration, analysis, and development work.

## Common Development Commands

- **Install dependencies**: `pip install -r requirements.txt`
- **Create database**: `python create_project_database.py`
- **Generate sample data**: `python generate_sample_data.py`
- **Run analysis**: `python analyze_projects.py`

## Database Architecture

The SQLite database (`project_management.db`) contains 8 main tables with foreign key relationships to the projects table:

- **projects**: Core project information (client, dates, status)
- **astm_tests**: Acoustic test results and raw data
- **budget**: Financial tracking (total, spent, remaining)
- **acoustic_materials**: Material specs with NRC/STC/IIC ratings and octave-band data
- **equipment_spaces**: Room specifications with dimensions, NC requirements, RT60 values
- **equipment**: Mechanical equipment with octave-band sound power levels
- **email_correspondence**: Project communications timeline
- **deliverables**: Project deliverables and submission tracking
- **milestones**: Project milestones with planned vs actual dates

## File Structure

- The first project creates a physical folder structure under `Project_1_Acoustic_Design/` with subdirectories for each data type
- Remaining projects exist only in the database
- Sample files are created in the first project's folders for demonstration

## Data Patterns

- All acoustic data follows ASTM standards
- NRC values are stored both as single values and octave-band data (125Hz-4000Hz)
- Sound power levels use octave-band format (125Hz-8000Hz)
- RT60 measurements at 500Hz, 1000Hz, and 2000Hz
- NC requirements and background noise levels in dBA
- Dates span 2024-2025 timeframe

## Analysis Tools

The `analyze_projects.py` script provides:
- Room volume comparisons across projects
- Material performance vs cost analysis
- Visualization generation (matplotlib/seaborn)
- CSV export of detailed analysis results