import numpy as np

from src.case_studies import (
    compute_beam_pattern,
    array_gain,
    design_log_periodic_array,
    atmospheric_transmission_detailed,
    channel_capacity_vs_env,
    min_detectable_power,
    snr_curve,
    operating_point,
    information_rate_time_series,
    rate_coding_metrics,
    nmf_unmix,
    lda_baseline,
    sweep_plasmonic_quality,
    olfactory_active_inference_step,
)


class TestAppendixA_SensillaArray:
    def test_beam_and_gain_and_design(self):
        wl = np.linspace(2.0, 10.0, 50)
        pos = design_log_periodic_array(1.0, 50.0, 1.3, 5)
        gains = np.ones_like(pos)
        out = compute_beam_pattern(wl, pos, gains)
        assert out['wavelengths_um'].shape == wl.shape
        assert out['pattern'].min() >= 0.0 and out['pattern'].max() <= 1.0
        g = array_gain(out['pattern'])
        assert np.isfinite(g)


class TestAppendixB_EnvironmentalChannel:
    def test_transmission_and_capacity(self):
        wl = np.array([3.0, 10.0, 20.0])
        t = atmospheric_transmission_detailed(wl, humidity=0.5, temperature_k=300.0, path_m=100.0)
        assert t.shape == wl.shape and np.all((t >= 0) & (t <= 1))
        grid_h = np.linspace(0.2, 0.8, 5)
        grid_T = np.linspace(280.0, 320.0, 4)
        cap = channel_capacity_vs_env(1.5, 1e-6, 1e6, grid_h, grid_T, 100.0)
        assert cap['capacity_bits_per_s'].shape == (grid_h.size, grid_T.size)


class TestAppendixC_DetectionLimits:
    def test_min_power_and_snr_and_op(self):
        pmin = min_detectable_power(300.0, 1e6, 10.0)
        assert pmin > 0
        s = snr_curve(np.array([0.0, pmin, 10*pmin]), 300.0, 1e6)
        assert s.shape == (3,) and s[-1] > s[1] >= s[0]
        op = operating_point(1.23e6, 3.0)
        assert op['snr_linear'] == pytest.approx(10**(3.0/10.0))


class TestAppendixD_NeuralEncoding:
    def test_info_rate_and_metrics(self):
        x = np.sin(np.linspace(0, 2*np.pi, 1000))
        ir = information_rate_time_series(x, dt_s=0.001, noise_std=0.1)
        assert ir['channel_capacity_bits'] >= 0 and ir['information_rate_bits'] >= 0
        y = np.r_[np.zeros(500), np.ones(500)]
        m = rate_coding_metrics(x, y)
        assert 'd_prime' in m


class TestAppendixE_SpectralUnmixing:
    def test_nmf_and_lda(self):
        rng = np.random.default_rng(42)
        W_true = rng.random((20, 2))
        H_true = rng.random((2, 30))
        X = W_true @ H_true
        nmf = nmf_unmix(X, n_components=2, seed=42)
        assert nmf['W'].shape == (20, 2) and nmf['H'].shape == (2, 30)

        # Two-class toy LDA
        feat = np.vstack([rng.normal(0, 1, (30, 3)), rng.normal(1, 1, (30, 3))])
        lab = np.r_[np.zeros(30), np.ones(30)]
        lda = lda_baseline(feat, lab, seed=42)
        assert 0.5 <= lda['train_accuracy'] <= 1.0


class TestAppendixF_PlasmonicGeometry:
    def test_sweep_q(self):
        radii = np.linspace(10e-9, 200e-9, 10)
        out = sweep_plasmonic_quality(radii, metal_epsilon_imag=1.0, medium_epsilon_real=1.5)
        assert out['q_factor_proxy'].shape == radii.shape
        assert np.all(out['q_factor_proxy'] >= 0)


class TestAppendixG_ActiveInference:
    def test_step(self):
        s = {'x': 1.0, 'y': 0.0}
        p = {'step': 0.1, 'gain': 1.0}
        new_s = olfactory_active_inference_step(s, p)
        assert new_s['x'] < s['x'] and new_s['y'] == pytest.approx(0.0)


import pytest  # placed at end to avoid linters flagging unused if markers vary


