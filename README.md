# Project Management Database

This project implements a SQLite database for managing acoustic design projects, including test results, budgets, materials, equipment, and project communications.

## Project Structure

The database includes the following main components:

1. **Projects Table**: Core project information including name, client, dates, and status
2. **ASTM Tests**: Test results and raw data
3. **Budget**: Project financial information
4. **Acoustic Materials**: Material specifications with NRC and STC ratings
5. **Equipment Spaces**: Room specifications and NC requirements
6. **Equipment**: Mechanical equipment with sound power data
7. **Email Correspondence**: Project communications
8. **Deliverables**: Project deliverables and their status
9. **Milestones**: Project milestones and their status

## File Structure

For the first project (Project_1_Acoustic_Design), the following folder structure is created:

```
Project_1_Acoustic_Design/
├── astm_tests_db/
├── budget/
├── acoustic_materials_db/
├── equipment_spaces_db/
├── email_db/
└── deliverables_db/
```

## Setup and Usage

1. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

2. Create the database and generate sample data:
   ```bash
   python create_project_database.py
   python generate_sample_data.py
   ```

3. The database will be created as `project_management.db` in the current directory.

## Database Migrations

The project includes a migration system to manage database schema changes. This allows for:
- Version-controlled schema changes
- Rollback capabilities
- Migration history tracking
- Safe schema evolution
- Quick database reset and refresh

### Using Migrations

1. Create a new migration:
   ```python
   from database_migrations import DatabaseMigration
   
   migrator = DatabaseMigration()
   
   # Define your schema changes
   up_sql = '''
   -- Your schema changes here
   ALTER TABLE table_name ADD COLUMN new_column TEXT;
   '''
   
   down_sql = '''
   -- How to undo the changes
   ALTER TABLE table_name DROP COLUMN new_column;
   '''
   
   # Create the migration file
   version, filename = migrator.create_migration('migration_name', up_sql, down_sql)
   ```

2. Apply pending migrations:
   ```python
   migrator.migrate()
   ```

3. Rollback migrations:
   ```python
   # Rollback the last migration
   migrator.rollback()
   
   # Rollback multiple migrations
   migrator.rollback(steps=3)
   ```

4. Check migration status:
   ```python
   # List applied migrations
   for version, name, applied_at, status in migrator.get_applied_migrations():
       print(f"{version} - {name} ({applied_at}) - {status}")
   ```

5. Reset or refresh the database:
   ```python
   # Completely reset the database (removes all data and schema)
   migrator.reset_database()
   
   # Refresh the database (resets and reapplies all migrations)
   migrator.refresh_database()
   ```

### Migration Files

Migrations are stored in the `migrations/` directory as JSON files with the following structure:
```json
{
  "version": "V20240315123456",
  "name": "migration_name",
  "up": "SQL to apply changes",
  "down": "SQL to undo changes",
  "checksum": "hash_of_migration_content"
}
```

### Database Reset and Refresh

The migration system provides two powerful commands for managing your database:

1. **Reset Database** (`reset_database()`):
   - Completely removes the existing database file
   - Creates a fresh database with only the initial schema
   - Useful when you want to start from scratch
   - All data and schema changes are removed

2. **Refresh Database** (`refresh_database()`):
   - Resets the database to a clean state
   - Automatically reapplies all migrations in order
   - Maintains your schema evolution history
   - Useful when you want to test your migrations
   - Perfect for development and testing environments

## Sample Data

The database includes:
- 5 sample projects
- Realistic acoustic material data with NRC values
- Equipment specifications with octave-band sound power levels
- Email correspondence spanning the project timeline
- Milestones and deliverables with realistic dates

## Database Schema

Each table includes appropriate foreign key relationships to the projects table, ensuring data integrity and proper relationships between different aspects of each project.

## Notes

- The first project includes actual files in the folder structure
- The remaining projects are stored in the database only
- All dates are within the 2024-2025 timeframe
- Acoustic data follows ASTM standards for isolation performance 