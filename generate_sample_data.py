import sqlite3
import pandas as pd
import numpy as np
from datetime import datetime, timedelta
import random
import json

def generate_acoustic_material_data(conn, project_id):
    # Sample acoustic materials with realistic values
    materials = [
        # Room Treatment Materials (NRC values)
        {
            'name': 'Acoustic Panel A',
            'type': 'Room Treatment',
            'nrc_single': 0.85,
            'nrc_bands': [0.75, 0.80, 0.85, 0.90, 0.85, 0.80],
            'stc': None,
            'iic': None,
            'cost_per_sqft': 12.50  # Premium acoustic panel
        },
        {
            'name': 'Bass Trap B',
            'type': 'Room Treatment',
            'nrc_single': 0.95,
            'nrc_bands': [0.95, 0.90, 0.85, 0.80, 0.75, 0.70],
            'stc': None,
            'iic': None,
            'cost_per_sqft': 15.75  # High-performance bass trap
        },
        {
            'name': 'Ceiling Tile C',
            'type': 'Room Treatment',
            'nrc_single': 0.75,
            'nrc_bands': [0.65, 0.70, 0.75, 0.80, 0.75, 0.70],
            'stc': None,
            'iic': None,
            'cost_per_sqft': 8.25   # Standard acoustic ceiling tile
        },
        # Underlayment Materials (STC/IIC values)
        {
            'name': 'Floor Underlayment X',
            'type': 'Underlayment',
            'nrc_single': None,
            'nrc_bands': [None, None, None, None, None, None],
            'stc': 55,
            'iic': 65,
            'cost_per_sqft': 3.95    # Standard floor underlayment
        },
        {
            'name': 'Isolation Mat Y',
            'type': 'Underlayment',
            'nrc_single': None,
            'nrc_bands': [None, None, None, None, None, None],
            'stc': 52,
            'iic': 62,
            'cost_per_sqft': 2.75    # Basic isolation mat
        },
        {
            'name': 'Sound Barrier Z',
            'type': 'Underlayment',
            'nrc_single': None,
            'nrc_bands': [None, None, None, None, None, None],
            'stc': 58,
            'iic': 68,
            'cost_per_sqft': 5.25    # Premium sound barrier
        }
    ]
    
    for material in materials:
        conn.execute('''
        INSERT INTO acoustic_materials (
            project_id, material_name, material_type, nrc_single_value,
            nrc_125, nrc_250, nrc_500, nrc_1000, nrc_2000, nrc_4000,
            stc_rating, iic_rating, cost_per_sqft, notes
        ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        ''', (
            project_id,
            material['name'],
            material['type'],
            material['nrc_single'],
            *material['nrc_bands'],
            material['stc'],
            material['iic'],
            material['cost_per_sqft'],
            f"Sample {material['type']} material"
        ))

def generate_equipment_data(conn, project_id):
    # Sample equipment with realistic sound power levels
    equipment_list = [
        {
            'name': 'HVAC Unit A',
            'type': 'Mechanical',
            'sound_power': [75, 78, 80, 82, 80, 78, 75]
        },
        {
            'name': 'Generator B',
            'type': 'Electrical',
            'sound_power': [85, 88, 90, 92, 90, 88, 85]
        },
        {
            'name': 'Pump C',
            'type': 'Mechanical',
            'sound_power': [70, 73, 75, 77, 75, 73, 70]
        }
    ]
    
    for equipment in equipment_list:
        conn.execute('''
        INSERT INTO equipment (
            project_id, equipment_name, equipment_type,
            sound_power_125, sound_power_250, sound_power_500,
            sound_power_1000, sound_power_2000, sound_power_4000,
            sound_power_8000, notes
        ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        ''', (
            project_id,
            equipment['name'],
            equipment['type'],
            *equipment['sound_power'],
            f"Sample {equipment['type']} equipment"
        ))

def generate_equipment_spaces_data(conn, project_id):
    # Sample noise sensitive spaces with realistic dimensions and acoustic parameters
    spaces = [
        {
            'name': 'Main Conference Room',
            'type': 'Meeting Space',
            'length_ft': 30.0,
            'width_ft': 20.0,
            'height_ft': 10.0,
            'nc_requirement': 30,
            'rt60_500hz': 0.6,    # Optimized for speech intelligibility
            'rt60_1000hz': 0.5,
            'rt60_2000hz': 0.4,
            'background_noise_dba': 35.0,
            'notes': 'Primary meeting space with video conferencing'
        },
        {
            'name': 'Executive Office',
            'type': 'Office Space',
            'length_ft': 15.0,
            'width_ft': 12.0,
            'height_ft': 9.0,
            'nc_requirement': 35,
            'rt60_500hz': 0.4,    # Shorter RT60 for smaller space
            'rt60_1000hz': 0.35,
            'rt60_2000hz': 0.3,
            'background_noise_dba': 40.0,
            'notes': 'Private executive office'
        },
        {
            'name': 'Recording Studio',
            'type': 'Specialized Space',
            'length_ft': 25.0,
            'width_ft': 18.0,
            'height_ft': 12.0,
            'nc_requirement': 20,
            'rt60_500hz': 0.3,    # Very controlled RT60 for recording
            'rt60_1000hz': 0.25,
            'rt60_2000hz': 0.2,
            'background_noise_dba': 25.0,
            'notes': 'Professional recording studio'
        },
        {
            'name': 'Open Office Area',
            'type': 'Work Space',
            'length_ft': 50.0,
            'width_ft': 40.0,
            'height_ft': 9.0,
            'nc_requirement': 40,
            'rt60_500hz': 0.5,    # Moderate RT60 for open office
            'rt60_1000hz': 0.45,
            'rt60_2000hz': 0.4,
            'background_noise_dba': 45.0,
            'notes': 'Open plan office space'
        },
        {
            'name': 'Quiet Room',
            'type': 'Specialized Space',
            'length_ft': 12.0,
            'width_ft': 10.0,
            'height_ft': 8.0,
            'nc_requirement': 25,
            'rt60_500hz': 0.2,    # Very short RT60 for quiet room
            'rt60_1000hz': 0.15,
            'rt60_2000hz': 0.1,
            'background_noise_dba': 30.0,
            'notes': 'Sound isolated quiet room'
        }
    ]
    
    for space in spaces:
        # Calculate volume in cubic feet
        volume = space['length_ft'] * space['width_ft'] * space['height_ft']
        
        conn.execute('''
        INSERT INTO equipment_spaces (
            project_id, space_name, space_type,
            length_ft, width_ft, height_ft,
            volume_cubic_ft, nc_requirement,
            rt60_500hz, rt60_1000hz, rt60_2000hz,
            background_noise_dba, notes
        ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        ''', (
            project_id,
            space['name'],
            space['type'],
            space['length_ft'],
            space['width_ft'],
            space['height_ft'],
            volume,
            space['nc_requirement'],
            space['rt60_500hz'],
            space['rt60_1000hz'],
            space['rt60_2000hz'],
            space['background_noise_dba'],
            space['notes']
        ))

def generate_email_correspondence(conn, project_id, start_date):
    # Sample email templates
    email_templates = [
        {
            'subject': 'Project Kickoff Meeting',
            'content': 'Dear team,\n\nI hope this email finds you well. I would like to schedule our project kickoff meeting for next week...'
        },
        {
            'subject': 'Status Update - Week {week}',
            'content': 'Hello team,\n\nHere is our weekly status update...'
        },
        {
            'subject': 'Material Selection Review',
            'content': 'Hi team,\n\nPlease review the attached material specifications...'
        }
    ]
    
    # Generate emails over the project timeline
    current_date = start_date
    while current_date < start_date + timedelta(days=365):
        if random.random() < 0.3:  # 30% chance of email on any given day
            template = random.choice(email_templates)
            conn.execute('''
            INSERT INTO email_correspondence (
                project_id, sender, recipient, subject, content,
                sent_date, is_read
            ) VALUES (?, ?, ?, ?, ?, ?, ?)
            ''', (
                project_id,
                'project.manager@company.com',
                'team@company.com',
                template['subject'].format(week=random.randint(1, 52)),
                template['content'],
                current_date.strftime('%Y-%m-%d %H:%M:%S'),
                random.choice([0, 1])
            ))
        current_date += timedelta(days=1)

def generate_milestones(conn, project_id, start_date, end_date):
    milestone_types = [
        'Project Percent Completion',
        'Project Invoice',
        'Team Meeting',
        'Field Test',
        'Report Submission'
    ]
    
    current_date = start_date
    while current_date < end_date:
        if random.random() < 0.2:  # 20% chance of milestone on any given day
            milestone_type = random.choice(milestone_types)
            conn.execute('''
            INSERT INTO milestones (
                project_id, milestone_name, milestone_type,
                planned_date, actual_date, status, notes
            ) VALUES (?, ?, ?, ?, ?, ?, ?)
            ''', (
                project_id,
                f"{milestone_type} - {current_date.strftime('%Y-%m-%d')}",
                milestone_type,
                current_date.strftime('%Y-%m-%d'),
                (current_date + timedelta(days=random.randint(-2, 2))).strftime('%Y-%m-%d'),
                random.choice(['Completed', 'In Progress', 'Delayed']),
                f"Sample {milestone_type} milestone"
            ))
        current_date += timedelta(days=1)

def main():
    conn = sqlite3.connect('project_management.db')
    
    # Get all projects
    cursor = conn.cursor()
    cursor.execute('SELECT project_id, start_date, end_date FROM projects')
    projects = cursor.fetchall()
    
    for project_id, start_date, end_date in projects:
        # Generate data for each project
        generate_acoustic_material_data(conn, project_id)
        generate_equipment_data(conn, project_id)
        generate_equipment_spaces_data(conn, project_id)
        generate_email_correspondence(conn, project_id, datetime.strptime(start_date, '%Y-%m-%d'))
        generate_milestones(conn, project_id, 
                          datetime.strptime(start_date, '%Y-%m-%d'),
                          datetime.strptime(end_date, '%Y-%m-%d'))
    
    conn.commit()
    conn.close()

if __name__ == "__main__":
    main() 