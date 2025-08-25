"""
Advanced visualization capabilities for insect analysis research.

This module provides enhanced plotting capabilities, interactive visualizations,
and publication-quality figure generation with better styling and customization
options.

Key Features:
- Publication-quality plots with consistent styling
- Interactive plotting support
- Advanced figure layouts and annotations
- Statistical visualization helpers
- Colorblind-friendly palettes
"""

import numpy as np
import matplotlib.pyplot as plt
import matplotlib.gridspec as gridspec
from matplotlib.patches import Rectangle, Circle
from matplotlib.colors import LinearSegmentedColormap
try:
    import seaborn as sns
    HAS_SEABORN = True
except ImportError:
    HAS_SEABORN = False
from typing import Dict, List, Optional, Tuple, Union, Any
import warnings

# Import configuration system
try:
    from .config import get_config
except ImportError:
    # Fallback for testing
    def get_config():
        class MockConfig:
            def get(self, key, default=None):
                return default
        return MockConfig()


class PlotStyler:
    """
    Advanced plot styling and theming system.

    Provides consistent, publication-quality styling with support for
    colorblind-friendly palettes and academic journal requirements.

    Examples:
        >>> styler = PlotStyler()
        >>> styler.apply_style('nature')
        >>> fig, ax = plt.subplots()
        >>> styler.format_axes(ax, xlabel='Wavenumber (cm⁻¹)', ylabel='Absorbance')
    """

    # Enhanced colorblind-friendly color palettes with better contrast
    COLORBLIND_PALETTE = [
        '#0072B2',  # Blue
        '#E69F00',  # Orange
        '#009E73',  # Green
        '#CC79A7',  # Pink
        '#56B4E9',  # Light blue
        '#D55E00',  # Red
        '#F0E442',  # Yellow
        '#000000'   # Black
    ]

    # High contrast palette for accessibility
    HIGH_CONTRAST_PALETTE = [
        '#000000',  # Black
        '#004488',  # Dark blue
        '#DDAA33',  # Yellow
        '#BB5566',  # Red
        '#000000',  # Black (duplicate for more options)
        '#004488',  # Dark blue
        '#DDAA33',  # Yellow
        '#BB5566'   # Red
    ]

    ACADEMIC_STYLES = {
        # Enhanced accessibility styles with larger fonts and better contrast
        'nature': {
            'font.family': 'sans-serif',
            'font.size': 12,  # Increased from 7 for better readability
            'font.weight': 'normal',
            'axes.linewidth': 1.0,  # Thicker lines for better visibility
            'xtick.major.size': 4,  # Larger ticks
            'ytick.major.size': 4,
            'xtick.major.width': 1.0,
            'ytick.major.width': 1.0,
            'xtick.labelsize': 11,  # Explicit tick label size
            'ytick.labelsize': 11,
            'axes.labelsize': 12,   # Larger axis labels
            'axes.titlesize': 14,   # Larger titles
            'legend.fontsize': 11,  # Larger legend text
            'grid.alpha': 0.4,      # More visible grid
            'figure.dpi': 600,
            'lines.linewidth': 2.0,  # Thicker plot lines
            'lines.markersize': 6    # Larger markers
        },
        'science': {
            'font.family': 'sans-serif',
            'font.size': 13,  # Increased from 8
            'font.weight': 'normal',
            'axes.linewidth': 1.2,  # Thicker lines
            'xtick.major.size': 5,  # Larger ticks
            'ytick.major.size': 5,
            'xtick.major.width': 1.2,
            'ytick.major.width': 1.2,
            'xtick.labelsize': 12,
            'ytick.labelsize': 12,
            'axes.labelsize': 13,
            'axes.titlesize': 15,
            'legend.fontsize': 12,
            'grid.alpha': 0.5,
            'figure.dpi': 600,
            'lines.linewidth': 2.5,
            'lines.markersize': 7
        },
        'ieee': {
            'font.family': 'serif',
            'font.size': 12,  # Increased from 8
            'font.weight': 'normal',
            'axes.linewidth': 1.0,
            'xtick.major.size': 4,
            'ytick.major.size': 4,
            'xtick.major.width': 1.0,
            'ytick.major.width': 1.0,
            'xtick.labelsize': 11,
            'ytick.labelsize': 11,
            'axes.labelsize': 12,
            'axes.titlesize': 14,
            'legend.fontsize': 11,
            'grid.alpha': 0.4,
            'figure.dpi': 300,
            'lines.linewidth': 2.0,
            'lines.markersize': 6
        }
    }

    def __init__(self, style: str = 'default'):
        """
        Initialize plot styler.

        Args:
            style: Initial style to apply ('default', 'nature', 'science', 'ieee')
        """
        self.current_style = style
        self.apply_style(style)

    def apply_style(self, style: str) -> None:
        """
        Apply a predefined style to matplotlib.

        Args:
            style: Style name to apply
        """
        if style == 'default':
            # Reset to matplotlib defaults with some improvements
            try:
                plt.style.use('default')
            except Exception as e:
                warnings.warn(f"Failed to apply base style 'default': {e}")
            plt.rcParams.update({
                'font.size': 10,
                'font.family': 'sans-serif',
                'axes.linewidth': 0.8,
                'axes.grid': True,
                'grid.alpha': 0.3,
                'figure.dpi': 150
            })
        elif style in self.ACADEMIC_STYLES:
            try:
                plt.style.use('default')
            except Exception:
                # If applying the default style fails, continue and attempt to update rcParams
                warnings.warn("Could not apply default style; continuing with rcParams update")
            settings = self.ACADEMIC_STYLES[style]
            try:
                plt.rcParams.update(settings)
            except Exception as e:
                # Handle invalid matplotlib parameters gracefully (KeyError or other)
                warnings.warn(f"Some style parameters may be invalid or update failed: {e}")
                # Update only valid parameters where possible
                try:
                    valid_settings = {k: v for k, v in settings.items() if k in plt.rcParams}
                    if valid_settings:
                        try:
                            plt.rcParams.update(valid_settings)
                        except Exception as e2:
                            warnings.warn(f"Failed to update partial rcParams: {e2}")
                except Exception:
                    # In case plt.rcParams is not subscriptable or other failure
                    pass
        else:
            try:
                plt.style.use(style)
            except OSError:
                warnings.warn(f"Style '{style}' not found, using default")
                self.apply_style('default')

        self.current_style = style

    def get_colors(self, n: int, palette: str = 'colorblind') -> List[str]:
        """
        Get a list of colors from a predefined palette with enhanced accessibility.

        Args:
            n: Number of colors needed
            palette: Palette name ('colorblind', 'high_contrast', 'viridis', 'plasma', 'tab10')

        Returns:
            List of color hex codes optimized for accessibility
        """
        if palette == 'colorblind':
            colors = self.COLORBLIND_PALETTE
        elif palette == 'high_contrast':
            colors = self.HIGH_CONTRAST_PALETTE
        else:
            try:
                cmap = plt.get_cmap(palette)
                colors = [cmap(i/n) for i in range(n)]
                colors = [plt.matplotlib.colors.to_hex(c) for c in colors]
            except ValueError:
                warnings.warn(f"Palette '{palette}' not found, using colorblind")
                colors = self.COLORBLIND_PALETTE

        # Cycle through colors if n > palette size
        return [colors[i % len(colors)] for i in range(n)]

    def format_axes(self, ax: plt.Axes, xlabel: str = None, ylabel: str = None,
                   title: str = None, legend: bool = True, enhance_accessibility: bool = True) -> plt.Axes:
        """
        Format axes with enhanced accessibility and consistent styling.

        Args:
            ax: Matplotlib axes to format
            xlabel: X-axis label
            ylabel: Y-axis label
            title: Plot title
            legend: Whether to show legend if present
            enhance_accessibility: Whether to apply accessibility enhancements

        Returns:
            Formatted axes object
        """
        if xlabel:
            ax.set_xlabel(xlabel, fontweight='bold', fontsize=12)
        if ylabel:
            ax.set_ylabel(ylabel, fontweight='bold', fontsize=12)
        if title:
            ax.set_title(title, fontweight='bold', pad=15, fontsize=14)

        # Enhanced tick formatting for accessibility
        if enhance_accessibility:
            ax.tick_params(axis='both', which='major', labelsize=11, width=1.0, length=4)
            # Ensure minimum tick spacing for readability
            ax.xaxis.set_major_locator(plt.MaxNLocator(6))
            ax.yaxis.set_major_locator(plt.MaxNLocator(6))

        # Add more visible grid for better data reading
        ax.grid(True, alpha=0.4, linestyle='-', linewidth=0.8, color='gray')

        # Remove top and right spines for cleaner look (but keep bottom/left thicker)
        ax.spines['top'].set_visible(False)
        ax.spines['right'].set_visible(False)
        ax.spines['bottom'].set_linewidth(1.2)
        ax.spines['left'].set_linewidth(1.2)

        if legend and ax.get_legend_handles_labels()[1]:
            legend_obj = ax.legend(frameon=True, fancybox=True, shadow=False,
                                 framealpha=0.9, loc='best', fontsize=11)
            # Make legend frame more visible
            legend_obj.get_frame().set_linewidth(1.5)

        # Add subtle background color for better contrast
        if enhance_accessibility:
            ax.set_facecolor('#FAFAFA')

        return ax

    def create_figure_grid(self, rows: int, cols: int, figsize: Tuple[float, float] = None,
                          **kwargs) -> Tuple[plt.Figure, np.ndarray]:
        """
        Create a figure with a grid layout optimized for academic publishing.

        Args:
            rows: Number of subplot rows
            cols: Number of subplot columns
            figsize: Figure size tuple (width, height)
            **kwargs: Additional arguments for plt.subplots

        Returns:
            Tuple of (figure, axes_array)
        """
        if figsize is None:
            # Auto-scale figure size based on grid dimensions
            base_size = 4
            figsize = (base_size * cols, base_size * rows)

        fig, axes = plt.subplots(rows, cols, figsize=figsize, **kwargs)

        # Handle single subplot case to return single axis, not array
        if rows == 1 and cols == 1:
            axes_single = axes  # Keep as single axis object
        else:
            # Ensure axes is always an array for multiple subplots
            axes_single = axes if isinstance(axes, np.ndarray) else np.array([axes])

        # Flatten for easier iteration
        if isinstance(axes, np.ndarray):
            axes_flat = axes.flatten()
        else:
            axes_flat = np.array([axes])

        # Apply consistent formatting to all subplots
        for i, ax in enumerate(axes_flat):
            ax.grid(True, alpha=0.3)

        plt.tight_layout()

        # Return appropriate format based on grid dimensions
        if rows == 1 and cols == 1:
            return fig, axes_single
        else:
            return fig, axes_single


class AdvancedVisualizer:
    """
    Advanced visualization tools for insect analysis data.

    Provides specialized plotting functions for different types of analysis
    with enhanced styling and publication-quality output.

    Examples:
        >>> visualizer = AdvancedVisualizer()
        >>> fig = visualizer.plot_spectral_analysis(wavenumbers, intensities)
        >>> visualizer.save_figure(fig, 'spectral_analysis.png')
    """

    def __init__(self, style: str = 'default'):
        """
        Initialize advanced visualizer.

        Args:
            style: Plot style to use
        """
        self.styler = PlotStyler(style)
        self.config = get_config()

    def plot_spectral_analysis(self, wavenumbers: np.ndarray, intensities: np.ndarray,
                             peaks: Optional[np.ndarray] = None,
                             title: str = "Spectral Analysis") -> plt.Figure:
        """
        Create an advanced spectral analysis plot.

        Args:
            wavenumbers: Wavenumber array
            intensities: Intensity array
            peaks: Optional array of peak positions
            title: Plot title

        Returns:
            Matplotlib figure
        """
        # Basic validation
        if wavenumbers is None or intensities is None:
            raise ValueError("wavenumbers and intensities must be provided")
        if not isinstance(wavenumbers, np.ndarray):
            wavenumbers = np.asarray(wavenumbers)
        if not isinstance(intensities, np.ndarray):
            intensities = np.asarray(intensities)
        if wavenumbers.ndim != 1 or intensities.ndim != 1:
            raise ValueError("wavenumbers and intensities must be 1D arrays")
        if wavenumbers.size != intensities.size:
            raise ValueError("wavenumbers and intensities must have the same length")
        if wavenumbers.size == 0:
            # Return an informative empty figure
            fig, ax = plt.subplots(figsize=(8, 4))
            ax.text(0.5, 0.5, 'Empty spectrum', ha='center', va='center', transform=ax.transAxes,
                    fontsize=12, color='gray')
            ax.axis('off')
            return fig

        fig, (ax1, ax2) = self.styler.create_figure_grid(2, 1, figsize=(12, 10))

        # Main spectrum plot
        colors = self.styler.get_colors(2)
        ax1.plot(wavenumbers, intensities, color=colors[0], linewidth=2, label='Spectrum')

        if peaks is not None:
            peak_intensities = np.interp(peaks, wavenumbers, intensities)
            ax1.scatter(peaks, peak_intensities, color=colors[1], s=100,
                       marker='v', label='Peaks', zorder=5)

        self.styler.format_axes(ax1, xlabel='Wavenumber (cm⁻¹)',
                               ylabel='Intensity (a.u.)', title=title)

        # Derivative plot for peak detection and confidence interval shading
        if len(intensities) > 5:
            from scipy import signal, stats
            derivative = np.gradient(intensities)
            # Estimate a simple moving standard deviation as a proxy for variability
            window = min(7, max(3, len(intensities)//20))
            pad = window // 2
            mov_std = np.array([np.std(intensities[max(0, i-pad):min(len(intensities), i+pad+1)]) for i in range(len(intensities))])

            ax2.plot(wavenumbers, derivative, color=colors[1], linewidth=1.5, label='Derivative')
            # Shade +/- 1 std around derivative to show confidence region
            ax2.fill_between(wavenumbers, derivative - mov_std, derivative + mov_std, color=colors[1], alpha=0.2)
            ax2.axhline(y=0, color='black', linestyle='--', alpha=0.5)
            self.styler.format_axes(ax2, xlabel='Wavenumber (cm⁻¹)',
                                   ylabel='Derivative', title='First Derivative (with local std)')

            # If peaks not provided, try to detect using SciPy's find_peaks
            if peaks is None:
                try:
                    peaks_idx, _ = signal.find_peaks(intensities, prominence=(np.max(intensities)*0.05))
                    peaks = wavenumbers[peaks_idx]
                    peak_vals = intensities[peaks_idx]
                    # annotate peaks on main axis
                    for x, y in zip(peaks, peak_vals):
                        ax1.annotate(f'{x:.1f}', xy=(x, y), xytext=(0, 6), textcoords='offset points', ha='center', fontsize=8)
                except Exception:
                    peaks = None

        plt.tight_layout()
        return fig

    @staticmethod
    def annotate_top_peaks(ax: plt.Axes, wavenumbers: np.ndarray, intensities: np.ndarray,
                           num_peaks: int = 5) -> None:
        """
        Annotate the top-N peaks by intensity on an axes.

        Args:
            ax: Target matplotlib Axes
            wavenumbers: 1D array of wavenumbers (cm⁻¹)
            intensities: 1D array of intensities
            num_peaks: Number of peaks to annotate
        """
        if wavenumbers.ndim != 1 or intensities.ndim != 1 or wavenumbers.size != intensities.size:
            return
        if wavenumbers.size == 0:
            return
        try:
            idx = np.argsort(intensities)[-num_peaks:][::-1]
            for i in idx:
                ax.annotate(f'{wavenumbers[i]:.1f}', xy=(wavenumbers[i], intensities[i]),
                            xytext=(0, 6), textcoords='offset points', ha='center', fontsize=8)
        except Exception:
            # Best-effort: do not raise in visualization helper
            pass

    def plot_correlation_matrix(self, data: Dict[str, np.ndarray],
                              variables: List[str],
                              title: str = "Correlation Analysis") -> plt.Figure:
        """
        Create a correlation matrix visualization.

        Args:
            data: Dictionary of variable arrays
            variables: List of variable names to correlate
            title: Plot title

        Returns:
            Matplotlib figure
        """
        # Create correlation matrix
        n_vars = len(variables)
        corr_matrix = np.zeros((n_vars, n_vars))

        for i, var1 in enumerate(variables):
            for j, var2 in enumerate(variables):
                if var1 in data and var2 in data:
                    corr_matrix[i, j] = np.corrcoef(data[var1], data[var2])[0, 1]

        # Create figure
        fig, ax = plt.subplots(figsize=(10, 8))

        # Create heatmap
        im = ax.imshow(corr_matrix, cmap='RdBu_r', vmin=-1, vmax=1)

        # Add colorbar
        cbar = plt.colorbar(im, ax=ax)
        cbar.set_label('Correlation Coefficient')

        # Add labels
        ax.set_xticks(np.arange(n_vars))
        ax.set_yticks(np.arange(n_vars))
        ax.set_xticklabels(variables, rotation=45, ha='right')
        ax.set_yticklabels(variables)

        # Add correlation values as text
        for i in range(n_vars):
            for j in range(n_vars):
                text = ax.text(j, i, f'{corr_matrix[i, j]:.2f}',
                             ha='center', va='center', color='black')

        ax.set_title(title, fontweight='bold', pad=20)
        plt.tight_layout()

        return fig

    def plot_multi_panel_analysis(self, data_dict: Dict[str, Dict],
                                title: str = "Multi-Panel Analysis",
                                enhance_accessibility: bool = True) -> plt.Figure:
        """
        Create a comprehensive multi-panel analysis figure with enhanced accessibility.

        Args:
            data_dict: Dictionary containing analysis data for each panel
            title: Overall figure title
            enhance_accessibility: Whether to apply accessibility enhancements

        Returns:
            Matplotlib figure
        """
        n_panels = len(data_dict)
        if n_panels <= 3:
            rows, cols = 1, n_panels
        else:
            rows = int(np.ceil(n_panels / 3))
            cols = min(n_panels, 3)

        fig, axes = self.styler.create_figure_grid(rows, cols, figsize=(5*cols, 4*rows))
        axes_flat = axes.flatten()

        colors = self.styler.get_colors(n_panels, palette='high_contrast' if enhance_accessibility else 'colorblind')

        for i, (panel_name, panel_data) in enumerate(data_dict.items()):
            ax = axes_flat[i]

            # Plot based on data type with enhanced styling
            if 'x' in panel_data and 'y' in panel_data:
                line = ax.plot(panel_data['x'], panel_data['y'], color=colors[i], linewidth=2.5,
                             marker='o' if len(panel_data['x']) < 20 else None,
                             markersize=4 if len(panel_data['x']) < 20 else None)
                if 'xlabel' in panel_data:
                    ax.set_xlabel(panel_data['xlabel'], fontweight='bold', fontsize=12)
                if 'ylabel' in panel_data:
                    ax.set_ylabel(panel_data['ylabel'], fontweight='bold', fontsize=12)

                # Add data point annotations for small datasets
                if len(panel_data['x']) <= 10 and 'annotate' in panel_data and panel_data['annotate']:
                    for j, (x_val, y_val) in enumerate(zip(panel_data['x'], panel_data['y'])):
                        ax.annotate(f'({x_val:.1f}, {y_val:.1f})', (x_val, y_val),
                                  textcoords="offset points", xytext=(0, 8), ha='center',
                                  fontsize=9, bbox=dict(boxstyle='round,pad=0.2', facecolor='white', alpha=0.8))

            elif 'histogram_data' in panel_data:
                data = panel_data['histogram_data']
                n, bins, patches = ax.hist(data, bins=30, alpha=0.8, color=colors[i], edgecolor='black', linewidth=1.5)
                if 'xlabel' in panel_data:
                    ax.set_xlabel(panel_data['xlabel'], fontweight='bold', fontsize=12)

                # Add statistics annotation
                if len(data) > 0:
                    mean_val = np.mean(data)
                    std_val = np.std(data)
                    ax.axvline(mean_val, color='red', linestyle='--', linewidth=2, label=f'μ={mean_val:.2f}')
                    ax.text(0.02, 0.98, f'μ={mean_val:.2f}\nσ={std_val:.2f}',
                           transform=ax.transAxes, verticalalignment='top',
                           bbox=dict(boxstyle='round,pad=0.3', facecolor='white', alpha=0.9),
                           fontsize=10, fontweight='bold')

            # Enhanced title and formatting
            ax.set_title(f'{panel_name}', fontweight='bold', fontsize=13, pad=10)

            # Apply accessibility formatting
            if enhance_accessibility:
                ax.grid(True, alpha=0.4, linewidth=0.8)
                ax.tick_params(axis='both', which='major', labelsize=11)

        # Hide unused subplots
        for i in range(n_panels, len(axes_flat)):
            axes_flat[i].set_visible(False)

        # Enhanced main title with better spacing
        fig.suptitle(title, fontsize=16, fontweight='bold', y=0.95)

        # Add metadata annotation
        if enhance_accessibility:
            fig.text(0.02, 0.02, f'Generated with enhanced accessibility features | {len(data_dict)} panels',
                    fontsize=8, style='italic', alpha=0.7)

        plt.tight_layout()
        return fig

    def create_interactive_plot(self, x_data: np.ndarray, y_data: np.ndarray,
                              title: str = "Interactive Plot") -> Any:
        """
        Create an interactive plot if plotly is available.

        Args:
            x_data: X-axis data
            y_data: Y-axis data
            title: Plot title

        Returns:
            Plotly figure or matplotlib figure if plotly unavailable
        """
        try:
            import plotly.graph_objects as go
            import plotly.express as px

            fig = go.Figure(data=go.Scatter(x=x_data, y=y_data, mode='lines+markers'))
            fig.update_layout(
                title=title,
                xaxis_title='X Values',
                yaxis_title='Y Values',
                template='plotly_white'
            )
            return fig

        except ImportError:
            warnings.warn("Plotly not available, falling back to matplotlib")
            fig, ax = plt.subplots(figsize=(10, 6))
            ax.plot(x_data, y_data, 'b-', linewidth=2)
            ax.set_title(title)
            ax.grid(True, alpha=0.3)
            return fig

    def create_statistical_summary_plot(self, data: Dict[str, Any],
                                       title: str = "Statistical Summary") -> plt.Figure:
        """
        Create a comprehensive statistical summary plot with enhanced accessibility.

        Args:
            data: Dictionary containing statistical data to plot
            title: Overall figure title

        Returns:
            Matplotlib figure with statistical summaries
        """
        fig, axes = self.styler.create_figure_grid(2, 2, figsize=(12, 10))

        colors = self.styler.get_colors(8, palette='high_contrast')

        # Panel 1: Data distributions
        if 'distributions' in data:
            ax = axes[0, 0]
            for i, (name, values) in enumerate(data['distributions'].items()):
                if len(values) > 0:
                    ax.hist(values, bins=20, alpha=0.7, color=colors[i],
                           label=f'{name}\nμ={np.mean(values):.2f}', linewidth=1.5)
            ax.set_xlabel('Value', fontweight='bold', fontsize=12)
            ax.set_ylabel('Frequency', fontweight='bold', fontsize=12)
            ax.set_title('Data Distributions', fontweight='bold', fontsize=13)
            ax.legend(fontsize=10)
            ax.grid(True, alpha=0.4)

        # Panel 2: Box plots for comparison
        if 'boxplot_data' in data:
            ax = axes[0, 1]
            labels = list(data['boxplot_data'].keys())
            values = [data['boxplot_data'][label] for label in labels]
            bp = ax.boxplot(values, labels=labels, patch_artist=True)
            for patch, color in zip(bp['boxes'], colors):
                patch.set_facecolor(color)
                patch.set_alpha(0.7)
            ax.set_ylabel('Value', fontweight='bold', fontsize=12)
            ax.set_title('Box Plot Comparison', fontweight='bold', fontsize=13)
            ax.grid(True, alpha=0.4, axis='y')

        # Panel 3: Correlation matrix if available
        if 'correlation_matrix' in data:
            ax = axes[1, 0]
            corr_matrix = data['correlation_matrix']
            im = ax.imshow(corr_matrix, cmap='RdBu_r', vmin=-1, vmax=1)
            ax.set_title('Correlation Matrix', fontweight='bold', fontsize=13)

            # Add correlation values
            for i in range(corr_matrix.shape[0]):
                for j in range(corr_matrix.shape[1]):
                    text = ax.text(j, i, f'{corr_matrix[i, j]:.2f}',
                                 ha='center', va='center', color='black', fontsize=10)

            plt.colorbar(im, ax=ax, shrink=0.8)

        # Panel 4: Summary statistics table
        if 'summary_stats' in data:
            ax = axes[1, 1]
            ax.axis('off')
            stats = data['summary_stats']

            # Create table data
            table_data = []
            for key, values in stats.items():
                if isinstance(values, dict):
                    for subkey, val in values.items():
                        table_data.append([f'{key}\n{subkey}', f'{val:.3f}'])
                else:
                    table_data.append([key, f'{values:.3f}'])

            table = ax.table(cellText=table_data, colLabels=['Metric', 'Value'],
                           loc='center', cellLoc='center', colColours=['lightgray', 'lightgray'])
            table.auto_set_font_size(False)
            table.set_fontsize(10)
            table.scale(1, 1.5)
            ax.set_title('Summary Statistics', fontweight='bold', fontsize=13, pad=20)

        fig.suptitle(title, fontsize=16, fontweight='bold', y=0.95)
        plt.tight_layout()

        return fig

    def save_figure(self, fig: plt.Figure, filename: str,
                   dpi: int = None, format: str = None, enhance_for_accessibility: bool = True) -> None:
        """
        Save figure with optimal settings for publication and accessibility.

        Args:
            fig: Matplotlib figure to save
            filename: Output filename
            dpi: Resolution (uses high DPI for accessibility if None)
            format: File format (inferred from extension if None)
            enhance_for_accessibility: Whether to use high DPI for better accessibility
        """
        if dpi is None:
            dpi = 600 if enhance_for_accessibility else self.config.get('plot_dpi', 300)

        if format is None:
            format = filename.split('.')[-1].lower()

        # Ensure output directory exists
        import os
        os.makedirs(os.path.dirname(filename) if os.path.dirname(filename) else '.',
                   exist_ok=True)

        # Save with enhanced settings for accessibility
        fig.savefig(filename, dpi=dpi, format=format, bbox_inches='tight',
                   facecolor='white', edgecolor='none', pad_inches=0.1)

        print(f"✅ Saved figure: {filename} (DPI: {dpi}, Format: {format}, Accessibility: {enhance_for_accessibility})")


def create_publication_figure(data: Dict[str, Any], style: str = 'nature') -> plt.Figure:
    """
    Create a publication-ready figure with optimal styling.

    Args:
        data: Dictionary containing figure data
        style: Publication style ('nature', 'science', 'ieee')

    Returns:
        Matplotlib figure optimized for publication
    """
    visualizer = AdvancedVisualizer(style)

    # Create figure based on data type
    if 'spectral_data' in data:
        return visualizer.plot_spectral_analysis(
            data['wavenumbers'],
            data['intensities'],
            data.get('peaks'),
            data.get('title', 'Spectral Analysis')
        )
    elif 'correlation_data' in data:
        return visualizer.plot_correlation_matrix(
            data['correlation_data'],
            data['variables'],
            data.get('title', 'Correlation Analysis')
        )
    else:
        # Generic multi-panel figure
        return visualizer.plot_multi_panel_analysis(
            data,
            data.get('title', 'Analysis Figure')
        )


# Convenience functions
def set_plot_style(style: str) -> None:
    """Set the global plot style."""
    styler = PlotStyler()
    styler.apply_style(style)

def get_colorblind_palette(n_colors: int = 8) -> List[str]:
    """Get a colorblind-friendly color palette."""
    styler = PlotStyler()
    return styler.get_colors(n_colors, 'colorblind')

def create_subplots(n_rows: int, n_cols: int, style: str = 'science',
                   figsize: Tuple[float, float] = None,
                   enhance_accessibility: bool = True) -> Tuple[plt.Figure, np.ndarray]:
    """Create subplots with enhanced accessibility and consistent styling."""
    styler = PlotStyler(style)

    # Apply enhanced style for accessibility
    if enhance_accessibility and style in ['nature', 'science', 'ieee']:
        # The styles already include accessibility enhancements
        pass

    return styler.create_figure_grid(n_rows, n_cols, figsize)

def create_accessible_figure(data_dict: Dict[str, Dict], title: str = "Analysis Figure",
                           style: str = 'science') -> plt.Figure:
    """
    Create an accessible figure with enhanced features for better understanding.

    Args:
        data_dict: Dictionary containing plot data for each panel
        title: Overall figure title
        style: Plot style to use

    Returns:
        Matplotlib figure optimized for accessibility
    """
    visualizer = AdvancedVisualizer(style)
    return visualizer.plot_multi_panel_analysis(data_dict, title, enhance_accessibility=True)
