# 🆘 HELP & FAQ

## ⚡ I Just Want to Start NOW

**TL;DR - Just run these 3 commands**:

```bash
# Step 1: Generate everything (30 sec)
python scripts/full_setup.py

# Step 2: Open in Power BI Desktop
open FlavorOps_Dashboard_Template.pbix

# Step 3: Load CSVs
# Home → Transform Data → New Source → Text/CSV → Select all 5 from data/
# Then Close & Apply
```

**Time**: 3 minutes ⏱️

---

## ❓ Frequently Asked Questions

### Q1: "What do I need installed?"
**Python 3.7+** and **Power BI Desktop**. That's it!

Install pandas & numpy first:
```bash
pip install pandas numpy
```

### Q2: "Where do I start?"
1. Read: `DEMARRAGE_RAPIDE.md` (3 min)
2. Run: `python scripts/full_setup.py` (30 sec)
3. Open: `FlavorOps_Dashboard_Template.pbix` in Power BI
4. Load: 5 CSV files from `data/` folder

### Q3: "How long does setup take?"
**3 minutes total**:
- Setup script: 30 seconds
- Open Power BI & load data: 2-3 minutes

### Q4: "Can I customize it?"
**Yes!**

Edit DAX measures: `DAX_MEASURES_REFERENCE.md`
Edit data sources: `POWERQUERY_EXAMPLES.md`
Edit visuals: Power BI GUI (drag/drop)

### Q5: "How many rows of data?"
**~2000 rows total**:
- Flavors: 10
- Apps: 15
- Instances: ~50
- Metrics: ~1500
- Timeline: 14

### Q6: "Can I use this on Power BI Service (cloud)?"
**Yes!** After loading in Desktop:
- File → Publish
- Choose workspace
- Configure refresh schedule
- Share with team

### Q7: "What if it doesn't work?"
Check: **TROUBLESHOOTING.md**

Or see the **"Common Issues"** section below.

---

## 🔴 Common Issues & Solutions

### Issue: "ModuleNotFoundError: No module named 'pandas'"

**Solution**:
```bash
pip install pandas numpy
```

Then retry the script.

---

### Issue: "Python command not found"

**Solution**:
1. Verify Python installed: `python --version`
2. If not: Download from https://www.python.org
3. Try: `python3` instead of `python`
4. Or use full path: `/usr/bin/python3`

---

### Issue: CSV files not created

**Solution**:
1. Check write permissions in project folder
2. Verify Python has no errors during run
3. Check `data/` directory exists: `ls -la data/`
4. Try running `generate_data.py` separately:
   ```bash
   python scripts/generate_data.py
   ```

---

### Issue: "No data" in Power BI dashboard

**Solution**:
1. Refresh: Ctrl+R (Cmd+R Mac)
2. Check Data tab: Verify tables loaded
3. Check relationships: Model → Manage Relationships
4. Check measures: View table columns

---

### Issue: "Relationship errors" or "Missing tables"

**Solution**:
1. Go to: Model tab (top ribbon)
2. Click: Manage Relationships
3. Verify all relationships exist:
   - Instances.AppID → Apps.AppID
   - Instances.FlavorName → Flavors.FlavorName
   - Metrics.InstanceID → Instances.InstanceID
   - Timeline.AppID → Apps.AppID

---

### Issue: "Colors not showing correctly"

**Solution**:
1. Close Power BI & reopen
2. Apply theme again:
   - Format → Theme → GitHub Dark
3. Or configure manually:
   - Refer to `.powerbi_config.json` for colors

---

### Issue: "Template file (.pbix) not created"

**Solution**:
1. Check if template already exists:
   ```bash
   ls -la FlavorOps_Dashboard_Template.pbix
   ```

2. If not, verify script ran without errors
3. Try running manually:
   ```bash
   python scripts/create_powerbi_template.py
   ```

4. Check disk space: `df -h` (Mac/Linux)

---

### Issue: "Import Error" when running script

**Solution**:
1. Check Python version: `python --version` (Need 3.7+)
2. Install dependencies:
   ```bash
   pip install pandas numpy
   ```

3. Try upgrading pip:
   ```bash
   pip install --upgrade pip
   ```

---

## 📚 Documentation Quick Links

| Need | Read | Time |
|------|------|------|
| Just start | DEMARRAGE_RAPIDE.md | 3 min |
| Understand setup | POWERBI_TEMPLATE_GUIDE.md | 10 min |
| Learn everything | POWERBI_COMPLETE_GUIDE.md | 2 hours |
| See all formulas | DAX_MEASURES_REFERENCE.md | 1 hour |
| Detailed index | INDEX_COMPLET.md | 5 min |
| Troubleshooting | TROUBLESHOOTING.md | 5-30 min |
| Validate vs original | COMPARAISON_HTML_vs_POWERBI.md | 10 min |

---

## 🎯 Step-by-Step Walkthrough

### Walkthrough 1: First Time Setup

**Step 1**: Open Terminal/CMD and navigate to project:
```bash
cd /Users/haris/Documents/PROJECTS/powerbi
```

**Step 2**: Run one-click setup:
```bash
python scripts/full_setup.py
```

**Step 3**: Verify files created:
```bash
ls -la data/
# Should see: apps.csv, instances.csv, flavors.csv, metrics.csv, timeline.csv
```

**Step 4**: Open Power BI Desktop

**Step 5**: File → Open → `FlavorOps_Dashboard_Template.pbix`

**Step 6**: When prompted to load data:
- Home → Transform Data
- New Source → Text/CSV
- Browse to `data/` folder
- Select: `flavors.csv` → Load
- Select: `apps.csv` → Load
- Select: `instances.csv` → Transform Data
- Select: `metrics.csv` → Transform Data
- Select: `timeline.csv` → Load

**Step 7**: Home → Close & Apply

✅ **DONE!** Your dashboard is live!

---

### Walkthrough 2: Customizing the Dashboard

**1. Change Colors**:
- Format (ribbon) → Theme
- Choose or customize colors
- Refer to `.powerbi_config.json` for hex codes

**2. Edit Measures**:
- Model tab → See table
- Click measure to edit
- Refer to `DAX_MEASURES_REFERENCE.md` for formulas

**3. Add Visualizations**:
- Insert → [Chart type]
- Drag fields from Fields pane
- Format as desired

**4. Create New Page**:
- Insert → New Page
- Name it
- Add visuals

---

### Walkthrough 3: Deploying to Power BI Service

**Prerequisites**: Power BI Pro subscription

**Steps**:
1. In Power BI Desktop: Home → Publish
2. Select workspace (or create new)
3. Wait for upload
4. Go to Power BI Service website
5. Configure:
   - Settings → Scheduled Refresh
   - Set schedule (daily/hourly)
6. Share:
   - Report → Share
   - Enter email addresses
   - Send

---

## 🆘 Getting Help

### Reading Files

**For quick answers**: Search the documentation
- DEMARRAGE_RAPIDE.md (French quick start)
- TROUBLESHOOTING.md (Common issues)
- FAQ sections in POWERBI_COMPLETE_GUIDE.md

### Running Scripts

**If script fails**:
```bash
# Run with verbose output
python -v scripts/full_setup.py

# Or run components separately
python scripts/generate_data.py
python scripts/create_powerbi_template.py
```

### Power BI Specific

**In Power BI Desktop**:
- Help → Getting Started
- Help → Power BI Support
- File → Options → Reliability

### External Resources

- Microsoft Power BI Docs: https://docs.microsoft.com/power-bi
- DAX Guide: https://dax.guide
- Power Query: https://docs.microsoft.com/power-query

---

## ✅ Verification Checklist

After following the guide, verify:

- [ ] Python 3.7+ installed
- [ ] pandas & numpy installed
- [ ] 5 CSV files in `data/` folder
- [ ] `FlavorOps_Dashboard_Template.pbix` exists
- [ ] Power BI Desktop can open the template
- [ ] CSV files loaded into Power BI
- [ ] Dashboard pages are visible
- [ ] KPI cards show values
- [ ] Charts render properly
- [ ] Slicers are interactive

If all ✅, **you're ready!**

---

## 🎓 Learning Resources

### Beginner Level (1-2 hours)
- DEMARRAGE_RAPIDE.md
- QUICKSTART_READY.md
- Explore the dashboard in Power BI

### Intermediate Level (4-6 hours)
- POWERBI_TEMPLATE_GUIDE.md
- POWERBI_COMPLETE_GUIDE.md (Sections 1-6)
- DAX_MEASURES_REFERENCE.md (Basic)

### Advanced Level (8+ hours)
- POWERBI_COMPLETE_GUIDE.md (All)
- DAX_MEASURES_REFERENCE.md (All)
- POWERQUERY_EXAMPLES.md
- Microsoft Docs & External resources

---

## 💡 Pro Tips

1. **Backup your work**:
   ```bash
   cp FlavorOps_Dashboard_Template.pbix FlavorOps_Dashboard_Template.backup.pbix
   ```

2. **Refresh data regularly**:
   - Regenerate CSVs: `python scripts/generate_data.py`
   - In Power BI: Home → Refresh

3. **Use Bookmarks**:
   - Insert → Bookmark
   - Save dashboard states
   - Quick navigation

4. **Monitor Performance**:
   - Check query times
   - Optimize DAX measures
   - See POWERBI_COMPLETE_GUIDE.md for tips

5. **Version Control** (Optional):
   ```bash
   git init
   git add .
   git commit -m "Initial FlavorOps Power BI setup"
   ```

---

## 🚀 Next Steps

### Today
- [ ] Run `python scripts/full_setup.py`
- [ ] Open template in Power BI
- [ ] Load CSV files
- [ ] Explore the dashboard

### This Week
- [ ] Read POWERBI_TEMPLATE_GUIDE.md
- [ ] Learn key features
- [ ] Customize if needed

### This Month
- [ ] Deploy to Power BI Service
- [ ] Share with team
- [ ] Set up automatic refresh
- [ ] Monitor usage

---

**Need Help?**
- Start with: DEMARRAGE_RAPIDE.md
- Then check: TROUBLESHOOTING.md
- Finally: Review appropriate section in POWERBI_COMPLETE_GUIDE.md

**Still stuck?**
- Review the error message carefully
- Check "Common Issues" above
- Search documentation files
- Refer to external resources

---

**Version**: 1.0  
**Last Updated**: 2024  
**Status**: ✅ Complete  

**Good luck! 🎉**
