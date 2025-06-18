import sqlite3
import os
from datetime import datetime
import json
from pathlib import Path
import shutil

class DatabaseMigration:
    def __init__(self, db_path='project_management.db'):
        self.db_path = db_path
        self.migrations_dir = Path('migrations')
        self.migrations_dir.mkdir(exist_ok=True)
        self._init_migrations_table()

    def _init_migrations_table(self):
        """Initialize the migrations tracking table if it doesn't exist."""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        cursor.execute('''
        CREATE TABLE IF NOT EXISTS schema_migrations (
            id INTEGER PRIMARY KEY,
            version TEXT NOT NULL,
            name TEXT NOT NULL,
            applied_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            checksum TEXT NOT NULL,
            status TEXT DEFAULT 'applied'
        )
        ''')
        
        conn.commit()
        conn.close()

    def create_migration(self, name, up_sql, down_sql):
        """Create a new migration file."""
        timestamp = datetime.now().strftime('%Y%m%d%H%M%S')
        version = f"V{timestamp}"
        filename = f"{version}_{name}.sql"
        
        migration_content = {
            'version': version,
            'name': name,
            'up': up_sql,
            'down': down_sql,
            'checksum': self._calculate_checksum(up_sql + down_sql)
        }
        
        migration_path = self.migrations_dir / filename
        with open(migration_path, 'w') as f:
            json.dump(migration_content, f, indent=2)
        
        return version, filename

    def _calculate_checksum(self, content):
        """Calculate a simple checksum for the migration content."""
        return str(hash(content))

    def get_applied_migrations(self):
        """Get list of applied migrations."""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        cursor.execute('''
        SELECT version, name, applied_at, status
        FROM schema_migrations
        ORDER BY id
        ''')
        
        migrations = cursor.fetchall()
        conn.close()
        return migrations

    def get_pending_migrations(self):
        """Get list of pending migrations."""
        applied = {m[0] for m in self.get_applied_migrations()}
        pending = []
        
        for migration_file in sorted(self.migrations_dir.glob('V*.sql')):
            with open(migration_file, 'r') as f:
                migration = json.load(f)
                if migration['version'] not in applied:
                    pending.append(migration)
        
        return pending

    def apply_migration(self, migration):
        """Apply a single migration."""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        try:
            # Execute the migration
            cursor.executescript(migration['up'])
            
            # Record the migration
            cursor.execute('''
            INSERT INTO schema_migrations (version, name, checksum)
            VALUES (?, ?, ?)
            ''', (migration['version'], migration['name'], migration['checksum']))
            
            conn.commit()
            print(f"Applied migration: {migration['version']} - {migration['name']}")
            
        except Exception as e:
            conn.rollback()
            print(f"Error applying migration {migration['version']}: {str(e)}")
            raise
        
        finally:
            conn.close()

    def rollback_migration(self, migration):
        """Rollback a single migration."""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        try:
            # Execute the rollback
            cursor.executescript(migration['down'])
            
            # Remove the migration record
            cursor.execute('''
            DELETE FROM schema_migrations
            WHERE version = ?
            ''', (migration['version'],))
            
            conn.commit()
            print(f"Rolled back migration: {migration['version']} - {migration['name']}")
            
        except Exception as e:
            conn.rollback()
            print(f"Error rolling back migration {migration['version']}: {str(e)}")
            raise
        
        finally:
            conn.close()

    def migrate(self):
        """Apply all pending migrations."""
        pending = self.get_pending_migrations()
        
        if not pending:
            print("No pending migrations.")
            return
        
        print(f"Applying {len(pending)} pending migrations...")
        
        for migration in pending:
            self.apply_migration(migration)
        
        print("All migrations completed successfully.")

    def rollback(self, steps=1):
        """Rollback the last N migrations."""
        applied = self.get_applied_migrations()
        
        if not applied:
            print("No migrations to rollback.")
            return
        
        to_rollback = applied[-steps:]
        print(f"Rolling back {len(to_rollback)} migrations...")
        
        for version, name, _, _ in reversed(to_rollback):
            migration_file = next(self.migrations_dir.glob(f"{version}_*.sql"))
            with open(migration_file, 'r') as f:
                migration = json.load(f)
                self.rollback_migration(migration)
        
        print("Rollback completed successfully.")

    def reset_database(self):
        """Completely reset the database by removing it and recreating it."""
        print(f"Resetting database: {self.db_path}")
        
        # Close any existing connections
        try:
            conn = sqlite3.connect(self.db_path)
            conn.close()
        except:
            pass
        
        # Remove the database file
        if os.path.exists(self.db_path):
            os.remove(self.db_path)
            print("Removed existing database file.")
        
        # Recreate the database with initial schema
        self._init_migrations_table()
        print("Created fresh database with initial schema.")

    def refresh_database(self):
        """Refresh the database by resetting it and reapplying all migrations."""
        print("Refreshing database...")
        
        # Get all migrations before reset
        all_migrations = []
        for migration_file in sorted(self.migrations_dir.glob('V*.sql')):
            with open(migration_file, 'r') as f:
                all_migrations.append(json.load(f))
        
        # Reset the database
        self.reset_database()
        
        # Apply all migrations
        if all_migrations:
            print(f"Applying {len(all_migrations)} migrations...")
            for migration in all_migrations:
                self.apply_migration(migration)
            print("All migrations applied successfully.")
        else:
            print("No migrations to apply.")

def main():
    # Example usage
    migrator = DatabaseMigration()
    
    # Create a new migration
    up_sql = '''
    -- Add new column to projects table
    ALTER TABLE projects ADD COLUMN priority TEXT DEFAULT 'medium';
    '''
    
    down_sql = '''
    -- Remove the priority column
    CREATE TABLE projects_backup AS SELECT project_id, project_name, client_name, 
        start_date, end_date, status, percent_complete, created_at FROM projects;
    DROP TABLE projects;
    ALTER TABLE projects_backup RENAME TO projects;
    '''
    
    version, filename = migrator.create_migration(
        'add_priority_to_projects',
        up_sql,
        down_sql
    )
    print(f"Created migration: {filename}")
    
    # Apply pending migrations
    migrator.migrate()
    
    # Show migration status
    print("\nApplied migrations:")
    for version, name, applied_at, status in migrator.get_applied_migrations():
        print(f"{version} - {name} ({applied_at}) - {status}")

if __name__ == "__main__":
    main() 