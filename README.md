# Aedes UML Framework

A reproducible, UML-based conceptual modeling framework for *Aedes* mosquito population dynamics, specified using PlantUML.

> **Associated manuscript:**  
> "A Reproducible UML-Based Framework for Conceptual Modeling of *Aedes* Population Dynamics"  
> Submitted to *Environmental Modelling and Software*

---

## Overview

This repository provides all materials needed to reproduce and extend the UML conceptual framework described in the manuscript. The framework formalises the structure, life-cycle dynamics, ecological processes, and environmental interactions of *Aedes* population systems as version-controlled, text-based UML diagrams. It supports consistent translation to ordinary differential equation (ODE), stage-structured matrix, and individual-based (IBM) models.

---

## Repository Structure

```
aedes-uml-framework/
├── plantuml/                  # PlantUML source files
│   ├── AedesClassDiagram.puml
│   ├── AedesStateMachine.puml
│   ├── AedesActivityDiagram.puml
│   ├── AedesSequenceDiagram.puml
│   ├── SimplifiedOverview.puml
│   └── figures/               # Rendered PNG/PDF/SVG outputs
│
├── figures/                   # High-resolution PNG/PDF copies for manuscript
│
├── code_generators/           # Skeleton code generators
│   ├── generate_python_ode.py     # Python ODE model skeleton (scipy)
│   ├── generate_r_matrix.R        # R stage-structured matrix model skeleton
│   └── generate_netlogo.nls       # NetLogo individual-based model skeleton
│
├── supplementary/             # Supplementary materials
│   ├── S1_questionnaire.md        # Expert evaluation questionnaire
│   ├── S2_uml_lite_guide.md       # UML-lite quick-start guide
│   ├── S3_assumption_analysis.md  # Quantitative assumption analysis results
│   └── S4_terminology_mapping.md  # Ecological terminology mapping table
│
└── scripts/                   # Utility scripts
    ├── render_figures.sh          # Render all PlantUML diagrams
    └── render_figures_path.sh     # Render with custom PlantUML path
```

---

## Prerequisites

### Viewing and editing UML diagrams

- [PlantUML](https://plantuml.com/) ≥ 1.2024.3  
- Java 8+ (required by PlantUML)  
- Optional: VS Code with the [PlantUML extension](https://marketplace.visualstudio.com/items?itemName=jebbs.plantuml)

### Rendering diagrams

```bash
# Install PlantUML (Debian/Ubuntu)
sudo apt-get install plantuml

# Or download the JAR directly
wget https://github.com/plantuml/plantuml/releases/latest/download/plantuml.jar
```

### Code generators

| Generator | Language | Requirements |
|-----------|----------|-------------|
| `generate_python_ode.py` | Python 3.8+ | `numpy`, `scipy` |
| `generate_r_matrix.R` | R 4.0+ | `Matrix` package |
| `generate_netlogo.nls` | NetLogo 6.x | [NetLogo](https://ccl.northwestern.edu/netlogo/) |

---

## Quick Start

### 1. Render all UML diagrams

```bash
cd scripts
chmod +x render_figures.sh
./render_figures.sh
```

Rendered images will be placed in `plantuml/figures/`.

### 2. Generate a model skeleton

**Python ODE model:**
```bash
python code_generators/generate_python_ode.py > aedes_ode_model.py
```

**R matrix model:**
```bash
Rscript code_generators/generate_r_matrix.R > aedes_matrix_model.R
```

**NetLogo IBM:**  
Open `code_generators/generate_netlogo.nls` directly in NetLogo 6.x.

### 3. Explore the UML diagrams

Open any `.puml` file in your PlantUML-enabled editor, or render manually:

```bash
java -jar plantuml.jar plantuml/AedesClassDiagram.puml
```

---

## UML Diagram Descriptions

| Diagram | File | Purpose |
|---------|------|---------|
| Class diagram | `AedesClassDiagram.puml` | System structure: life stages, environment, control |
| State machine | `AedesStateMachine.puml` | Life-cycle transitions and diapause logic |
| Activity diagram | `AedesActivityDiagram.puml` | Daily simulation workflow |
| Sequence diagram | `AedesSequenceDiagram.puml` | Gonotrophic cycle interactions |
| Simplified overview | `SimplifiedOverview.puml` | Entry-level conceptual summary |

---

## Code Generator Notes

All three generators produce **skeleton code only** — placeholder vital-rate functions are clearly marked with `TODO` comments. They are intended as starting points that users fill in with species- and site-specific parameterisations.

The skeletons implement the same conceptual structure as the UML diagrams:
- Life stages: Egg → Larva (4 instars) → Pupa → Adult
- Environmental drivers: temperature, photoperiod, precipitation
- Density-dependence: larval carrying capacity
- Control measures: larvicide, adulticide

---

## Supplementary Materials

| File | Content |
|------|---------|
| `S1_questionnaire.md` | Structured questionnaire used in the expert usability assessment |
| `S2_uml_lite_guide.md` | Simplified UML notation guide for ecologists without UML background |
| `S3_assumption_analysis.md` | Full results of the quantitative assumption analysis across three published models |
| `S4_terminology_mapping.md` | Mapping between ecological terminology and UML element types |

---

## Citation

If you use this framework, please cite:

> [Authors]. A Reproducible UML-Based Framework for Conceptual Modeling of *Aedes* Population Dynamics. *Environmental Modelling and Software* (submitted).

Repository archived on Zenodo: DOI `10.5281/zenodo.XXXXXXX` *(to be assigned upon acceptance)*

---

## License

MIT License. See [LICENSE](LICENSE) for details.

PlantUML is licensed under the GPL. NetLogo is free for non-commercial use.

---

## Contributing

Issues and pull requests are welcome. Please open an issue to discuss proposed changes before submitting a pull request.
