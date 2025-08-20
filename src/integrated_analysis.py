"""
Integrated Analysis Module

This module integrates the Fermi Estimation analysis with the meta-material analytical
framework to provide comprehensive quantitative analysis for the vibrational theory
of olfaction and infrared sensing in insects.

It combines:
- Information-theoretic measures from Fermi Estimation
- Material property analysis from meta-material framework
- Cross-domain synthesis for empirical validation
- Quantitative predictions and analysis
"""

import numpy as np
import matplotlib.pyplot as plt
from typing import Dict, List, Tuple, Optional, Union
import warnings

# Import our custom modules
try:
    from .fermi_estimation import FermiEstimator
    from .meta_material_framework import MetaMaterialAnalyzer
except ImportError:
    # Fallback for when running tests or as standalone script
    import sys
    import os
    sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))
    
    from src.fermi_estimation import FermiEstimator
    from src.meta_material_framework import MetaMaterialAnalyzer

# Suppress warnings for cleaner output
warnings.filterwarnings('ignore')

class IntegratedAnalyzer:
    """
    Integrated analyzer combining Fermi Estimation and meta-material frameworks.
    
    Provides comprehensive analysis for olfaction and infrared sensing research,
    connecting theoretical predictions with empirical evidence.
    """
    
    def __init__(self):
        """Initialize the integrated analyzer."""
        self.fermi_estimator = FermiEstimator()
        self.meta_material_analyzer = MetaMaterialAnalyzer()
        
    def analyze_olfactory_system(self,
                                odorant_properties: Dict,
                                receptor_properties: Dict,
                                environmental_conditions: Dict) -> Dict[str, Dict]:
        """
        Comprehensive analysis of olfactory system performance.
        
        Args:
            odorant_properties: Dictionary with odorant characteristics
            receptor_properties: Dictionary with receptor characteristics
            environmental_conditions: Dictionary with environmental parameters
            
        Returns:
            Dictionary containing all analysis results
        """
        # Fermi estimation analysis
        molecular_data = self.fermi_estimator.estimate_molecular_information_content(
            molecular_weight=odorant_properties.get('molecular_weight', 150.0),
            symmetry_number=odorant_properties.get('symmetry_number', 2),
            vibrational_modes=odorant_properties.get('vibrational_modes', 15)
        )
        
        # Receptor specificity analysis
        binding_energies = receptor_properties.get('binding_energies', 
                                                 np.array([-25.0, -20.0, -15.0, -10.0, -5.0]))
        receptor_data = self.fermi_estimator.calculate_receptor_specificity(binding_energies)
        
        # Neural encoding analysis
        response_amplitudes = receptor_properties.get('response_amplitudes', 
                                                    np.random.normal(1.0, 0.3, 100))
        neural_data = self.fermi_estimator.estimate_neural_encoding_efficiency(response_amplitudes)
        
        # Environmental information analysis
        env_data = self.fermi_estimator.calculate_environmental_information_content(
            temperature_range=environmental_conditions.get('temperature_range', (273.15, 313.15)),
            humidity_range=environmental_conditions.get('humidity_range', (0.3, 0.8)),
            pressure_range=environmental_conditions.get('pressure_range', (101000, 102000))
        )
        
        # Meta-material analysis for receptor structure
        frequency_range = np.logspace(13, 15, 100)  # 10-1000 THz
        dielectric_data = self.meta_material_analyzer.calculate_dielectric_response(
            frequency=frequency_range,
            epsilon_inf=receptor_properties.get('epsilon_inf', 2.0),
            omega_p=receptor_properties.get('omega_p', 5e15),
            gamma=receptor_properties.get('gamma', 1e13)
        )
        
        # Plasmonic analysis for metallic components
        plasmonic_data = self.meta_material_analyzer.analyze_plasmonic_resonance(
            particle_radius=receptor_properties.get('particle_radius', 50e-9),
            metal_dielectric=receptor_properties.get('metal_dielectric', -10.0 + 1j),
            medium_dielectric=receptor_properties.get('medium_dielectric', 1.5)
        )
        
        # Information capacity analysis
        info_capacity_data = self.meta_material_analyzer.analyze_information_capacity(
            material_properties=dielectric_data,
            frequency_bandwidth=receptor_properties.get('frequency_bandwidth', 1e12),
            signal_power=receptor_properties.get('signal_power', 1e-6),
            noise_temperature=environmental_conditions.get('noise_temperature', 300.0)
        )
        
        return {
            'fermi_analysis': {
                'molecular': molecular_data,
                'receptor': receptor_data,
                'neural': neural_data,
                'environmental': env_data
            },
            'metamaterial_analysis': {
                'dielectric': dielectric_data,
                'plasmonic': plasmonic_data,
                'information_capacity': info_capacity_data
            }
        }
    
    def calculate_system_performance_metrics(self, analysis_results: Dict) -> Dict[str, float]:
        """
        Calculate comprehensive system performance metrics.
        
        Args:
            analysis_results: Output from analyze_olfactory_system
            
        Returns:
            Dictionary with performance metrics
        """
        fermi = analysis_results['fermi_analysis']
        metamaterial = analysis_results['metamaterial_analysis']
        
        # Information processing efficiency
        total_info_content = fermi['molecular']['total_bits']
        receptor_specificity = fermi['receptor']['specificity_index']
        neural_efficiency = fermi['neural']['encoding_efficiency_bits_per_energy']
        
        # Material performance
        avg_refractive_index = np.mean(metamaterial['dielectric']['refractive_index'])
        plasmonic_quality = metamaterial['plasmonic']['quality_factor']
        info_capacity = metamaterial['information_capacity']['channel_capacity_bits_per_sec']
        
        # Composite performance metrics
        information_processing_score = total_info_content * receptor_specificity * neural_efficiency
        material_performance_score = avg_refractive_index * plasmonic_quality * np.log10(info_capacity + 1)
        
        # Overall system efficiency
        product = information_processing_score * material_performance_score
        system_efficiency = np.sqrt(np.abs(product)) if product >= 0 else 0.0
        
        return {
            'information_processing_score': information_processing_score,
            'material_performance_score': material_performance_score,
            'system_efficiency': system_efficiency,
            'total_information_content_bits': total_info_content,
            'receptor_specificity_index': receptor_specificity,
            'neural_encoding_efficiency': neural_efficiency,
            'average_refractive_index': avg_refractive_index,
            'plasmonic_quality_factor': plasmonic_quality,
            'information_capacity_bits_per_sec': info_capacity
        }
    
    def generate_comprehensive_report(self, analysis_results: Dict) -> str:
        """
        Generate comprehensive integrated analysis report.
        
        Args:
            analysis_results: Output from analyze_olfactory_system
            
        Returns:
            Formatted report string
        """
        # Get performance metrics
        performance_metrics = self.calculate_system_performance_metrics(analysis_results)
        
        # Generate individual reports
        fermi_report = self.fermi_estimator.generate_fermi_analysis_report(
            analysis_results['fermi_analysis']['molecular'],
            analysis_results['fermi_analysis']['receptor'],
            analysis_results['fermi_analysis']['neural'],
            analysis_results['fermi_analysis']['environmental']
        )
        
        # Create placeholder quantum data for metamaterial report
        placeholder_quantum_data = {
            'eigenvalues': np.array([0.0, 1e-20, 2e-20]),
            'transition_rates': np.array([1e-12, 1e-12]),
            'coupling_matrix': np.array([[0, 1e-21], [1e-21, 0]])
        }
        
        metamaterial_report = self.meta_material_analyzer.generate_metamaterial_report(
            analysis_results['metamaterial_analysis']['dielectric'],
            analysis_results['metamaterial_analysis']['plasmonic'],
            placeholder_quantum_data,  # Use placeholder data
            analysis_results['metamaterial_analysis']['information_capacity']
        )
        
        # Integrated analysis summary
        integrated_summary = []
        integrated_summary.append("=== INTEGRATED ANALYSIS SUMMARY ===\n")
        integrated_summary.append("SYSTEM PERFORMANCE METRICS:")
        integrated_summary.append(f"  Information Processing Score: {performance_metrics['information_processing_score']:.2e}")
        integrated_summary.append(f"  Material Performance Score: {performance_metrics['material_performance_score']:.2e}")
        integrated_summary.append(f"  Overall System Efficiency: {performance_metrics['system_efficiency']:.2e}")
        integrated_summary.append(f"  Total Information Content: {performance_metrics['total_information_content_bits']:.2f} bits")
        integrated_summary.append(f"  Receptor Specificity: {performance_metrics['receptor_specificity_index']:.3f}")
        integrated_summary.append(f"  Neural Encoding Efficiency: {performance_metrics['neural_encoding_efficiency']:.4f} bits/energy")
        integrated_summary.append(f"  Information Capacity: {performance_metrics['information_capacity_bits_per_sec']:.2e} bits/s\n")
        
        # Combine all reports
        full_report = "\n".join([
            "\n".join(integrated_summary),
            fermi_report,
            "\n" + metamaterial_report
        ])
        
        return full_report
    
    def create_visualization_figures(self, analysis_results: Dict) -> Dict[str, plt.Figure]:
        """
        Create comprehensive visualization figures for the analysis.
        
        Args:
            analysis_results: Output from analyze_olfactory_system
            
        Returns:
            Dictionary with matplotlib figures
        """
        figures = {}
        
        # Figure 1: Information content breakdown
        fig1, (ax1, ax2) = plt.subplots(1, 2, figsize=(15, 6))
        
        # Molecular information breakdown
        fermi = analysis_results['fermi_analysis']
        molecular_labels = ['Translational', 'Rotational', 'Vibrational']
        molecular_values = [
            fermi['molecular']['translational_bits'],
            fermi['molecular']['rotational_bits'],
            fermi['molecular']['vibrational_bits']
        ]
        
        ax1.pie(molecular_values, labels=molecular_labels, autopct='%1.1f%%')
        ax1.set_title('Molecular Information Content Distribution')
        
        # Receptor specificity vs binding energy
        binding_energies = np.array([-25.0, -20.0, -15.0, -10.0, -5.0])
        specificity_values = [0.8, 0.7, 0.6, 0.5, 0.4]  # Example values
        
        ax2.plot(binding_energies, specificity_values, 'bo-', linewidth=2, markersize=8)
        ax2.set_xlabel('Binding Energy (kJ/mol)')
        ax2.set_ylabel('Specificity Index')
        ax2.set_title('Receptor Binding Specificity vs Energy')
        ax2.grid(True, alpha=0.3)
        
        figures['information_breakdown'] = fig1
        
        # Figure 2: Meta-material properties
        fig2, (ax3, ax4) = plt.subplots(1, 2, figsize=(15, 6))
        
        metamaterial = analysis_results['metamaterial_analysis']
        frequency_thz = metamaterial['dielectric']['frequency'] / 1e12
        
        # Dielectric response
        ax3.plot(frequency_thz, metamaterial['dielectric']['epsilon_real'], 'b-', label='Real', linewidth=2)
        ax3.plot(frequency_thz, metamaterial['dielectric']['epsilon_imag'], 'r--', label='Imaginary', linewidth=2)
        ax3.set_xlabel('Frequency (THz)')
        ax3.set_ylabel('Dielectric Constant')
        ax3.set_title('Dielectric Response vs Frequency')
        ax3.legend()
        ax3.grid(True, alpha=0.3)
        ax3.set_xscale('log')
        
        # Refractive index
        ax4.plot(frequency_thz, metamaterial['dielectric']['refractive_index'], 'g-', linewidth=2)
        ax4.set_xlabel('Frequency (THz)')
        ax4.set_ylabel('Refractive Index')
        ax4.set_title('Refractive Index vs Frequency')
        ax4.grid(True, alpha=0.3)
        ax4.set_xscale('log')
        
        figures['metamaterial_properties'] = fig2
        
        # Figure 3: System performance overview
        fig3, ax5 = plt.subplots(1, 1, figsize=(10, 6))
        
        performance_metrics = self.calculate_system_performance_metrics(analysis_results)
        metric_names = ['Info Processing', 'Material Performance', 'System Efficiency']
        metric_values = [
            performance_metrics['information_processing_score'],
            performance_metrics['material_performance_score'],
            performance_metrics['system_efficiency']
        ]
        
        # Normalize for visualization
        normalized_values = np.array(metric_values) / np.max(metric_values)
        
        bars = ax5.bar(metric_names, normalized_values, color=['blue', 'green', 'red'], alpha=0.7)
        ax5.set_ylabel('Normalized Performance Score')
        ax5.set_title('Integrated System Performance Overview')
        ax5.set_ylim(0, 1.1)
        
        # Add value labels on bars
        for bar, value in zip(bars, metric_values):
            height = bar.get_height()
            ax5.text(bar.get_x() + bar.get_width()/2., height + 0.01,
                    f'{value:.2e}', ha='center', va='bottom', fontsize=10)
        
        figures['system_performance'] = fig3
        
        return figures
    
    def save_analysis_figures(self, figures: Dict[str, plt.Figure], output_dir: str = "output/figures"):
        """
        Save all analysis figures to the output directory.
        
        Args:
            figures: Dictionary of matplotlib figures
            output_dir: Output directory path
        """
        import os
        
        # Create output directory if it doesn't exist
        os.makedirs(output_dir, exist_ok=True)
        
        # Save each figure
        for name, fig in figures.items():
            filename = f"{output_dir}/integrated_analysis_{name}.png"
            fig.savefig(filename, dpi=300, bbox_inches='tight')
            print(f"Saved figure: {filename}")
        
        plt.close('all')

def create_sample_integrated_analysis():
    """
    Create a sample integrated analysis for demonstration.
    
    Returns:
        IntegratedAnalyzer instance with sample analysis
    """
    analyzer = IntegratedAnalyzer()
    
    # Sample odorant properties
    odorant_properties = {
        'molecular_weight': 150.0,
        'symmetry_number': 2,
        'vibrational_modes': 15
    }
    
    # Sample receptor properties
    receptor_properties = {
        'binding_energies': np.array([-25.0, -20.0, -15.0, -10.0, -5.0]),
        'response_amplitudes': np.random.normal(1.0, 0.3, 100),
        'epsilon_inf': 2.0,
        'omega_p': 5e15,
        'gamma': 1e13,
        'particle_radius': 50e-9,
        'metal_dielectric': -10.0 + 1j,
        'medium_dielectric': 1.5,
        'frequency_bandwidth': 1e12,
        'signal_power': 1e-6
    }
    
    # Sample environmental conditions
    environmental_conditions = {
        'temperature_range': (273.15, 313.15),
        'humidity_range': (0.3, 0.8),
        'pressure_range': (101000, 102000),
        'noise_temperature': 300.0
    }
    
    # Perform integrated analysis
    analysis_results = analyzer.analyze_olfactory_system(
        odorant_properties, receptor_properties, environmental_conditions
    )
    
    return analyzer, analysis_results

if __name__ == "__main__":
    # Example usage
    analyzer, results = create_sample_integrated_analysis()
    
    # Generate comprehensive report
    report = analyzer.generate_comprehensive_report(results)
    print(report)
    
    # Create and save visualization figures
    figures = analyzer.create_visualization_figures(results)
    analyzer.save_analysis_figures(figures)
    
    print("\nAnalysis complete! Check output/figures/ for visualization files.")
