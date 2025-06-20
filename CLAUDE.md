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

## Email Correspondence Generation

To generate realistic email correspondence files for project documentation, use the following prompt structure:

```markdown
Generate a series of email exchanges between [ROLE_1] and [ROLE_2] regarding [TOPIC]. The correspondence should:

1. Follow a chronological sequence with:
   - Proper email headers (From, To, Subject, Date)
   - Realistic timestamps
   - Professional salutations and closings
   - Clear subject line progression (RE: RE: RE: etc.)

2. Include technical details such as:
   - Specific measurements and specifications
   - Cost breakdowns and payment terms
   - Project timelines and milestones
   - Technical requirements and standards

3. Maintain professional tone while showing:
   - Natural negotiation progression
   - Clear action items and next steps
   - Proper documentation of decisions
   - Professional conflict resolution

4. Format each email with:
   - Clear separation between emails (---)
   - Proper indentation for lists and sections
   - Consistent formatting for numbers and dates
   - Professional signature blocks

Example prompt:
"Generate email correspondence between a project manager and client account manager regarding project billing and deliverables. Include detailed payment schedules, deliverable acceptance criteria, and budget tracking requirements. The correspondence should show a natural progression from initial proposal to final agreement."

Key elements to include:
- Project-specific details (numbers, dates, costs)
- Industry-standard terminology
- Realistic negotiation points
- Clear documentation requirements
- Professional formatting and structure

File naming convention:
- Use descriptive names: [topic]_correspondence.txt
- Place in appropriate project subdirectory
- Maintain consistent formatting across all correspondence files
```

This prompt structure ensures:
1. Consistent formatting across all correspondence
2. Realistic technical and business details
3. Natural progression of discussions
4. Professional tone and structure
5. Proper documentation of decisions and agreements

## Acoustic Materials Data Generation

To generate comprehensive acoustic materials data files, use the following structure:

### Equipment Sound Data Files

```markdown
Generate sound data files for [EQUIPMENT_TYPE] with the following structure:

1. Equipment Specifications:
   - Equipment type and model
   - Capacity and operating conditions
   - Location and installation details

2. Sound Power Levels (dB re 10^-12 W):
   - Octave band frequencies: 31.5, 63, 125, 250, 500, 1000, 2000, 4000, 8000 Hz
   - Overall sound power level
   - Realistic values based on equipment size and type

3. Operating Conditions:
   - Speed, pressure, temperature, humidity
   - Load conditions and operating modes

4. Noise Control Requirements:
   - Silencer specifications
   - Vibration isolation requirements
   - Installation requirements

5. Notes and Standards:
   - Testing standards (AHRI, ISO, ASTM)
   - Measurement conditions
   - Performance considerations

Example prompt:
"Generate sound data files for Air Handling Units (AHUs), Emergency Generators, VAV boxes, and Duct Silencers. Include realistic sound power levels for different equipment sizes and operating conditions."
```

### Space Requirements Files

```markdown
Generate space requirements files for [SPACE_TYPE] with the following structure:

1. Space Specifications:
   - Dimensions and volume calculations
   - Occupancy and usage requirements
   - Floor-to-floor heights

2. Noise Criteria Requirements:
   - NC ratings for different areas
   - Background noise levels
   - Speech intelligibility requirements

3. Acoustic Treatments:
   - Ceiling system specifications (NRC, CAC ratings)
   - Wall treatment requirements (coverage, mounting)
   - Floor covering specifications
   - Additional treatments (baffles, masking)

4. Design Considerations:
   - Speech privacy requirements
   - Reverberation time targets
   - Sound transmission requirements

5. HVAC Requirements:
   - Air distribution specifications
   - Ductwork requirements
   - Noise control measures

6. Testing and Maintenance:
   - Pre/post installation testing
   - Maintenance requirements
   - Performance monitoring

Example prompt:
"Generate space requirements files for Open Office Areas, Conference Rooms, and Testing Laboratories. Include detailed acoustic specifications, treatment requirements, and performance criteria."
```

### Material Test Data CSV

```markdown
Generate a CSV file with comprehensive test data for acoustic materials:

Columns should include:
- Material_Type (Wall_Panel, Ceiling_Tile, Floor_Covering, Underlayment)
- Product_Name (Manufacturer and model)
- Thickness_inches, Density_pcf
- NRC_Rating, STC_Rating, CAC_Rating, IIC_Rating
- Fire_Rating
- Absorption coefficients for 6 octave bands (125-4000 Hz)

Data should include:
- Multiple manufacturers and product types
- Realistic performance ratings
- Industry-standard absorption coefficients
- Proper categorization and specifications

Example prompt:
"Generate a comprehensive CSV file with test data for wall treatments, ceiling materials, floor coverings, and underlayments. Include realistic NRC, STC, CAC, and IIC ratings with absorption coefficients."
```

## Project Deliverables Generation

To generate comprehensive project deliverable documents, use the following structure:

### Site Survey Reports

```markdown
Generate a detailed site survey report with the following sections:

1. Executive Summary:
   - Survey overview and methodology
   - Key findings and recommendations

2. Survey Methodology:
   - Equipment used and standards followed
   - Measurement procedures and conditions

3. Survey Results:
   - Background noise measurements by space type
   - Reverberation time measurements
   - Sound transmission measurements
   - Noise source identification

4. Space Analysis:
   - Detailed space specifications
   - Current vs. target conditions
   - Treatment requirements

5. Recommendations:
   - Immediate, medium-term, and long-term actions
   - Cost implications and priorities

6. Appendices:
   - Measurement data, photos, equipment specs

Example prompt:
"Generate a comprehensive site survey report for an acoustic design project. Include realistic measurements, analysis, and recommendations for various space types."
```

### Acoustic Modeling Results

```markdown
Generate acoustic modeling results with the following structure:

1. Modeling Methodology:
   - Software used and standards followed
   - Model parameters and assumptions

2. Modeling Results by Space:
   - Sound pressure level predictions
   - Reverberation time calculations
   - Speech intelligibility analysis
   - Performance comparisons

3. Material Performance Analysis:
   - Ceiling, wall, floor treatment analysis
   - Performance vs. target comparisons

4. HVAC Noise Control Analysis:
   - Equipment-specific requirements
   - Noise control measures

5. Validation and Recommendations:
   - Model validation procedures
   - Material selection recommendations
   - Installation requirements

Example prompt:
"Generate acoustic modeling results for various space types. Include 3D analysis, performance predictions, and material recommendations."
```

### ASTM Test Reports

```markdown
Generate ASTM test reports with the following structure:

1. Test Report Summary:
   - Testing laboratory information
   - Standards and procedures used

2. Test Results by Type:
   - Sound absorption testing (ASTM C423)
   - Sound transmission loss testing (ASTM E90)
   - Impact sound transmission testing (ASTM E492)
   - Reverberation time testing

3. Test Information for Each Specimen:
   - Test date and conditions
   - Equipment and procedures
   - Results with uncertainty analysis
   - Pass/fail status

4. Quality Control:
   - Equipment calibration
   - Test conditions
   - Data analysis procedures

5. Certification:
   - Laboratory accreditation
   - Engineer signatures
   - Quality assurance

Example prompt:
"Generate comprehensive ASTM test reports for acoustic materials and assemblies. Include realistic test data, uncertainty analysis, and proper certification."
```

### RFI Review Documents

```markdown
Generate RFI review documents with the following structure:

1. RFI Summary:
   - Project information and tracking

2. Individual RFI Reviews:
   - Submitted by and date
   - Question and engineering review
   - Response with justification
   - Cost and schedule impact

3. RFI Categories:
   - Material compatibility issues
   - Installation method questions
   - Performance requirement clarifications
   - System integration questions

4. Quality Control:
   - RFI tracking procedures
   - Documentation requirements
   - Follow-up actions

Example prompt:
"Generate RFI review documents for an acoustic design project. Include realistic questions from contractors and detailed engineering responses."
```

### Installation Supervision Reports

```markdown
Generate installation supervision reports with the following structure:

1. Daily Installation Logs:
   - Work completed each day
   - Quality control checks
   - Issues identified and resolved
   - Progress tracking

2. Progress Documentation:
   - Overall project progress
   - Work completed by category
   - Schedule and quality metrics

3. Quality Control:
   - Daily quality control process
   - Quality metrics and targets
   - Issue resolution procedures

4. Documentation:
   - Photographic documentation
   - Performance verification
   - Issue tracking system

Example prompt:
"Generate installation supervision reports for acoustic treatments. Include daily logs, quality control procedures, and progress documentation."
```

## File Organization Guidelines

### Directory Structure:
```
Project_1_Acoustic_Design/
├── email_db/                    # Email correspondence files
├── equipment_spaces_db/         # Equipment sound data and space requirements
├── acoustic_materials_db/       # Material specifications and test data
├── budget/                      # Budget and scope documents
├── deliverables_db/             # Project deliverables and reports
└── sample_data/                 # Additional sample data files
```

### File Naming Conventions:
- Use descriptive, lowercase names with underscores
- Include file type in name (e.g., `_correspondence.txt`, `_sound_data.txt`)
- Group related files with consistent prefixes
- Use `.txt` for text files, `.csv` for data files, `.md` for markdown

### Content Standards:
- All technical data should follow industry standards (ASTM, AHRI, ISO)
- Realistic values based on actual product specifications
- Professional formatting and consistent structure
- Proper documentation and certification requirements
- Quality control and verification procedures

This comprehensive guidance ensures consistent, professional, and technically accurate generation of acoustic engineering project data and documentation.