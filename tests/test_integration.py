"""
Integration tests and end-to-end testing.

This file tests the integration between modules and end-to-end workflows.
"""

import numpy as np
import pytest
import matplotlib.pyplot as plt

# Import modules for integration testing
from src.core import calculate_atmospheric_transmission, calculate_response_time_improvement
from src.sensilla import analyze_sensilla_dimensions, calculate_wavelength_matching
from src.spectroscopy import analyze_chc_spectra, calculate_spectral_overlap
from src.visualization import AdvancedVisualizer, PlotStyler
from src.behavioral import analyze_behavioral_response
from src.integrated_analysis import IntegratedAnalyzer, create_sample_integrated_analysis


def _results_for_visualization():
    _, results = create_sample_integrated_analysis()
    return results


class TestModuleIntegration:
    """Test integration between different modules."""

    def test_sensilla_spectroscopy_integration(self):
        """Test integration between sensilla and spectroscopy modules."""
        # Generate sensilla data
        lengths = np.array([50.0, 100.0, 150.0])
        diameters = np.array([5.0, 10.0, 15.0])
        sensilla_result = analyze_sensilla_dimensions(lengths, diameters)

        # Generate wavelength data
        wavelengths = np.linspace(2.0, 25.0, 100)

        # Test wavelength matching with sensilla dimensions
        for length in lengths:
            matching = calculate_wavelength_matching(wavelengths, length)
            assert matching.shape == (100,)
            assert np.all(matching >= 0)

        # Verify sensilla analysis includes resonance data
        assert 'resonance_frequencies' in sensilla_result

    def test_core_spectroscopy_integration(self):
        """Test integration between core and spectroscopy modules."""
        wavelengths = np.linspace(2.0, 25.0, 100)

        # Get atmospheric transmission
        transmission = calculate_atmospheric_transmission(wavelengths)

        # Create synthetic spectrum affected by atmospheric transmission
        base_spectrum = np.exp(-((wavelengths - 10) / 3)**2)
        attenuated_spectrum = base_spectrum * transmission

        # Analyze both spectra
        base_analysis = analyze_chc_spectra(wavelengths, base_spectrum) 
        attenuated_analysis = analyze_chc_spectra(wavelengths, attenuated_spectrum)  

        # Attenuated spectrum should have different characteristics
        assert len(base_analysis['peak_wavelengths']) >= len(attenuated_analysis['peak_wavelengths'])

    def test_visualization_core_integration(self):
        """Test integration between visualization and core modules."""
        visualizer = AdvancedVisualizer()

        # Generate data using core functions
        wavelengths = np.linspace(2.0, 25.0, 100)
        transmission = calculate_atmospheric_transmission(wavelengths)
        response_improvement = calculate_response_time_improvement(10.0, 5.0)

        # Create visualization with core data
        fig = visualizer.plot_spectral_analysis(wavelengths, transmission)
        assert isinstance(fig, plt.Figure)
        plt.close(fig)

    def test_spectroscopy_behavioral_integration(self):
        """Test integration between spectroscopy and behavioral analysis."""
        # Create synthetic spectral data
        wavelengths = np.linspace(2.0, 25.0, 100)
        spectrum1 = np.exp(-((wavelengths - 10) / 3)**2)
        spectrum2 = np.exp(-((wavelengths - 15) / 2)**2)

        # Analyze spectra
        analysis1 = analyze_chc_spectra(wavelengths, spectrum1) 
        analysis2 = analyze_chc_spectra(wavelengths, spectrum2)

        # Calculate spectral overlap
        overlap = calculate_spectral_overlap(spectrum1, spectrum2)

        # Create mock behavioral response data
        n_trials = 20
        response_data = np.random.randn(n_trials, 100)

        # Analyze behavioral response
        behavioral_result = analyze_behavioral_response(response_data)

        # Integration: spectral differences should correlate with behavioral differences
        assert 'mean_response' in behavioral_result
        assert 0.0 <= overlap <= 1.0


class TestEndToEndWorkflows:
    """Test complete end-to-end workflows."""

    def test_complete_spectral_analysis_workflow(self):
        """Test complete spectral analysis workflow."""
        # Step 1: Generate wavelengths
        wavelengths = np.linspace(2.0, 25.0, 100)

        # Step 2: Calculate atmospheric effects
        transmission = calculate_atmospheric_transmission(wavelengths)

        # Step 3: Create synthetic CHC spectrum
        chc_spectrum = np.exp(-((wavelengths - 10) / 2)**2) + 0.5 * np.exp(-((wavelengths - 15) / 1)**2)

        # Step 4: Apply atmospheric effects
        observed_spectrum = chc_spectrum * transmission

        # Step 5: Analyze spectrum
        analysis = analyze_chc_spectra(wavelengths, observed_spectrum)  # Fixed argument order

        # Step 6: Visualize results
        visualizer = AdvancedVisualizer()
        fig = visualizer.plot_spectral_analysis(wavelengths, observed_spectrum)
        assert isinstance(fig, plt.Figure)
        plt.close(fig)

        # Verify analysis contains expected components
        assert 'peak_wavelengths' in analysis
        assert 'peak_intensities' in analysis

    def test_sensilla_analysis_workflow(self):
        """Test complete sensilla analysis workflow."""
        # Step 1: Define sensilla dimensions
        lengths = np.array([50.0, 100.0, 150.0])
        diameters = np.array([5.0, 10.0, 15.0])

        # Step 2: Analyze dimensions
        dimensions = analyze_sensilla_dimensions(lengths, diameters)

        # Step 3: Generate wavelength matching data
        wavelengths = np.linspace(2.0, 25.0, 100)
        matching_data = []
        for length in lengths:
            matching = calculate_wavelength_matching(wavelengths, length)
            matching_data.append(matching)

        # Step 4: Create visualization
        visualizer = AdvancedVisualizer()
        fig = visualizer.plot_multi_panel_analysis({
            'sensilla_dimensions': {
                'x': lengths,
                'y': diameters,
                'xlabel': 'Length (μm)',
                'ylabel': 'Diameter (μm)'
            },
            'wavelength_matching': {
                'x': wavelengths,
                'y': matching_data[0],
                'xlabel': 'Wavelength (μm)',
                'ylabel': 'Matching Factor'
            }
        })
        assert isinstance(fig, plt.Figure)
        plt.close(fig)

        # Verify dimensions analysis
        assert 'aspect_ratios' in dimensions
        assert 'surface_areas' in dimensions

    def test_integrated_analysis_workflow(self):
        """Test integrated analysis workflow."""
        # Step 1: Initialize integrated analyzer
        analyzer = IntegratedAnalyzer()

        # Step 2: Generate comprehensive report with mock analysis results
        analysis_results = {
            'fermi_analysis': {
                'molecular': {
                    'translational_bits': 2.5,
                    'rotational_bits': 1.8,
                    'vibrational_bits': 3.2,
                    'total_bits': 2.5 + 1.8 + 3.2,  # Sum of all molecular bits
                    'total_bytes': (2.5 + 1.8 + 3.2) / 8  # Convert bits to bytes
                },
                'receptor': {
                    'molecular_recognition_bits': 4.1,
                    'binding_energy_bits': 2.8,
                    'binding_entropy_bits': 3.2,
                    'specificity_index': 0.85,
                    'signal_to_noise_ratio': 12.5,
                    'total_bits': 4.1 + 2.8 + 3.2  # Sum of all receptor bits
                },
                'neural': {
                    'encoding_efficiency_bits_per_energy': 0.75,
                    'temporal_precision_ms': 50.0,
                    'spike_rate_hz': 25.0,
                    'channel_capacity_bits': 2.8,
                    'information_rate_bits': 1.9
                },
                'environmental': {
                    'temperature_k': 298.0,
                    'humidity_percent': 65.0,
                    'pressure_pa': 101325.0,
                    'total_environmental_bits': 1.2,
                    'temperature_bits': 0.4,
                    'humidity_bits': 0.5,
                    'pressure_bits': 0.3
                }
            },
            'metamaterial_analysis': {  # Fix key name to match what the function expects
                'information_capacity': {
                    'molecular_bits': 8.5,
                    'receptor_bits': 6.9,
                    'channel_capacity_bits_per_sec': 1.2e6,
                    'signal_to_noise_ratio': 15.0,
                    'information_density_bits_per_joule_meter': 2.5e8,
                    'quantum_limit_bits_per_sec': 8.5e5
                },
                'dielectric': {
                    'refractive_index': [1.5, 1.6, 1.4, 1.7],
                    'absorption_coefficient': 0.02,
                    'permittivity': 2.25,
                    'frequency': [10.0e12, 15.0e12, 20.0e12, 25.0e12]  # THz range
                },
                'plasmonic': {
                    'quality_factor': 45.0,
                    'resonance_frequency_thz': 15.0,
                    'resonance_frequency_hz': 15.0e12,  # Convert THz to Hz
                    'resonance_wavelength_m': 3e8 / 15.0e12,  # c/f in meters
                    'field_enhancement': 25.0
                }
            }
        }
        report = analyzer.comprehensive_report(analysis_results)
        assert 'SYSTEM SUMMARY' in report
        assert 'INTEGRATED ANALYSIS SUMMARY' in report

        # Step 3: Generate visualization
        fig = analyzer.generate_visualization()
        assert isinstance(fig, plt.Figure)
        plt.close(fig)

    def test_visualization_workflow_with_styling(self):
        """Test complete visualization workflow with styling."""
        # Step 1: Create styler with specific style
        styler = PlotStyler('science')

        # Step 2: Generate test data
        x = np.linspace(0, 10, 100)
        y = np.sin(x) * np.exp(-x/5)

        # Step 3: Create figure with styling
        fig, axes = styler.create_figure_grid(1, 1)
        ax = axes[0]
        ax.plot(x, y, color=styler.get_colors(1)[0])
        styler.format_axes(ax, xlabel='Time', ylabel='Amplitude', title='Test Signal')

        # Step 4: Verify styling applied
        assert fig.get_size_inches()[0] > 0
        assert ax.get_xlabel() == 'Time'
        assert ax.get_ylabel() == 'Amplitude'
        plt.close(fig)


class TestDataFlowIntegration:
    """Test data flow between modules."""

    def test_wavelength_data_flow(self):
        """Test wavelength data flow through multiple modules."""
        wavelengths = np.linspace(2.0, 25.0, 50)

        # Flow through core module
        transmission = calculate_atmospheric_transmission(wavelengths)

        # Flow through sensilla module
        sensilla_length = 100.0
        matching = calculate_wavelength_matching(wavelengths, sensilla_length)

        # Flow through visualization
        visualizer = AdvancedVisualizer()
        fig = visualizer.plot_multi_panel_analysis({
            'transmission': {
                'x': wavelengths,
                'y': transmission,
                'xlabel': 'Wavelength (μm)',
                'ylabel': 'Transmission'
            },
            'sensilla_matching': {
                'x': wavelengths,
                'y': matching,
                'xlabel': 'Wavelength (μm)',
                'ylabel': 'Matching Factor'
            }
        })
        assert isinstance(fig, plt.Figure)
        plt.close(fig)

        # Verify data integrity
        assert transmission.shape == (50,)
        assert matching.shape == (50,)
        assert np.all(transmission >= 0) and np.all(transmission <= 1)

    def test_spectral_data_flow(self):
        """Test spectral data flow through analysis pipeline."""
        wavelengths = np.linspace(2.0, 25.0, 100)
        original_spectrum = np.exp(-((wavelengths - 10) / 2)**2)

        # Analyze original spectrum
        original_analysis = analyze_chc_spectra(wavelengths, original_spectrum)

        # Modify spectrum (simulate measurement effects) - ensure non-negative
        modified_spectrum = original_spectrum * 0.8 + np.abs(np.random.normal(0, 0.05, len(original_spectrum)))

        # Analyze modified spectrum
        modified_analysis = analyze_chc_spectra(wavelengths, modified_spectrum) 

        # Compare analyses
        assert 'peak_wavelengths' in original_analysis
        assert 'peak_wavelengths' in modified_analysis

        # Calculate overlap between original and modified
        overlap = calculate_spectral_overlap(original_spectrum, modified_spectrum)
        assert 0.0 <= overlap <= 1.0

# --- merged from test_coverage_integrated_analysis.py ---

def test_generate_visualization_all_branches():
    analyzer = IntegratedAnalyzer()
    fig = analyzer.generate_visualization(_results_for_visualization())
    assert hasattr(fig, "savefig")
    # 2x2 panel grid is created regardless of which branches fire.
    assert len(fig.axes) >= 4
    plt.close(fig)


def test_generate_visualization_none_and_empty():
    analyzer = IntegratedAnalyzer()
    fig_none = analyzer.generate_visualization(None)
    assert hasattr(fig_none, "savefig")
    plt.close(fig_none)

    fig_empty = analyzer.generate_visualization({})
    assert hasattr(fig_empty, "savefig")
    plt.close(fig_empty)


def test_comprehensive_report_alias_matches_full_report():
    analyzer, results = create_sample_integrated_analysis()
    alias = analyzer.comprehensive_report(results)
    direct = analyzer.generate_comprehensive_report(results)
    assert isinstance(alias, str)
    assert len(alias) > 0
    assert alias == direct
    plt.close("all")


def test_create_sample_and_full_chain():
    analyzer, results = create_sample_integrated_analysis()
    assert "fermi_analysis" in results
    assert "metamaterial_analysis" in results

    metrics = analyzer.calculate_system_performance_metrics(results)
    assert "system_efficiency" in metrics
    assert np.isfinite(metrics["system_efficiency"])
    assert metrics["system_efficiency"] >= 0.0

    figures = analyzer.create_visualization_figures(results)
    assert set(figures.keys()) == {
        "information_breakdown",
        "metamaterial_properties",
        "system_performance",
    }
    for fig in figures.values():
        assert hasattr(fig, "savefig")
    plt.close("all")

# --- merged from test_coverage_demock_extra.py (integrated) ---

# ── IntegratedAnalyzer real factory + visualization/report/save paths ───────
class TestIntegratedAnalyzerReal:
    def test_sample_analysis_structure(self):
        analyzer, results = create_sample_integrated_analysis()
        assert isinstance(analyzer, IntegratedAnalyzer)
        assert isinstance(results, dict) and len(results) > 0

    def test_comprehensive_report_has_content(self):
        analyzer, results = create_sample_integrated_analysis()
        report = analyzer.generate_comprehensive_report(results)
        assert isinstance(report, str) and len(report) > 100
        assert any(c.isdigit() for c in report)

    def test_generate_visualization_real_figure(self):
        analyzer, results = create_sample_integrated_analysis()
        fig = analyzer.generate_visualization(results)
        assert isinstance(fig, plt.Figure)
        assert len(fig.axes) >= 1
        plt.close("all")

    def test_create_visualization_figures_real(self):
        analyzer, results = create_sample_integrated_analysis()
        figs = analyzer.create_visualization_figures(results)
        assert isinstance(figs, dict) and len(figs) >= 1
        for f in figs.values():
            assert isinstance(f, plt.Figure)
        plt.close("all")

    def test_save_analysis_figures_writes_files(self, tmp_path):
        analyzer, results = create_sample_integrated_analysis()
        figs = analyzer.create_visualization_figures(results)
        analyzer.save_analysis_figures(figs, str(tmp_path))
        written = list(tmp_path.glob("*.png"))
        assert len(written) >= 1
        assert all(p.stat().st_size > 0 for p in written)
        plt.close("all")
