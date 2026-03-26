#!/usr/bin/env python3
"""
Quick Reference - FlavorOps Power BI Project
"""

print("""
═══════════════════════════════════════════════════════════════════════════════
                    FLAVOROPS POWER BI - QUICK REFERENCE
═══════════════════════════════════════════════════════════════════════════════

📁 PROJECT STRUCTURE:
├── .github/skills/powerbi/SKILL.md          [Skill definition]
├── scripts/
│   ├── generate_data.py                     [Generate CSV data]
│   └── powerbi_python_load.py               [Python script for Power BI]
├── data/                                    [Generated CSV files]
│   ├── apps.csv                             [15 applications]
│   ├── instances.csv                        [~50 VM instances]
│   ├── flavors.csv                          [10 AWS flavor types]
│   ├── metrics.csv                          [CPU/RAM metrics]
│   └── timeline.csv                         [Monthly evolution]
├── README.md                                [Quick start guide]
├── POWERBI_COMPLETE_GUIDE.md                [Full documentation]
├── POWERQUERY_EXAMPLES.md                   [M language examples]
├── DAX_MEASURES_REFERENCE.md                [DAX formulas]
└── FlavorOps_Dashboard_Preview.html         [HTML reference]

═══════════════════════════════════════════════════════════════════════════════

⚡ QUICK START (5 MINUTES):

1️⃣  Generate Data
    $ cd /Users/haris/Documents/PROJECTS/powerbi
    $ python scripts/generate_data.py
    ✓ Creates 5 CSV files in data/ folder

2️⃣  Open Power BI Desktop
    Launch Power BI → File → New

3️⃣  Load CSVs
    Home → Get Data → Text/CSV
    Select: flavors.csv → Load
    Repeat for: apps.csv, instances.csv, metrics.csv, timeline.csv

4️⃣  Create Data Model
    Model view → Add relationships:
    • Instances.AppID → Apps.AppID
    • Instances.FlavorName → Flavors.FlavorName
    • Metrics.InstanceID → Instances.InstanceID

5️⃣  Add Measures
    See DAX_MEASURES_REFERENCE.md for all 30+ measures

6️⃣  Build Dashboard
    See POWERBI_COMPLETE_GUIDE.md Section 6 for layouts

═══════════════════════════════════════════════════════════════════════════════

📊 DASHBOARD PAGES (HTML → Power BI):

PAGE 1: Vue Globale (Global Overview)
├── KPI Cards: Total Apps, Critiques, Sur-Conso, OK
├── Donut Chart: Status distribution (4 categories)
├── Line Chart: Evolution - Apps Corrigées (14 months)
└── Table: Top 8 problematic apps

PAGE 2: Détail App (Application Deep-Dive)
├── Slicers: App, Status, Percentile (p50/p90/p95/p99)
├── KPI Cards: Instance count, CPU avg, RAM avg
├── Bar Chart: Top 15 instances (CPU+RAM dual axis)
└── Table: Instance details with recommendations

PAGE 3: Instances & Config (Full Configuration)
├── Dropdowns: Filter by App, Filter by Flavor
├── Bar Charts: CPU p95 & RAM p95 distribution by flavor
└── Table: Full instance config (cost, savings, etc.)

═══════════════════════════════════════════════════════════════════════════════

🎨 DATA MODEL:

┌─ Flavors (Lookup)
│  ├── FlavorID (key)
│  ├── FlavorName (t2.micro, m5.large, etc.)
│  ├── CPU_vCPU
│  ├── RAM_GB
│  └── Cost_Monthly
│
├─ Apps (Lookup)
│  ├── AppID (key)
│  ├── AppName
│  ├── Domain (Finance, Security, etc.)
│  └── Environment (Production, Staging)
│
├─ Instances (Dimension)
│  ├── InstanceID (key)
│  ├── AppID → Apps.AppID (FK)
│  ├── FlavorName → Flavors.FlavorName (FK)
│  ├── Status (CRITIQUE, SUR-CONSO, OK, SOUS-CONSO)
│  ├── Corrected (Y/N)
│  └── RecFlavorName
│
├─ Metrics (Fact table - large)
│  ├── MetricID
│  ├── InstanceID → Instances.InstanceID (FK)
│  ├── MeasureDate
│  ├── CPU_P50, CPU_P90, CPU_P95, CPU_P99
│  └── RAM_P50, RAM_P90, RAM_P95, RAM_P99
│
└─ Timeline (Time dimension)
   ├── TimelineID
   ├── Month
   ├── SnapshotDate
   ├── TotalInstances
   ├── CriticalCount, OverConsumptionCount, OKCount, UnderConsumptionCount
   ├── CorrectedCount
   └── CorrectionPct

═══════════════════════════════════════════════════════════════════════════════

📐 KEY MEASURES (30+ Total):

COUNT MEASURES:
  • Count_Critique, Count_SurConso, Count_OK, Count_SousConso, Count_Total
  • Count_Corrected, Count_NeedingCorrection

AVERAGE MEASURES:
  • Avg_CPU_P50/P90/P95/P99
  • Avg_RAM_P50/P90/P95/P99

RATE & RATIO:
  • Correction_Rate (0-1)
  • Correction_Rate_Pct (formatted %)
  • Pct_Critique, Pct_SurConso, Pct_OK, Pct_SousConso

COST:
  • Total_Current_Cost
  • Total_Potential_Savings
  • Savings_Percentage

DYNAMIC:
  • Selected_App, Overall_Status, Dashboard_Title
  • AppHealthScore_Pct

See DAX_MEASURES_REFERENCE.md for all 50+ formulas with examples.

═══════════════════════════════════════════════════════════════════════════════

🔧 POWER QUERY TRANSFORMATIONS:

1. Load CSV (5 files)
2. Auto-detect headers & types
3. Add calculated columns:
   - StatusPriority (for sorting)
   - CorrectionNeeded (boolean flag)
   - YearMonth (for grouping)
   - CPU_Status, RAM_Status (classification)
   - Overall_Status (worst of CPU/RAM)

See POWERQUERY_EXAMPLES.md for complete M code.

═══════════════════════════════════════════════════════════════════════════════

📝 FILE DOCUMENTATION:

POWERBI_COMPLETE_GUIDE.md (Primary Reference)
├── 1. Data Preparation (CSV generation)
├── 2. Power Query Section (M language transformations)
├── 3. Data Model Section (relationships)
├── 4. DAX Measures (30+ formulas)
├── 5. Calculated Columns
├── 6. Dashboard Pages (3 pages, detailed layouts)
├── 7. Color Scheme (dark theme)
├── 8. Interactions (slicers, drill-through)
├── 9. Performance Tips (aggregations, query folding)
├── 10. Distribution (publish to Service)
├── 11. RLS Configuration
└── 12. Troubleshooting

POWERQUERY_EXAMPLES.md (M Language Reference)
├── Full Power Query code for each table
├── Advanced patterns (query folding, error handling)
├── Tips & tricks
└── Common errors & fixes

DAX_MEASURES_REFERENCE.md (DAX Formula Library)
├── Count measures (status, applications, corrections)
├── Percentage & rate measures
├── Aggregation measures (cpu, ram, min/max)
├── Dynamic & context-aware measures
├── Time-series measures
├── Cost & savings measures
├── Calculated columns
├── Number formatting
├── Common DAX patterns
└── Performance tips

═══════════════════════════════════════════════════════════════════════════════

🚀 STEP-BY-STEP WORKFLOW:

PHASE 1: DATA GENERATION (5 min)
  1. Open Terminal
  2. python scripts/generate_data.py
  3. Verify data/ folder has 5 CSVs

PHASE 2: POWER BI SETUP (10 min)
  1. Open Power BI Desktop
  2. File → New
  3. Get Data → Text/CSV → Load all 5 files
  4. Go to Model view
  5. Create 3 relationships (Apps, Flavors→InstanceID)

PHASE 3: DAX & CALCULATIONS (15 min)
  1. Create 30+ measures (copy from DAX_MEASURES_REFERENCE.md)
  2. Test each measure in a sample visual
  3. Create calculated columns in Power Query

PHASE 4: VISUALIZATIONS (20 min)
  1. Create Vista Globale page (KPIs + charts + table)
  2. Create Détail App page (slicers + details)
  3. Create Instances page (configs + distribution)
  4. Format with theme colors
  5. Set up interactions

PHASE 5: TESTING (10 min)
  1. Test slicers on each page
  2. Verify drill-through functionality
  3. Check measure calculations
  4. Test performance (refresh time)

PHASE 6: PUBLISH (5 min)
  1. Save as .pbix
  2. File → Publish (if Power BI Service available)
  3. Configure refresh schedule

═══════════════════════════════════════════════════════════════════════════════

💡 TIPS & TRICKS:

✓ Use variables in complex DAX:
  MyMeasure = VAR Count = [Count_Critique] RETURN COUNT * 2

✓ Test with slicer to debug:
  Add measure to card, add slicer, test with/without filter

✓ Copy whole Power Query blocks from POWERQUERY_EXAMPLES.md

✓ Use Table.Profile in Power Query to check data quality

✓ Enable Query Performance Analyzer:
  Home → Transform Data → Tools → Query Diagnostics

✓ Save .pbix as backup before major changes

═══════════════════════════════════════════════════════════════════════════════

❓ TROUBLESHOOTING:

Q: CSV not loading?
A: Check path, encoding (UTF-8), delimiter (comma), file permissions

Q: Relationship not working?
A: Verify column names match EXACTLY (case-sensitive), check data types

Q: Measure shows error?
A: Use DAX Studio to debug, check filter context

Q: Dashboard slow?
A: Profile with Analyze in Excel, reduce Metrics rows, add aggregation

Q: Slicer not filtering?
A: Check Format → Interactions tab, ensure relationship is set to Active

═══════════════════════════════════════════════════════════════════════════════

📞 SUPPORT RESOURCES:

Power BI Documentation:
  https://docs.microsoft.com/en-us/power-bi/

DAX Language Reference:
  https://dax.guide/

Power Query M Reference:
  https://docs.microsoft.com/en-us/powerquery-m/

Power BI Community:
  https://community.powerbi.com/

═══════════════════════════════════════════════════════════════════════════════

✨ NEXT STEPS:

1. Run: python scripts/generate_data.py
2. Read: POWERBI_COMPLETE_GUIDE.md (Section 1-3)
3. Open: Power BI Desktop
4. Load: All 5 CSV files
5. Build: Data model (relationships)
6. Copy: DAX measures from DAX_MEASURES_REFERENCE.md
7. Create: Visualizations per POWERBI_COMPLETE_GUIDE.md Section 6
8. Test: Each page and slicer
9. Save: As .pbix file
10. Enjoy: Your FlavorOps Dashboard! 🎉

═══════════════════════════════════════════════════════════════════════════════
""")
