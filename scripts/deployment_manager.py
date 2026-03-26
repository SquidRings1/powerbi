#!/usr/bin/env python3
"""
FlavorOps Power BI - Deployment & Configuration Manager
Handles template configuration, data updates, and Power BI publishing
"""

import os
import sys
import json
from pathlib import Path
from datetime import datetime

class PowerBIDeploymentManager:
    """Manages Power BI template deployment and configuration"""
    
    def __init__(self, project_dir=None):
        self.project_dir = project_dir or Path(__file__).parent.parent
        self.template_file = self.project_dir / "FlavorOps_Dashboard_Template.pbix"
        self.data_dir = self.project_dir / "data"
        self.config_file = self.project_dir / ".deployment_config.json"
        
    def create_deployment_config(self):
        """Create deployment configuration file"""
        config = {
            "version": "1.0",
            "created": datetime.now().isoformat(),
            "powerbi": {
                "service": {
                    "workspace": "FlavorOps",
                    "datasetName": "FlavorOps_Dataset",
                    "reportName": "FlavorOps_Dashboard",
                    "refreshSchedule": "daily"
                },
                "desktop": {
                    "autoLoad": True,
                    "autoRefresh": True,
                    "refreshInterval": 60
                }
            },
            "data": {
                "sourceFormat": "CSV",
                "location": str(self.data_dir),
                "tables": [
                    {
                        "name": "Flavors",
                        "file": "flavors.csv",
                        "primaryKey": "FlavorName",
                        "type": "Dimension"
                    },
                    {
                        "name": "Apps",
                        "file": "apps.csv",
                        "primaryKey": "AppID",
                        "type": "Dimension"
                    },
                    {
                        "name": "Instances",
                        "file": "instances.csv",
                        "primaryKey": "InstanceID",
                        "type": "Fact",
                        "foreignKeys": {
                            "AppID": "Apps",
                            "FlavorName": "Flavors"
                        }
                    },
                    {
                        "name": "Metrics",
                        "file": "metrics.csv",
                        "primaryKey": "MetricID",
                        "type": "Fact",
                        "foreignKeys": {
                            "InstanceID": "Instances"
                        }
                    },
                    {
                        "name": "Timeline",
                        "file": "timeline.csv",
                        "primaryKey": "TimelineID",
                        "type": "Fact",
                        "foreignKeys": {
                            "AppID": "Apps"
                        }
                    }
                ]
            },
            "theme": {
                "name": "GitHub Dark",
                "colors": {
                    "primary": "#2196F3",
                    "critical": "#D32F2F",
                    "warning": "#FF6D00",
                    "success": "#00C853",
                    "secondary": "#7C4DFF",
                    "accent": "#00BCD4",
                    "background": "#0D1117",
                    "surface": "#161B22"
                }
            },
            "measures": {
                "count": 30,
                "categories": ["Counts", "Averages", "Rates", "Rankings"]
            },
            "pages": [
                {
                    "name": "Vue Globale",
                    "description": "Executive Overview",
                    "order": 1,
                    "isDefault": True
                },
                {
                    "name": "Détail App",
                    "description": "Application Deep-dive",
                    "order": 2,
                    "isDefault": False
                },
                {
                    "name": "Instances & Config",
                    "description": "Instance Details",
                    "order": 3,
                    "isDefault": False
                }
            ]
        }
        
        with open(self.config_file, 'w') as f:
            json.dump(config, f, indent=2)
        
        return config
    
    def validate_setup(self):
        """Validate that all components are in place"""
        issues = []
        
        # Check template
        if not self.template_file.exists():
            issues.append(f"❌ Template not found: {self.template_file}")
        else:
            size_mb = self.template_file.stat().st_size / (1024 * 1024)
            print(f"✓ Template found ({size_mb:.2f} MB)")
        
        # Check data files
        required_files = ["flavors.csv", "apps.csv", "instances.csv", "metrics.csv", "timeline.csv"]
        for fname in required_files:
            fpath = self.data_dir / fname
            if not fpath.exists():
                issues.append(f"❌ Data file missing: {fname}")
            else:
                size_kb = fpath.stat().st_size / 1024
                print(f"✓ {fname} ({size_kb:.1f} KB)")
        
        return issues
    
    def generate_power_bi_script(self):
        """Generate Power BI M language script for data loading"""
        script = '''
// Power Query Script for FlavorOps Dashboard
// Copy this into Power BI Query Editor

let
    // Configuration
    DataFolder = "${DATA_DIR}",
    
    // Load Flavors
    Flavors = Csv.Document(File.Contents(DataFolder & "/flavors.csv"),[Delimiter=",", Columns=3, Encoding=1252, QuoteStyle=QuoteStyle.None]),
    FlavorTypes = Table.PromoteHeaders(Flavors, [PromoteAllScalars=true]),
    
    // Load Apps
    Apps = Csv.Document(File.Contents(DataFolder & "/apps.csv"),[Delimiter=",", Columns=4, Encoding=1252, QuoteStyle=QuoteStyle.None]),
    AppTypes = Table.PromoteHeaders(Apps, [PromoteAllScalars=true]),
    
    // Load Instances
    Instances = Csv.Document(File.Contents(DataFolder & "/instances.csv"),[Delimiter=",", Columns=6, Encoding=1252, QuoteStyle=QuoteStyle.None]),
    InstanceTypes = Table.PromoteHeaders(Instances, [PromoteAllScalars=true]),
    
    // Load Metrics
    Metrics = Csv.Document(File.Contents(DataFolder & "/metrics.csv"),[Delimiter=",", Columns=7, Encoding=1252, QuoteStyle=QuoteStyle.None]),
    MetricsTypes = Table.PromoteHeaders(Metrics, [PromoteAllScalars=true]),
    
    // Load Timeline
    Timeline = Csv.Document(File.Contents(DataFolder & "/timeline.csv"),[Delimiter=",", Columns=5, Encoding=1252, QuoteStyle=QuoteStyle.None]),
    TimelineTypes = Table.PromoteHeaders(Timeline, [PromoteAllScalars=true])

in
    {FlavorTypes, AppTypes, InstanceTypes, MetricsTypes, TimelineTypes}
'''
        return script
    
    def get_dag_metrics(self):
        """Return key metrics for DAX calculations"""
        return {
            "dimension_tables": ["Flavors", "Apps"],
            "fact_tables": ["Instances", "Metrics", "Timeline"],
            "key_measures": [
                "Count_Total",
                "Count_Critique",
                "Avg_CPU_P95",
                "Avg_RAM_P95",
                "Correction_Rate",
                "Total_Spend"
            ],
            "aggregation_levels": [
                "By App",
                "By Flavor",
                "By Instance",
                "By Status",
                "By Month"
            ]
        }

def main():
    """Main deployment workflow"""
    print("""
    ╔════════════════════════════════════════════════════════════════════════════╗
    ║                                                                            ║
    ║           📊 FlavorOps Power BI - Deployment Manager 📊                   ║
    ║                                                                            ║
    ╚════════════════════════════════════════════════════════════════════════════╝
    """)
    
    manager = PowerBIDeploymentManager()
    
    print("\n📋 VALIDATION")
    print("-" * 70)
    issues = manager.validate_setup()
    
    if issues:
        print("\n⚠️  Issues found:")
        for issue in issues:
            print(f"  {issue}")
        print("\nRun: python scripts/full_setup.py")
        return False
    
    print("\n✅ All components validated!\n")
    
    print("⚙️  CONFIGURATION")
    print("-" * 70)
    config = manager.create_deployment_config()
    print(f"✓ Created deployment config: .deployment_config.json")
    print(f"✓ Workspace: {config['powerbi']['service']['workspace']}")
    print(f"✓ Refresh: {config['powerbi']['service']['refreshSchedule']}")
    print(f"✓ Measures: {config['measures']['count']}")
    print(f"✓ Pages: {len(config['pages'])}\n")
    
    print("📊 DAG METRICS")
    print("-" * 70)
    metrics = manager.get_dag_metrics()
    print(f"✓ Dimensions: {', '.join(metrics['dimension_tables'])}")
    print(f"✓ Facts: {', '.join(metrics['fact_tables'])}")
    print(f"✓ Key Measures: {', '.join(metrics['key_measures'][:3])}...")
    print(f"✓ Aggregations: {len(metrics['aggregation_levels'])} levels\n")
    
    print("🎯 NEXT STEPS")
    print("-" * 70)
    print("""
1. Open Power BI Desktop

2. File → Open → FlavorOps_Dashboard_Template.pbix

3. Home → Transform Data

4. Load each CSV:
   - Click New Source → Text/CSV
   - Navigate to data/ folder
   - Load: flavors.csv, apps.csv
   - Transform: instances.csv, metrics.csv, timeline.csv

5. Home → Close & Apply

6. Your dashboard is live! 🎉

📖 For detailed instructions:
   → See POWERBI_TEMPLATE_GUIDE.md
   → See POWERBI_COMPLETE_GUIDE.md for advanced topics
    """)
    
    return True

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)
