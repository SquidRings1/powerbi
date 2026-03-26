# Power Query (M Language) - Complete Examples

## Overview

Power Query uses the **M language** to transform data during import. Apply these transformations in Power BI:
1. Get Data → Text/CSV → Edit
2. Paste M code into Advanced Editor
3. Apply transformations

---

## 1. Flavors Table - Simple Load

```m
let
    Source = Csv.Document(File.Contents("C:\data\flavors.csv"),[Delimiter=",", Columns=5]),
    Promoted = Table.PromoteHeaders(Source, [PromoteAllScalars=true]),
    TypedTable = Table.TransformColumnTypes(Promoted,{
        {"FlavorID", type text},
        {"FlavorName", type text},
        {"CPU_vCPU", Int64.Type},
        {"RAM_GB", Int64.Type},
        {"Cost_Monthly", type number}
    })
in
    TypedTable
```

---

## 2. Apps Table - Lookup Reference

```m
let
    Source = Csv.Document(File.Contents("C:\data\apps.csv"),[Delimiter=",", Columns=4]),
    Promoted = Table.PromoteHeaders(Source, [PromoteAllScalars=true]),
    TypedTable = Table.TransformColumnTypes(Promoted,{
        {"AppID", type text},
        {"AppName", type text},
        {"Domain", type text},
        {"Environment", type text}
    })
in
    TypedTable
```

---

## 3. Instances Table - With Calculated Columns

```m
let
    Source = Csv.Document(File.Contents("C:\data\instances.csv"),[Delimiter=","]),
    Promoted = Table.PromoteHeaders(Source, [PromoteAllScalars=true]),
    
    // Initial type conversion
    TypedTable = Table.TransformColumnTypes(Promoted,{
        {"InstanceID", type text},
        {"AppID", type text},
        {"AppName", type text},
        {"Domain", type text},
        {"FlavorName", type text},
        {"CPU_vCPU", Int64.Type},
        {"RAM_GB", Int64.Type},
        {"RecFlavorName", type text},
        {"Status", type text},
        {"Corrected", type logical},
        {"CreatedDate", type date}
    }),
    
    // Add Status Priority (for sorting)
    AddStatusPriority = Table.AddColumn(TypedTable, "StatusPriority", each
        if [Status] = "CRITIQUE" then 1
        else if [Status] = "SUR-CONSO" then 2
        else if [Status] = "OK" then 3
        else 4,  // SOUS-CONSO
    type number),
    
    // Add Correction Needed flag
    AddCorrectionNeeded = Table.AddColumn(AddStatusPriority, "CorrectionNeeded", each
        [Status] = "CRITIQUE" or [Status] = "SUR-CONSO",
    type logical),
    
    // Add Has Different Flavor Recommendation
    AddDifferentFlavor = Table.AddColumn(AddCorrectionNeeded, "HasDifferentFlavor", each
        [FlavorName] <> [RecFlavorName],
    type logical),
    
    // Remove unnecessary columns (optional)
    // FinalTable = Table.SelectColumns(AddDifferentFlavor, {"InstanceID", "AppID", "AppName", "Domain", "FlavorName", "CPU_vCPU", "RAM_GB", "Status", "Corrected", "CreatedDate"})
    
    FinalTable = AddDifferentFlavor
in
    FinalTable
```

---

## 4. Metrics Table - With Date & Aggregation Keys

```m
let
    Source = Csv.Document(File.Contents("C:\data\metrics.csv"),[Delimiter=","]),
    Promoted = Table.PromoteHeaders(Source, [PromoteAllScalars=true]),
    
    TypedTable = Table.TransformColumnTypes(Promoted,{
        {"MetricID", type text},
        {"InstanceID", type text},
        {"AppID", type text},
        {"MeasureDate", type date},
        {"CPU_Avg", type number},
        {"CPU_P50", type number},
        {"CPU_P90", type number},
        {"CPU_P95", type number},
        {"CPU_P99", type number},
        {"RAM_Avg", type number},
        {"RAM_P50", type number},
        {"RAM_P90", type number},
        {"RAM_P95", type number},
        {"RAM_P99", type number}
    }),
    
    // Add Year-Month for grouping
    AddYearMonth = Table.AddColumn(TypedTable, "YearMonth", each 
        Date.ToText([MeasureDate], "yyyy-MM"), type text),
    
    // Add Year for time series
    AddYear = Table.AddColumn(AddYearMonth, "Year", each 
        Date.Year([MeasureDate]), type number),
    
    // Add Month number
    AddMonth = Table.AddColumn(AddYear, "Month", each 
        Date.Month([MeasureDate]), type number),
    
    // Add Day of Week (0=Sunday, 6=Saturday)
    AddDayOfWeek = Table.AddColumn(AddMonth, "DayOfWeek", each 
        Date.DayOfWeek([MeasureDate]), type number),
    
    // Add CPU Status classification
    AddCPUStatus = Table.AddColumn(AddDayOfWeek, "CPU_Status", each
        if [CPU_P95] > 90 then "CRITIQUE"
        else if [CPU_P95] > 80 then "SUR-CONSO"
        else if [CPU_P95] > 50 then "OK"
        else "SOUS-CONSO",
    type text),
    
    // Add RAM Status classification
    AddRAMStatus = Table.AddColumn(AddCPUStatus, "RAM_Status", each
        if [RAM_P95] > 90 then "CRITIQUE"
        else if [RAM_P95] > 80 then "SUR-CONSO"
        else if [RAM_P95] > 50 then "OK"
        else "SOUS-CONSO",
    type text),
    
    // Add Overall Status (most severe)
    AddOverallStatus = Table.AddColumn(AddRAMStatus, "Overall_Status", each
        if [CPU_P95] > 90 or [RAM_P95] > 90 then "CRITIQUE"
        else if [CPU_P95] > 80 or [RAM_P95] > 80 then "SUR-CONSO"
        else if [CPU_Avg] < 10 and [RAM_Avg] < 15 then "SOUS-CONSO"
        else "OK",
    type text)
in
    AddOverallStatus
```

---

## 5. Timeline Table - Monthly Aggregation

```m
let
    Source = Csv.Document(File.Contents("C:\data\timeline.csv"),[Delimiter=","]),
    Promoted = Table.PromoteHeaders(Source, [PromoteAllScalars=true]),
    
    TypedTable = Table.TransformColumnTypes(Promoted,{
        {"TimelineID", type text},
        {"Month", type text},
        {"SnapshotDate", type date},
        {"TotalApps", Int64.Type},
        {"TotalInstances", Int64.Type},
        {"CriticalCount", Int64.Type},
        {"OverConsumptionCount", Int64.Type},
        {"OKCount", Int64.Type},
        {"UnderConsumptionCount", Int64.Type},
        {"CorrectedCount", Int64.Type},
        {"CorrectionPct", type number}
    }),
    
    // Add Year from SnapshotDate
    AddYear = Table.AddColumn(TypedTable, "Year", each 
        Date.Year([SnapshotDate]), type number),
    
    // Add Month number
    AddMonthNum = Table.AddColumn(AddYear, "MonthNum", each 
        Date.Month([SnapshotDate]), type number),
    
    // Add Critical Rate %
    AddCriticalRate = Table.AddColumn(AddMonthNum, "CriticalRate_Pct", each
        if [TotalInstances] > 0 then 
            ([CriticalCount] / [TotalInstances] * 100)
        else 
            0,
    type number),
    
    // Add Health Score (0-100)
    AddHealthScore = Table.AddColumn(AddCriticalRate, "HealthScore", each
        100 - (
            ([CriticalCount] / [TotalInstances] * 40) +
            ([OverConsumptionCount] / [TotalInstances] * 30) +
            ([UnderConsumptionCount] / [TotalInstances] * 20)
        ),
    type number),
    
    // Round Health Score
    RoundHealth = Table.TransformColumns(AddHealthScore, {{"HealthScore", each Number.Round(_, 1)}})
in
    RoundHealth
```

---

## Advanced Patterns

### Pattern: Query Folding Optimization

**Good (Folds to source - fast):**
```m
let
    Source = Csv.Document(...),
    Promoted = Table.PromoteHeaders(Source),
    FilteredRows = Table.SelectRows(Promoted, each [Status] = "CRITIQUE"),
    SelectedColumns = Table.SelectColumns(FilteredRows, {"InstanceID", "Status"})
in
    SelectedColumns
```

**Bad (Doesn't fold - slower):**
```m
let
    Source = Csv.Document(...),
    Promoted = Table.PromoteHeaders(Source),
    CustomColumn = Table.AddColumn(Promoted, "IsProduction", each [Environment] = "Production"),
    Filter = Table.SelectRows(CustomColumn, each [IsProduction] = true)
in
    Filter
```

**Better (Apply custom columns in Power BI calc instead):**
```m
let
    Source = Csv.Document(...),
    Promoted = Table.PromoteHeaders(Source),
    Filter = Table.SelectRows(Promoted, each [Environment] = "Production"),
    SelectedColumns = Table.SelectColumns(Filter, {"InstanceID", "Status", "Environment"})
in
    SelectedColumns
```

---

### Pattern: Error Handling

```m
let
    Source = Csv.Document(File.Contents("C:\data\instances.csv"), [Delimiter=","]),
    Promoted = Table.PromoteHeaders(Source),
    
    // Handle missing or invalid numeric values
    TypedTable = try
        Table.TransformColumnTypes(Promoted,{
            {"CPU_vCPU", Int64.Type},
            {"RAM_GB", Int64.Type}
        })
    otherwise
        Promoted,  // Return original if conversion fails
    
    // Replace errors with 0
    ReplaceErrors = Table.ReplaceErrorValues(TypedTable, {{"CPU_vCPU", 0}, {"RAM_GB", 0}})
in
    ReplaceErrors
```

---

### Pattern: Conditional Loading

Load different CSV based on environment:

```m
let
    Environment = "Production",  // Change as needed
    
    FilePath = if Environment = "Production" then
        "C:\data\metrics_prod.csv"
    else if Environment = "Staging" then
        "C:\data\metrics_staging.csv"
    else
        "C:\data\metrics_dev.csv",
    
    Source = Csv.Document(File.Contents(FilePath), [Delimiter=","]),
    Promoted = Table.PromoteHeaders(Source)
in
    Promoted
```

---

## Tips & Tricks

1. **Reuse M queries:** Create separate queries then reference:
   ```m
   let
       Source = #"MyLoadedTable"
   in
       Source
   ```

2. **Handle duplicates** before loading:
   ```m
   let
       Source = ...,
       RemoveDuplicates = Table.Distinct(Source, {"InstanceID"})
   in
       RemoveDuplicates
   ```

3. **Convert text to number safely:**
   ```m
   let
       Source = ...,
       SafeNumber = Table.TransformColumns(Source, 
           {"CPU_Avg", (v) => try Number.From(v) otherwise null})
   in
       Source
   ```

4. **Unpivot if needed** (reshape wide to long):
   ```m
   let
       Source = ...,
       Unpivoted = Table.Unpivot(Source, {"CPU_P50", "CPU_P90", "CPU_P95"}, "Attribute", "Value")
   in
       Unpivoted
   ```

5. **Merge tables** if you need to combine:
   ```m
   let
       Instances = ...,
       Flavors = ...,
       Merged = Table.NestedJoin(Instances, {"FlavorName"}, Flavors, {"FlavorName"}, "Flavor"),
       Expanded = Table.ExpandTableColumn(Merged, "Flavor", {"Cost_Monthly"})
   in
       Expanded
   ```

---

## Common Errors & Fixes

| Error | Cause | Fix |
|-------|-------|-----|
| "File not found" | Wrong path | Verify file path, use forward slashes or raw strings (`r"..."`) |
| "Column not found" | Typo in column name | Check CSV headers match exactly (case-sensitive) |
| "Type conversion failed" | Value can't convert | Use `try ... otherwise null` or check source data |
| "Null values" | Missing data | Use `Table.ReplaceNullValues()` or `Table.FillDown()` |
| "Encoding issues" | Wrong character set | Add `Encoding=1252` or `Encoding=65001` to CSV.Document |

---

## Integration with DAX

Once transformed, use these in DAX measures:

```dax
// Reference column
AvgCPUByInstance = CALCULATE(
    AVERAGE(Metrics[CPU_P95]),
    FILTER(Metrics, Metrics[InstanceID] = "INST-0001")
)

// Reference calculated column from Power Query
CriticalCount = CALCULATE(
    COUNTA(Instances[InstanceID]),
    FILTER(Instances, Instances[StatusPriority] = 1)
)
```

---
