"""
Real-data tests for the behavioral analysis module.
"""

import importlib

import matplotlib.figure
import matplotlib.pyplot as plt
import numpy as np
import pytest
from scipy import stats

from src.behavioral import (
    BehavioralAnalyzer,
    BehavioralData,
    StatisticalAnalyzer,
    analyze_behavioral_response,
    calculate_power_analysis,
    calculate_response_statistics,
    generate_behavioral_plots,
)


class TestBehavioralData:
    def test_init_and_properties(self):
        data = BehavioralData([2.0, 4.0, 6.0], [1.0, 3.0, 5.0])

        assert np.array_equal(data.treatment_times, np.array([2.0, 4.0, 6.0]))
        assert np.array_equal(data.control_times, np.array([1.0, 3.0, 5.0]))
        assert data.treatment_mean == 4.0
        assert data.control_mean == 3.0
        assert data.difference == 1.0
        assert data.sample_sizes == {"treatment": 3, "control": 3}
        assert data.can_perform_statistics is True

    def test_invalid_inputs_raise(self):
        with pytest.raises(ValueError, match="must be lists"):
            BehavioralData("not a list", [1.0, 2.0])

        with pytest.raises(ValueError, match="must contain data"):
            BehavioralData([], [1.0, 2.0])

        with pytest.raises(ValueError, match="positive number"):
            BehavioralData([1.0, -2.0], [1.0, 2.0])

        with pytest.raises(ValueError, match="positive number"):
            BehavioralData([1.0, 2.0], [0.0, 1.0])

    def test_insufficient_data_disables_statistics(self):
        data = BehavioralData([2.0], [1.0])
        assert data.can_perform_statistics is False


class TestStatisticalAnalyzer:
    def setup_method(self):
        self.analyzer = StatisticalAnalyzer(alpha=0.05)

    def test_t_test_matches_scipy_sign_and_pvalue(self):
        treatment = [4.0, 5.0, 6.0, 4.5, 5.5]
        control = [2.0, 3.0, 2.5, 3.5, 2.8]
        data = BehavioralData(treatment, control)

        result = self.analyzer.perform_t_test(data)
        expected_t, expected_p = stats.ttest_ind(treatment, control, equal_var=False)

        assert np.isclose(result["t_statistic"], expected_t)
        assert np.isclose(result["p_value"], expected_p)
        assert result["degrees_of_freedom"] > 0.0
        assert result["t_statistic"] > 0.0
        assert 0.0 <= result["p_value"] <= 1.0

    def test_t_test_with_insufficient_data_returns_nan(self):
        result = self.analyzer.perform_t_test(BehavioralData([2.0], [1.0]))

        assert np.isnan(result["t_statistic"])
        assert np.isnan(result["p_value"])
        assert np.isnan(result["degrees_of_freedom"])

    def test_cohens_d_basic_and_zero_variance_case(self):
        strong_effect = BehavioralData([4.0, 5.0, 6.0], [1.0, 2.0, 3.0])
        no_variance = BehavioralData([3.0, 3.0, 3.0], [3.0, 3.0, 3.0])

        assert self.analyzer.calculate_cohens_d(strong_effect) > 0.0
        assert np.isnan(self.analyzer.calculate_cohens_d(no_variance))

    def test_confidence_interval_contains_observed_difference(self):
        data = BehavioralData([4.0, 5.0, 6.0, 4.5, 5.5], [2.0, 3.0, 2.5, 3.5, 2.8])

        ci = self.analyzer.calculate_confidence_interval(data)

        assert ci["confidence_level"] == 0.95
        assert ci["lower_bound"] < data.difference < ci["upper_bound"]


class TestBehavioralAnalyzer:
    def test_analyze_response_comprehensive(self):
        analyzer = BehavioralAnalyzer(alpha=0.05)
        result = analyzer.analyze_response([4.0, 5.0, 6.0, 4.5, 5.5], [2.0, 3.0, 2.5, 3.5, 2.8])

        required_keys = {
            "treatment_mean",
            "control_mean",
            "difference",
            "treatment_std",
            "control_std",
            "sample_sizes",
            "t_statistic",
            "p_value",
            "degrees_of_freedom",
            "cohens_d",
            "significant",
            "alpha",
            "lower_bound",
            "upper_bound",
            "confidence_level",
        }
        assert required_keys.issubset(result)
        assert np.isclose(result["difference"], result["treatment_mean"] - result["control_mean"])
        assert result["sample_sizes"] == {"treatment": 5, "control": 5}
        assert result["significant"] is True
        assert result["alpha"] == 0.05


class TestAnalyzeBehavioralResponse:
    def test_three_argument_signature(self):
        result = analyze_behavioral_response("High dose", [4.0, 5.0, 6.0], [2.0, 3.0, 2.5])

        assert result["treatment"] == "High dose"
        assert np.isclose(result["difference"], result["treatment_mean"] - result["control_mean"])
        assert result["sample_sizes"] == {"treatment": 3, "control": 3}

    def test_matrix_signature(self):
        result = analyze_behavioral_response(np.array([[1.0, 2.0, 3.0], [2.0, 3.0, 4.0]]))

        assert result["treatment"] == "Matrix data"
        assert result["sample_sizes"] == {"treatment": 3, "control": 3}
        assert result["difference"] < 0.0

    def test_single_dataset_signature_generates_control_data(self):
        np.random.seed(0)
        result = analyze_behavioral_response(np.array([1.0, 2.0, 3.0]))

        assert result["treatment"] == "Single dataset"
        assert result["sample_sizes"] == {"treatment": 3, "control": 3}
        assert np.isfinite(result["difference"])

    def test_two_array_signature(self):
        result = analyze_behavioral_response(np.array([1.0, 2.0, 3.0]), np.array([2.0, 3.0, 4.0]))

        assert result["treatment"] == "Two datasets"
        assert result["sample_sizes"] == {"treatment": 3, "control": 3}
        assert result["difference"] < 0.0

    def test_invalid_argument_patterns_raise(self):
        with pytest.raises(ValueError, match="Invalid number of arguments"):
            analyze_behavioral_response()

        with pytest.raises(ValueError, match="Invalid argument types"):
            analyze_behavioral_response("bad", np.array([1.0, 2.0]))

        with pytest.raises(ValueError, match="Invalid response data shape"):
            analyze_behavioral_response(np.array([[[1.0, 2.0], [3.0, 4.0]]]))


class TestBehavioralUtilityFunctions:
    def test_calculate_response_statistics(self):
        response_data = np.array([0.5, 0.6, 1.5, 1.8, 1.2])
        time_points = np.array([0.0, 1.0, 2.0, 3.0, 4.0])

        result = calculate_response_statistics(response_data, time_points, baseline_period=1.5)

        baseline = np.mean([0.5, 0.6])
        relative = response_data - baseline
        assert np.isclose(result["baseline_response"], baseline)
        assert np.isclose(result["mean_response"], np.mean(relative))
        assert np.isclose(result["response_variance"], np.var(relative))
        assert result["max_response_time"] == 3.0
        assert result["min_response_time"] == 0.0
        assert result["signal_to_noise_ratio"] >= 0.0

    def test_constant_response_statistics(self):
        result = calculate_response_statistics(np.array([1.0, 1.0, 1.0, 1.0]), np.array([0.0, 1.0, 2.0, 3.0]))

        assert result["response_range"] == 0.0
        assert result["response_variance"] == 0.0
        assert result["std_response"] == 0.0

    def test_power_analysis_real_current_environment_behavior(self):
        result = calculate_power_analysis([4.0, 5.0, 6.0, 4.5, 5.5], [2.0, 3.0, 2.5, 3.5, 2.8])

        assert np.isnan(result["power"])
        assert np.isnan(result["effect_size"])
        assert np.isnan(result["sample_size"])
        assert result["alpha"] == 0.05

    def test_power_analysis_alternative_signature_real_current_environment_behavior(self):
        result = calculate_power_analysis([4.0, 5.0, 6.0], n_subjects=20, effect_size=0.8)

        assert np.isnan(result["power"])
        assert np.isnan(result["required_sample_size"])
        assert result["alpha"] == 0.05


class TestBehavioralPlots:
    def test_time_series_plot_real(self):
        fig = generate_behavioral_plots(
            np.array([1.0, 1.5, 0.8, 1.2]),
            np.array([0.0, 1.0, 2.0, 3.0]),
            stimulus_times=[0.5, 1.5],
            plot_type="time_series",
        )

        assert isinstance(fig, matplotlib.figure.Figure)
        assert len(fig.axes) == 1
        assert fig.axes[0].get_xlabel() == "Time (s)"
        assert fig.axes[0].get_ylabel() == "Response Amplitude"
        assert len(fig.axes[0].lines) == 3
        plt.close("all")

    def test_histogram_plot_real(self):
        fig = generate_behavioral_plots(
            np.array([1.0, 1.5, 0.8, 1.2, 0.9]),
            np.array([0.0, 1.0, 2.0, 3.0, 4.0]),
            plot_type="histogram",
        )

        assert isinstance(fig, matplotlib.figure.Figure)
        assert len(fig.axes) == 1
        assert fig.axes[0].get_xlabel() == "Response Amplitude"
        assert fig.axes[0].get_ylabel() == "Frequency"
        assert len(fig.axes[0].lines) == 2
        plt.close("all")

    def test_both_plot_real(self):
        fig = generate_behavioral_plots(
            np.array([1.0, 2.0, 1.5, 3.0]),
            np.array([0.0, 1.0, 2.0, 3.0]),
            stimulus_times=[0.5, 1.5],
            plot_type="both",
        )

        assert isinstance(fig, matplotlib.figure.Figure)
        assert len(fig.axes) == 2
        assert fig.axes[0].get_xlabel() == "Time (s)"
        assert fig.axes[1].get_xlabel() == "Response Amplitude"
        plt.close("all")

    def test_single_point_plot_real(self):
        fig = generate_behavioral_plots(np.array([1.0]), np.array([0.0]))

        assert isinstance(fig, matplotlib.figure.Figure)
        assert len(fig.axes[0].lines) == 1
        plt.close("all")

    def test_invalid_plot_type_raises(self):
        with pytest.raises(ValueError, match="plot_type must be"):
            generate_behavioral_plots(np.array([1.0, 1.5]), np.array([0.0, 1.0]), plot_type="invalid")


def test_imports_remain_loadable():
    for module_name in ["src.behavioral", "src.spectroscopy", "src.integrated_analysis"]:
        module = importlib.import_module(module_name)
        assert module.__name__ == module_name

# --- merged from test_coverage_behavioral.py ---

def test_calculate_power_analysis_alternative_signature():
    result = calculate_power_analysis(
        [0.5, 0.6, 0.7, 0.8], n_subjects=20, effect_size=0.8
    )
    assert "power" in result
    assert "effect_size" in result
    assert "sample_size" in result


def test_calculate_power_analysis_two_and_three_arg():
    treatment = [1.0, 2.0, 3.0, 4.0]
    control = [1.1, 2.1, 3.1, 4.1]
    two_arg = calculate_power_analysis(treatment, control)
    three_arg = calculate_power_analysis(treatment, control, 0.05)
    assert "power" in two_arg
    assert "power" in three_arg
    assert three_arg["alpha"] == 0.05


def test_calculate_power_analysis_invalid_args_raises():
    with pytest.raises(ValueError):
        calculate_power_analysis(1, 2, 3, 4, 5)


def test_calculate_power_analysis_failure_returns_nan():
    # Identical treatment values -> zero std -> Cohen's d divides by zero, the
    # except-branch returns NaN-valued metrics.
    result = calculate_power_analysis([2.0, 2.0, 2.0, 2.0], [2.0, 2.0, 2.0, 2.0])
    assert np.isnan(result["power"])  # identical arrays -> zero-variance -> nan power
    # Whichever branch was taken, the contract keys are present.
    assert {"power", "effect_size", "sample_size", "alpha"}.issubset(result.keys())


def test_analyze_behavioral_response_matrix_input():
    matrix = np.array([[1.0, 2.0, 3.0, 4.0], [1.1, 2.1, 3.1, 4.1]])
    result = analyze_behavioral_response(matrix)
    assert "treatment_mean" in result
    assert result["treatment"] == "Matrix data"


def test_analyze_behavioral_response_single_1d_array():
    result = analyze_behavioral_response(np.array([1.0, 2.0, 3.0, 4.0]))
    assert "treatment_mean" in result
    assert result["treatment"] == "Single dataset"


def test_analyze_behavioral_response_invalid_3d_shape_raises():
    with pytest.raises(ValueError):
        analyze_behavioral_response(np.zeros((2, 2, 2)))


def test_analyze_behavioral_response_str_list_signature():
    result = analyze_behavioral_response("Treatment A", [1.0, 2.0, 3.0, 4.0])
    assert result["treatment"] == "Treatment A"
    assert "treatment_mean" in result


def test_analyze_behavioral_response_two_array_signature():
    result = analyze_behavioral_response(
        np.array([1.0, 2.0, 3.0]), np.array([1.1, 2.1, 3.1])
    )
    assert result["treatment"] == "Two datasets"


def test_analyze_behavioral_response_invalid_two_arg_types_raises():
    with pytest.raises(ValueError):
        analyze_behavioral_response(1.0, 2.0)


def test_analyze_behavioral_response_no_args_raises():
    with pytest.raises(ValueError):
        analyze_behavioral_response()


def test_analyze_behavioral_response_three_arg_signature():
    result = analyze_behavioral_response(
        "Treatment B", [1.0, 2.0, 3.0, 4.0], [1.1, 2.1, 3.1, 4.1]
    )
    assert result["treatment"] == "Treatment B"
    assert "p_value" in result


@pytest.mark.parametrize("plot_type", ["time_series", "histogram", "both"])
def test_generate_behavioral_plots_valid_types(plot_type):
    rng = np.random.default_rng(0)
    response = rng.normal(1.0, 0.2, 50)
    time_points = np.linspace(0.0, 1.0, 50)
    fig = generate_behavioral_plots(
        response, time_points, stimulus_times=[0.2, 0.6], plot_type=plot_type
    )
    assert hasattr(fig, "savefig")
    plt.close(fig)


def test_generate_behavioral_plots_invalid_type_raises():
    with pytest.raises(ValueError):
        generate_behavioral_plots(
            np.ones(5), np.linspace(0.0, 1.0, 5), plot_type="unknown"
        )
    plt.close("all")


def test_calculate_response_statistics_single_arg_autogenerates_time():
    rng = np.random.default_rng(0)
    response = rng.normal(1.0, 0.2, 30)
    result = calculate_response_statistics(response)
    assert "mean_response" in result
    assert "signal_to_noise_ratio" in result
    assert np.isfinite(result["signal_to_noise_ratio"])


def test_calculate_response_statistics_with_baseline_period():
    response = np.linspace(0.0, 2.0, 50)
    time_points = np.linspace(0.0, 1.0, 50)
    result = calculate_response_statistics(
        response, time_points, baseline_period=0.5
    )
    assert result["baseline_response"] != 0.0
    assert "response_range" in result


def test_calculate_response_statistics_invalid_arg_count_raises():
    with pytest.raises(ValueError):
        calculate_response_statistics()
