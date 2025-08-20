# cohereants

**When do bugs see (infra)red? On the Visual and Infra-red in the Insect Perceptual Apparatus**

A comprehensive research project investigating the vibrational theory of olfaction in insects, exploring how insects may detect infrared radiation from semiochemicals rather than relying solely on molecular binding mechanisms.

## Research Overview

This project investigates the hypothesis that insect olfaction operates through the detection of infrared electromagnetic radiation emitted by semiochemicals, rather than through traditional molecular binding mechanisms. We examine evidence from multiple domains including:

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

## Project Structure

The project follows a standardized research structure:

- **`src/`** - Source code with comprehensive test coverage for data analysis
- **`tests/`** - Test files ensuring 100% coverage of analysis functions
- **`scripts/`** - Project-specific scripts for generating figures and data
- **`markdown/`** - Source markdown files for the manuscript
- **`output/`** - Generated outputs (PDFs, figures, data)
- **`repo_utilities/`** - Utility scripts for project management

## Key Features

### Test-Driven Development
All source code must have 100% test coverage before PDF generation proceeds, as enforced by the build system.

### Automated Script Execution
Project-specific scripts in the `scripts/` directory are automatically executed to generate figures and data, ensuring reproducibility.

### Markdown to PDF Pipeline
Individual markdown modules are converted to PDFs, and a combined document is generated with proper cross-referencing.

### Research Data Analysis
Comprehensive functions for analyzing:
- Sensilla dimensions and optimal detection wavelengths
- Atmospheric transmission in infrared windows
- Cuticular hydrocarbon spectra
- Behavioral response data
- Response time comparisons across sensory modalities

## Manuscript Organization

The manuscript is organized into several key sections:

1. **Abstract** (Section \ref{sec:abstract}): Research overview and key findings
2. **Introduction** (Section \ref{sec:introduction}): Background on olfaction and limitations of current theories
3. **Methodology** (Section \ref{sec:methodology}): The vibrational theory and evidence from morphology
4. **Experimental Results** (Section \ref{sec:experimental_results}): Neurological, behavioral, and spectroscopic evidence
5. **Discussion** (Section \ref{sec:discussion}): Implications and broader significance
6. **Conclusion** (Section \ref{sec:conclusion}): Summary and future research directions
7. **Empirical Studies** (Section \ref{sec:empirical_studies}): Comprehensive review of supporting evidence

## Example Figures

The project generates several key visualizations:

- **Atmospheric Transmission**: Shows infrared transmission windows in Earth's atmosphere
- **Sensilla Dimensions**: Plots insect sensilla morphology and optimal detection wavelengths
- **CHC Spectra**: Example cuticular hydrocarbon infrared spectra
- **Response Time Comparison**: Comparison across different sensory modalities

## Data Availability

All generated data is saved alongside figures for reproducibility:

- **Figures**: PNG format in `output/figures/`
- **Data**: NPZ and CSV formats in `output/data/`
- **PDFs**: Individual and combined documents in `output/pdf/`
- **LaTeX**: Source files in `output/tex/`

## Usage

To generate the complete manuscript:

```bash
# Clean previous outputs
./repo_utilities/clean_output.sh

# Generate everything (tests + scripts + PDFs)
./repo_utilities/render_pdf.sh
```

The system will automatically:
1. Run all tests with 100% coverage requirement
2. Execute project-specific scripts to generate figures and data
3. Validate markdown references and images
4. Generate individual and combined PDFs
5. Export LaTeX source files

## Research Significance

Understanding the vibrational basis of insect olfaction has implications for:

- **Entomology**: Fundamental understanding of insect perception and behavior
- **Evolutionary Biology**: How organisms adapt to exploit environmental niches
- **Biomimetics**: Developing new technologies inspired by insect sensory systems
- **Agriculture**: More targeted and environmentally friendly pest control methods
- **Conservation**: Understanding how environmental changes affect insect populations

## Authors

- **Tucker Chambers**
- **Daniel A. Friedman**

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## Contributing

Please read [CONTRIBUTING.md](CONTRIBUTING.md) for details on our code of conduct and the process for submitting pull requests.

## Acknowledgments

This research builds upon the pioneering work of Dr. Philip S. Callahan and others who first proposed the vibrational theory of olfaction in the 1960s and 1970s.

## Future Research Directions

While the evidence presented here is compelling, much work remains to be done to fully validate the vibrational theory. Key areas for future research include:

1. **Direct Experimental Validation**: Testing the responses of insect sensilla to specific infrared frequencies
2. **Behavioral Studies**: Investigating how insects respond to infrared radiation in the absence of molecular stimuli
3. **Neural Recording**: Measuring the responses of olfactory receptor neurons to infrared stimulation
4. **Comparative Studies**: Examining the infrared detection capabilities across different insect taxa
5. **Environmental Studies**: Understanding how changes in the infrared environment affect insect behavior

The vibrational theory of olfaction represents a paradigm shift in our understanding of insect perception and behavior, opening new avenues for research into insect cognition, evolution, and their role in the natural world.