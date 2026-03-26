# Power BI Dashboard - Flavor Optimization
## Guide de setup complet

---

## 📁 Fichiers fournis
- `PowerBI_FlavorOptimization_Data.xlsx` → Source de données (4 feuilles)
- Ce guide → Instructions + DAX Measures

---

## 1. Importer les données

1. Ouvrir **Power BI Desktop**
2. **Accueil → Obtenir des données → Excel**
3. Sélectionner `PowerBI_FlavorOptimization_Data.xlsx`
4. Cocher les 4 tables : `Apps`, `Instances`, `AppSummary`, `EvolutionMensuelle`
5. Cliquer **Charger**

---

## 2. Modèle de données (Relations)

Dans **Vue Modèle**, créer les relations :
- `Apps[AppID]` → `Instances[AppID]` (1 à plusieurs)
- `Apps[AppID]` → `AppSummary[AppID]` (1 à 1)

---

## 3. Mesures DAX à créer

### Table de mesures : créer une table vide "Measures"
> Modélisation → Nouvelle Table → `Measures = {}`

```dax
// ── Comptages globaux ──────────────────────────────────────

Total Apps = DISTINCTCOUNT(Apps[AppID])

Total Instances = COUNTROWS(Instances)

Apps Critiques = 
CALCULATE(
    DISTINCTCOUNT(AppSummary[AppID]),
    AppSummary[AppStatus] = "CRITIQUE"
)

Apps Sur-Conso = 
CALCULATE(
    DISTINCTCOUNT(AppSummary[AppID]),
    AppSummary[AppStatus] = "SUR-CONSO"
)

Apps OK = 
CALCULATE(
    DISTINCTCOUNT(AppSummary[AppID]),
    AppSummary[AppStatus] = "OK"
)

Apps Sous-Conso = 
CALCULATE(
    DISTINCTCOUNT(AppSummary[AppID]),
    AppSummary[AppStatus] = "SOUS-CONSO"
)

Apps Corrigées Total = 
CALCULATE(
    DISTINCTCOUNT(AppSummary[AppID]),
    AppSummary[FlavorsCorrected] > 0
)

// ── Taux ──────────────────────────────────────────────────

Taux Correction % = 
DIVIDE([Apps Corrigées Total], [Total Apps], 0) * 100

Taux Sur-Conso % = 
DIVIDE([Apps Sur-Conso] + [Apps Critiques], [Total Apps], 0) * 100

// ── Métriques CPU/RAM par instance ────────────────────────

CPU P95 Moyen = AVERAGE(Instances[CPU_p95])
RAM P95 Moyen = AVERAGE(Instances[RAM_p95])
CPU P99 Moyen = AVERAGE(Instances[CPU_p99])
RAM P99 Moyen = AVERAGE(Instances[RAM_p99])

// ── Indicateurs de sur-consommation ───────────────────────

Instances Sur-Conso = 
CALCULATE(
    COUNTROWS(Instances),
    Instances[Status] = "SUR-CONSO" || Instances[Status] = "CRITIQUE"
)

Instances Critiques = 
CALCULATE(
    COUNTROWS(Instances),
    Instances[Status] = "CRITIQUE"
)

Instances OK = 
CALCULATE(
    COUNTROWS(Instances),
    Instances[Status] = "OK"
)

// ── Sélection percentile dynamique (avec slicer) ──────────
// Créer une table paramètre : Modélisation → Nouveau paramètre
// Nom: "Percentile", valeurs: p50, p90, p95, p99

CPU Percentile Sélectionné = 
SWITCH(
    SELECTEDVALUE('Percentile'[Percentile]),
    "p50", AVERAGE(Instances[CPU_p50]),
    "p90", AVERAGE(Instances[CPU_p90]),
    "p95", AVERAGE(Instances[CPU_p95]),
    "p99", AVERAGE(Instances[CPU_p99]),
    AVERAGE(Instances[CPU_p95])  -- défaut p95
)

RAM Percentile Sélectionné = 
SWITCH(
    SELECTEDVALUE('Percentile'[Percentile]),
    "p50", AVERAGE(Instances[RAM_p50]),
    "p90", AVERAGE(Instances[RAM_p90]),
    "p95", AVERAGE(Instances[RAM_p95]),
    "p99", AVERAGE(Instances[RAM_p99]),
    AVERAGE(Instances[RAM_p95])
)

// ── Évolution : Correction cumulative ─────────────────────

Tendance Correction = 
VAR LastMonth = MAX(EvolutionMensuelle[Mois])
VAR PrevMonth = CALCULATE(
    MAX(EvolutionMensuelle[Mois]),
    FILTER(EvolutionMensuelle, EvolutionMensuelle[Mois] < LastMonth)
)
RETURN
CALCULATE(SUM(EvolutionMensuelle[AppsCorrigees]), EvolutionMensuelle[Mois] = LastMonth)
- CALCULATE(SUM(EvolutionMensuelle[AppsCorrigees]), EvolutionMensuelle[Mois] = PrevMonth)
```

---

## 4. Structure des pages

### Page 1 : "Vue Globale" (Main Dashboard)
```
┌─────────────────────────────────────────────────────────┐
│  KPI Cards: Total Apps | Critiques | Sur-Conso | OK     │
├──────────────────────────┬──────────────────────────────┤
│  Graphique Anneau        │  Courbe Évolution            │
│  (Statut des Apps)       │  (Apps corrigées / mois)     │
│                          │                              │
├──────────────────────────┴──────────────────────────────┤
│  Tableau : Top 5 apps les plus problématiques           │
└─────────────────────────────────────────────────────────┘
```

**Graphique Anneau** :
- Valeurs : `[Apps Critiques]`, `[Apps Sur-Conso]`, `[Apps OK]`, `[Apps Sous-Conso]`
- Couleurs : Rouge foncé (#B00020), Orange (#FF6D00), Vert (#2E7D32), Bleu (#1565C0)
- Légende : activée

**Courbe Évolution** :
- Source : table `EvolutionMensuelle`
- Axe X : `Mois`
- Valeurs : `AppsCorrigees`, `AppsCritiques`, `AppsSurConso`
- Activer les marqueurs

---

### Page 2 : "Détail par App"
```
┌─────────────────────────────────────────────────────────┐
│  Slicer : Liste déroulante Apps (AppName)               │
├──────────┬──────────────────────────────────────────────┤
│ Slicer   │  KPIs : Instances | CPU p95 | RAM p95        │
│ Percentile│                                             │
│ (p50/    ├──────────────────────────────────────────────┤
│  p90/    │  Tableau Instances avec colonnes :           │
│  p95/    │  InstanceID | Flavor | CPU% | RAM% | Status │
│  p99)    │  + Mise en forme conditionnelle              │
└──────────┴──────────────────────────────────────────────┘
```

**Slicer Apps** : Type = Liste déroulante, champ = `Apps[AppName]`
**Slicer Percentile** : Type = Liste, champ = `Percentile[Percentile]`

---

### Page 3 : "Instances & Config"
```
┌─────────────────────────────────────────────────────────┐
│  Slicers : App | Statut | Flavor actuel                 │
├─────────────────────────────────────────────────────────┤
│  Tableau complet des instances :                        │
│  InstanceID | App | Flavor | CPU vCPUs | RAM GB |       │
│  CPU_p50 | CPU_p90 | CPU_p95 | CPU_p99 |               │
│  RAM_p50 | RAM_p90 | RAM_p95 | RAM_p99 |               │
│  Statut | Flavor Recommandé | Corrigé ?                 │
├─────────────────────────────────────────────────────────┤
│  Barres : CPU P95 et RAM P95 par instance               │
└─────────────────────────────────────────────────────────┘
```

---

## 5. Mise en forme conditionnelle

### Colonne "Status" dans les tableaux :
- `CRITIQUE` → Fond rouge (#FFCDD2), texte rouge foncé (#B71C1C)
- `SUR-CONSO` → Fond orange (#FFE0B2), texte orange (#E65100)
- `OK` → Fond vert (#C8E6C9), texte vert (#1B5E20)
- `SOUS-CONSO` → Fond bleu clair (#BBDEFB), texte bleu (#0D47A1)

### Colonnes CPU_p95 / RAM_p95 :
- > 90 : Rouge
- 80-90 : Orange
- 50-80 : Vert
- < 50 : Bleu

---

## 6. Paramètre Percentile (slicer dynamique)

1. **Modélisation → Nouveau paramètre → Champ**
2. Nom : `Percentile`
3. Type : Texte
4. Valeurs : `p50`, `p90`, `p95`, `p99`
5. Ce slicer change automatiquement les métriques affichées via les mesures DAX ci-dessus

---

## 7. Thème couleurs recommandé

JSON à importer via **Affichage → Thèmes → Parcourir** :
```json
{
  "name": "FlavorOps Dark",
  "dataColors": ["#1565C0","#2E7D32","#FF6D00","#B00020","#6A1B9A","#00838F"],
  "background": "#FAFAFA",
  "foreground": "#1E3A5F",
  "tableAccent": "#1565C0",
  "visualStyles": {
    "card": {
      "*": {"labels": [{"color": {"solid": {"color": "#1E3A5F"}}}]}
    }
  }
}
```

---

## Checklist finale
- [ ] 4 tables importées et relations créées
- [ ] Toutes les mesures DAX créées dans la table "Measures"
- [ ] Paramètre Percentile créé
- [ ] 3 pages créées avec les bons visuels
- [ ] Mise en forme conditionnelle appliquée sur Status et percentiles
- [ ] Thème couleur importé
- [ ] Publier sur Power BI Service (optionnel)
