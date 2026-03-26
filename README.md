#!/usr/bin/env python3
"""
Quick Start: Generate Data + Summary
Run this to create all CSV files and see summary stats.
"""

import sys
import os

# Add scripts directory to path
scripts_dir = os.path.join(os.path.dirname(__file__), 'scripts')
sys.path.insert(0, scripts_dir)

# Import and run the generator
print("\n" + "="*70)
print("  FlavorOps Data Generator - Quick Start")
print("="*70 + "\n")

try:
    exec(open(os.path.join(scripts_dir, 'generate_data.py')).read())
except Exception as e:
    print(f"Error running generator: {e}")
    sys.exit(1)

# Print next steps
print("\n" + "="*70)
print("  NEXT STEPS")
print("="*70)
print("""
1. OPEN POWER BI DESKTOP
   - Launch Power BI Desktop application

2. LOAD CSV FILES
   Option A (Manual):
   - Home → Get Data → Text/CSV
   - Browse to: data/ folder
   - Load each file: flavors → apps → instances → metrics → timeline
   
   Option B (Automated - Python Script):
   - Home → Get Data → Python script
   - Paste content from: scripts/powerbi_python_load.py
   - Modify DATA_PATH to your data folder
   - Execute

3. SETUP DATA MODEL
   - Go to Model view
   - Create relationships:
     * Instances.AppID → Apps.AppID
     * Instances.FlavorName → Flavors.FlavorName
     * Metrics.InstanceID → Instances.InstanceID

4. ADD DAX MEASURES
   - See POWERBI_COMPLETE_GUIDE.md Section 4
   - Create measures like:
     * Count_Critique = CALCULATE(COUNTA(Instances[InstanceID]), ...)
     * Avg_CPU_P95 = AVERAGE(Metrics[CPU_P95])
     * etc.

5. BUILD VISUALIZATIONS
   - See POWERBI_COMPLETE_GUIDE.md Section 6
   - Create 3 pages:
     * Page 1: Vue Globale (Dashboard overview)
     * Page 2: Détail App (Drill-down)
     * Page 3: Instances & Config (Full table)

6. SAVE & PUBLISH
   - File → Save as .pbix
   - Optionally: Publish to Power BI Service

DOCUMENTATION:
  📖 Full guide: POWERBI_COMPLETE_GUIDE.md
  📋 Skill details: .github/skills/powerbi/SKILL.md
  🐍 Python scripts: scripts/
  📊 Generated data: data/

SUPPORT:
  - Check POWERBI_COMPLETE_GUIDE.md Section 11 for troubleshooting
  - All Power Query examples in Section 2
  - All DAX measure codes in Section 4
""")

print("="*70 + "\n")
