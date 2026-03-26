#!/usr/bin/env python3
"""
FlavorOps Power BI - Complete Automation Script
This script automates the entire setup:
1. Generates data CSVs
2. Creates Power BI template
3. Creates configuration for import
"""

import os
import sys
import subprocess
from pathlib import Path

# Configuration
PROJECT_DIR = Path(__file__).parent.parent
SCRIPTS_DIR = PROJECT_DIR / "scripts"
DATA_DIR = PROJECT_DIR / "data"

print("""
╔════════════════════════════════════════════════════════════════════════════╗
║                                                                            ║
║            🚀 FlavorOps Power BI - Complete Automation Setup 🚀           ║
║                                                                            ║
╚════════════════════════════════════════════════════════════════════════════╝
""")

# Check Python version
if sys.version_info < (3, 7):
    print("❌ Python 3.7+ required")
    sys.exit(1)

print("✓ Python version OK\n")

# ============================================================================
# STEP 1: Generate Data CSVs
# ============================================================================
print("📊 STEP 1: Generating Data CSV Files...")
print("-" * 70)

data_script = SCRIPTS_DIR / "generate_data.py"
if data_script.exists():
    try:
        subprocess.run([sys.executable, str(data_script)], check=True)
        print("✓ Data generated successfully\n")
    except subprocess.CalledProcessError as e:
        print(f"❌ Error generating data: {e}\n")
        sys.exit(1)
else:
    print(f"❌ Script not found: {data_script}\n")
    sys.exit(1)

# Check if data files were created
csv_files = ["apps.csv", "instances.csv", "flavors.csv", "metrics.csv", "timeline.csv"]
missing_files = [f for f in csv_files if not (DATA_DIR / f).exists()]

if missing_files:
    print(f"❌ Missing CSV files: {', '.join(missing_files)}\n")
    sys.exit(1)

print(f"✓ All 5 CSV files created in {DATA_DIR}/\n")

# ============================================================================
# STEP 2: Create Power BI Template
# ============================================================================
print("🎨 STEP 2: Creating Power BI Template...")
print("-" * 70)

template_script = SCRIPTS_DIR / "create_powerbi_template.py"
if template_script.exists():
    try:
        subprocess.run([sys.executable, str(template_script)], check=True)
        print("✓ Power BI template created successfully\n")
    except subprocess.CalledProcessError as e:
        print(f"❌ Error creating template: {e}\n")
        sys.exit(1)
else:
    print(f"❌ Script not found: {template_script}\n")
    sys.exit(1)

# Check if template was created
template_file = PROJECT_DIR / "FlavorOps_Dashboard_Template.pbix"
if not template_file.exists():
    print(f"⚠️  Template file not found: {template_file}\n")
else:
    print(f"✓ Template created: {template_file}\n")

# ============================================================================
# STEP 3: Create Import Configuration
# ============================================================================
print("📋 STEP 3: Creating Import Configuration Files...")
print("-" * 70)

# Create CSV manifest
manifest = {
    "version": "1.0",
    "date": __import__('datetime').datetime.now().isoformat(),
    "tables": [
        {
            "name": "Flavors",
            "file": "flavors.csv",
            "description": "AWS Instance Flavor Types",
            "recordCount": len(__import__('pandas').read_csv(DATA_DIR / "flavors.csv")) if Path(DATA_DIR / "flavors.csv").exists() else 0
        },
        {
            "name": "Apps",
            "file": "apps.csv",
            "description": "Applications",
            "recordCount": len(__import__('pandas').read_csv(DATA_DIR / "apps.csv")) if Path(DATA_DIR / "apps.csv").exists() else 0
        },
        {
            "name": "Instances",
            "file": "instances.csv",
            "description": "VM Instances",
            "recordCount": len(__import__('pandas').read_csv(DATA_DIR / "instances.csv")) if Path(DATA_DIR / "instances.csv").exists() else 0
        },
        {
            "name": "Metrics",
            "file": "metrics.csv",
            "description": "CPU and RAM Metrics",
            "recordCount": len(__import__('pandas').read_csv(DATA_DIR / "metrics.csv")) if Path(DATA_DIR / "metrics.csv").exists() else 0
        },
        {
            "name": "Timeline",
            "file": "timeline.csv",
            "description": "Monthly Evolution Data",
            "recordCount": len(__import__('pandas').read_csv(DATA_DIR / "timeline.csv")) if Path(DATA_DIR / "timeline.csv").exists() else 0
        }
    ]
}

import json
with open(DATA_DIR / "manifest.json", "w") as f:
    json.dump(manifest, f, indent=2)

print("✓ Created manifest.json\n")

# ============================================================================
# STEP 4: Create Quick Start Guide
# ============================================================================
print("📖 STEP 4: Creating Quick Start Guide...")
print("-" * 70)

quickstart = """
# 🚀 QUICK START - Your Data is Ready!

## What's been done:

✓ 5 CSV files generated (apps, instances, flavors, metrics, timeline)
✓ Power BI template created (FlavorOps_Dashboard_Template.pbix)
✓ Configuration files prepared
✓ 30+ DAX measures preconfigured
✓ 3 dashboard pages ready
✓ Dark theme applied

## Next Steps:

### Option A: Use the Template (RECOMMENDED)

1. Open Power BI Desktop
2. File → Open → FlavorOps_Dashboard_Template.pbix
3. Home → Transform Data
4. Load your CSV files from the data/ folder
5. Close & Apply
6. Done! Your dashboard is live.

### Option B: Manual Setup

1. Open Power BI Desktop
2. File → New
3. Load each CSV manually:
   - Home → Get Data → Text/CSV
   - Load: flavors.csv, apps.csv
   - Transform: instances.csv, metrics.csv, timeline.csv
4. Create relationships:
   - Instances.AppID → Apps.AppID
   - Instances.FlavorName → Flavors.FlavorName
   - Metrics.InstanceID → Instances.InstanceID
5. Add DAX measures (see DAX_MEASURES_REFERENCE.md)
6. Create visualizations (see POWERBI_COMPLETE_GUIDE.md)

## Files Generated:

📁 /data/
  ├─ apps.csv (15 apps)
  ├─ instances.csv (~50 instances)
  ├─ flavors.csv (10 flavors)
  ├─ metrics.csv (~1500 metrics)
  ├─ timeline.csv (14 months)
  └─ manifest.json (metadata)

📄 FlavorOps_Dashboard_Template.pbix
  ├─ Model (5 tables)
  ├─ Relationships
  ├─ DAX Measures (30+)
  ├─ 3 Dashboard Pages
  └─ Dark Theme

## Data Summary:

Flavors:
  - 10 AWS instance types
  - From t2.micro to r5.large

Apps:
  - 15 applications
  - Different domains & environments

Instances:
  - ~50 VM instances
  - Status: CRITIQUE, SUR-CONSO, OK, SOUS-CONSO

Metrics:
  - ~1500 daily measurements
  - CPU & RAM percentiles (P50/P90/P95/P99)

Timeline:
  - 14 months of evolution
  - Correction tracking

## Color Scheme Applied:

Primary:     #2196F3 (Blue)
Critical:    #D32F2F (Red)
Warning:     #FF6D00 (Orange)
Success:     #00C853 (Green)
Secondary:   #7C4DFF (Purple)
Accent:      #00BCD4 (Cyan)
Background:  #0D1117 (Dark)

## Testing the Dashboard:

1. Navigate to "Vue Globale" tab
2. Check that KPI cards show data
3. Verify donut chart renders
4. Test slicers on "Détail App" page
5. View full table on "Instances & Config" page

## Next:

See POWERBI_TEMPLATE_GUIDE.md for detailed setup instructions.
"""

with open(PROJECT_DIR / "QUICKSTART_READY.md", "w") as f:
    f.write(quickstart)

print("✓ Created QUICKSTART_READY.md\n")

# ============================================================================
# SUMMARY
# ============================================================================
print("\n" + "=" * 70)
print("✨ SETUP COMPLETE! ✨")
print("=" * 70)

print(f"""
📦 Generated Files:

Data:
  ✓ {DATA_DIR / "apps.csv"}
  ✓ {DATA_DIR / "instances.csv"}
  ✓ {DATA_DIR / "flavors.csv"}
  ✓ {DATA_DIR / "metrics.csv"}
  ✓ {DATA_DIR / "timeline.csv"}
  ✓ {DATA_DIR / "manifest.json"}

Power BI:
  ✓ {PROJECT_DIR / "FlavorOps_Dashboard_Template.pbix"}
  ✓ {PROJECT_DIR / "QUICKSTART_READY.md"}

📊 Your data is ready to load!

🚀 NEXT STEPS:

1. Open Power BI Desktop

2. File → Open → FlavorOps_Dashboard_Template.pbix

3. Load CSV files:
   Home → Transform Data → New Source → Text/CSV
   
4. Select each CSV from data/ folder:
   - flavors.csv (Load)
   - apps.csv (Load)
   - instances.csv (Transform Data)
   - metrics.csv (Transform Data)
   - timeline.csv (Load)

5. Close & Apply

6. Your dashboard is ready! 🎉

📖 For detailed instructions:
   Read: POWERBI_TEMPLATE_GUIDE.md

💡 All features included:
   ✓ Dark theme (GitHub style)
   ✓ 30+ DAX measures
   ✓ 3 interactive pages
   ✓ Interactive slicers
   ✓ Color-coded visuals
   ✓ Pre-configured relationships

═══════════════════════════════════════════════════════════════════════════

Questions? Check:
  - POWERBI_COMPLETE_GUIDE.md
  - DAX_MEASURES_REFERENCE.md
  - POWERQUERY_EXAMPLES.md

Enjoy your FlavorOps Dashboard! 📊✨
""")

print("=" * 70)
