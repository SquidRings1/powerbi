#!/usr/bin/env python3
"""
FlavorOps Data Generation Script
Generates CSV files for Power BI dashboard based on the HTML preview pattern.
"""

import pandas as pd
import numpy as np
from datetime import datetime, timedelta
import os
import random

# Configuration
DATA_DIR = "data"
RANDOM_SEED = 42
NUM_MONTHS = 14  # Historical months
CURRENT_DATE = datetime(2026, 3, 26)

# Ensure data directory exists
os.makedirs(DATA_DIR, exist_ok=True)

# Set random seed for reproducibility
random.seed(RANDOM_SEED)
np.random.seed(RANDOM_SEED)

print("FlavorOps Data Generator")
print(f"Output directory: {DATA_DIR}/")

# ============================================================================
# 1. FLAVORS (AWS Instance Types)
# ============================================================================

flavors_data = [
    {"FlavorID": "F001", "FlavorName": "t2.micro", "CPU_vCPU": 1, "RAM_GB": 1, "Cost_Monthly": 8.50},
    {"FlavorID": "F002", "FlavorName": "t2.small", "CPU_vCPU": 1, "RAM_GB": 2, "Cost_Monthly": 17.00},
    {"FlavorID": "F003", "FlavorName": "t2.medium", "CPU_vCPU": 2, "RAM_GB": 4, "Cost_Monthly": 34.00},
    {"FlavorID": "F004", "FlavorName": "t3.medium", "CPU_vCPU": 2, "RAM_GB": 4, "Cost_Monthly": 30.60},
    {"FlavorID": "F005", "FlavorName": "t3.large", "CPU_vCPU": 2, "RAM_GB": 8, "Cost_Monthly": 61.20},
    {"FlavorID": "F006", "FlavorName": "m5.large", "CPU_vCPU": 2, "RAM_GB": 8, "Cost_Monthly": 95.75},
    {"FlavorID": "F007", "FlavorName": "m5.xlarge", "CPU_vCPU": 4, "RAM_GB": 16, "Cost_Monthly": 191.50},
    {"FlavorID": "F008", "FlavorName": "m5.2xlarge", "CPU_vCPU": 8, "RAM_GB": 32, "Cost_Monthly": 383.00},
    {"FlavorID": "F009", "FlavorName": "c5.xlarge", "CPU_vCPU": 4, "RAM_GB": 8, "Cost_Monthly": 170.00},
    {"FlavorID": "F010", "FlavorName": "r5.large", "CPU_vCPU": 2, "RAM_GB": 16, "Cost_Monthly": 156.50},
]

df_flavors = pd.DataFrame(flavors_data)
df_flavors.to_csv(f"{DATA_DIR}/flavors.csv", index=False)
print(f"✓ Created flavors.csv ({len(df_flavors)} records)")

# ============================================================================
# 2. APPS (Applications)
# ============================================================================

apps_data = [
    {"AppID": "APP-001", "AppName": "payment-service", "Domain": "Finance", "Environment": "Production"},
    {"AppID": "APP-002", "AppName": "auth-gateway", "Domain": "Security", "Environment": "Production"},
    {"AppID": "APP-003", "AppName": "user-profile-api", "Domain": "CRM", "Environment": "Production"},
    {"AppID": "APP-004", "AppName": "notification-svc", "Domain": "Messaging", "Environment": "Production"},
    {"AppID": "APP-005", "AppName": "report-engine", "Domain": "Analytics", "Environment": "Production"},
    {"AppID": "APP-006", "AppName": "data-ingestion", "Domain": "Data", "Environment": "Staging"},
    {"AppID": "APP-007", "AppName": "order-processor", "Domain": "Commerce", "Environment": "Production"},
    {"AppID": "APP-008", "AppName": "inventory-api", "Domain": "Commerce", "Environment": "Production"},
    {"AppID": "APP-009", "AppName": "search-service", "Domain": "Discovery", "Environment": "Production"},
    {"AppID": "APP-010", "AppName": "ml-scoring", "Domain": "AI/ML", "Environment": "Staging"},
    {"AppID": "APP-011", "AppName": "image-resizer", "Domain": "Media", "Environment": "Production"},
    {"AppID": "APP-012", "AppName": "audit-logger", "Domain": "Security", "Environment": "Production"},
    {"AppID": "APP-013", "AppName": "scheduler-svc", "Domain": "Ops", "Environment": "Staging"},
    {"AppID": "APP-014", "AppName": "api-gateway", "Domain": "Infra", "Environment": "Production"},
    {"AppID": "APP-015", "AppName": "cache-manager", "Domain": "Infra", "Environment": "Production"},
]

df_apps = pd.DataFrame(apps_data)
df_apps.to_csv(f"{DATA_DIR}/apps.csv", index=False)
print(f"✓ Created apps.csv ({len(df_apps)} records)")

# ============================================================================
# 3. INSTANCES (VM Instances)
# ============================================================================

def gaussian_percentile(avg, std=15):
    """Generate realistic percentile distribution."""
    values = {
        "p50": max(1, avg - np.random.uniform(0, std * 0.3)),
        "p90": min(99, avg + np.random.uniform(std * 0.3, std * 0.7)),
        "p95": min(100, avg + np.random.uniform(std * 0.5, std * 0.9)),
        "p99": min(100, avg + np.random.uniform(std * 0.8, std)),
    }
    # Ensure ordering
    values["p50"] = min(values["p50"], values["p90"])
    values["p90"] = min(values["p90"], values["p95"])
    values["p95"] = min(values["p95"], values["p99"])
    return values

patterns = ["OVER", "CORRECT", "UNDER", "OVER", "CORRECT", "OVER", "CORRECT", 
            "OVER", "UNDER", "CORRECT", "OVER", "CORRECT", "UNDER", "OVER", "CORRECT"]

instances_data = []
instance_id = 1

for app_idx, app in enumerate(df_apps.itertuples()):
    num_instances = np.random.randint(2, 6)
    flavor_idx = np.random.randint(0, len(df_flavors))
    flavor = df_flavors.iloc[flavor_idx]
    pattern = patterns[app_idx % len(patterns)]
    
    # Determine avg CPU/RAM based on pattern
    if pattern == "OVER":
        cpu_avg = np.random.uniform(75, 95)
        ram_avg = np.random.uniform(70, 92)
    elif pattern == "UNDER":
        cpu_avg = np.random.uniform(2, 15)
        ram_avg = np.random.uniform(3, 18)
    else:  # CORRECT
        cpu_avg = np.random.uniform(25, 65)
        ram_avg = np.random.uniform(20, 60)
    
    for j in range(num_instances):
        cpu_pct = gaussian_percentile(cpu_avg)
        ram_pct = gaussian_percentile(ram_avg, std=12)
        
        # Determine status
        over_cpu = cpu_pct["p95"] > 80
        over_ram = ram_pct["p95"] > 80
        crit_cpu = cpu_pct["p95"] > 90
        crit_ram = ram_pct["p95"] > 90
        
        if crit_cpu or crit_ram:
            status = "CRITIQUE"
        elif over_cpu or over_ram:
            status = "SUR-CONSO"
        elif cpu_avg < 10 and ram_avg < 15:
            status = "SOUS-CONSO"
        else:
            status = "OK"
        
        # Recommendation
        rec_flavor_idx = flavor_idx
        if over_cpu or over_ram:
            rec_flavor_idx = min(flavor_idx + 1, len(df_flavors) - 1)
        elif cpu_avg < 10 and ram_avg < 15:
            rec_flavor_idx = max(flavor_idx - 2, 0)
        
        rec_flavor = df_flavors.iloc[rec_flavor_idx]
        corrected = (over_cpu or over_ram) and np.random.random() < 0.3
        
        instances_data.append({
            "InstanceID": f"INST-{str(instance_id).zfill(4)}",
            "AppID": app.AppID,
            "AppName": app.AppName,
            "Domain": app.Domain,
            "FlavorName": flavor.FlavorName,
            "CPU_vCPU": flavor.CPU_vCPU,
            "RAM_GB": flavor.RAM_GB,
            "RecFlavorName": rec_flavor.FlavorName,
            "Status": status,
            "Corrected": "Yes" if corrected else "No",
            "CreatedDate": (CURRENT_DATE - timedelta(days=np.random.randint(0, 180))).date(),
        })
        instance_id += 1

df_instances = pd.DataFrame(instances_data)
df_instances.to_csv(f"{DATA_DIR}/instances.csv", index=False)
print(f"✓ Created instances.csv ({len(df_instances)} records)")

# ============================================================================
# 4. METRICS (CPU/RAM per Instance over time)
# ============================================================================

metrics_data = []
metric_id = 1

for instance in df_instances.itertuples():
    # Generate 30 daily data points
    for day_offset in range(-29, 1):
        date = CURRENT_DATE + timedelta(days=day_offset)
        
        # Pattern-based metric generation
        cpu_avg = 50 + np.random.uniform(-15, 15)
        ram_avg = 45 + np.random.uniform(-15, 15)
        
        if instance.Status == "CRITIQUE":
            cpu_avg += np.random.uniform(20, 40)
            ram_avg += np.random.uniform(20, 40)
        elif instance.Status == "SUR-CONSO":
            cpu_avg += np.random.uniform(10, 20)
            ram_avg += np.random.uniform(10, 20)
        elif instance.Status == "SOUS-CONSO":
            cpu_avg = np.random.uniform(2, 15)
            ram_avg = np.random.uniform(3, 18)
        
        metrics_data.append({
            "MetricID": f"MET-{str(metric_id).zfill(6)}",
            "InstanceID": instance.InstanceID,
            "AppID": instance.AppID,
            "MeasureDate": date,
            "CPU_Avg": round(max(0, min(100, cpu_avg)), 1),
            "CPU_P50": round(max(0, cpu_avg - np.random.uniform(5, 15)), 1),
            "CPU_P90": round(min(100, cpu_avg + np.random.uniform(5, 15)), 1),
            "CPU_P95": round(min(100, cpu_avg + np.random.uniform(10, 20)), 1),
            "CPU_P99": round(min(100, cpu_avg + np.random.uniform(15, 30)), 1),
            "RAM_Avg": round(max(0, min(100, ram_avg)), 1),
            "RAM_P50": round(max(0, ram_avg - np.random.uniform(5, 15)), 1),
            "RAM_P90": round(min(100, ram_avg + np.random.uniform(5, 15)), 1),
            "RAM_P95": round(min(100, ram_avg + np.random.uniform(10, 20)), 1),
            "RAM_P99": round(min(100, ram_avg + np.random.uniform(15, 30)), 1),
        })
        metric_id += 1

df_metrics = pd.DataFrame(metrics_data)
df_metrics.to_csv(f"{DATA_DIR}/metrics.csv", index=False)
print(f"✓ Created metrics.csv ({len(df_metrics)} records)")

# ============================================================================
# 5. TIMELINE (Evolution - Monthly Aggregation)
# ============================================================================

timeline_data = []

# Generate monthly snapshots for the past NUM_MONTHS
for month_offset in range(NUM_MONTHS - 1, -1, -1):
    snapshot_date = CURRENT_DATE - timedelta(days=30 * month_offset)
    month_str = snapshot_date.strftime("%Y-%m")
    
    # Filter instances active during this month
    month_instances = df_instances[
        (df_instances["CreatedDate"] <= snapshot_date.date())
    ]
    
    # Calculate status distribution
    total = len(month_instances)
    crit = len(month_instances[month_instances["Status"] == "CRITIQUE"])
    sur = len(month_instances[month_instances["Status"] == "SUR-CONSO"])
    ok = len(month_instances[month_instances["Status"] == "OK"])
    under = len(month_instances[month_instances["Status"] == "SOUS-CONSO"])
    corrected = len(month_instances[month_instances["Corrected"] == "Yes"])
    
    correction_pct = round((corrected / total * 100), 1) if total > 0 else 0
    
    timeline_data.append({
        "TimelineID": f"TL-{month_str}",
        "Month": month_str,
        "SnapshotDate": snapshot_date.date(),
        "TotalApps": 15,
        "TotalInstances": total,
        "CriticalCount": crit,
        "OverConsumptionCount": sur,
        "OKCount": ok,
        "UnderConsumptionCount": under,
        "CorrectedCount": corrected,
        "CorrectionPct": correction_pct,
    })

df_timeline = pd.DataFrame(timeline_data)
df_timeline.to_csv(f"{DATA_DIR}/timeline.csv", index=False)
print(f"✓ Created timeline.csv ({len(df_timeline)} records)")

# ============================================================================
# SUMMARY
# ============================================================================

print("\n" + "="*60)
print("Data Generation Complete!")
print("="*60)
print(f"\nGenerated {len(df_flavors)} flavors")
print(f"Generated {len(df_apps)} applications")
print(f"Generated {len(df_instances)} instances")
print(f"Generated {len(df_metrics)} metric records")
print(f"Generated {len(df_timeline)} timeline snapshots")
print(f"\nAll files saved to: {os.path.abspath(DATA_DIR)}/")
print("\nNext steps:")
print("1. Open Power BI Desktop")
print("2. File → Get Data → Text/CSV")
print("3. Load each CSV file from the data/ folder")
print("4. Create relationships between tables")
print("5. Build visualizations using the provided DAX measures")
