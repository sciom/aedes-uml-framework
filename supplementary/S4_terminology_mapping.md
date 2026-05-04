# Supplementary Material S4: UML-to-Ecology Terminology Mapping

## Bridging Software Engineering and Ecological Concepts

---

## Introduction

This document provides a comprehensive mapping between UML terminology and ecological modeling concepts. It is designed to help ecologists interpret UML diagrams and software engineers understand ecological context.

---

## Class Diagram Terminology

| UML Term | Definition | Ecological Equivalent | Example |
|----------|------------|----------------------|---------|
| **Class** | A template defining attributes and behaviors | Population compartment, state variable, or entity type | `Larva` class represents larval stage |
| **Object** | An instance of a class | Individual organism or cohort | A specific larval cohort on day 15 |
| **Attribute** | A property of a class | State variable, parameter | `abundance: float` = population size |
| **Method/Operation** | A behavior of a class | Process, rate calculation | `develop(temp)` = development function |
| **Association** | Relationship between classes | Ecological interaction | Temperature affects Larva |
| **Aggregation (◇)** | "Has-a" relationship (loose) | Contains, hosts | BreedingSite has Eggs |
| **Composition (◆)** | "Has-a" relationship (strong) | Integral component | Environment contains Temperature |
| **Inheritance (△)** | "Is-a" relationship | Taxonomic or functional grouping | Larva is-a LifeStage |
| **Abstract class** | Template that can't be instantiated | Generalized category | `LifeStage` (not instantiated directly) |
| **Interface** | Contract specifying required behaviors | Functional role | `Developable` interface |
| **Multiplicity** | How many instances relate | Population size constraints | `"many"` larvae in `"1"` breeding site |
| **Visibility (-, +)** | Access level (private, public) | Internal vs. observable | `-` internal rate, `+` observable abundance |

### Ecological Interpretations

**Class = Compartment**
```
┌─────────────┐
│   Larva     │  ← This represents the larval stage compartment
├─────────────┤     in a stage-structured model
│ - N: float  │  ← N(t) = larval abundance at time t
│ - μ: float  │  ← μ = mortality rate parameter
├─────────────┤
│ + die()     │  ← Mortality process
│ + develop() │  ← Development process
└─────────────┘
```

**Inheritance = Stage Hierarchy**
```
      LifeStage          ← Shared properties of all stages
          △
    ┌─────┴─────┐
 Aquatic    Terrestrial   ← Habitat-based grouping
    △           △
  ┌─┴─┐         │
Egg Larva     Adult       ← Specific stages
```

---

## State Machine Terminology

| UML Term | Definition | Ecological Equivalent | Example |
|----------|------------|----------------------|---------|
| **State** | A condition or mode | Life stage, physiological state | `Larva`, `Bloodfed`, `Diapausing` |
| **Transition** | Change from one state to another | Development, mortality, behavior change | Larva → Pupa |
| **Guard [condition]** | Condition that must be true | Environmental threshold, trigger | `[temp > 10°C]` |
| **Action / effect** | What happens during transition | Process execution | `/ accumulateDD()` |
| **Entry action** | What happens when entering state | Initialization | `entry / resetDegreeDays()` |
| **Do activity** | Ongoing behavior in state | Continuous process | `do / feed()` |
| **Exit action** | What happens when leaving state | Finalization | `exit / recordDuration()` |
| **Initial state (●)** | Starting point | Birth, introduction | Egg from oviposition |
| **Final state (◉)** | Termination point | Death, removal | Mortality |
| **Composite state** | State containing substates | Stage with internal structure | Larva with instars L1-L4 |
| **Fork/Join** | Parallel state activation | Simultaneous processes | Development AND feeding |

### Ecological Interpretations

**State = Life Stage or Physiological Condition**
```
┌─────────────────┐
│   Bloodfed      │  ← Physiological state of female adult
│                 │
│ entry/start     │  ← Begin gonotrophic cycle
│   gonotrophic   │
│   Cycle()       │
│                 │
│ do/developEggs  │  ← Ongoing egg development
│   (temp)        │
└────────┬────────┘
         │ [cycle complete]  ← Guard: when eggs mature
         ▼
┌─────────────────┐
│     Gravid      │  ← Ready to oviposit
└─────────────────┘
```

**Guard = Environmental Threshold**
```
Egg ──[temp > 10°C AND moisture > 0.5]──> Larva
         │
         └── This guard specifies:
             - Minimum temperature for hatching
             - Minimum moisture for survival
             - Both must be true simultaneously
```

---

## Activity Diagram Terminology

| UML Term | Definition | Ecological Equivalent | Example |
|----------|------------|----------------------|---------|
| **Activity** | A unit of work | Process, calculation | "Calculate mortality" |
| **Action** | An atomic step | Single operation | "Update temperature" |
| **Control flow (→)** | Sequence of activities | Process ordering | Development before mortality |
| **Decision node (◇)** | Branching point | Conditional logic | If gravid, then oviposit |
| **Merge node (◇)** | Joining branches | Convergence | All paths lead to output |
| **Fork bar (═)** | Start parallel activities | Simultaneous processes | Development ∥ Mortality calc |
| **Join bar (═)** | Wait for all parallel | Synchronization | Wait for all rates |
| **Partition/Swimlane** | Responsibility grouping | Stage-specific processes | "Larval dynamics" partition |
| **Object node** | Data being passed | Variable, parameter | Temperature value |
| **Initial node (●)** | Start of workflow | Time step begins | Start of daily update |
| **Final node (◉)** | End of workflow | Time step complete | End of daily update |

### Ecological Interpretations

**Activity = Simulation Process**
```
┌─────────────────────────┐
│ Calculate development   │  ← This activity computes
│ rates                   │     stage-specific development
│                         │     based on temperature
│ Input: Temperature      │
│ Output: devRate[stage]  │
└─────────────────────────┘
```

**Fork/Join = Parallel Processes**
```
        ═══════════════════  ← Fork: start parallel
        │         │        │
        ▼         ▼        ▼
    ┌───────┐ ┌───────┐ ┌───────┐
    │ Eggs  │ │Larvae │ │ Pupae │  ← Independent stage updates
    └───┬───┘ └───┬───┘ └───┬───┘
        │         │        │
        ═══════════════════  ← Join: synchronize
                  │
                  ▼
           ┌───────────┐
           │  Output   │
           └───────────┘
```

---

## Sequence Diagram Terminology

| UML Term | Definition | Ecological Equivalent | Example |
|----------|------------|----------------------|---------|
| **Lifeline** | Object over time | Component through simulation | Larva population lifeline |
| **Message (→)** | Communication between objects | Data/signal passing | Temperature sends rate to Larva |
| **Activation bar** | Period of activity | Active processing time | Larva processing development |
| **Return message (⟵)** | Response to a call | Result, feedback | Larva returns survival prob |
| **Self-message** | Object calls itself | Internal calculation | Larva calculates mortality |
| **Alt fragment** | Alternative paths | Conditional behavior | If DD >= threshold then advance |
| **Loop fragment** | Repeated execution | Iteration | For each instar |
| **Opt fragment** | Optional execution | Conditional process | If gravid, oviposit |
| **Par fragment** | Parallel execution | Simultaneous processes | Update all stages |

### Ecological Interpretations

**Lifeline = Component Through Time**
```
   Larva          Temperature
     │                 │
     │  getDevRate()   │
     │────────────────>│  ← Larva requests development rate
     │                 │
     │    devRate      │
     │<────────────────│  ← Temperature returns rate
     │                 │
     │  develop()      │
     │────┐            │  ← Larva updates internal state
     │<───┘            │
     │                 │
```

**Alt Fragment = Conditional Branching**
```
     Larva
       │
   ┌───┴───────────────────┐
   │ alt [DD >= threshold] │
   ├───────────────────────┤
   │   advanceInstar()     │  ← If threshold met
   ├───────────────────────┤
   │ [else]                │
   │   continue()          │  ← Otherwise continue
   └───────────────────────┘
```

---

## Common UML-Ecology Mappings

### Population Dynamics Concepts

| Ecological Concept | UML Representation |
|-------------------|-------------------|
| Stage-structured population | Class hierarchy with LifeStage parent |
| Vital rates | Class attributes (developmentRate, mortalityRate) |
| Density dependence | Method with population density parameter |
| Environmental forcing | Association with Environment/Temperature class |
| Carrying capacity | Attribute in habitat/BreedingSite class |
| Fecundity | Method in Adult class returning egg count |
| Immigration/Emigration | Methods or transitions to/from external states |

### Process Representations

| Ecological Process | UML Element |
|-------------------|-------------|
| Development | Transition with degree-day guard |
| Mortality | Transition to final state or method call |
| Reproduction | Message from Adult to Egg (sequence) or oviposit() method |
| Diapause | Composite state with entry/exit conditions |
| Competition | Dependency relationship or density parameter |
| Predation | Association with Predator class |

### Model Structure

| Model Component | UML Element |
|----------------|-------------|
| State variable | Class attribute (e.g., `abundance: float`) |
| Parameter | Class attribute or constant |
| Forcing function | Method in Environment class |
| Time step | Activity diagram workflow |
| Feedback loop | Circular message sequence |
| Spatial unit | Separate class or package |

---

## Quick Reference Card

### Reading Class Diagrams
```
┌─────────────────┐
│ ClassName       │  → What population/component?
├─────────────────┤
│ - attribute     │  → What state variables?
├─────────────────┤
│ + method()      │  → What processes?
└─────────────────┘

A ───> B          → A affects/uses B
A ◇─── B          → A contains B (loosely)
A ◆─── B          → A contains B (tightly)
A ──△  B          → A is a type of B
```

### Reading State Machines
```
● → Start here (birth/introduction)
┌───┐
│   │ → Current state (life stage, condition)
└───┘
──[condition]──> → Transition when condition true
◉ → End here (death/removal)
```

### Reading Activity Diagrams
```
● → Begin time step
:Action; → Do this process
◇ → Make decision
═ → Start/end parallel
◉ → End time step
```

### Reading Sequence Diagrams
```
│ → Component exists over time
────> → Sends data/signal
<──── → Returns result
┌──┐
│  │ → Active (processing)
└──┘
```

---

## Glossary

| Term | Domain | Definition |
|------|--------|------------|
| Aggregation | UML | Whole-part relationship where parts can exist independently |
| Attribute | UML | Property of a class; maps to state variable or parameter |
| Cohort | Ecology | Group of individuals of same age/stage |
| Compartment | Ecology | Subdivision of population (e.g., by stage) |
| Composition | UML | Strong whole-part relationship; parts cannot exist alone |
| Degree-day | Ecology | Heat accumulation unit for development |
| Guard | UML | Boolean condition enabling a transition |
| Lifeline | UML | Vertical line showing object existence over time |
| Multiplicity | UML | Number of instances in a relationship |
| State variable | Ecology | Quantity that changes over time (e.g., abundance) |
| Stereotype | UML | Extension mechanism (e.g., `<<stochastic>>`) |
| Transition | UML | Change from one state to another |
| Vital rate | Ecology | Demographic rate (birth, death, development) |

---

*Document version: 1.0*
*Last updated: 2024*
