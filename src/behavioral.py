"""
Behavioral response analysis functions.

This module provides functions for analyzing behavioral response data,
including statistical testing and effect size calculations.
"""

import numpy as np
from typing import List, Dict, Optional, Union
from scipy import stats
from .core import validate_numeric_inputs, safe_division
import matplotlib.pyplot as plt


class BehavioralData:
    """Container for behavioral response data with validation."""
    
    def __init__(self, treatment_times: List[float], control_times: List[float]):
        """
        Initialize behavioral data.
        
        Args:
            treatment_times: Response times under treatment conditions
            control_times: Response times under control conditions
            
        Raises:
            ValueError: If inputs are invalid
        """
        if not isinstance(treatment_times, list) or not isinstance(control_times, list):
            raise ValueError("Treatment and control times must be lists")
        
        if not treatment_times or not control_times:
            raise ValueError("Both treatment and control times must contain data")
        
        # Validate all values are positive numbers
        for i, time in enumerate(treatment_times):
            if not isinstance(time, (int, float)) or time <= 0:
                raise ValueError(f"Treatment time at index {i} must be a positive number, got {time}")
        
        for i, time in enumerate(control_times):
            if not isinstance(time, (int, float)) or time <= 0:
                raise ValueError(f"Control time at index {i} must be a positive number, got {time}")
        
        self.treatment_times = np.array(treatment_times, dtype=float)
        self.control_times = np.array(control_times, dtype=float)
    
    @property
    def treatment_mean(self) -> float:
        """Mean response time under treatment conditions."""
        return float(np.mean(self.treatment_times))
    
    @property
    def control_mean(self) -> float:
        """Mean response time under control conditions."""
        return float(np.mean(self.control_times))
    
    @property
    def treatment_std(self) -> float:
        """Standard deviation of treatment response times."""
        return float(np.std(self.treatment_times, ddof=1))
    
    @property
    def control_std(self) -> float:
        """Standard deviation of control response times."""
        return float(np.std(self.control_times, ddof=1))
    
    @property
    def difference(self) -> float:
        """Difference between treatment and control means."""
        return self.treatment_mean - self.control_mean
    
    @property
    def can_perform_statistics(self) -> bool:
        """Check if we have enough data for statistical testing."""
        return len(self.treatment_times) >= 2 and len(self.control_times) >= 2
    
    @property
    def sample_sizes(self) -> Dict[str, int]:
        """Get sample sizes for both groups."""
        return {
            'treatment': len(self.treatment_times),
            'control': len(self.control_times)
        }


class StatisticalAnalyzer:
    """Statistical analysis for behavioral data."""
    
    def __init__(self, alpha: float = 0.05):
        """
        Initialize statistical analyzer.
        
        Args:
            alpha: Significance level for hypothesis testing
        """
        self.alpha = alpha
    
    def perform_t_test(self, behavioral_data: BehavioralData) -> Dict[str, float]:
        """
        Perform independent t-test comparing treatment and control groups.
        
        Args:
            behavioral_data: BehavioralData object to analyze
            
        Returns:
            Dictionary containing t-test results
        """
        if not behavioral_data.can_perform_statistics:
            return {
                't_statistic': np.nan,
                'p_value': np.nan,
                'degrees_of_freedom': np.nan
            }
        
        try:
            t_stat, p_value = stats.ttest_ind(
                behavioral_data.treatment_times, 
                behavioral_data.control_times,
                equal_var=False  # Welch's t-test
            )
            
            # Calculate degrees of freedom for Welch's t-test
            n1, n2 = len(behavioral_data.treatment_times), len(behavioral_data.control_times)
            s1, s2 = behavioral_data.treatment_std, behavioral_data.control_std
            
            # Welch-Satterthwaite equation
            df = ((s1**2/n1 + s2**2/n2)**2) / ((s1**2/n1)**2/(n1-1) + (s2**2/n2)**2/(n2-1))
            
            return {
                't_statistic': float(t_stat),
                'p_value': float(p_value),
                'degrees_of_freedom': float(df)
            }
            
        except Exception:
            # Return NaN values if statistical test fails
            return {
                't_statistic': np.nan,
                'p_value': np.nan,
                'degrees_of_freedom': np.nan
            }
    
    def calculate_cohens_d(self, behavioral_data: BehavioralData) -> float:
        """
        Calculate Cohen's d effect size.
        
        Args:
            behavioral_data: BehavioralData object to analyze
            
        Returns:
            Cohen's d effect size
        """
        if not behavioral_data.can_perform_statistics:
            return np.nan
        
        try:
            # Calculate pooled standard deviation
            n1, n2 = len(behavioral_data.treatment_times), len(behavioral_data.control_times)
            s1, s2 = behavioral_data.treatment_std, behavioral_data.control_std
            
            # Pooled standard deviation
            pooled_std = np.sqrt(((n1 - 1) * s1**2 + (n2 - 1) * s2**2) / (n1 + n2 - 2))
            
            if pooled_std == 0:
                return np.nan
            
            # Cohen's d
            cohens_d = behavioral_data.difference / pooled_std
            return float(cohens_d)
            
        except Exception:
            return np.nan
    
    def calculate_confidence_interval(self, behavioral_data: BehavioralData, 
                                   confidence: float = 0.95) -> Dict[str, float]:
        """
        Calculate confidence interval for the mean difference.
        
        Args:
            behavioral_data: BehavioralData object to analyze
            confidence: Confidence level (default: 0.95)
            
        Returns:
            Dictionary containing confidence interval bounds
        """
        if not behavioral_data.can_perform_statistics:
            return {
                'lower_bound': np.nan,
                'upper_bound': np.nan,
                'confidence_level': confidence
            }
        
        try:
            # Use Welch's t-test for confidence interval
            t_result = self.perform_t_test(behavioral_data)
            
            if np.isnan(t_result['t_statistic']):
                return {
                    'lower_bound': np.nan,
                    'upper_bound': np.nan,
                    'confidence_level': confidence
                }
            
            # Calculate standard error of the difference
            n1, n2 = len(behavioral_data.treatment_times), len(behavioral_data.control_times)
            s1, s2 = behavioral_data.treatment_std, behavioral_data.control_std
            
            se_diff = np.sqrt(s1**2/n1 + s2**2/n2)
            
            # Critical t-value
            df = t_result['degrees_of_freedom']
            t_critical = stats.t.ppf((1 + confidence) / 2, df)
            
            # Confidence interval
            margin_of_error = t_critical * se_diff
            lower_bound = behavioral_data.difference - margin_of_error
            upper_bound = behavioral_data.difference + margin_of_error
            
            return {
                'lower_bound': float(lower_bound),
                'upper_bound': float(upper_bound),
                'confidence_level': confidence
            }
            
        except Exception:
            return {
                'lower_bound': np.nan,
                'upper_bound': np.nan,
                'confidence_level': confidence
            }


class BehavioralAnalyzer:
    """Main analyzer for behavioral response data."""
    
    def __init__(self, alpha: float = 0.05):
        """
        Initialize behavioral analyzer.
        
        Args:
            alpha: Significance level for hypothesis testing
        """
        self.statistical_analyzer = StatisticalAnalyzer(alpha)
        self.alpha = alpha
    
    def analyze_response(self, treatment_times: List[float], 
                        control_times: List[float]) -> Dict:
        """
        Perform comprehensive behavioral response analysis.
        
        Args:
            treatment_times: Response times under treatment conditions
            control_times: Response times under control conditions
            
        Returns:
            Dictionary containing analysis results
        """
        # Create behavioral data object
        behavioral_data = BehavioralData(treatment_times, control_times)
        
        # Perform statistical analysis
        t_test_results = self.statistical_analyzer.perform_t_test(behavioral_data)
        cohens_d = self.statistical_analyzer.calculate_cohens_d(behavioral_data)
        confidence_interval = self.statistical_analyzer.calculate_confidence_interval(behavioral_data)
        
        # Determine significance
        significant = False
        if not np.isnan(t_test_results['p_value']):
            significant = t_test_results['p_value'] < self.alpha
        
        # Compile results
        results = {
            'treatment_mean': behavioral_data.treatment_mean,
            'control_mean': behavioral_data.control_mean,
            'difference': behavioral_data.difference,
            'treatment_std': behavioral_data.treatment_std,
            'control_std': behavioral_data.control_std,
            'sample_sizes': behavioral_data.sample_sizes,
            't_statistic': t_test_results['t_statistic'],
            'p_value': t_test_results['p_value'],
            'degrees_of_freedom': t_test_results['degrees_of_freedom'],
            'cohens_d': cohens_d,
            'significant': significant,
            'alpha': self.alpha,
            **confidence_interval
        }
        
        return results


def analyze_behavioral_response(treatment: str, 
                              response_times: List[float],
                              control_times: List[float]) -> Dict:
    """
    Analyze behavioral response data comparing treatment to control.
    
    Args:
        treatment: Description of the treatment
        response_times: Response times under treatment conditions
        control_times: Response times under control conditions
        
    Returns:
        Dictionary containing statistical analysis results
        
    Raises:
        ValueError: If inputs are invalid
    """
    # Create analyzer and perform analysis
    analyzer = BehavioralAnalyzer()
    results = analyzer.analyze_response(response_times, control_times)
    
    # Add treatment description
    results['treatment'] = str(treatment)
    
    return results


def calculate_power_analysis(treatment_times: List[float], 
                           control_times: List[float],
                           alpha: float = 0.05) -> Dict[str, float]:
    """
    Calculate statistical power for the comparison.
    
    Args:
        treatment_times: Response times under treatment conditions
        control_times: Response times under control conditions
        alpha: Significance level
        
    Returns:
        Dictionary containing power analysis results
    """
    try:
        from scipy import stats
        
        # Calculate effect size
        behavioral_data = BehavioralData(treatment_times, control_times)
        cohens_d = abs(behavioral_data.difference / behavioral_data.treatment_std)
        
        # Calculate power using t-test power analysis
        n1, n2 = len(treatment_times), len(control_times)
        
        # Use the smaller sample size for conservative estimate
        n = min(n1, n2)
        
        # Calculate power
        power = stats.power.tt_ind_solve_power(
            effect_size=cohens_d,
            nobs1=n,
            alpha=alpha,
            ratio=1.0
        )
        
        return {
            'power': float(power),
            'effect_size': float(cohens_d),
            'sample_size': n,
            'alpha': alpha
        }
        
    except Exception:
        return {
            'power': np.nan,
            'effect_size': np.nan,
            'sample_size': np.nan,
            'alpha': alpha
        }


def calculate_response_statistics(response_data: np.ndarray,
                                time_points: np.ndarray,
                                baseline_period: float = 0.0) -> Dict[str, float]:
    """
    Calculate comprehensive statistics for behavioral response data.
    
    Args:
        response_data: Array of response amplitudes over time
        time_points: Array of time points corresponding to responses
        baseline_period: Time period to use for baseline calculation
        
    Returns:
        Dictionary with response statistics
    """
    # Find baseline period
    if baseline_period > 0:
        baseline_mask = time_points <= baseline_period
        baseline_response = np.mean(response_data[baseline_mask])
    else:
        baseline_response = 0.0
    
    # Calculate response relative to baseline
    relative_response = response_data - baseline_response
    
    # Basic statistics
    mean_response = np.mean(relative_response)
    std_response = np.std(relative_response)
    max_response = np.max(relative_response)
    min_response = np.min(relative_response)
    
    # Response timing
    max_response_time = time_points[np.argmax(relative_response)]
    min_response_time = time_points[np.argmin(relative_response)]
    
    # Response dynamics
    response_range = max_response - min_response
    response_variance = np.var(relative_response)
    
    # Signal-to-noise ratio
    signal_power = np.var(relative_response)
    noise_power = np.var(response_data[response_data < np.percentile(response_data, 25)])
    snr = signal_power / (noise_power + 1e-12)
    
    return {
        'mean_response': float(mean_response),
        'std_response': float(std_response),
        'max_response': float(max_response),
        'min_response': float(min_response),
        'response_range': float(response_range),
        'response_variance': float(response_variance),
        'max_response_time': float(max_response_time),
        'min_response_time': float(min_response_time),
        'signal_to_noise_ratio': float(snr),
        'baseline_response': float(baseline_response)
    }

def generate_behavioral_plots(response_data: np.ndarray,
                             time_points: np.ndarray,
                             stimulus_times: Optional[List[float]] = None,
                             plot_type: str = 'time_series') -> plt.Figure:
    """
    Generate behavioral response plots.
    
    Args:
        response_data: Array of response amplitudes over time
        time_points: Array of time points corresponding to responses
        stimulus_times: Optional list of stimulus presentation times
        plot_type: Type of plot ('time_series', 'histogram', 'both')
        
    Returns:
        Matplotlib figure with behavioral plots
    """
    if plot_type == 'time_series':
        fig, ax = plt.subplots(1, 1, figsize=(12, 6))
        
        # Plot response over time
        ax.plot(time_points, response_data, 'b-', linewidth=2, label='Response')
        
        # Add stimulus markers if provided
        if stimulus_times:
            for stim_time in stimulus_times:
                ax.axvline(x=stim_time, color='red', linestyle='--', alpha=0.7, 
                          label='Stimulus' if stim_time == stimulus_times[0] else "")
        
        ax.set_xlabel('Time (s)')
        ax.set_ylabel('Response Amplitude')
        ax.set_title('Behavioral Response Over Time')
        ax.legend()
        ax.grid(True, alpha=0.3)
        
    elif plot_type == 'histogram':
        fig, ax = plt.subplots(1, 1, figsize=(10, 6))
        
        # Plot response distribution
        ax.hist(response_data, bins=30, alpha=0.7, color='green', edgecolor='black')
        ax.axvline(np.mean(response_data), color='red', linestyle='--', linewidth=2,
                  label=f'Mean: {np.mean(response_data):.2f}')
        ax.axvline(np.median(response_data), color='orange', linestyle='--', linewidth=2,
                  label=f'Median: {np.median(response_data):.2f}')
        
        ax.set_xlabel('Response Amplitude')
        ax.set_ylabel('Frequency')
        ax.set_title('Response Amplitude Distribution')
        ax.legend()
        ax.grid(True, alpha=0.3)
        
    elif plot_type == 'both':
        fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(16, 6))
        
        # Time series plot
        ax1.plot(time_points, response_data, 'b-', linewidth=2, label='Response')
        if stimulus_times:
            for stim_time in stimulus_times:
                ax1.axvline(x=stim_time, color='red', linestyle='--', alpha=0.7,
                           label='Stimulus' if stim_time == stimulus_times[0] else "")
        ax1.set_xlabel('Time (s)')
        ax1.set_ylabel('Response Amplitude')
        ax1.set_title('Behavioral Response Over Time')
        ax1.legend()
        ax1.grid(True, alpha=0.3)
        
        # Histogram plot
        ax2.hist(response_data, bins=30, alpha=0.7, color='green', edgecolor='black')
        ax2.axvline(np.mean(response_data), color='red', linestyle='--', linewidth=2,
                   label=f'Mean: {np.mean(response_data):.2f}')
        ax2.axvline(np.median(response_data), color='orange', linestyle='--', linewidth=2,
                   label=f'Median: {np.median(response_data):.2f}')
        ax2.set_xlabel('Response Amplitude')
        ax2.set_ylabel('Frequency')
        ax2.set_title('Response Amplitude Distribution')
        ax2.legend()
        ax2.grid(True, alpha=0.3)
        
    else:
        raise ValueError("plot_type must be 'time_series', 'histogram', or 'both'")
    
    plt.tight_layout()
    return fig
