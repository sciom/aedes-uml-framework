# Supplementary Material S3: Detailed Assumption Analysis

## Implicit Assumptions Revealed Through UML Reconstruction

---

## Overview

This document provides detailed results from the quantitative assumption analysis conducted across three published *Aedes* population models. Two independent reviewers identified assumptions from both original publications and UML reconstructions.

---

## Methodology

### Reviewers
- **Reviewer A:** Ecological modeler, 8 years experience, no prior UML experience
- **Reviewer B:** Software engineer, 5 years experience in ecological modeling systems

### Assumption Categories
1. **Structural assumptions:** Which components exist and how they relate
2. **Behavioral assumptions:** Process ordering, transition conditions, timing
3. **Boundary assumptions:** What is included/excluded from the model

### Protocol
1. Reviewers independently read original publication
2. Listed all identifiable assumptions (30 min per model)
3. Received UML reconstruction (no additional explanation)
4. Listed all assumptions visible from UML (30 min per model)
5. Classifications compared and reconciled

---

## Model 1: Hackenberger et al. (2013)

### Reference
Hackenberger, B. K., Hackenberger, D. K., & Jarić, I. (2013). Stage and age structured *Aedes vexans* and *Culex pipiens* (Diptera: Culicidae) climate-dependent matrix population model. *Theoretical Population Biology*, 83, 82–94.

### Assumptions Identified from Original Publication

| # | Assumption | Category | Source in Paper |
|---|------------|----------|-----------------|
| 1 | Temperature-dependent development (degree-days) | Behavioral | Equations 3-5 |
| 2 | Photoperiod-triggered diapause | Behavioral | Section 2.3 |
| 3 | Density-dependent larval mortality | Structural | Equation 8 |

**Total from original: 3**

### Additional Assumptions Revealed by UML

| # | Assumption | Category | UML Element | Status in Original |
|---|------------|----------|-------------|-------------------|
| 4 | Synchronous daily time step | Behavioral | Activity diagram: sequential process ordering | Implicit |
| 5 | Instantaneous stage transitions | Behavioral | State machine: no transition duration states | Implicit (inferrable) |
| 6 | Homogeneous population (no individual variation) | Structural | Class diagram: no variance attributes | Implicit |
| 7 | Single breeding site type | Structural | Class diagram: one BreedingSite class | Implicit |
| 8 | Immediate oviposition after gonotrophic cycle | Behavioral | State machine: Gravid → HostSeeking direct | Implicit (inferrable) |

**Total from UML: 8**
**Newly revealed: 5**

### Reviewer Agreement
- Cohen's κ = 0.82 (almost perfect agreement)
- Disagreement on #5: Reviewer A marked as "explicit," Reviewer B as "implicit (inferrable)"
- Resolution: Classified as "implicit (inferrable)" - inferrable from equations but not stated

---

## Model 2: Cailly et al. (2012)

### Reference
Cailly, P., Tran, A., Balenghien, T., L'Ambert, G., Toty, C., & Ezanno, P. (2012). A climate-driven abundance model to assess mosquito control strategies. *Ecological Modelling*, 227, 7–17.

### Assumptions Identified from Original Publication

| # | Assumption | Category | Source in Paper |
|---|------------|----------|-----------------|
| 1 | Temperature-dependent vital rates (Briere function) | Behavioral | Section 2.2 |
| 2 | Rainfall affects breeding site availability | Structural | Section 2.3 |
| 3 | Nulliparous/parous adult distinction | Structural | Figure 1 |
| 4 | Control measures as mortality modifiers | Structural | Section 2.5 |

**Total from original: 4**

### Additional Assumptions Revealed by UML

| # | Assumption | Category | UML Element | Status in Original |
|---|------------|----------|-------------|-------------------|
| 5 | Multiple breeding site types with different dynamics | Structural | Class diagram: SiteType enum | Implicit |
| 6 | Sex ratio determination at emergence | Behavioral | State machine: determineSex() at Pupa→Adult | Implicit |
| 7 | Bloodmeal required before each oviposition | Behavioral | State machine: HostSeeking→Bloodfed→Gravid cycle | Implicit (inferrable) |
| 8 | No adult immigration/emigration | Boundary | Class diagram: closed population | Implicit |
| 9 | Environmental drivers affect all stages uniformly | Structural | Sequence diagram: single Temperature object | Partially explicit |
| 10 | Deterministic dynamics (no stochasticity) | Behavioral | No <<stochastic>> stereotypes | Implicit |
| 11 | No predation mortality component | Boundary | Class diagram: no Predator class | Implicit |

**Total from UML: 11**
**Newly revealed: 7**

### Reviewer Agreement
- Cohen's κ = 0.78 (substantial agreement)
- Disagreement on #9: Debate whether "partially explicit" counts as "revealed"
- Resolution: Included as revealed since full scope became apparent only through UML

---

## Model 3: Tran et al. (2013)

### Reference
Tran, A., L'Ambert, G., Lacour, G., Benoît, R., Demarchi, M., Cros, M., Cailly, P., Aubry-Kientz, M., Balenghien, T., & Ezanno, P. (2013). A rainfall- and temperature-driven abundance model for *Aedes albopictus* populations. *International Journal of Environmental Research and Public Health*, 10(5), 1698–1719.

### Assumptions Identified from Original Publication

| # | Assumption | Category | Source in Paper |
|---|------------|----------|-----------------|
| 1 | Rainfall-dependent carrying capacity | Structural | Equation 4 |
| 2 | Temperature-dependent development | Behavioral | Section 2.2 |

**Total from original: 2**

### Additional Assumptions Revealed by UML

| # | Assumption | Category | UML Element | Status in Original |
|---|------------|----------|-------------|-------------------|
| 3 | Four larval instars with separate thresholds | Structural | State machine: L1→L2→L3→L4 states | Implicit |
| 4 | Pupal stage non-feeding | Behavioral | Class diagram: no feedingRate in Pupa | Implicit |
| 5 | Adult males do not affect population dynamics | Structural | Class diagram: reproduction in Female only | Implicit |
| 6 | Single gonotrophic cycle length (no variation) | Behavioral | Class diagram: fixed gonotrophicCycleLength | Implicit |
| 7 | No egg bank (all eggs hatch or die) | Boundary | State machine: no persistent egg state | Implicit |
| 8 | Habitat desiccation causes egg mortality | Behavioral | Activity diagram: desiccation mortality branch | Implicit |
| 9 | Process order: development before mortality | Behavioral | Activity diagram: explicit ordering | Implicit |

**Total from UML: 9**
**Newly revealed: 7**

### Reviewer Agreement
- Cohen's κ = 0.85 (almost perfect agreement)
- Minor disagreement on #4: Both agreed it was implicit but debated importance
- Resolution: Included all assumptions regardless of perceived importance

---

## Summary Statistics

### Assumptions by Model

| Model | Original | After UML | Newly Revealed | % Increase |
|-------|----------|-----------|----------------|------------|
| Hackenberger et al. (2013) | 3 | 8 | 5 | 167% |
| Cailly et al. (2012) | 4 | 11 | 7 | 175% |
| Tran et al. (2013) | 2 | 9 | 7 | 350% |
| **Mean** | **3.0** | **9.3** | **6.3** | **210%** |

### Assumptions by Category

| Category | Original Total | UML Total | Newly Revealed |
|----------|---------------|-----------|----------------|
| Structural | 4 | 13 | 9 |
| Behavioral | 4 | 12 | 8 |
| Boundary | 1 | 3 | 2 |
| **Total** | **9** | **28** | **19** |

### Inter-Rater Reliability

| Model | Cohen's κ | Interpretation |
|-------|-----------|----------------|
| Hackenberger et al. (2013) | 0.82 | Almost perfect |
| Cailly et al. (2012) | 0.78 | Substantial |
| Tran et al. (2013) | 0.85 | Almost perfect |
| **Mean** | **0.82** | **Almost perfect** |

Interpretation scale (Landis & Koch, 1977):
- 0.81–1.00: Almost perfect
- 0.61–0.80: Substantial
- 0.41–0.60: Moderate
- 0.21–0.40: Fair
- 0.00–0.20: Slight

---

## Categories of Revealed Assumptions

### 1. Temporal Structure (6 assumptions)
- Process ordering within time steps
- Synchronous vs. asynchronous updates
- Instantaneous vs. duration-based transitions

### 2. Spatial Homogeneity (4 assumptions)
- Single vs. multiple breeding site types
- Closed population boundaries
- Uniform environmental effects

### 3. Population Structure (5 assumptions)
- Individual variation (or lack thereof)
- Sex-specific dynamics
- Age/stage sub-structure

### 4. Process Boundaries (4 assumptions)
- Included vs. excluded mortality sources
- Immigration/emigration
- Predation effects

---

## Implications

1. **Narrative descriptions consistently underspecify models** - On average, only 32% of assumptions were identifiable from original publications.

2. **UML reveals behavioral assumptions most effectively** - Process ordering and transition logic became explicit through activity and state machine diagrams.

3. **High inter-rater agreement validates UML interpretability** - Reviewers from different backgrounds reached similar conclusions from UML specifications.

4. **Boundary assumptions are frequently implicit** - What is *excluded* from models is rarely stated explicitly.

---

## References

Landis, J. R., & Koch, G. G. (1977). The measurement of observer agreement for categorical data. *Biometrics*, 33(1), 159–174.

---

*Document version: 1.0*
*Last updated: 2024*
