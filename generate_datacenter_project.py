import sqlite3
import random
from datetime import datetime, timedelta

def generate_datacenter_project_data():
    conn = sqlite3.connect('project_management.db')
    project_id = 11  # Data Center Acoustic Mitigation project
    
    # Generate budget data
    total_budget = 485000.00
    spent_amount = 218250.00  # 45% complete
    remaining_amount = total_budget - spent_amount
    
    conn.execute('''
    INSERT INTO budget (project_id, total_budget, spent_amount, remaining_amount, last_updated)
    VALUES (?, ?, ?, ?, ?)
    ''', (project_id, total_budget, spent_amount, remaining_amount, '2024-06-15'))
    
    # Generate ASTM test data specific to data centers
    astm_tests = [
        ('ASTM E90 - Server Room Wall Assembly', '2024-04-20', 'Sound Transmission Loss', 52.0, 'STC', 'Wall assembly test for server room isolation'),
        ('ASTM C423 - Acoustic Ceiling Tiles', '2024-05-05', 'Sound Absorption', 0.85, 'NRC', 'Ceiling treatment absorption testing'),
        ('ASTM E492 - Raised Floor System', '2024-05-12', 'Impact Insulation', 58.0, 'IIC', 'Impact isolation for raised floor system'),
        ('ASTM E336 - Server Cabinet Enclosure', '2024-05-25', 'Sound Transmission Loss', 35.0, 'STC', 'Cabinet enclosure sound isolation test'),
        ('ASTM E1050 - Background Noise Survey', '2024-06-01', 'Noise Level', 42.0, 'dBA', 'Ambient noise measurement in data center')
    ]
    
    for test_name, test_date, test_type, result_value, result_unit, notes in astm_tests:
        conn.execute('''
        INSERT INTO astm_tests (project_id, test_name, test_date, test_type, result_value, result_unit, notes)
        VALUES (?, ?, ?, ?, ?, ?, ?)
        ''', (project_id, test_name, test_date, test_type, result_value, result_unit, notes))
    
    # Generate acoustic materials specific to data centers
    materials = [
        ('High-Performance Acoustic Panels', 'Wall Treatment', 0.90, [0.85, 0.88, 0.90, 0.92, 0.90, 0.88], None, None, 24.50, 'Fire-rated panels for server room walls'),
        ('Perforated Metal Ceiling System', 'Ceiling Treatment', 0.75, [0.70, 0.72, 0.75, 0.78, 0.75, 0.72], None, None, 18.75, 'Perforated metal with acoustic backing'),
        ('Vibration Isolation Pads', 'Equipment Mounting', None, [None, None, None, None, None, None], None, None, 45.00, 'Heavy-duty isolation pads for server racks'),
        ('Acoustic Enclosure Panels', 'Equipment Enclosure', 0.65, [0.60, 0.63, 0.65, 0.68, 0.65, 0.62], 48, None, 32.25, 'Modular panels for equipment enclosures'),
        ('Sound-Absorbing Duct Liner', 'HVAC Treatment', 0.80, [0.75, 0.78, 0.80, 0.82, 0.80, 0.78], None, None, 8.95, 'Duct liner for HVAC noise control'),
        ('Raised Floor Underlayment', 'Floor Treatment', None, [None, None, None, None, None, None], 45, 55, 12.50, 'Underlayment for raised floor system')
    ]
    
    for name, mat_type, nrc_single, nrc_bands, stc, iic, cost, notes in materials:
        conn.execute('''
        INSERT INTO acoustic_materials (
            project_id, material_name, material_type, nrc_single_value,
            nrc_125, nrc_250, nrc_500, nrc_1000, nrc_2000, nrc_4000,
            stc_rating, iic_rating, cost_per_sqft, notes
        ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        ''', (project_id, name, mat_type, nrc_single, *nrc_bands, stc, iic, cost, notes))
    
    # Generate equipment spaces specific to data centers
    spaces = [
        ('Server Room A', 'Critical Space', 40.0, 30.0, 12.0, 35, 0.8, 0.7, 0.6, 48.0, 'Primary server room with 200 racks'),
        ('Server Room B', 'Critical Space', 35.0, 25.0, 12.0, 35, 0.8, 0.7, 0.6, 47.0, 'Secondary server room with 150 racks'),
        ('Network Operations Center', 'Control Room', 25.0, 20.0, 10.0, 40, 0.6, 0.5, 0.4, 45.0, 'NOC with 24/7 monitoring staff'),
        ('UPS Room', 'Mechanical Space', 20.0, 15.0, 12.0, 50, 1.2, 1.0, 0.8, 65.0, 'Uninterruptible power supply equipment'),
        ('Cooling Equipment Room', 'Mechanical Space', 30.0, 20.0, 14.0, 55, 1.5, 1.2, 1.0, 72.0, 'HVAC cooling equipment'),
        ('Electrical Switchgear Room', 'Mechanical Space', 18.0, 12.0, 10.0, 45, 1.0, 0.8, 0.6, 58.0, 'Main electrical distribution'),
        ('Generator Room', 'Mechanical Space', 25.0, 18.0, 15.0, 60, 2.0, 1.8, 1.5, 85.0, 'Backup generator equipment'),
        ('Office Space', 'Administrative', 30.0, 25.0, 9.0, 35, 0.5, 0.4, 0.3, 40.0, 'Administrative offices'),
        ('Conference Room', 'Meeting Space', 20.0, 15.0, 9.0, 30, 0.6, 0.5, 0.4, 35.0, 'Meeting room for technical discussions')
    ]
    
    for name, space_type, length, width, height, nc_req, rt60_500, rt60_1000, rt60_2000, bg_noise, notes in spaces:
        volume = length * width * height
        conn.execute('''
        INSERT INTO equipment_spaces (
            project_id, space_name, space_type, length_ft, width_ft, height_ft,
            volume_cubic_ft, nc_requirement, rt60_500hz, rt60_1000hz, rt60_2000hz,
            background_noise_dba, notes
        ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        ''', (project_id, name, space_type, length, width, height, volume, nc_req, rt60_500, rt60_1000, rt60_2000, bg_noise, notes))
    
    # Generate equipment data specific to data centers
    equipment_list = [
        ('Precision Air Conditioning Unit', 'HVAC', [78, 82, 85, 87, 85, 82, 78], 'Main cooling unit for server room'),
        ('Server Rack Cooling Fan', 'Cooling', [65, 68, 70, 72, 70, 68, 65], 'Individual rack cooling fans'),
        ('UPS System', 'Electrical', [72, 75, 78, 80, 78, 75, 72], 'Uninterruptible power supply'),
        ('Backup Generator', 'Electrical', [90, 95, 98, 100, 98, 95, 90], 'Emergency backup generator'),
        ('Chiller System', 'HVAC', [85, 88, 90, 92, 90, 88, 85], 'Main chiller for cooling'),
        ('Air Handling Unit', 'HVAC', [80, 83, 85, 87, 85, 83, 80], 'Air distribution system'),
        ('Transformer Bank', 'Electrical', [75, 78, 80, 82, 80, 78, 75], 'Power distribution transformer'),
        ('Fire Suppression Compressor', 'Safety', [70, 73, 75, 77, 75, 73, 70], 'Fire suppression system compressor')
    ]
    
    for name, eq_type, sound_power, notes in equipment_list:
        conn.execute('''
        INSERT INTO equipment (
            project_id, equipment_name, equipment_type,
            sound_power_125, sound_power_250, sound_power_500,
            sound_power_1000, sound_power_2000, sound_power_4000,
            sound_power_8000, notes
        ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        ''', (project_id, name, eq_type, *sound_power, notes))
    
    # Generate email correspondence
    emails = [
        ('project.manager@cloudtech.com', 'acoustics.team@consultingfirm.com', 'Data Center Acoustic Requirements', 
         'Hello team,\n\nAttached are the acoustic requirements for our new data center facility. Key concerns include:\n\n1. Server room noise isolation (target NC-35)\n2. Generator room sound control\n3. Staff comfort in NOC areas\n\nPlease review and provide initial assessment.\n\nBest regards,\nMark Thompson\nProject Manager', 
         '2024-03-20 09:15:00'),
        ('acoustics.team@consultingfirm.com', 'project.manager@cloudtech.com', 'RE: Data Center Acoustic Requirements',
         'Hi Mark,\n\nThank you for the project details. After reviewing the requirements, we recommend:\n\n1. Comprehensive acoustic testing of existing conditions\n2. Specialized equipment enclosures for high-noise sources\n3. Targeted room treatments for critical spaces\n\nWe\'ll schedule a site visit for next week.\n\nBest,\nSarah Chen\nAcoustic Engineer',
         '2024-03-22 14:30:00'),
        ('project.manager@cloudtech.com', 'acoustics.team@consultingfirm.com', 'Site Visit Feedback',
         'Sarah,\n\nGreat meeting with your team yesterday. The preliminary assessment looks good. Please prioritize:\n\n1. Generator room isolation (immediate concern)\n2. Server room treatments (Phase 1)\n3. NOC comfort improvements (Phase 2)\n\nLet\'s discuss budget allocations this week.\n\nThanks,\nMark',
         '2024-04-15 11:45:00')
    ]
    
    for sender, recipient, subject, content, sent_date in emails:
        conn.execute('''
        INSERT INTO email_correspondence (project_id, sender, recipient, subject, content, sent_date, is_read)
        VALUES (?, ?, ?, ?, ?, ?, ?)
        ''', (project_id, sender, recipient, subject, content, sent_date, 1))
    
    # Generate deliverables
    deliverables = [
        ('Acoustic Assessment Report', 'Technical Report', '2024-04-30', '2024-04-28', 'Completed', 'Initial site assessment and recommendations'),
        ('Equipment Noise Control Specifications', 'Technical Specification', '2024-05-15', '2024-05-12', 'Completed', 'Detailed specs for equipment enclosures'),
        ('Room Treatment Design Package', 'Design Package', '2024-06-01', '2024-06-03', 'Completed', 'Acoustic treatment designs for all spaces'),
        ('Installation Supervision Report', 'Progress Report', '2024-07-15', None, 'In Progress', 'Ongoing installation oversight'),
        ('Final Commissioning Report', 'Technical Report', '2024-12-01', None, 'Pending', 'Final testing and commissioning results'),
        ('Operation and Maintenance Manual', 'Documentation', '2024-12-15', None, 'Pending', 'User manual for acoustic systems')
    ]
    
    for name, del_type, due_date, sub_date, status, notes in deliverables:
        conn.execute('''
        INSERT INTO deliverables (project_id, deliverable_name, deliverable_type, due_date, submission_date, status, notes)
        VALUES (?, ?, ?, ?, ?, ?, ?)
        ''', (project_id, name, del_type, due_date, sub_date, status, notes))
    
    # Generate milestones
    milestones = [
        ('Project Kickoff', 'Project Management', '2024-03-15', '2024-03-15', 'Completed', 'Initial project meeting and planning'),
        ('Site Assessment Complete', 'Technical', '2024-04-30', '2024-04-28', 'Completed', 'Comprehensive acoustic assessment finished'),
        ('Design Phase Complete', 'Design', '2024-06-01', '2024-06-03', 'Completed', 'All design packages approved'),
        ('Equipment Installation Start', 'Installation', '2024-07-01', '2024-07-01', 'Completed', 'Installation phase begins'),
        ('Phase 1 Installation Complete', 'Installation', '2024-09-15', None, 'In Progress', 'Server room treatments installed'),
        ('Phase 2 Installation Complete', 'Installation', '2024-11-01', None, 'Pending', 'Mechanical room treatments installed'),
        ('Final Testing', 'Testing', '2024-11-15', None, 'Pending', 'Commissioning and performance testing'),
        ('Project Completion', 'Project Management', '2024-12-15', None, 'Pending', 'Final project delivery and closeout')
    ]
    
    for name, milestone_type, planned_date, actual_date, status, notes in milestones:
        conn.execute('''
        INSERT INTO milestones (project_id, milestone_name, milestone_type, planned_date, actual_date, status, notes)
        VALUES (?, ?, ?, ?, ?, ?, ?)
        ''', (project_id, name, milestone_type, planned_date, actual_date, status, notes))
    
    conn.commit()
    conn.close()
    print("Data center project data generated successfully!")

if __name__ == "__main__":
    generate_datacenter_project_data()