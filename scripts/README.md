# Scripts

Utility scripts for project maintenance, building, and automation.

## Available Scripts

### Development
- `setup.sh` - Initial project setup
- `test.sh` - Run all tests
- `lint.sh` - Code linting and formatting
- `build.sh` - Build all components

### Maintenance
- `update-deps.sh` - Update dependencies
- `check-links.sh` - Validate documentation links
- `generate-docs.sh` - Auto-generate documentation

### CI/CD
- `ci-test.sh` - Continuous integration testing
- `release.sh` - Prepare releases
- `deploy.sh` - Deployment automation

## Usage

Make scripts executable:
```bash
chmod +x scripts/*.sh
```

Run a script:
```bash
./scripts/setup.sh
```

## Contributing Scripts

When adding new scripts:
- Include clear documentation
- Add error handling
- Make them idempotent when possible
- Follow shell scripting best practices
- Test on multiple platforms if applicable