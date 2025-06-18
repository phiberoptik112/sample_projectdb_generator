import sqlite3
import pandas as pd
import numpy as np
from datetime import datetime, timedelta
import os
import random
from pathlib import Path

# Database setup
def create_database():
    conn = sqlite3.connect('project_management.db')
    cursor = conn.cursor()
    
    # Create tables
    cursor.executescript('''
    -- Projects table
    CREATE TABLE IF NOT EXISTS projects (
        project_id INTEGER PRIMARY KEY,
        project_name TEXT NOT NULL,
        client_name TEXT NOT NULL,
        start_date DATE NOT NULL,
        end_date DATE NOT NULL,
        status TEXT NOT NULL,
        percent_complete INTEGER DEFAULT 0,
        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
    );

    -- ASTM Tests table
    CREATE TABLE IF NOT EXISTS astm_tests (
        test_id INTEGER PRIMARY KEY,
        project_id INTEGER,
        test_name TEXT NOT NULL,
        test_date DATE NOT NULL,
        test_type TEXT NOT NULL,
        result_value REAL,
        result_unit TEXT,
        notes TEXT,
        FOREIGN KEY (project_id) REFERENCES projects(project_id)
    );

    -- Budget table
    CREATE TABLE IF NOT EXISTS budget (
        budget_id INTEGER PRIMARY KEY,
        project_id INTEGER,
        total_budget REAL NOT NULL,
        spent_amount REAL DEFAULT 0,
        remaining_amount REAL,
        last_updated DATE,
        FOREIGN KEY (project_id) REFERENCES projects(project_id)
    );

    -- Acoustic Materials table
    CREATE TABLE IF NOT EXISTS acoustic_materials (
        material_id INTEGER PRIMARY KEY,
        project_id INTEGER,
        material_name TEXT NOT NULL,
        material_type TEXT NOT NULL,
        nrc_single_value REAL,
        nrc_125 REAL,
        nrc_250 REAL,
        nrc_500 REAL,
        nrc_1000 REAL,
        nrc_2000 REAL,
        nrc_4000 REAL,
        stc_rating INTEGER,
        iic_rating INTEGER,
        cost_per_sqft REAL NOT NULL,
        notes TEXT,
        FOREIGN KEY (project_id) REFERENCES projects(project_id)
    );

    -- Equipment Spaces table
    CREATE TABLE IF NOT EXISTS equipment_spaces (
        space_id INTEGER PRIMARY KEY,
        project_id INTEGER,
        space_name TEXT NOT NULL,
        space_type TEXT NOT NULL,
        length_ft REAL NOT NULL,
        width_ft REAL NOT NULL,
        height_ft REAL NOT NULL,
        volume_cubic_ft REAL NOT NULL,
        nc_requirement INTEGER,
        rt60_500hz REAL,  -- Reverberation time at 500Hz in seconds
        rt60_1000hz REAL, -- Reverberation time at 1000Hz in seconds
        rt60_2000hz REAL, -- Reverberation time at 2000Hz in seconds
        background_noise_dba REAL, -- Background noise level in dBA
        notes TEXT,
        FOREIGN KEY (project_id) REFERENCES projects(project_id)
    );

    -- Equipment table
    CREATE TABLE IF NOT EXISTS equipment (
        equipment_id INTEGER PRIMARY KEY,
        project_id INTEGER,
        equipment_name TEXT NOT NULL,
        equipment_type TEXT NOT NULL,
        sound_power_125 REAL,
        sound_power_250 REAL,
        sound_power_500 REAL,
        sound_power_1000 REAL,
        sound_power_2000 REAL,
        sound_power_4000 REAL,
        sound_power_8000 REAL,
        notes TEXT,
        FOREIGN KEY (project_id) REFERENCES projects(project_id)
    );

    -- Email Correspondence table
    CREATE TABLE IF NOT EXISTS email_correspondence (
        email_id INTEGER PRIMARY KEY,
        project_id INTEGER,
        sender TEXT NOT NULL,
        recipient TEXT NOT NULL,
        subject TEXT NOT NULL,
        content TEXT NOT NULL,
        sent_date TIMESTAMP NOT NULL,
        is_read BOOLEAN DEFAULT 0,
        FOREIGN KEY (project_id) REFERENCES projects(project_id)
    );

    -- Deliverables table
    CREATE TABLE IF NOT EXISTS deliverables (
        deliverable_id INTEGER PRIMARY KEY,
        project_id INTEGER,
        deliverable_name TEXT NOT NULL,
        deliverable_type TEXT NOT NULL,
        due_date DATE NOT NULL,
        submission_date DATE,
        status TEXT NOT NULL,
        notes TEXT,
        FOREIGN KEY (project_id) REFERENCES projects(project_id)
    );

    -- Milestones table
    CREATE TABLE IF NOT EXISTS milestones (
        milestone_id INTEGER PRIMARY KEY,
        project_id INTEGER,
        milestone_name TEXT NOT NULL,
        milestone_type TEXT NOT NULL,
        planned_date DATE NOT NULL,
        actual_date DATE,
        status TEXT NOT NULL,
        notes TEXT,
        FOREIGN KEY (project_id) REFERENCES projects(project_id)
    );
    ''')
    
    conn.commit()
    return conn

def generate_sample_data(conn):
    # Sample project names and clients
    project_names = [
        "Acoustic Design - Corporate Office",
        "Concert Hall Renovation",
        "Recording Studio Design",
        "Educational Facility Acoustics",
        "Healthcare Facility Noise Control"
    ]
    
    clients = [
        "TechCorp Inc.",
        "City Arts Foundation",
        "SoundWave Studios",
        "Education District",
        "HealthCare Plus"
    ]
    
    # Generate projects
    for i in range(5):
        start_date = datetime(2024, 1, 1) + timedelta(days=random.randint(0, 60))
        end_date = start_date + timedelta(days=random.randint(180, 365))
        
        conn.execute('''
        INSERT INTO projects (project_name, client_name, start_date, end_date, status, percent_complete)
        VALUES (?, ?, ?, ?, ?, ?)
        ''', (
            project_names[i],
            clients[i],
            start_date.strftime('%Y-%m-%d'),
            end_date.strftime('%Y-%m-%d'),
            random.choice(['In Progress', 'Planning', 'Review', 'Completed']),
            random.randint(0, 100)
        ))
    
    conn.commit()

def main():
    # Create database and tables
    conn = create_database()
    
    # Generate sample data
    generate_sample_data(conn)
    
    # Create folder structure for the first project
    project_folders = [
        'astm_tests_db',
        'budget',
        'acoustic_materials_db',
        'equipment_spaces_db',
        'email_db',
        'deliverables_db'
    ]
    
    base_path = Path('Project_1_Acoustic_Design')
    for folder in project_folders:
        (base_path / folder).mkdir(parents=True, exist_ok=True)
    
    # Create sample text files
    sample_files = {
        'astm_tests_db': ['test_results_001.txt', 'raw_data_001.txt'],
        'budget': ['project_budget.xlsx', 'scope_of_work.txt'],
        'acoustic_materials_db': ['material_specs.txt', 'nrc_ratings.csv'],
        'equipment_spaces_db': ['space_requirements.txt', 'equipment_list.csv'],
        'email_db': ['client_correspondence.txt', 'team_meetings.txt'],
        'deliverables_db': ['final_report.txt', 'presentation.pptx']
    }
    
    for folder, files in sample_files.items():
        for file in files:
            with open(base_path / folder / file, 'w') as f:
                f.write(f"Sample content for {file}\n")
    
    conn.close()

if __name__ == "__main__":
    main() 