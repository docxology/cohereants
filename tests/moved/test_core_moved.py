import numpy as np
from src.core import (
    calculate_wavelength_from_wavenumber,
    calculate_wavenumber_from_wavelength,
    calculate_atmospheric_transmission,
    calculate_response_time_improvement,
    validate_numeric_inputs,
    safe_division,
)


def test_core_numeric_and_edge_cases():
    assert calculate_wavelength_from_wavenumber(np.array([])).size == 0

    try:
        calculate_wavelength_from_wavenumber('not-a-number')
    except TypeError:
        pass

    assert np.isclose(calculate_wavenumber_from_wavelength(2.5), 4000.0)
    assert np.isclose(calculate_atmospheric_transmission(10.0), 0.9)
    assert np.isclose(calculate_response_time_improvement(10.0, 2.0), 5.0)

    try:
        validate_numeric_inputs('a')
        raise AssertionError('Expected TypeError')
    except TypeError:
        pass

    res = safe_division(0.0, 0.0)
    assert np.isnan(res)


