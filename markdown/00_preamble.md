```latex
% LaTeX Preamble for Insect Perception Research
\documentclass[11pt,a4paper]{article}
\usepackage[utf8]{inputenc}
\usepackage[T1]{fontenc}
\usepackage{geometry}
\usepackage{graphicx}
\usepackage{amsmath}
\usepackage{amsfonts}
\usepackage{amssymb}
\usepackage{booktabs}
\usepackage{hyperref}
\usepackage{color}
\usepackage{xcolor}
\usepackage{listings}
\usepackage{fancyvrb}

% Page geometry
\geometry{margin=1in}

% Hyperref setup
\hypersetup{
    colorlinks=true,
    linkcolor=blue,
    filecolor=magenta,      
    urlcolor=cyan,
    citecolor=red
}

% Custom colors
\definecolor{codebg}{RGB}{245, 245, 245}
\definecolor{codeborder}{RGB}{200, 200, 200}
\definecolor{codefg}{RGB}{50, 50, 50}

% Code listing setup
\lstset{
    backgroundcolor=\color{codebg},
    basicstyle=\footnotesize\ttfamily\color{codefg},
    breakatwhitespace=false,
    breaklines=true,
    captionpos=b,
    frame=single,
    framerule=0.5pt,
    framesep=5pt,
    rulecolor=\color{codeborder},
    numbers=left,
    numbersep=5pt,
    numberstyle=\tiny\color{codefg}
}

% Title and author
\title{When do bugs see (infra)red? \\ On the Visual and Infra-red in the Insect Perceptual Apparatus}
\author{Tucker Chambers \and Daniel A. Friedman}
\date{\today}

% Document begin
\begin{document}
\maketitle

# Preamble {#sec:preamble}

## Document Information

**Title**: When do bugs see (infra)red? On the Visual and Infra-red in the Insect Perceptual Apparatus

**Authors**: Tucker Chambers, Daniel A. Friedman

**Abstract**: This research presents a comprehensive review of evidence supporting the vibrational theory of olfaction in insects, exploring how insects may detect infrared radiation from semiochemicals rather than relying solely on molecular binding.

## Research Overview

This paper investigates the hypothesis that insect olfaction operates through the detection of infrared electromagnetic radiation emitted by semiochemicals, rather than through traditional molecular binding mechanisms. We examine evidence from multiple domains including:

- **Morphology**: The structure and arrangement of insect antennae and sensilla
- **Neurology**: The rapid response times of olfactory receptor neurons
- **Behavior**: Observed insect responses to different stimuli
- **Spectroscopy**: The infrared emission spectra of insect semiochemicals

## Key Research Questions

1. How do insects achieve such rapid olfactory response times (1-5 ms)?
2. What explains the morphological adaptations of antennae and sensilla?
3. How do insects discriminate between different semiochemicals?
4. What role does infrared radiation play in insect perception?

## Theoretical Framework

The vibrational theory of olfaction proposes that insects detect the unique electromagnetic signatures of molecules rather than their geometric or chemical properties. This theory provides a unified explanation for:

- The rapid response times of insect olfaction
- The morphological adaptations of antennae and sensilla  
- The behavioral responses to different semichemicals
- The evolutionary diversity of sensilla types across insect taxa

## Research Significance

Understanding the vibrational basis of insect olfaction has implications for:

- **Entomology**: Fundamental understanding of insect perception and behavior
- **Evolutionary Biology**: How organisms adapt to exploit environmental niches
- **Biomimetics**: Developing new technologies inspired by insect sensory systems
- **Agriculture**: More targeted and environmentally friendly pest control methods
- **Conservation**: Understanding how environmental changes affect insect populations

## Document Structure

This manuscript is organized into several key sections:

1. **Abstract** (Section \ref{sec:abstract}): Research overview and key findings
2. **Introduction** (Section \ref{sec:introduction}): Background on olfaction and limitations of current theories
3. **Methodology** (Section \ref{sec:methodology}): The vibrational theory and evidence from morphology
4. **Experimental Results** (Section \ref{sec:experimental_results}): Neurological, behavioral, and spectroscopic evidence
5. **Discussion** (Section \ref{sec:discussion}): Implications and broader significance
6. **Conclusion** (Section \ref{sec:conclusion}): Summary and future research directions
7. **Mathematical Appendix** (Section \ref{sec:mathematical_appendix}): Complete mathematical framework and equations

## Cross-Referencing System

The manuscript uses comprehensive cross-referencing:

- **Section References**: Use `\ref{sec:section_name}` to reference sections
- **Figure References**: Use `\ref{fig:figure_name}` to reference figures
- **Table References**: Use `\ref{tab:table_name}` to reference tables
- **Equation References**: Use `\ref{eq:equation_name}` to reference equations

All references are automatically numbered and updated when the document is regenerated.

## Mathematical Content

The manuscript includes extensive mathematical content in Section \ref{sec:mathematical_appendix}, featuring:
- Maxwell's equations for electromagnetic wave propagation
- Waveguide theory for sensilla modeling
- Vibrational spectroscopy equations
- Antenna theory and signal processing
- Piezoelectric response of microtubules
- Statistical analysis of behavioral responses
- Quantum mechanical considerations
