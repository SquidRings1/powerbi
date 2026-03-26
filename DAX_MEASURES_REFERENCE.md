# DAX Measures & Formulas - Complete Reference

## Overview

DAX (Data Analysis Expressions) is used in Power BI for:
- **Measures**: Aggregations calculated on-the-fly (affected by filters)
- **Calculated Columns**: Static values computed during data load
- **KPIs**: Measures with targets and trends

---

## 1. Count Measures

### Basic Status Counts

```dax
// Count instances by status
Count_Critique = 
    CALCULATE(
        COUNTA(Instances[InstanceID]),
        Instances[Status] = "CRITIQUE"
    )

Count_SurConso = 
    CALCULATE(
        COUNTA(Instances[InstanceID]),
        Instances[Status] = "SUR-CONSO"
    )

Count_OK = 
    CALCULATE(
        COUNTA(Instances[InstanceID]),
        Instances[Status] = "OK"
    )

Count_SousConso = 
    CALCULATE(
        COUNTA(Instances[InstanceID]),
        Instances[Status] = "SOUS-CONSO"
    )

Count_Total = 
    COUNTA(Instances[InstanceID])
```

### Application Counts

```dax
Count_UniqueApps = 
    DISTINCTCOUNT(Instances[AppID])

Count_ProdApps = 
    CALCULATE(
        DISTINCTCOUNT(Apps[AppID]),
        Apps[Environment] = "Production"
    )

Count_StagingApps = 
    CALCULATE(
        DISTINCTCOUNT(Apps[AppID]),
        Apps[Environment] = "Staging"
    )
```

### Instance Corrections

```dax
// Instances that have been corrected (flavor changed)
Count_Corrected = 
    CALCULATE(
        COUNTA(Instances[InstanceID]),
        Instances[Corrected] = "Yes"
    )

// Instances still needing correction
Count_NeedingCorrection = 
    CALCULATE(
        COUNTA(Instances[InstanceID]),
        Instances[CorrectionNeeded] = TRUE
    )

// Instances with recommended flavor different
Count_HasRecommendation = 
    CALCULATE(
        COUNTA(Instances[InstanceID]),
        Instances[HasDifferentFlavor] = TRUE
    )
```

---

## 2. Percentage & Rate Measures

### Status Distribution

```dax
// Percentage of total by status
Pct_Critique = 
    DIVIDE(
        [Count_Critique],
        [Count_Total],
        0
    )

Pct_SurConso = 
    DIVIDE(
        [Count_SurConso],
        [Count_Total],
        0
    )

Pct_OK = 
    DIVIDE(
        [Count_OK],
        [Count_Total],
        0
    )

Pct_SousConso = 
    DIVIDE(
        [Count_SousConso],
        [Count_Total],
        0
    )

// As percentages (0-100)
Pct_Critique_100 = [Pct_Critique] * 100
Pct_SurConso_100 = [Pct_SurConso] * 100
Pct_OK_100 = [Pct_OK] * 100
Pct_SousConso_100 = [Pct_SousConso] * 100
```

### Correction Rate

```dax
Correction_Rate = 
    DIVIDE(
        [Count_Corrected],
        [Count_Total],
        0
    )

// Display as percentage
Correction_Rate_Pct = 
    FORMAT([Correction_Rate], "0.0%")

// Formatted text
Correction_Summary = 
    [Count_Corrected] & " / " & [Count_Total] & 
    " (" & [Correction_Rate_Pct] & ")"
```

### Application Health Rate

```dax
AppHealthScore = 
    1 - 
    (
        ([Count_Critique] / [Count_Total] * 0.4) +
        ([Count_SurConso] / [Count_Total] * 0.3) +
        ([Count_SousConso] / [Count_Total] * 0.2)
    )

AppHealthScore_Pct = 
    FORMAT([AppHealthScore] * 100, "0.0") & "%"
```

---

## 3. Average & Aggregation Measures

### CPU Metrics

```dax
// CPU Averages by percentile
Avg_CPU_P50 = 
    AVERAGE(Metrics[CPU_P50])

Avg_CPU_P90 = 
    AVERAGE(Metrics[CPU_P90])

Avg_CPU_P95 = 
    AVERAGE(Metrics[CPU_P95])

Avg_CPU_P99 = 
    AVERAGE(Metrics[CPU_P99])

Avg_CPU_Overall = 
    AVERAGE(Metrics[CPU_Avg])

// CPU Standard Deviation
CPU_StdDev = 
    STDEV.S(Metrics[CPU_P95])
```

### RAM Metrics

```dax
// RAM Averages by percentile
Avg_RAM_P50 = 
    AVERAGE(Metrics[RAM_P50])

Avg_RAM_P90 = 
    AVERAGE(Metrics[RAM_P90])

Avg_RAM_P95 = 
    AVERAGE(Metrics[RAM_P95])

Avg_RAM_P99 = 
    AVERAGE(Metrics[RAM_P99])

Avg_RAM_Overall = 
    AVERAGE(Metrics[RAM_Avg])

// RAM Standard Deviation
RAM_StdDev = 
    STDEV.S(Metrics[RAM_P95])
```

### Min/Max Range

```dax
// CPU Range
CPU_P95_Min = 
    MIN(Metrics[CPU_P95])

CPU_P95_Max = 
    MAX(Metrics[CPU_P95])

CPU_P95_Range = 
    [CPU_P95_Max] - [CPU_P95_Min]

// RAM Range
RAM_P95_Min = 
    MIN(Metrics[RAM_P95])

RAM_P95_Max = 
    MAX(Metrics[RAM_P95])

RAM_P95_Range = 
    [RAM_P95_Max] - [RAM_P95_Min]
```

---

## 4. Dynamic & Context-Aware Measures

### Dynamic Titles

```dax
// Selected dimension display
Selected_App = 
    IF(
        HASONEVALUE(Apps[AppName]),
        VALUES(Apps[AppName]),
        "All Applications"
    )

Selected_Flavor = 
    IF(
        HASONEVALUE(Flavors[FlavorName]),
        VALUES(Flavors[FlavorName]),
        "All Flavors"
    )

Selected_Domain = 
    IF(
        HASONEVALUE(Apps[Domain]),
        VALUES(Apps[Domain]),
        "All Domains"
    )

// Friendly display
Dashboard_Title = 
    "Performance Analysis: " & [Selected_App]
```

### Overall Status (Pessimistic - returns worst status)

```dax
Overall_Status = 
    IF(
        [Count_Critique] > 0, "CRITICAL",
        IF(
            [Count_SurConso] > ([Count_Total] * 0.4), "AT RISK",
            IF(
                [Count_SousConso] > ([Count_Total] * 0.5), "UNDER-UTILIZED",
                "HEALTHY"
            )
        )
    )

// Status emoji (for cards)
Status_Indicator = 
    IF([Overall_Status] = "CRITICAL", "🔴",
    IF([Overall_Status] = "AT RISK", "🟠",
    IF([Overall_Status] = "UNDER-UTILIZED", "🔵", "🟢")))
```

### Conditional Summary

```dax
// Summary based on context
Summary = 
    IF(
        [Count_Critique] = 0,
        "No critical issues",
        [Count_Critique] & " instances at critical level requiring immediate action"
    ) &
    CONCATENATEX(
        VALUES(Instances[Status]),
        " | " & [Status] & ": " & 
        CALCULATE([Count_Total], Instances[Status] = [Status])
    )
```

---

## 5. Time-Series Measures

### Timeline Metrics

```dax
// From Timeline table
Total_Apps_History = 
    SUM(Timeline[TotalApps])

Total_Instances_History = 
    SUM(Timeline[TotalInstances])

Total_Corrected_Overall = 
    SUM(Timeline[CorrectedCount])

Avg_Correction_Rate = 
    AVERAGE(Timeline[CorrectionPct])

// Trend (Month-over-Month)
Correction_Trend = 
    CALCULATE(
        [Correction_Rate],
        Timeline[Month] = 
            MAX(Timeline[Month])
    ) - 
    CALCULATE(
        [Correction_Rate],
        Timeline[Month] = 
            MAX(Timeline[Month]) - 1
    )
```

### Date-Based Filters

```dax
// Last 30 days
Avg_CPU_Last30Days = 
    CALCULATE(
        [Avg_CPU_P95],
        FILTER(
            Metrics,
            [MeasureDate] >= TODAY() - 30
        )
    )

// This month
Avg_CPU_ThisMonth = 
    CALCULATE(
        [Avg_CPU_P95],
        FILTER(
            Metrics,
            MONTH([MeasureDate]) = MONTH(TODAY()) &&
            YEAR([MeasureDate]) = YEAR(TODAY())
        )
    )

// Previous month
Avg_CPU_PrevMonth = 
    CALCULATE(
        [Avg_CPU_P95],
        FILTER(
            Metrics,
            MONTH([MeasureDate]) = MONTH(TODAY()) - 1
        )
    )
```

---

## 6. Cost & Savings Measures

### Flavor Costs

```dax
// Total current cost
Total_Current_Cost = 
    SUMX(
        Instances,
        RELATED(Flavors[Cost_Monthly])
    )

// Total recommended cost (if all changed to recommended)
Total_Recommended_Cost = 
    SUMX(
        Instances,
        LOOKUPVALUE(
            Flavors[Cost_Monthly],
            Flavors[FlavorName], Instances[RecFlavorName]
        )
    )

// Total potential savings
Total_Potential_Savings = 
    [Total_Current_Cost] - [Total_Recommended_Cost]

// Savings percentage
Savings_Percentage = 
    DIVIDE(
        [Total_Potential_Savings],
        [Total_Current_Cost],
        0
    ) * 100
```

### Cost per Status

```dax
Cost_Critique = 
    CALCULATE(
        [Total_Current_Cost],
        Instances[Status] = "CRITIQUE"
    )

Cost_SurConso = 
    CALCULATE(
        [Total_Current_Cost],
        Instances[Status] = "SUR-CONSO"
    )

Savings_If_All_Corrected = 
    CALCULATE(
        [Total_Potential_Savings],
        Instances[CorrectionNeeded] = TRUE
    )
```

---

## 7. Calculated Columns

These are added to tables in Power BI Desktop → Transform Data

### Instances Calculated Columns

```dax
// Column: Urgency Score (1-10)
Urgency_Score = 
    IF(Instances[Status] = "CRITIQUE", 10,
    IF(Instances[Status] = "SUR-CONSO", 7,
    IF(Instances[Status] = "OK", 3,
    IF(Instances[Status] = "SOUS-CONSO", 1, 0))))

// Column: Estimated Savings
Estimated_Savings = 
    IF(
        RELATED(Flavors[FlavorName]) <> Instances[RecFlavorName],
        RELATED(Flavors[Cost_Monthly]) -
        LOOKUPVALUE(
            Flavors[Cost_Monthly],
            Flavors[FlavorName], Instances[RecFlavorName]
        ),
        0
    )

// Column: Days Since Creation
Days_Since_Creation = 
    INT(TODAY() - Instances[CreatedDate])
```

### Metrics Calculated Columns

```dax
// Column: CPU Alert Level
CPU_Alert_Level = 
    IF(Metrics[CPU_P95] > 90, "CRITICAL",
    IF(Metrics[CPU_P95] > 80, "WARNING",
    IF(Metrics[CPU_P95] > 50, "OK", "EFFICIENT")))

// Column: Resource Utilization Score (0-100)
Resource_Score = 
    (ABS(Metrics[CPU_P95] - 70) + ABS(Metrics[RAM_P95] - 70)) / 2

// Column: Recommendation
Recommendation = 
    IF(Metrics[CPU_P95] > 85 OR Metrics[RAM_P95] > 85,
        "Increase capacity",
        IF(Metrics[CPU_Avg] < 10 AND Metrics[RAM_Avg] < 15,
            "Downsize instance",
            "Maintain current"
        )
    )
```

---

## 8. Number Formatting Measures

### Formatted Displays

```dax
// Format CPU as percentage
Avg_CPU_Formatted = 
    FORMAT([Avg_CPU_P95], "0.0") & "%"

// Format RAM as percentage
Avg_RAM_Formatted = 
    FORMAT([Avg_RAM_P95], "0.0") & "%"

// Format cost as currency
Total_Cost_Formatted = 
    FORMAT([Total_Current_Cost], "$#,##0.00")

// Format savings as currency
Savings_Formatted = 
    FORMAT([Total_Potential_Savings], "$#,##0.00")

// Human-readable numbers
Instance_Count_Formatted = 
    IF([Count_Total] > 1000,
        FORMAT([Count_Total] / 1000, "0.0") & "K",
        FORMAT([Count_Total], "#,##0")
    )
```

---

## 9. Common Patterns

### Multi-Criteria Count

```dax
// Count with multiple conditions
Count_Prod_Critical = 
    CALCULATE(
        COUNTA(Instances[InstanceID]),
        Instances[Status] = "CRITIQUE",
        RELATED(Apps[Environment]) = "Production"
    )

// Count OR condition
Count_Urgent = 
    CALCULATE(
        COUNTA(Instances[InstanceID]),
        Instances[Status] = "CRITIQUE" ||
        Instances[Status] = "SUR-CONSO"
    )
```

### Year-to-Date (YTD) Aggregation

```dax
YTD_Corrections = 
    CALCULATE(
        [Count_Corrected],
        DATESYTD(Timeline[SnapshotDate])
    )

// Month-to-Date
MTD_Corrections = 
    CALCULATE(
        [Count_Corrected],
        DATESMTD(Timeline[SnapshotDate])
    )
```

### Ranking

```dax
// Rank app by average CPU
App_CPU_Rank = 
    RANK(
        [Avg_CPU_P95],
        CALCULATE(
            [Avg_CPU_P95],
            ALLEXCEPT(Apps, Apps[AppID])
        ),
        DESC
    )
```

---

## 10. Tooltips & Context Measures

### Rich Tooltip Content

```dax
// Multi-line tooltip
Tooltip_Instance = 
    "Instance: " & Instances[InstanceID] & 
    UNICHAR(10) &
    "App: " & Instances[AppName] & 
    UNICHAR(10) &
    "Flavor: " & Instances[FlavorName] & 
    UNICHAR(10) &
    "Status: " & Instances[Status] & 
    UNICHAR(10) &
    "CPU P95: " & FORMAT([Avg_CPU_P95], "0.0%") & 
    UNICHAR(10) &
    "RAM P95: " & FORMAT([Avg_RAM_P95], "0.0%")

Tooltip_App = 
    [Selected_App] &
    " (" & [Count_Total] & " instances)" &
    UNICHAR(10) &
    "Health: " & [Overall_Status] &
    UNICHAR(10) &
    "Avg CPU: " & [Avg_CPU_Formatted] &
    UNICHAR(10) &
    "Potential Savings: " & [Savings_Formatted]
```

---

## Tips & Best Practices

1. **Use variables** to avoid recalculating:
   ```dax
   MyMeasure = 
       VAR CriticalCount = [Count_Critique]
       VAR Total = [Count_Total]
       RETURN DIVIDE(CriticalCount, Total)
   ```

2. **Use CALCULATE** for context manipulation (filtering)

3. **Use SUMX/MAXX** for row-by-row calculations

4. **Avoid ALL()** when possible; prefer REMOVEFILTERS()

5. **Format directly** in measure (more flexible than visual formatting)

6. **Test with slicer** to ensure filter context works

7. **Use BLANK()** for missing values (better than 0 for some calculations)

---

## Performance Tips

| Issue | Solution |
|-------|----------|
| Slow DAX | Pre-aggregate in table; use variables to cache |
| Context issues | Test with and without slicer selections |
| Circular reference | Check column vs measure dependencies |
| #ERROR in visual | Add IFERROR() wrapper or default value |
| Unexpected results | Verify relationship cardinality |

---
