import json
import re
import time
from typing import Protocol

import requests

from backend.src.domain.models import AnalysisResult, EmailMessage


class AiClient(Protocol):
    def analyze_email(self, email_message: EmailMessage) -> AnalysisResult:
        ...


class MockAiClient:
    """API anahtarı yokken veya testlerde kullanılır."""

    def analyze_email(self, email_message: EmailMessage) -> AnalysisResult:
        body_lower = (email_message.body or "").lower()
        suspicious = any(
            w in body_lower
            for w in ("winner", "urgent", "verify", "click here", "prize", "bitcoin")
        )
        if suspicious:
            return AnalysisResult(
                risk_score=88,
                label="spam",
                reason="Heuristic mock: suspicious keywords.",
                model_name="mock-model",
            )
        return AnalysisResult(
            risk_score=12,
            label="safe",
            reason="Heuristic mock: no strong signals.",
            model_name="mock-model",
        )


class OpenAiCompatibleClient:
    def __init__(
        self,
        api_key: str,
        base_url: str,
        model: str,
        max_retries: int = 3,
        retry_delay_seconds: float = 1.0,
    ) -> None:
        self.api_key = api_key
        self.base_url = base_url.rstrip("/")
        self.model = model
        self.max_retries = max_retries
        self.retry_delay_seconds = retry_delay_seconds

    def analyze_email(self, email_message: EmailMessage) -> AnalysisResult:
        prompt = (
            "You are an email security analyst. Assess phishing, malware links, credential harvesting, "
            "spoofed senders, and financial fraud. Return ONLY valid JSON in this format: "
            '{"risk_score": <0-100 int>, "label": "spam|safe", "reason": "<short reason>"}.\n\n'
            f"From: {email_message.sender}\n"
            f"Subject: {email_message.subject}\n"
            f"Body: {email_message.body[:4000]}"
        )

        last_error: Exception | None = None
        for attempt in range(1, self.max_retries + 1):
            try:
                response = requests.post(
                    f"{self.base_url}/chat/completions",
                    headers={
                        "Authorization": f"Bearer {self.api_key}",
                        "Content-Type": "application/json",
                    },
                    json={
                        "model": self.model,
                        "messages": [
                            {
                                "role": "system",
                                "content": (
                                    "You classify emails for security. "
                                    "Respond with a single JSON object only, no markdown."
                                ),
                            },
                            {"role": "user", "content": prompt},
                        ],
                        "temperature": 0,
                    },
                    timeout=30,
                )
                response.raise_for_status()
                payload = response.json()
                text = payload["choices"][0]["message"]["content"]
                data = self._extract_json(text)
                return self._to_result(data)
            except (
                requests.RequestException,
                ValueError,
                KeyError,
                TypeError,
                json.JSONDecodeError,
            ) as exc:
                last_error = exc
                if attempt < self.max_retries:
                    time.sleep(self.retry_delay_seconds * attempt)

        reason = (
            "AI analysis failed after retries"
            if last_error is None
            else f"AI analysis failed after retries: {type(last_error).__name__}"
        )
        return AnalysisResult(
            risk_score=50,
            label="safe",
            reason=reason,
            model_name=f"{self.model}-fallback",
        )

    def _to_result(self, data: dict) -> AnalysisResult:
        risk_score = int(data.get("risk_score", 50))
        risk_score = max(0, min(100, risk_score))
        label = str(data.get("label", "safe")).lower()
        if label not in {"spam", "safe"}:
            label = "spam" if risk_score >= 50 else "safe"
        reason = str(data.get("reason", "Model did not provide reason")).strip()

        return AnalysisResult(
            risk_score=risk_score,
            label=label,
            reason=reason,
            model_name=self.model,
        )

    @staticmethod
    def _extract_json(text: str) -> dict:
        text = text.strip()
        if text.startswith("{") and text.endswith("}"):
            return json.loads(text)

        match = re.search(r"\{.*\}", text, re.DOTALL)
        if not match:
            raise ValueError("AI response does not contain JSON")
        return json.loads(match.group(0))
