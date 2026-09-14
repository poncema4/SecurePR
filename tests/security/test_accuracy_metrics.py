from scripts.accuracy_metrics import calculate


def test_accuracy_metrics_confusion_matrix_and_formulas():
    metrics = calculate([
        {"expected": "BLOCK", "actual": "BLOCK"},
        {"expected": "PASS", "actual": "BLOCK"},
        {"expected": "PASS", "actual": "PASS"},
        {"expected": "BLOCK", "actual": "PASS"},
    ])
    assert (metrics.tp, metrics.fp, metrics.tn, metrics.fn) == (1, 1, 1, 1)
    assert metrics.precision == 0.5
    assert metrics.recall == 0.5
    assert metrics.f1 == 0.5


def test_accuracy_metrics_handles_perfect_results():
    metrics = calculate([
        {"expected": "BLOCK", "actual": "BLOCK"},
        {"expected": "PASS", "actual": "PASS"},
    ])
    assert metrics.precision == 1.0
    assert metrics.recall == 1.0
    assert metrics.f1 == 1.0
