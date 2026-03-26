# ⚡ DÉMARRAGE RAPIDE - 3 MINUTES

**Vous avez un Power BI Dashboard complet et prêt à l'emploi.**

---

## 🚀 Étape 1: ONE-CLICK Setup (30 secondes)

Ouvrez Terminal/CMD et exécutez:

```bash
cd /Users/haris/Documents/PROJECTS/powerbi
python scripts/full_setup.py
```

✅ Cela crée:
- 5 fichiers CSV de données
- Template Power BI prêt à charger  
- Fichiers de configuration

---

## 📊 Étape 2: Charger dans Power BI (1 minute)

1. **Ouvrir Power BI Desktop**

2. **Fichier → Ouvrir**
   ```
   FlavorOps_Dashboard_Template.pbix
   ```

3. **Accueil → Transformer les données**

4. **Nouvelle source → CSV**
   - Accédez au dossier `data/`
   - Chargez **chaque fichier**:
     1. flavors.csv → Charger
     2. apps.csv → Charger
     3. instances.csv → Transformer les données
     4. metrics.csv → Transformer les données
     5. timeline.csv → Charger

5. **Accueil → Fermer et appliquer**

🎉 **TERMINÉ!** Votre dashboard est actif!

---

## ✅ Vérification Rapide

Après le chargement:

| Élément | À vérifier |
|---------|-----------|
| **Vue Globale** | 4 boîtes de KPI avec nombres |
| **Graphique Donut** | Doit afficher les statuts |
| **Tableau** | Affiche instances et données |
| **Slicers** | Peuvent être cliqués |

---

## 📁 Fichiers Clés

```
powerbi/
├── FlavorOps_Dashboard_Template.pbix ← Ouvrir ici
├── data/
│   ├── apps.csv           ← Charger ici
│   ├── instances.csv
│   ├── flavors.csv
│   ├── metrics.csv
│   └── timeline.csv
└── scripts/
    ├── full_setup.py      ← Exécuter ici (une fois)
    └── generate_data.py   ← Rafraîchir données
```

---

## 🎨 Tableau de Bord Inclus

| Page | Contenu |
|------|---------|
| **Vue Globale** | KPIs, graphique tendance, distribution |
| **Détail App** | Filtres + données par application |
| **Instances & Config** | Liste complète + graphiques |

**Couleurs** (Dark Theme):
- 🔵 Bleu = Info principale
- 🔴 Rouge = Critique
- 🟠 Orange = Alerte
- 🟢 Vert = OK

---

## 💡 Astucieux

### Rafraîchir les données
```bash
python scripts/generate_data.py
```
Puis dans Power BI: `Accueil → Actualiser`

### Voir Les Formules DAX
Dans Power BI:
```
Accueil → Affichage des modèles
→ Instances → Regarder les mesures
```

### Modifier les Couleurs
```
Format → Thème → Personnalisé
(Colors définis dans FINAL_SETUP_SUMMARY.md)
```

---

## ❓ Problèmes Courants

### "Python introuvable"
```bash
# Installer Python 3.7+
# https://www.python.org/downloads/

# Puis installer dépendances:
pip install pandas numpy
```

### "Fichiers CSV non trouvés"
Vérifiez que `data/` contient 5 fichiers CSV.

### "Pas de données dans graphs"
1. Actualiser: Ctrl+R (Windows) ou Cmd+R (Mac)
2. Vérifier: Onglet Données → Vue d'ensemble

### "Erreur de relation"
Allez à: Modélisation → Gérer les relations
Vérifiez que toutes les relations sont présentes.

---

## 📚 Documentation Complète

| Document | Quand l'utiliser |
|----------|-----------------|
| Ce fichier | Premier démarrage (vous êtes ici) |
| `POWERBI_TEMPLATE_GUIDE.md` | Pour les détails d'utilisation |
| `DAX_MEASURES_REFERENCE.md` | Pour modifier les formules |
| `POWERBI_COMPLETE_GUIDE.md` | Pour approfondir |

---

## 🎯 Résumé en 3 Points

1. ✅ **Exécuter**: `python scripts/full_setup.py`
2. ✅ **Ouvrir**: `FlavorOps_Dashboard_Template.pbix` 
3. ✅ **Charger**: 5 fichiers CSV du dossier `data/`

**C'est tout!** 🎉

---

**Questions?** Consultez `FINAL_SETUP_SUMMARY.md` pour plus de détails.

**Besoin d'aide?** Voir `POWERBI_TEMPLATE_GUIDE.md` section "Dépannage".
