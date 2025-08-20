from src.integrated_analysis import create_sample_integrated_analysis


def test_integrated_analysis_save_figures(tmp_path):
    analyzer, results = create_sample_integrated_analysis()
    figs = analyzer.create_visualization_figures(results)
    outdir = tmp_path / 'figs'
    analyzer.save_analysis_figures(figs, output_dir=str(outdir))
    saved = list(outdir.glob('*.png'))
    assert len(saved) >= 1


