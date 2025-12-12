# Utility Scripts

This directory contains utility and test scripts for MectoFitness CRM.

## Database Management

### `init_db.py`
Initialize the database with tables and schema.

```bash
python scripts/init_db.py
```

### `diagnose_db.py`
Diagnose database connection and configuration issues.

```bash
python scripts/diagnose_db.py
```

### `migrate_organizations.py`
Migrate data to organization-based structure.

```bash
python scripts/migrate_organizations.py
```

### `run_migration.py`
Run database migrations.

```bash
python scripts/run_migration.py
```

## Data Seeding

### `seed_exercises.py`
Seed the database with exercise library data.

```bash
python scripts/seed_exercises.py
```

### `check_exercises.py`
Verify exercise library data integrity.

```bash
python scripts/check_exercises.py
```

## Role-Based Access Control (RBAC)

### `add_rbac_columns.py`
Add RBAC columns to existing database tables.

```bash
python scripts/add_rbac_columns.py
```

### `deploy_rbac.py`
Deploy RBAC system configuration.

```bash
python scripts/deploy_rbac.py
```

## Testing

### `test_api_endpoints.py`
Test API endpoints functionality.

```bash
python scripts/test_api_endpoints.py
```

### `test_db.py`
Test database connectivity and operations.

```bash
python scripts/test_db.py
```

### `test_homepage_access.py`
Test homepage access and routing.

```bash
python scripts/test_homepage_access.py
```

### `test_rbac_and_routes.py`
Test RBAC permissions and route access.

```bash
python scripts/test_rbac_and_routes.py
```

### `test_session_management.py`
Test session management functionality.

```bash
python scripts/test_session_management.py
```

### `test_user_crud.py`
Test user CRUD operations.

```bash
python scripts/test_user_crud.py
```

## Verification

### `verify_setup.py`
Verify application setup and configuration.

```bash
python scripts/verify_setup.py
```

### `verify-homepage.py`
Verify homepage build and deployment.

```bash
python scripts/verify-homepage.py
```

## Notes

- All scripts should be run from the project root directory
- Ensure your virtual environment is activated before running scripts
- Configure environment variables in `.env` before running setup scripts
- Some scripts require an active database connection

## Adding New Scripts

When adding new utility scripts:
1. Place them in this directory
2. Add a descriptive docstring at the top of the file
3. Update this README with usage instructions
4. Use the project's logging conventions
5. Handle errors gracefully with helpful messages
