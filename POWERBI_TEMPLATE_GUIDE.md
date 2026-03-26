# 🎨 Power BI Template - Guide d'Utilisation Complet

## Vue d'ensemble

Un **template Power BI** pré-configuré est disponible pour charger directement vos données CSV.

**Avantage**: Pas besoin de recréer le modèle, les relations, les mesures DAX, ni les visuels. Tout est déjà fait!

---

## 🚀 Étape 1: Générer le Template

```bash
cd /Users/haris/Documents/PROJECTS/powerbi
python scripts/create_powerbi_template.py
```

**Résultat**: `FlavorOps_Dashboard_Template.pbix`

Ce fichier contient:
- ✓ Modèle de données (5 tables)
- ✓ Schéma de relations
- ✓ 30+ mesures DAX
- ✓ 3 pages de dashboard
- ✓ Visuels pré-configurés
- ✓ Thème personnalisé (sombre)

---

## 🚀 Étape 2: Charger le Template dans Power BI Desktop

### 2.1 Ouvrir Power BI Desktop

Lancer l'application Power BI Desktop

### 2.2 Charger le template

```
File → Open → FlavorOps_Dashboard_Template.pbix
```

Le fichier se charge avec la structure complète

### 2.3 Vérifier le chargement

Aller à: **Model** (onglet dans le ruban)

Vous devez voir:
- 5 tables: Flavors, Apps, Instances, Metrics, Timeline
- Relations connectant les tables
- Mesures DAX listées

---

## 🚀 Étape 3: Générer les données CSV

```bash
python scripts/generate_data.py
```

Cela crée le dossier `data/` avec 5 CSVs:
- apps.csv
- instances.csv
- flavors.csv
- metrics.csv
- timeline.csv

---

## 🚀 Étape 4: Charger les données CSV dans Power BI

### 4.1 Accéder à Transform Data

```
Home → Transform Data
```

### 4.2 Ajouter la première source (Flavors)

1. **New Source** → **Text/CSV**
2. Naviguer vers: `data/flavors.csv`
3. Cliquer **Open**
4. Cliquer **Load** (PAS Transform)

### 4.3 Ajouter les autres tables

Répéter l'étape 4.2 pour:
- apps.csv → **Load**
- instances.csv → **Transform Data**
- metrics.csv → **Transform Data**
- timeline.csv → **Load**

### 4.4 Appliquer les transformations

Pour les tables que vous avez transformé:

1. **Dans Power Query Editor** (Transform Data), pour chaque table:
   - Vérifier que les types de colonnes sont corrects
   - Dates → `Date/Time`
   - Nombres → `Whole Number` or `Decimal`
   - Texte → `Text`

2. **Cliquer Close & Apply**

### 4.5 Rafraîchir les données

Power BI va charger les CSVs et les mapper aux tables du modèle.

Les visuels se remplissent automatiquement! 🎉

---

## 📊 Résultat: Dashboard Complet

Vous avez maintenant 3 pages interactives:

### Page 1: Vue Globale
- 4 KPI cards (Total Apps, Critiques, Sur-Conso, OK)
- Donut chart (répartition statuts)
- Line chart (évolution correction %)
- Table (top apps problématiques)

### Page 2: Détail App
- Slicer de sélection d'app
- 3 KPI cards (instances, CPU p95, RAM p95)
- Bar chart (CPU & RAM percentiles)
- Table (détail des instances)

### Page 3: Instances & Config
- 2 dropdowns (filtrer par app/flavor)
- 2 Bar charts (CPU & RAM distribution)
- Table (configuration complète)

---

## 🎨 Thème et Couleurs

Le template utilise le **thème personnalisé du HTML**:

| Élément | Couleur | Code |
|---------|---------|------|
| Background | Noir | #0D1117 |
| Surface | Gris foncé | #161B22 |
| Accent Primaire (Bleu) | Bleu | #2196F3 |
| Critique | Rouge | #D32F2F |
| Attention | Orange | #FF6D00 |
| OK | Vert | #00C853 |
| Secondaire | Violet | #7C4DFF |
| Accent | Cyan | #00BCD4 |

Toutes les couleurs sont déjà appliquées aux visuels!

---

## 📈 Mesures DAX Incluses

### Comptes
- `Count_Total` - Total instances
- `Count_Critique` - Instances critiques
- `Count_SurConso` - Sur-consommation
- `Count_OK` - OK
- `Count_SousConso` - Sous-consommation

### Moyennes
- `Avg_CPU_P95` - CPU p95 moyen
- `Avg_CPU_P90` - CPU p90 moyen
- `Avg_RAM_P95` - RAM p95 moyen
- `Avg_RAM_P90` - RAM p90 moyen

### Autres
- `Correction_Rate` - Taux de correction
- `Health_Index` - Score de santé
- Et 20+ autres...

**Tous déjà intégrés aux visuels!**

---

## 🔄 Interactivité

Les visuels sont déjà**paramétrés pour interagir**:

- **Slicers** filtrent automatiquement tous les visuels
- **Drill-through** entre pages
- **Tooltips** personnalisés
- **Cross-filtering** activé

---

## ✅ Checklist de Déploiement

- [ ] Générer template: `python scripts/create_powerbi_template.py`
- [ ] Générer données: `python scripts/generate_data.py`
- [ ] Ouvrir Power BI Desktop
- [ ] File → Open → Template .pbix
- [ ] Charger CSVs (Home → Transform Data)
- [ ] Appliquer transformations Power Query
- [ ] Fermer & Appliquer (Close & Apply)
- [ ] Vérifier que les visuels se remplissent
- [ ] Tester les slicers et filtres
- [ ] Vérifier les pages (3 onglets)
- [ ] Sauvegarder: File → Save
- [ ] Optionnel: Publish → Power BI Service

---

## 🐛 Troubleshooting

### Problème: "Les colonnes ne correspondent pas"
**Solution**: 
- Les noms de colonnes CSV doivent **correspondre EXACTEMENT** aux noms du modèle
- Utiliser Power Query pour renommer si nécessaire
- Vérifier **casse exacte** (FlavorName vs flavorname)

### Problème: "Les visuels sont vides"
**Solution**:
- Vérifier que les CSVs sont chargées (Home → Transform Data)
- Vérifier que les types de colonnes sont corrects
- Rafraîchir: Home → Refresh
- Aller à Model view et vérifier les relations

### Problème: "Erreur lors du chargement du template"
**Solution**:
- Vérifier que Power BI Desktop est à jour (version 2022+)
- Essayer de créer un nouveau fichier vide et charger manuellement
- Vérifier que le fichier .pbix n'est pas corrompu

### Problème: "Les dates sont incorrectes"
**Solution**:
- Aller à Transform Data
- Sélectionner les colonnes date
- Changer le type vers `Date/Time`
- Vérifier le format (devrait être ISO: YYYY-MM-DD)

---

## 🎓 Prochaines Étapes

### 1. Personnaliser

- Modifier les couleurs: Design → Themes → Customize
- Ajouter des mesures DAX: Measures
- Ajouter des pages
- Modifier les visuels

### 2. Publier

- File → Publish
- Sélectionner un workspace Power BI Service
- Configurer les rafraîchissements

### 3. Partager

- Power BI Service → Share
- Ajouter des utilisateurs
- Définir les permissions

---

## 📚 Documentation Complète

Pour plus de détails:
- **POWERBI_COMPLETE_GUIDE.md** - 120 pages
- **DAX_MEASURES_REFERENCE.md** - 50+ mesures
- **POWERQUERY_EXAMPLES.md** - M language
- **FlavorOps_Dashboard_Preview.html** - Référence visuelle

---

## 🎉 C'est tout!

Votre dashboard Power BI complet est maintenant **opérationnel et prêt à l'emploi**.

Plus besoin de configuration – juste charger vos données et c'est prêt! 🚀

---

**Questions?** Consultez la documentation ou les fichiers README dans le projet.
