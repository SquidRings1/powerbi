# Power BI FlavorOps Dashboard - Instructions Complètes

## 1. Préparation des données

### Étape 1.1: Générer les CSV

D'abord, exécutez le script Python pour générer les données:

```bash
cd /Users/haris/Documents/PROJECTS/powerbi
python scripts/generate_data.py
```

Cela crée 5 fichiers CSV dans le dossier `data/`:
- `flavors.csv` — Types instances (t2.micro, m5.large, etc.)
- `apps.csv` — Applications (payment-service, auth-gateway, etc.)
- `instances.csv` — Instances de VMs avec statuts
- `metrics.csv` — Données CPU/RAM par jour (30 jours)
- `timeline.csv` — Évolution mensuelle (14 mois)

### Étape 1.2: Charger les données dans Power BI

**Méthode A: Import Direct**

1. Ouvrir Power BI Desktop
2. Home → Get Data → Text/CSV
3. Naviguer vers `data/` folder
4. Sélectionner `flavors.csv`:
   - Cliquer "Load" (pas Transform, pour les données lookup)
5. Répéter pour les autres fichiers:
   - `apps.csv` → Load
   - `instances.csv` → Transform Data (voir Power Query ci-dessous)
   - `metrics.csv` → Transform Data
   - `timeline.csv` → Load

**Méthode B: Python Script dans Power BI**

Pour une solution plus automatisée:

1. Home → Get Data → Python script
2. Copier le contenu de `scripts/powerbi_python_load.py`
3. Modifier le chemin DATA_PATH (ligne 11)
4. Exécuter
5. Les 5 tables apparaissent automatiquement

---

## 2. Power Query (M Language)

Appliquez ces transformations après avoir cliqué "Transform Data":

### 2.1 Instances Table

```m
let
    Source = Csv.Document(File.Contents("C:\path\to\data\instances.csv"),[Delimiter=",", Columns=15, Encoding=1252, QuoteStyle=QuoteStyle.None]),
    Promoted = Table.PromoteHeaders(Source, [PromoteAllScalars=true]),
    ChangedType = Table.TransformColumnTypes(Promoted,{
        {"InstanceID", type text},
        {"AppID", type text},
        {"AppName", type text},
        {"Domain", type text}, 
        {"FlavorName", type text},
        {"CPU_vCPU", type number},
        {"RAM_GB", type number},
        {"RecFlavorName", type text},
        {"Status", type text},
        {"Corrected", type logical},
        {"CreatedDate", type date}
    }),
    
    // Ajouter colonnes calculées
    AddStatusCode = Table.AddColumn(ChangedType, "StatusCode", each
        if [Status] = "CRITIQUE" then 3
        else if [Status] = "SUR-CONSO" then 2
        else if [Status] = "OK" then 1
        else 0, type number),
        
    AddCorrectionNeeded = Table.AddColumn(AddStatusCode, "CorrectionNeeded", each
        [Status] <> "OK" and [Status] <> "SOUS-CONSO", type logical)
in
    AddCorrectionNeeded
```

### 2.2 Metrics Table

```m
let
    Source = Csv.Document(File.Contents("C:\path\to\data\metrics.csv"),[Delimiter=",", Encoding=1252]),
    Promoted = Table.PromoteHeaders(Source, [PromoteAllScalars=true]),
    ChangedType = Table.TransformColumnTypes(Promoted,{
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
    
    // Ajouter Year-Month pour agrégation
    AddYearMonth = Table.AddColumn(ChangedType, "YearMonth", each 
        Date.ToText([MeasureDate], "yyyy-MM"), type text)
in
    AddYearMonth
```

### 2.3 Timeline Table

```m
let
    Source = Csv.Document(File.Contents("C:\path\to\data\timeline.csv"),[Delimiter=",", Encoding=1252]),
    Promoted = Table.PromoteHeaders(Source, [PromoteAllScalars=true]),
    ChangedType = Table.TransformColumnTypes(Promoted,{
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
    })
in
    ChangedType
```

---

## 3. Modèle de données

### Créer les relations

Dans Power BI Desktop → Model view:

| From | To | Active | Many-to-One |
|------|----|----|:---:|
| Instances → AppID | Apps → AppID | ✓ | M:1 |
| Instances → FlavorName | Flavors → FlavorName | ✓ | M:1 |
| Metrics → InstanceID | Instances → InstanceID | ✓ | M:1 |
| Timeline → TotalApps | Apps table | Optional | N/A |

**Schéma:**
```
Flavors ◄─── Instances ──► Apps
                 │
             Metrics
             
Timeline ──► Apps
```

---

## 4. Mesures DAX

Créer les mesures suivantes:

### 4.1 Mesures de comptage

```dax
// Comptages par statut
Count_Critique = CALCULATE(COUNTA(Instances[InstanceID]), Instances[Status] = "CRITIQUE")
Count_SurConso = CALCULATE(COUNTA(Instances[InstanceID]), Instances[Status] = "SUR-CONSO")
Count_OK = CALCULATE(COUNTA(Instances[InstanceID]), Instances[Status] = "OK")
Count_SousConso = CALCULATE(COUNTA(Instances[InstanceID]), Instances[Status] = "SOUS-CONSO")

// Total
Count_Total = COUNTA(Instances[InstanceID])
```

### 4.2 Mesures moyennes

```dax
// CPU moyen
Avg_CPU_P95 = AVERAGE(Metrics[CPU_P95])
Avg_CPU_P90 = AVERAGE(Metrics[CPU_P90])
Avg_CPU_Overall = AVERAGE(Metrics[CPU_Avg])

// RAM moyen
Avg_RAM_P95 = AVERAGE(Metrics[RAM_P95])
Avg_RAM_P90 = AVERAGE(Metrics[RAM_P90])
Avg_RAM_Overall = AVERAGE(Metrics[RAM_Avg])
```

### 4.3 Mesures de correction

```dax
// Instances corrigées
Count_Corrected = CALCULATE(COUNTA(Instances[InstanceID]), Instances[Corrected] = "Yes")

// Taux de correction
Correction_Rate = 
    DIVIDE(
        [Count_Corrected],
        [Count_Total],
        0
    ) * 100

// Taux de correction formaté
Correction_Pct_Text = 
    FORMAT([Correction_Rate], "0.0") & "%"
```

### 4.4 Mesures dynamiques

```dax
// Titre dynamique pour slicer sélectionné
Selected_App = 
    IF(
        HASONEVALUE(Apps[AppName]),
        VALUES(Apps[AppName]),
        "All Applications"
    )

// Statut général
Overall_Status = 
    IF(
        [Count_Critique] > 0, "CRITICAL",
        IF([Count_SurConso] > [Count_Total] * 0.4, "OVERCONSUMPTION", "HEALTHY")
    )
```

### 4.5 Mesures avec conditionnelle de couleur

```dax
// Pour utiliser avec color by value
Critical_Count_Display = [Count_Critique]

// Index de santé (0-100)
Health_Index = 
    100 - (
        ([Count_Critique] / [Count_Total] * 40) +
        ([Count_SurConso] / [Count_Total] * 30) +
        ([Count_SousConso] / [Count_Total] * 20)
    )
```

---

## 5. Colonnes calculées

### Dans la table Instances

```dax
// Coût mensuel estimé
Monthly_Cost = 
    RELATED(Flavors[Cost_Monthly])

// Coût si correction appliquée
Recommended_Cost = 
    LOOKUPVALUE(
        Flavors[Cost_Monthly],
        Flavors[FlavorName], [RecFlavorName]
    )

// Économies potentielles
Potential_Savings = 
    IF(
        [Recommended_Cost] < [Monthly_Cost],
        [Monthly_Cost] - [Recommended_Cost],
        0
    )
```

### Dans la table Metrics

```dax
// Classification CPU
CPU_Status = 
    IF([CPU_P95] > 90, "CRITIQUE",
    IF([CPU_P95] > 80, "SUR-CONSO",
    IF([CPU_P95] > 50, "OK", "SOUS-CONSO")))

// Classification RAM
RAM_Status = 
    IF([RAM_P95] > 90, "CRITIQUE",
    IF([RAM_P95] > 80, "SUR-CONSO",
    IF([RAM_P95] > 50, "OK", "SOUS-CONSO")))

// Statut général (pessimiste)
Overall_Metric_Status =
    IF(
        OR([CPU_P95] > 90, [RAM_P95] > 90), "CRITIQUE",
        IF(
            OR([CPU_P95] > 80, [RAM_P95] > 80), "SUR-CONSO",
            IF(
                AND([CPU_Avg] < 10, [RAM_Avg] < 15), "SOUS-CONSO", "OK"
            )
        )
    )
```

---

## 6. Construction du Dashboard

### Page 1: Vue Globale

**Éléments:**

1. **KPI Card - Total Apps**
   - Field: COUNTA(Apps[AppID])
   - Format: #,##0
   - Color: Bleu

2. **KPI Card - Critiques**
   - Measure: Count_Critique
   - Format: #,##0
   - Color: Rouge

3. **KPI Card - Sur-Consommation**
   - Measure: Count_SurConso
   - Format: #,##0
   - Color: Orange

4. **KPI Card - Apps OK**
   - Measure: Count_OK
   - Format: #,##0
   - Color: Vert

5. **Donut Chart - Répartition statuts**
   - Legend: Instances[Status]
   - Values: Count_Critique, Count_SurConso, Count_OK, Count_SousConso
   - Colors:
     - CRITIQUE: #D32F2F (Rouge foncé)
     - SUR-CONSO: #FF6D00 (Orange)
     - OK: #00C853 (Vert)
     - SOUS-CONSO: #2196F3 (Bleu)

6. **Line Chart - Évolution apps corrigées**
   - X-axis: Timeline[Month]
   - Y-axis: Timeline[CorrectionPct]
   - Format: Line with markers

7. **Table - Top problèmes**
   - Columns:
     - Apps[AppName]
     - Apps[Domain]
     - Instances[AppID] (COUNTROWS)
     - Avg_CPU_P95
     - Avg_RAM_P95
     - Status (colour coded)
   - Sort: By status severity, then CPU desc
   - Top 8 rows

### Page 2: Détail App

**Layout:**
- Left sidebar (220px): Slicers
- Right area: KPIs + Charts + Tables

**Éléments:**

1. **Slicer - Sélectionner App**
   - Field: Apps[AppName]
   - Type: Dropdown or List
   - Default: All

2. **Slicer - Status**
   - Field: Instances[Status]
   - Type: Buttons (séparés)
   - Options: CRITIQUE, SUR-CONSO, OK, SOUS-CONSO

3. **Slicer - Percentile**
   - Custom Slicer or Buttons
   - Options: p50, p90, p95, p99

4. **KPI - Instances**
   - Count_Total (contextualisé par slicer)

5. **KPI - CPU Avg (Couleur dynamique)**
   - Avg_CPU_P90 ou selon slicer
   - Color Rules:
     - > 80: Rouge
     - > 50: Orange
     - ≤ 50: Vert

6. **KPI - RAM Avg (Couleur dynamique)**
   - Avg_RAM_P90 ou selon slicer
   - Color Rules: Identique CPU

7. **Bar Chart - Top 15 instances**
   - X: Instances[InstanceID]
   - Y: Metrics[CPU_P95] and Metrics[RAM_P95] (dual axis)
   - Colors: Selon statut

8. **Table - Instance Details**
   - Columns:
     - InstanceID (clickable pour drill-through)
     - AppName
     - FlavorName (badge)
     - CPU_P50, P90, P95, P99
     - RAM_P50, P90, P95, P99
     - Status (badge)
     - RecFlavorName (highlighted if different)

### Page 3: Instances & Config

**Éléments:**

1. **Dropdown - Filter by App**
   - Field: Apps[AppName]

2. **Dropdown - Filter by Flavor**
   - Field: Flavors[FlavorName]

3. **Bar Chart - CPU par Flavor**
   - X: Flavors[FlavorName]
   - Y: AVERAGE(Metrics[CPU_P95])
   - Colors: pctColor (gradient)

4. **Bar Chart - RAM par Flavor**
   - X: Flavors[FlavorName]
   - Y: AVERAGE(Metrics[RAM_P95])
   - Colors: pctColor (gradient)

5. **Table - Configuration complète**
   - Columns:
     - InstanceID
     - AppName
     - FlavorName
     - CPU_vCPU
     - RAM_GB
     - RecFlavorName
     - CPU_P95 (colour coded)
     - RAM_P95 (colour coded)
     - Monthly_Cost
     - Potential_Savings
   - Sort: By CPU_P95 desc
   - Conditional formatting: Highlight high values in red

---

## 7. Schémas de couleur

Aligner avec le design HTML:

```
Primary Accent:    #2196F3 (Bleu)     RGB(33,150,243)
Critical:          #D32F2F (Rouge)    RGB(211,47,47)
Warning:           #FF6D00 (Orange)   RGB(255,109,0)
Success:           #00C853 (Vert)     RGB(0,200,83)
Secondary:         #7C4DFF (Violet)   RGB(124,77,255)
Accent Cyan:       #00BCD4 (Cyan)     RGB(0,188,212)

Dark Background:   #0D1117
Surface:           #161B22
Surface Hover:     #1C2330
Border:            #2A3445
Text Primary:      #E6EDF3
Text Muted:        #8B949E
Text Dim:          #4A5568
```

### Appliquer dans Power BI:

1. Design → Themes → Customize current theme
2. Colors class: Set accent colors
3. Ou: Format → Data colors pour chaque visual

---

## 8. Interactions et Navigation

### Filtrage croisé

- **Slicer App** → Filtre tous charts/tables
- **Status buttons** → Filtre instances uniquement
- **Percentile buttons** → Change column affichée (p50/p90/p95/p99)
- **Flavor dropdown** → Filtre instances et metrics

### Drill-through

- Cliquer sur AppName → Page détail filtrée par App
- Cliquer sur InstanceID → Affiche détails instance (popup drill-through)

### Tooltips

Activer custom tooltips sur les charts avec:
- App Name
- Current values (CPU, RAM)
- Status
- Recommended action

---

## 9. Performance et Optimization

### Agrégations

Pour gros volumes de metrics (>1M rows):

1. Créer table agrégée: `Metrics_Daily_Agg`
   - GROUP BY: InstanceID, MeasureDate
   - Aggregate: AVG(CPU_P95), AVG(RAM_P95), etc.

2. Dans Model, créer agrégation:
   - Aggregations pane
   - Map Metrics_Daily_Agg columns to Metrics columns

3. Power BI utilisera l'agrégation automatiquement

### Query Folding

S'assurer que Power Query steps "fold back" à la source:

```m
// Good - folds
let Source = ... in Table.SelectColumns(Source, {"Col1", "Col2"})

// Bad - doesn't fold (appliquer en Power BI au lieu)
let Custom = ... in Table.AddColumn(Custom, "NewCol", each [Col1] * 2)
```

### RAW Incremental Refresh

Pour production avec données volumineuses:

1. Settings → Premium capacity
2. Enable incremental refresh
3. Define: Last X months → Import, older → DirectQuery

---

## 10. Distribution et Partage

### Publier sur Power BI Service

```powershell
# Via Power BI Desktop
File → Publish
Select workspace
Configure refresh schedule (daily si données live)
```

### Configurer partage

1. Service → Share button
2. Ajouter users/groups
3. Set permissions (View/Edit)

### RLS (Row-Level Security)

Pour multi-tenant (filter par Department/Domain):

```dax
[Domain] = USERNAME()
```

---

## 11. Troubleshooting

| Problème | Solution |
|----------|----------|
| CSV doesn't load | Vérifier encoding (UTF-8), separators, paths |
| Charts not updating | Check filter interactions; disable if needed |
| Slow dashboard | Profile avec Analyze in Excel; add aggregations |
| Relationships not working | Verify column names match exactly; check data types |
| Formula error in DAX | Use DAX Studio or error message to debug |
| Python script timeout | Reduce data size or optimize pandas operations |

---

## 12. Prochaines étapes

1. ✓ Exécuter `generate_data.py`
2. ✓ Charger CSVs dans Power BI
3. ✓ Appliquer Power Query transformations
4. ✓ Créer data model & relationships
5. ✓ Ajouter mesures DAX
6. ✓ Construire visualisations
7. ✓ Configurer slicers et filtres
8. ✓ Tester interactions
9. ⊕ Publier sur Service (optional)
10. ⊕ Configurer refresh schedule
