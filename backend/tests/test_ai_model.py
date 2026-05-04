import pandas as pd
import pytest

from backend.src.services.ai_model import SpamDetector


def test_spam_detector_train_load_predict(tmp_path, monkeypatch):
    detector = SpamDetector()
    monkeypatch.setattr(detector, "model_path", str(tmp_path / "spam_m.pkl"))
    monkeypatch.setattr(detector, "vectorizer_path", str(tmp_path / "vec.pkl"))

    df = pd.DataFrame(
        {
            "body": [
                "win prize click now limited offer",
                "urgent verify account bank details",
                "meeting at 3pm for project review",
                "notes from lecture attached below",
                "coffee tomorrow still good",
            ]
            * 3,
            "is_spam": [1, 1, 0, 0, 0] * 3,
        }
    )
    X_train, _X_test, y_train, _y_test = detector.prepare_data(df)
    detector.train(X_train, y_train)
    assert detector.load_model()

    pred = detector.predict("winner prize claim your free gift now")
    assert pred in (0, 1)
