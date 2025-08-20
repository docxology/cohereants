"""
Core utility functions for insect perception research.

This module provides fundamental calculations and conversions used across
the analysis pipeline. It includes physics-based calculations for wavelength
conversions, atmospheric transmission modeling, and response time analysis.

Key Functions:
- calculate_wavelength_from_wavenumber: Convert IR wavenumbers to wavelengths
- calculate_wavenumber_from_wavelength: Convert IR wavelengths to wavenumbers
- calculate_atmospheric_transmission: Model IR transmission through atmosphere
- calculate_response_time_improvement: Compare traditional vs insect response times

Examples:
    >>> from src.core import calculate_wavelength_from_wavenumber
    >>> wavelength = calculate_wavelength_from_wavenumber(2900)  # CHC peak
    >>> print(f"Wavelength: {wavelength:.2f} μm")
    Wavelength: 3.45 μm

    >>> from src.core import calculate_atmospheric_transmission
    >>> transmission = calculate_atmospheric_transmission([3, 10, 20])
    >>> print(f"Transmission at 10μm: {transmission[1]:.2f}")
    Transmission at 10μm: 0.90
"""

import numpy as np
from typing import Union, List, Optional
import warnings


def calculate_wavelength_from_wavenumber(wavenumber: Union[float, int, np.ndarray, List[float]]) -> Union[float, np.ndarray]:
    """
    Convert wavenumber (cm⁻¹) to wavelength (μm).

    This function converts infrared spectroscopy wavenumbers to wavelengths using
    the relationship: wavelength = 10000 / wavenumber.

    Args:
        wavenumber: Wavenumber in cm⁻¹ (scalar, int, or array-like). Must be positive.

    Returns:
        Wavelength in micrometers (scalar or array)

    Raises:
        ValueError: If wavenumber is zero, negative, or invalid
        TypeError: If wavenumber cannot be converted to numeric array

    Examples:
        >>> calculate_wavelength_from_wavenumber(2900)  # CHC C-H stretch
        3.4482758620689657

        >>> import numpy as np
        >>> wavenumbers = np.array([2500, 2900, 3000])
        >>> calculate_wavelength_from_wavenumber(wavenumbers)
        array([4.        , 3.44827586, 3.33333333])

    Notes:
        - Uses the standard IR spectroscopy conversion: λ(μm) = 10000 / ν(cm⁻¹)
        - Common IR peaks: 2900 cm⁻¹ → 3.45 μm (C-H stretch)
        - Handles both scalar and array inputs efficiently
        - Optimized for performance with large arrays
    """
    try:
        wavenumber = np.asarray(wavenumber, dtype=np.float64)
    except (ValueError, TypeError) as e:
        raise TypeError(f"Cannot convert wavenumber to numeric array: {e}")

    if wavenumber.size == 0:
        warnings.warn("Empty wavenumber array provided - returning empty wavelength array",
                     UserWarning, stacklevel=2)
        return np.array([])

    if np.any(wavenumber <= 0) or not np.all(np.isfinite(wavenumber)):
        invalid_mask = (wavenumber <= 0) | ~np.isfinite(wavenumber)
        invalid_values = wavenumber[invalid_mask]
        raise ValueError(f"All wavenumbers must be positive and finite. Invalid values: {invalid_values}")

    # Use vectorized operations for performance
    return np.divide(10000.0, wavenumber, out=np.empty_like(wavenumber), dtype=np.float64)


def calculate_wavenumber_from_wavelength(wavelength: Union[float, np.ndarray]) -> Union[float, np.ndarray]:
    """
    Convert wavelength (μm) to wavenumber (cm^-1).
    
    Args:
        wavelength: Wavelength in micrometers (scalar or array)
        
    Returns:
        Wavenumber in cm^-1 (scalar or array)
        
    Raises:
        ValueError: If wavelength is zero or negative
    """
    wavelength = np.asarray(wavelength)
    
    if wavelength.size == 0:
        return np.array([])
    
    if np.any(wavelength <= 0):
        raise ValueError("All wavelengths must be positive")
    
    return 10000 / wavelength


def calculate_atmospheric_transmission(wavelengths: Union[np.ndarray, List[float], float],
                                    distance: Union[float, np.ndarray] = None) -> Union[float, np.ndarray]:
    """
    Calculate atmospheric transmission for given wavelengths in the infrared spectrum.

    This function models atmospheric transmission windows in the IR spectrum:
    - Mid-IR window: 2-5 μm (80% transmission)
    - Long-wave IR window: 8-14 μm (90% transmission)
    - Far-IR window: 17-25 μm (70% transmission)
    - Outside windows: 10% transmission

    Args:
        wavelengths: Array, list, or scalar of wavelengths in μm. Must be positive.
        distance: Optional distance in meters (for future atmospheric modeling)

    Returns:
        Array or scalar of transmission values between 0 and 1

    Raises:
        ValueError: If wavelengths contain non-positive values

    Examples:
        >>> calculate_atmospheric_transmission(10.0)  # LWIR window
        0.9

        >>> wavelengths = [3, 10, 20, 30]
        >>> transmission = calculate_atmospheric_transmission(wavelengths)
        >>> print(transmission)
        array([0.8, 0.9, 0.7, 0.1])

    Notes:
        - Based on standard atmospheric IR transmission windows
        - Mid-IR (2-5μm): Good for thermal imaging, some absorption by CO2/H2O
        - LWIR (8-14μm): Excellent transmission, used by most IR cameras
        - Far-IR (17-25μm): Moderate transmission, some water vapor absorption
        - Distance parameter reserved for future atmospheric modeling
    """
    wavelengths = np.asarray(wavelengths)
    
    if wavelengths.size == 0:
        return np.array([])
    
    if np.any(wavelengths <= 0):
        raise ValueError("All wavelengths must be positive")
    
    transmission = np.ones_like(wavelengths, dtype=float)
    
    # Mid-infrared window (2-5 μm)
    mid_ir_mask = (wavelengths >= 2) & (wavelengths <= 5)
    transmission[mid_ir_mask] = 0.8
    
    # Long-wave infrared window (8-14 μm)
    lwir_mask = (wavelengths >= 8) & (wavelengths <= 14)
    transmission[lwir_mask] = 0.9
    
    # Far-infrared window (17-25 μm)
    fir_mask = (wavelengths >= 17) & (wavelengths <= 25)
    transmission[fir_mask] = 0.7
    
    # Outside windows - reduced transmission
    outside_windows = ~(mid_ir_mask | lwir_mask | fir_mask)
    transmission[outside_windows] = 0.1
    
    # If input was scalar, return scalar
    if wavelengths.ndim == 0:
        return float(transmission)
    
    return transmission


def calculate_response_time_improvement(traditional_time: Union[float, np.ndarray], 
                                     insect_time: Union[float, np.ndarray]) -> Union[float, np.ndarray]:
    """
    Calculate the improvement in response time compared to traditional olfaction.
    
    Args:
        traditional_time: Traditional olfaction response time in ms (scalar or array)
        insect_time: Insect ORN response time in ms (scalar or array)
        
    Returns:
        Improvement factor (traditional_time / insect_time) (scalar or array)
        
    Raises:
        ValueError: If either time is non-positive
    """
    traditional_time = np.asarray(traditional_time)
    insect_time = np.asarray(insect_time)
    
    # Handle scalar inputs
    if traditional_time.ndim == 0 and insect_time.ndim == 0:
        if traditional_time <= 0:
            raise ValueError("Traditional response time must be positive")
        if insect_time <= 0:
            raise ValueError("Insect response time must be positive")
        return float(traditional_time / insect_time)
    
    # Handle array inputs
    if np.any(traditional_time <= 0):
        raise ValueError("All traditional response times must be positive")
    if np.any(insect_time <= 0):
        raise ValueError("All insect response times must be positive")
    
    return traditional_time / insect_time


def validate_numeric_inputs(*args, **kwargs) -> None:
    """
    Validate that all numeric inputs are finite numbers.
    
    Args:
        *args: Positional arguments to validate
        **kwargs: Keyword arguments to validate
        
    Raises:
        TypeError: If any input is not a numeric type
        ValueError: If any numeric input is not finite
    """
    for i, arg in enumerate(args):
        if not isinstance(arg, (int, float, np.ndarray)):
            raise TypeError(f"Argument {i} must be a numeric type, got {type(arg)}: {arg}")
        
        if isinstance(arg, np.ndarray):
            if not np.issubdtype(arg.dtype, np.number):
                raise TypeError(f"Argument {i} must be a numeric array, got {arg.dtype}")
            if not np.all(np.isfinite(arg)):
                raise ValueError(f"Argument {i} must contain only finite numbers")
        elif not np.isfinite(arg):
            raise ValueError(f"Argument {i} must be a finite number, got {arg}")
    
    for key, value in kwargs.items():
        if not isinstance(value, (int, float, np.ndarray)):
            raise TypeError(f"Keyword argument '{key}' must be a numeric type, got {type(value)}: {value}")
        
        if isinstance(value, np.ndarray):
            if not np.issubdtype(value.dtype, np.number):
                raise TypeError(f"Keyword argument '{key}' must be a numeric array, got {value.dtype}")
            if not np.all(np.isfinite(value)):
                raise ValueError(f"Keyword argument '{key}' must contain only finite numbers")
        elif not np.isfinite(value):
            raise ValueError(f"Keyword argument '{key}' must be a finite number, got {value}")


def safe_division(numerator: Union[float, np.ndarray], 
                 denominator: Union[float, np.ndarray], 
                 default: float = np.inf) -> Union[float, np.ndarray]:
    """
    Safely perform division, returning infinity if denominator is zero.
    Returns NaN for 0/0 case.
    
    Args:
        numerator: The numerator (scalar or array)
        denominator: The denominator (scalar or array)
        default: Value to return if denominator is zero (defaults to infinity)
        
    Returns:
        Result of division or default value (scalar or array)
    """
    numerator = np.asarray(numerator)
    denominator = np.asarray(denominator)
    
    # Handle scalar inputs
    if numerator.ndim == 0 and denominator.ndim == 0:
        if denominator == 0:
            if numerator == 0:
                return np.nan  # 0/0 = NaN
            return default
        return float(numerator / denominator)
    
    # Handle array inputs
    result = np.full_like(numerator, default, dtype=float)
    valid_mask = denominator != 0
    result[valid_mask] = numerator[valid_mask] / denominator[valid_mask]
    
    # Handle 0/0 case for arrays
    zero_zero_mask = (numerator == 0) & (denominator == 0)
    result[zero_zero_mask] = np.nan
    
    return result
