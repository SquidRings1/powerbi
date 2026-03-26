---
name: powerbi
description: "Skill for Power BI dashboard development. Use when: building Power BI dashboards, creating DAX measures, writing Power Query transformations, generating dataset CSVs, optimizing performance, or designing data models for analytics."
---

# Power BI Skill

This skill provides templates, scripts, and best practices for building Power BI dashboards with Python data generation and Power Query transformations.

## What's Included

- **Data Generation** (`generate_data.py`): Python script to generate segmented CSV files (apps, instances, flavors, metrics)
- **Power Query Templates**: M language examples for data loading and transformation
- **DAX Measures**: Calculated columns and measures for analytics
- **Dashboard Design**: Layout and visualization patterns
- **Performance Tips**: Optimization for large datasets

## Quick Start

### 1. Generate Data

```bash
python scripts/generate_data.py
```

This creates:
- `data/apps.csv` — Application metadata
- `data/instances.csv` — Instance information  
- `data/flavors.csv` — Flavor specifications
- `data/metrics.csv` — CPU/RAM performance metrics
- `data/timeline.csv` — Historical evolution data

### 2. Load Data into Power BI

**Method A: Direct CSV Import**
- File → Get Data → Text/CSV
- Select each CSV file
- Transform as needed using Power Query Editor

**Method B: Python Script in Power BI**
- Power BI Desktop → Transform Data → Python script
- Paste script from `powerbi_python_load.py`
- Connect directly to CSV folder

### 3. Create Data Model

Import relationships:
- **Apps** ← → **Instances** (on AppID)
- **Instances** ← → **Flavors** (on FlavorName)
- **Metrics** ← → **Instances** (on InstanceID)
- **Timeline** links to **Apps** (on AppID)

### 4. Build Dashboard

Use DAX measures and Power Query to replicate the HTML dashboard:
- KPI cards with status colors
- Donut charts for status distribution
- Line charts for evolution
- Heatmaps for CPU/RAM usage
- Interactive slicers for filtering

## Key Scripts

### generate_data.py
Generates realistic test data based on the FlavorOps HTML dashboard pattern.

**Parameters:**
- `num_months`: Number of historical months (default: 14)
- `random_seed`: Reproducible data generation

**Output:** CSV files in `data/` folder

### powerbi_python_load.py
Python script to run inside Power BI for direct CSV loading.

```python
import pandas as pd
import os

data_path = r"path/to/data"
apps = pd.read_csv(os.path.join(data_path, "apps.csv"))
instances = pd.read_csv(os.path.join(data_path, "instances.csv"))
# etc.
```

## Power Query Recipes

### Load & Clean CSV
```m
let
    Source = Csv.Document(File.Contents("path/to/apps.csv"),[Delimiter=",", Columns=10, Encoding=1252, QuoteStyle=QuoteStyle.None]),
    Promoted = Table.PromoteHeaders(Source),
    TypedTable = Table.TransformColumnTypes(Promoted,{{"AppID", type text}, {"AppName", type text}, ...})
in
    TypedTable
```

### Add Percentile Columns
```m
let
    Source = ...,
    AddP95 = Table.AddColumn(Source, "CPU_P95_Status", each
        if [CPU_P95] > 90 then "CRITIQUE" 
        else if [CPU_P95] > 80 then "SUR-CONSO"
        else if [CPU_P95] > 50 then "OK"
        else "SOUS-CONSO")
in
    AddP95
```

## DAX Measures

### Count by Status
```dax
CountCritique = CALCULATE(COUNTA(Instances[InstanceID]), Instances[Status] = "CRITIQUE")
CountSurConso = CALCULATE(COUNTA(Instances[InstanceID]), Instances[Status] = "SUR-CONSO")
CountOK = CALCULATE(COUNTA(Instances[InstanceID]), Instances[Status] = "OK")
```

### Average Metrics
```dax
AvgCPU_P95 = AVERAGE(Metrics[CPU_P95])
AvgRAM_P95 = AVERAGE(Metrics[RAM_P95])
CorrectionRate = DIVIDE(COUNTA(Instances[InstanceID]), COUNTROWS(Instances))
```

### Dynamic Title
```dax
SelectedApp = IF(HASONEVALUE(Apps[AppName]), VALUES(Apps[AppName]), "All Apps")
```

## Dashboard Pages

1. **Vue Globale** — KPIs, donut chart, evolution line chart, top problems table
2. **Détail App** — Drill-down by application with instance-level metrics
3. **Instances & Config** — Full instance table with filtering by app/flavor
4. **Performance Analysis** — Flavor distribution, CPU/RAM heatmaps

## Performance Optimization

- **Aggregations**: Pre-aggregate monthly data in separate table
- **Query Folding**: Ensure Power Query steps fold back to source when possible
- **Incremental Refresh**: For large production datasets, set up incremental refresh
- **Composite Models**: Use DirectQuery for fact tables, Import for dimensions

## Deployment

1. Save Power BI file as `.pbix`
2. Publish to Power BI Service (optional)
3. Set data refresh schedule
4. Configure Row-Level Security (RLS) for multi-tenant scenarios

## Troubleshooting

**Chart not updating?** → Check slicer interactions in Format pane  
**Slow dashboard?** → Check cardinality of relationships; add aggregations  
**CSV not loading?** → Verify file encoding (UTF-8 recommended); check paths  
**DAX error?** → Use DAX Studio for debugging; check column references
