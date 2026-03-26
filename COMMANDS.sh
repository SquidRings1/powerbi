#!/bin/bash
# FlavorOps Power BI - Quick Commands
# Run any of these commands directly

# ============================================================================
# 🚀 ONE-CLICK SETUP (Recommended - Run This First!)
# ============================================================================
python scripts/full_setup.py

# ============================================================================
# 📊 Individual Commands
# ============================================================================

# Generate CSV data files
python scripts/generate_data.py

# Create Power BI template
python scripts/create_powerbi_template.py

# Validate setup & create config
python scripts/deployment_manager.py

# ============================================================================
# 🔍 Inspection & Verification
# ============================================================================

# Check if files exist
ls -la FlavorOps_Dashboard_Template.pbix
ls -la data/

# View data
python -c "import pandas as pd; print(pd.read_csv('data/apps.csv'))"

# Check Python packages
python -c "import pandas, numpy; print('All packages OK')"

# ============================================================================
# 📝 Read Documentation (macOS/Linux)
# ============================================================================

# Quick start
cat DEMARRAGE_RAPIDE.md

# Full index
cat INDEX_COMPLET.md

# Project status
cat PROJECT_COMPLETE.txt

# Setup summary
cat FINAL_SETUP_SUMMARY.md

# ============================================================================
# 📂 File Management
# ============================================================================

# Create data directory if missing
mkdir -p data

# List all important files
find . -name "*.md" -o -name "*.py" -o -name "*.pbix" | head -20

# Count lines of documentation
wc -l docs/*.md

# ============================================================================
# 🎯 Next Steps
# ============================================================================

# 1. Run setup
python scripts/full_setup.py

# 2. Open Power BI Desktop
# File → Open → Drag FlavorOps_Dashboard_Template.pbix

# 3. Load CSV files
# Home → Transform Data → New Source → Text/CSV
# Select all 5 CSV files from data/ folder

# 4. Apply
# Close & Apply

# ============================================================================
# 🔧 Troubleshooting
# ============================================================================

# If pandas not found:
pip install pandas numpy

# If Python not in PATH:
which python
# or
which python3

# Verify data generation
python -c "import pandas as pd; print(f'Apps: {len(pd.read_csv(\"data/apps.csv\"))} rows')"

# ============================================================================
# 📚 Additional Resources
# ============================================================================

# View complete guide
# → POWERBI_COMPLETE_GUIDE.md (120 pages)

# View all DAX measures
# → DAX_MEASURES_REFERENCE.md (50+ formulas)

# View Power Query examples
# → POWERQUERY_EXAMPLES.md (M language)

# View troubleshooting
# → TROUBLESHOOTING.md (FAQ & solutions)

# ============================================================================
# 💾 Backup & Maintenance
# ============================================================================

# Backup template
cp FlavorOps_Dashboard_Template.pbix FlavorOps_Dashboard_Template.backup.pbix

# Backup data
cp -r data/ data.backup/

# ============================================================================
# 🚀 Ready to go! Run the first command now:
# python scripts/full_setup.py
# ============================================================================
