from typing import Dict, List, Any
import requests

from .models import Lead
from .utils import log_action, normalize_domain


class HunterClient:
    def __init__(self, api_key: str, timeout_seconds: int = 30) -> None:
        self.api_key = api_key.strip()
        self.timeout_seconds = timeout_seconds
        self.base_url = "https://api.hunter.io/v2"

    def _get(self, path: str, params: Dict[str, Any]) -> Dict[str, Any]:
        url = f"{self.base_url}{path}"
        params = {**params, "api_key": self.api_key}
        log_action(f"Calling Hunter API: {path}")
        response = requests.get(url, params=params, timeout=self.timeout_seconds)
        response.raise_for_status()
        return response.json()

    def domain_search(self, domain: str) -> List[Lead]:
        clean_domain = normalize_domain(domain)
        try:
            data = self._get("/domain-search", {"domain": clean_domain, "limit": 100})
        except requests.HTTPError as exc:
            response = exc.response
            if response is not None:
                try:
                    payload = response.json()
                except ValueError:
                    payload = {}
                errors = payload.get("errors") or []
                if any(err.get("id") == "pagination_error" for err in errors):
                    log_action("Plan limit detected. Retrying Hunter Domain Search with limit=10.")
                    data = self._get("/domain-search", {"domain": clean_domain, "limit": 10})
                else:
                    raise
            else:
                raise
        emails = data.get("data", {}).get("emails", [])
        leads: List[Lead] = []
        for item in emails:
            first_name = (item.get("first_name") or "").strip()
            last_name = (item.get("last_name") or "").strip()
            role = (item.get("position") or item.get("title") or "").strip()
            email = (item.get("value") or "").strip()
            confidence = int(item.get("confidence") or 0)
            company = (item.get("company") or domain).strip()
            if not email:
                continue
            leads.append(
                Lead(
                    first_name=first_name,
                    last_name=last_name,
                    role=role,
                    email=email,
                    confidence=confidence,
                    company=company,
                )
            )
        return leads

    def email_finder(self, domain: str, first_name: str, last_name: str, company: str) -> Lead | None:
        if not first_name or not last_name:
            return None
        data = self._get(
            "/email-finder",
            {"domain": domain, "first_name": first_name, "last_name": last_name},
        )
        record = data.get("data") or {}
        email = (record.get("email") or "").strip()
        if not email:
            return None
        confidence = int(record.get("score") or record.get("confidence") or 0)
        return Lead(
            first_name=first_name,
            last_name=last_name,
            role=(record.get("position") or "").strip(),
            email=email,
            confidence=confidence,
            company=company,
        )
