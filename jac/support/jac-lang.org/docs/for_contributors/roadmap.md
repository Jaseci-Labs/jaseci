# Jac Language Development Roadmap

## Overview

This document outlines the roadmap for Jac. This document will be a bit fluid, however should capture the current plan.

## Roadmap

### Python Completeness

- **Objective:** Implement all required features to allow full compatibility and expressivity of Python.
- **Status**
    - [Complete]
- **Todos:**
    - Need good docs

### Purple Featureset

- **Objective:** Implement basic language improvement features for convenience that are not available in Python.
- **Status**
    - [Complete]
- **Todos:**
    - Need good docs

### Data Spatial Complete

- **Objective:** Implement language constructs for the Data Spatial programming model.
- **Status**
    - [Partially Complete]
- **Todos:**
    - Make Myca Lite complete

### Jac User/State Abstractions and Hooks

- **Objective:** Implement the semantics related to language-level abstractions for multi-user and cross-execution state.
- **Status**
    - [Architected - Not Implemented]
- **Todos:**
    -

### Plugin Infrastructure to Support Jaseci 2

- **Objective:** Complete hooks specification and implementation for plugins to Jac language core.
- **Status**
    - [Not Complete]
- **Todos:**
    -

### Jaseci 2 plugins for Jaseci 1 Completeness

- **Objective:** Create the minimal set of plugins required to achieve complete implementation of current Jaseci 1 functionality.
- **Status**
    - [Not Complete]
- **Todos:**
    -

### Compiler Correctness Analyses and Error Reporting

- **Objective:** Develop compiler correctness analyses and error reporting capabilities.
- **Status**
    - [Not Complete]
- **Todos:**
    - Type infer and checking pass
    - Code integrity checking pass (abstract methods are implemented in all subclasses etc)