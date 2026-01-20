# Quarto + VS Code Workflow

## Summary

This project is configured so that:
- ✅ **Quarto renders always use the `python3` kernel** (conda base)
- ✅ **VS Code Interactive Window can use any kernel you select**
- ✅ **No environment contamination between the two**

## ⚠️ Critical: The YAML Configuration

**Every `.qmd` file MUST include this line:**
```yaml
jupyter: python3
```

Without this, Quarto will default to whatever kernel it finds first (often `netml-311`), causing the PyYAML error.

---

## Configuration Files

### 1. **`.quarto.yml`** (Project Level)
```yaml
project:
  type: default

execute:
  daemon: false
  eval: true
```
- Minimal config, no engine specified
- Lets each document control its own execution

### 2. **`.qmd` YAML Header** (Document Level)
```yaml
---
title: "My Assignment"
author: "Your Name"
format: pdf
jupyter: python3
---
```
- **`jupyter: python3`** forces use of the `python3` kernel
- The `python3` kernel points to `/Users/chrislowzx/miniconda3/bin/python`
- This ensures base conda environment is always used for rendering

### 3. **`.vscode/settings.json`** (VS Code)
```json
{
  "python.defaultInterpreterPath": "/Users/chrislowzx/miniconda3/bin/python",
  "notebook.defaultInterpreterPath": "/Users/chrislowzx/miniconda3/bin/python"
}
```
- Sets default Python to conda base
- Prevents auto-selection of other kernels

---

## Workflow

### **For Homework Assignments**

1. **Create `.qmd` file** with this template:
   ```yaml
   ---
   title: "Assignment Title"
   author: "Your Name"
   format: pdf
   jupyter: python3
   ---
   ```

2. **Write code** in Python code blocks:
   ````markdown
   ```{python}
   import numpy as np
   print("Hello!")
   ```
   ````

3. **Render to PDF**:
   ```bash
   quarto render homework.qmd
   ```

### **For Interactive Exploration**

You can still use VS Code's **Interactive Window** or **Jupyter notebooks**:

1. **Run Python Cells Interactively**: 
   - Click "Run Cell" in VS Code (uses current kernel selection)
   - Select any kernel you want (`netml-311`, `python3`, etc.)

2. **This won't affect Quarto renders**:
   - Quarto always uses `jupyter: python3` from the YAML
   - VS Code kernel selection only affects interactive sessions

---

## Troubleshooting

### **Problem: Quarto uses wrong kernel**

**Solution**: Check your YAML header has `jupyter: python3`:
```yaml
---
jupyter: python3
---
```

### **Problem: Module not found during render**

**Solution**: Verify `python3` kernel uses base conda:
```bash
jupyter kernelspec list
cat $(jupyter --data-dir)/kernels/python3/kernel.json
```

Should show: `"/Users/chrislowzx/miniconda3/bin/python"`

### **Problem: VS Code keeps changing kernel**

**Solution**: 
1. Kernel selection in VS Code only affects interactive runs
2. Quarto renders ignore VS Code's kernel choice
3. No need to restart — they're separate execution paths

---

## Why This Works

**Quarto** and **VS Code Interactive** use **different execution mechanisms**:

| Tool | Execution Path | Configuration |
|------|---------------|---------------|
| **Quarto render** | Reads `jupyter: python3` from YAML | Always uses `python3` kernel |
| **VS Code Interactive** | Uses active kernel selection | You can choose any kernel |

They don't interfere with each other because:
- Quarto spawns its own Jupyter process based on the YAML
- VS Code's kernel selection only affects the Interactive Window
- Each `.qmd` file explicitly declares which kernel to use

---

## Template for New Assignments

```yaml
---
title: "Assignment N"
author: "Chris Low"
format: pdf
jupyter: python3
---

## Problem 1

```{python}
# Your code here
import numpy as np
```
```

Save this as `hwN.qmd`, then run:
```bash
quarto render hwN.qmd
```
