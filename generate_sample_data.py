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
    # Extended acoustic recommendation discussion thread
    acoustic_discussion_thread = [
        {
            'date_offset': 5,  # Day 5 of project
            'sender': 'sarah.johnson@acoustics.com',
            'recipient': 'design.team@company.com',
            'subject': 'Initial Acoustic Material Recommendation - Conference Room Treatment',
            'content': '''Dear Design Team,

I hope this email finds you well. Following our initial site assessment and acoustic modeling, I'm pleased to present our preliminary recommendations for the main conference room acoustic treatment.

**INITIAL RECOMMENDATION:**
Primary Material: Primacoustic Broadway Panel (Class A Fire Rating)
- NRC Rating: 0.95 (excellent absorption)
- Thickness: 2" 
- Coverage: 60% of wall surface area
- Estimated Cost: $18,500 for full installation

**TECHNICAL SPECIFICATIONS:**
- 125Hz: 0.85 NRC
- 250Hz: 0.90 NRC  
- 500Hz: 0.95 NRC
- 1000Hz: 0.98 NRC
- 2000Hz: 0.95 NRC
- 4000Hz: 0.92 NRC

This configuration will achieve the target RT60 of 0.6 seconds and NC-30 rating while maintaining excellent speech intelligibility for video conferencing.

Please review and let me know if you have any questions. I'm happy to discuss alternatives or modifications.

Best regards,
Sarah Johnson
Senior Acoustical Engineer
Acoustics Solutions Inc.'''
        },
        {
            'date_offset': 7,
            'sender': 'mike.anderson@company.com',
            'recipient': 'sarah.johnson@acoustics.com',
            'subject': 'RE: Initial Acoustic Material Recommendation - Conference Room Treatment',
            'content': '''Hi Sarah,

Thank you for the detailed recommendation. The design team has reviewed your proposal and we have several questions and concerns:

**DESIGN CONCERNS:**
1. The Broadway panels have a very industrial look - our client is looking for something more refined/executive
2. 60% wall coverage seems excessive visually - can we achieve similar results with less coverage?
3. The cost is significantly over our initial $12,000 budget allocation

**TECHNICAL QUESTIONS:**
1. What alternatives exist that might have better aesthetic integration?
2. Could we use a combination of ceiling treatment + reduced wall coverage?
3. Are there comparable materials at a lower price point?

The client specifically mentioned wanting a "warm, professional atmosphere" rather than a "recording studio feel."

Could we schedule a call this week to discuss alternatives?

Best regards,
Mike Anderson
Lead Interior Designer
Corporate Design Solutions'''
        },
        {
            'date_offset': 8,
            'sender': 'sarah.johnson@acoustics.com',
            'recipient': 'mike.anderson@company.com',
            'subject': 'RE: Conference Room Treatment - Alternative Options',
            'content': '''Hi Mike,

Great questions! I completely understand the aesthetic and budget concerns. Let me propose some alternatives that better align with your requirements:

**REVISED RECOMMENDATION - OPTION A:**
Primary: Architectural fabric-wrapped panels (custom colors available)
- NRC Rating: 0.88 (still excellent)
- Coverage: 45% wall + 30% ceiling treatment
- Aesthetic: Available in 200+ fabric options, looks like premium wall covering
- Cost: $14,200 (within revised budget)

**REVISED RECOMMENDATION - OPTION B:**
Hybrid approach with decorative elements:
- Perforated wood panels with acoustic backing (20% coverage)
- Acoustic ceiling tiles (premium grade)
- Strategic placement of acoustic art panels
- Cost: $13,800
- Aesthetic: Looks like intentional design feature

**PERFORMANCE COMPARISON:**
- Option A: RT60 = 0.65 seconds (vs 0.6 target)
- Option B: RT60 = 0.68 seconds (still acceptable)
- Both maintain NC-30 rating

I'm available for a call Wednesday afternoon or Thursday morning to review fabric samples and discuss integration with your overall design scheme.

Best regards,
Sarah'''
        },
        {
            'date_offset': 10,
            'sender': 'jennifer.clark@company.com',
            'recipient': 'sarah.johnson@acoustics.com',
            'subject': 'RE: Conference Room Treatment - Client Feedback',
            'content': '''Hi Sarah,

Thanks for the call yesterday. The client loved the fabric-wrapped panel concept (Option A) but had additional requests after seeing the samples:

**CLIENT FEEDBACK:**
✓ Approved: Charcoal gray fabric (#C2847) for main panels
✓ Approved: Reduced coverage approach  
✗ Concern: Ceiling treatment may interfere with existing lighting design
✗ New Request: Can we integrate company logo or branding elements?

**NEW REQUIREMENTS:**
1. Ceiling treatment must work around existing recessed lighting grid
2. Explore custom printed acoustic panels with subtle company branding
3. Ensure fire rating compliance (they specifically asked about this)

**TIMELINE UPDATE:**
The client has moved up the completion date by 3 weeks due to an important board meeting. New target: March 15th.

Can you provide updated specifications addressing these points by Friday?

Best regards,
Jennifer Clark
Project Manager
Corporate Design Solutions'''
        },
        {
            'date_offset': 12,
            'sender': 'sarah.johnson@acoustics.com',
            'recipient': 'jennifer.clark@company.com',
            'subject': 'UPDATED: Conference Room Acoustic Design - Final Specifications',
            'content': '''Hi Jennifer,

I've worked with our fabrication team to address all the client's requirements. Here's the updated specification:

**FINAL DESIGN SPECIFICATION:**
Primary Material: Custom fabric-wrapped acoustic panels with integrated branding
- Base panels: Charcoal gray fabric (#C2847) with Class A fire rating
- Custom branding: Subtle company logo integration (laser-cut perforation pattern)
- Wall coverage: 45% (strategically placed around lighting)
- Ceiling: Modified approach using acoustic tiles only where lighting allows

**TECHNICAL PERFORMANCE:**
- RT60: 0.64 seconds (excellent for speech intelligibility)
- NC Rating: 29 (better than target!)
- Fire Rating: Class A (meets all building codes)

**COST BREAKDOWN:**
- Custom fabric panels: $11,200
- Modified ceiling treatment: $2,400
- Custom branding integration: $800
- Total: $14,400 (within approved budget)

**TIMELINE:**
- Fabrication: 10 business days
- Installation: 3 days
- Total delivery: March 12th (3 days ahead of schedule!)

The custom logo integration uses a perforated pattern that actually enhances the acoustic performance while creating a sophisticated branding element.

Ready to proceed with fabrication upon approval.

Best regards,
Sarah Johnson'''
        },
        {
            'date_offset': 15,
            'sender': 'mike.anderson@company.com',
            'recipient': 'sarah.johnson@acoustics.com',
            'subject': 'RE: APPROVED - Conference Room Acoustic Design',
            'content': '''Hi Sarah,

Excellent work! The client approved the final design this morning. Please proceed with fabrication immediately.

**APPROVAL DETAILS:**
- Design specification: ✓ Approved
- Budget: ✓ Approved at $14,400
- Timeline: ✓ Approved for March 12th delivery
- Branding integration: ✓ Client very excited about this feature

**NEXT STEPS:**
1. Please send fabrication confirmation by tomorrow
2. We'll coordinate site access for installation
3. Schedule final inspection for March 13th

One small addition: The client would like a brief technical report documenting the acoustic performance for their facilities management team. Can you prepare a 2-page summary?

Looking forward to seeing this come together!

Best regards,
Mike Anderson'''
        },
        {
            'date_offset': 25,
            'sender': 'sarah.johnson@acoustics.com',
            'recipient': 'mike.anderson@company.com',
            'subject': 'Installation Update - Conference Room Acoustics',
            'content': '''Hi Mike,

Great news! Installation was completed yesterday and the results exceeded expectations.

**INSTALLATION SUMMARY:**
- Installation completed: March 11th (1 day ahead of schedule)
- No issues encountered during installation
- Custom panels fit perfectly within existing lighting layout
- Branding integration looks exceptional

**IMMEDIATE OBSERVATIONS:**
- Dramatic reduction in echo and reverberation
- Much clearer speech intelligibility
- Professional, sophisticated appearance
- The logo integration is subtle but effective

**NEXT STEPS:**
1. Technical report completed (attached)
2. Final acoustic testing scheduled for March 14th
3. Client walk-through scheduled for March 15th

The client's facilities manager was on-site during installation and was very impressed with both the acoustic performance and visual integration.

Looking forward to the final testing results!

Best regards,
Sarah'''
        },
        {
            'date_offset': 30,
            'sender': 'sarah.johnson@acoustics.com',
            'recipient': 'project.team@company.com',
            'subject': 'FINAL REPORT - Conference Room Acoustic Performance Testing',
            'content': '''Dear Project Team,

I'm pleased to report that the final acoustic testing has been completed with outstanding results.

**MEASURED PERFORMANCE:**
- RT60 @ 500Hz: 0.62 seconds (Target: 0.6 seconds) ✓
- RT60 @ 1000Hz: 0.59 seconds ✓
- NC Rating: 28 (Target: 30) ✓ EXCEEDED
- Speech Intelligibility (STI): 0.72 (Excellent rating)

**POST-INSTALLATION FEEDBACK:**
Client comments from March 15th walkthrough:
- "The room sounds completely different - we can actually hear each other clearly now"
- "The design looks like it was always meant to be there"
- "Our last video conference was the best we've ever had"

**PROJECT METRICS:**
- Delivered: 3 days ahead of schedule
- Budget: $14,400 (within approved amount)
- Performance: Exceeded all acoustic targets
- Aesthetic integration: Highly successful

**LESSONS LEARNED:**
1. Early collaboration between acoustic and design teams crucial
2. Custom branding integration added significant value
3. Fabric-wrapped panels offer excellent aesthetic flexibility
4. Modified ceiling approach worked perfectly with existing lighting

Thank you all for your collaboration on this successful project. The client has already inquired about acoustic treatment for their other conference rooms.

Best regards,
Sarah Johnson
Senior Acoustical Engineer

**TECHNICAL REPORT ATTACHED:**
- Complete acoustic measurements
- Performance verification
- Maintenance recommendations
- Warranty information'''
        },
        {
            'date_offset': 35,
            'sender': 'jennifer.clark@company.com',
            'recipient': 'sarah.johnson@acoustics.com',
            'subject': 'Client Testimonial & Future Projects',
            'content': '''Hi Sarah,

I wanted to share some fantastic feedback we received from the client following their first major board meeting in the newly treated conference room:

**CLIENT TESTIMONIAL:**
"The acoustic treatment has transformed our conference room into a truly professional meeting space. The improvement in audio quality for video conferences is remarkable - we can now participate in international calls without any audio issues. The design integration is flawless and several visitors have commented on the sophisticated appearance. We're particularly proud of the subtle branding element which adds a premium feel to the space."

**BUSINESS IMPACT:**
- 50% reduction in meeting time lost to audio issues
- Improved client presentation quality
- Enhanced professional image
- Increased employee satisfaction with meeting spaces

**FUTURE OPPORTUNITIES:**
The client has requested proposals for:
1. Executive boardroom (similar scope)
2. Open office acoustic treatment
3. Reception area sound masking
4. Training room acoustic optimization

Could we schedule a planning call next week to discuss these additional opportunities?

This project showcases the value of thorough acoustic engineering combined with thoughtful design integration. Thank you for making this such a success!

Best regards,
Jennifer Clark
Project Manager

P.S. The client specifically requested that you lead the acoustic design for all future projects.'''
        }
    ]
    
    # Generate the extended acoustic discussion thread
    for email in acoustic_discussion_thread:
        email_date = start_date + timedelta(days=email['date_offset'])
        conn.execute('''
        INSERT INTO email_correspondence (
            project_id, sender, recipient, subject, content,
            sent_date, is_read
        ) VALUES (?, ?, ?, ?, ?, ?, ?)
        ''', (
            project_id,
            email['sender'],
            email['recipient'],
            email['subject'],
            email['content'],
            email_date.strftime('%Y-%m-%d %H:%M:%S'),
            1  # Mark as read
        ))
    
    # Generate additional general project emails
    general_email_templates = [
        {
            'subject': 'Weekly Status Meeting - {week}',
            'content': 'Hello team,\n\nThis is a reminder about our weekly status meeting scheduled for tomorrow at 2:00 PM. Please come prepared with your updates and any issues that need team discussion.\n\nBest regards,\nProject Management'
        },
        {
            'subject': 'Budget Review - Q{quarter}',
            'content': 'Dear team,\n\nPlease review the attached budget summary for this quarter. We need to discuss any variances and plan for upcoming expenses.\n\nThank you,\nFinance Team'
        },
        {
            'subject': 'Site Visit Scheduled',
            'content': 'Hi everyone,\n\nI have scheduled a site visit for next Tuesday. Please let me know if you need to join us on site.\n\nBest regards,\nProject Manager'
        },
        {
            'subject': 'Client Feedback Session',
            'content': 'Dear team,\n\nThe client has requested a feedback session to review our progress. Please prepare your respective sections for presentation.\n\nThank you,\nProject Lead'
        }
    ]
    
    # Generate additional emails throughout the project timeline
    current_date = start_date + timedelta(days=40)  # Start after the acoustic discussion
    while current_date < start_date + timedelta(days=365):
        if random.random() < 0.2:  # 20% chance of email on any given day
            template = random.choice(general_email_templates)
            conn.execute('''
            INSERT INTO email_correspondence (
                project_id, sender, recipient, subject, content,
                sent_date, is_read
            ) VALUES (?, ?, ?, ?, ?, ?, ?)
            ''', (
                project_id,
                'project.manager@company.com',
                'team@company.com',
                template['subject'].format(week=random.randint(1, 52), quarter=random.randint(1, 4)),
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