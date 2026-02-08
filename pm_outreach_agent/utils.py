import csv
import os
from dataclasses import dataclass
from typing import Iterable, List, Dict, Any

import yaml

from .models import CompanyInput


@dataclass
class AgentConfig:
    target_roles: List[str]
    excluded_roles: List[str]
    min_email_confidence: int
    portfolio_url: str
    candidate_background_summary: str
    tone: str
    use_openai_drafts: bool
    openai_model: str
    sender_email: str
    use_gmail_drafts: bool
    gmail_credentials_path: str
    gmail_token_path: str
    domains: Dict[str, Any] = None


def load_config(path: str) -> AgentConfig:
    with open(path, "r", encoding="utf-8") as handle:
        raw = yaml.safe_load(handle) or {}
    return AgentConfig(
        target_roles=[role.strip() for role in raw.get("target_roles", [])],
        excluded_roles=[role.strip() for role in raw.get("excluded_roles", [])],
        min_email_confidence=int(raw.get("min_email_confidence", 80)),
        portfolio_url=str(raw.get("portfolio_url", "")).strip(),
        candidate_background_summary=str(raw.get("candidate_background_summary", "")).strip(),
        tone=str(raw.get("tone", "professional")).strip(),
        use_openai_drafts=bool(raw.get("use_openai_drafts", False)),
        openai_model=str(raw.get("openai_model", "gpt-4o-mini")).strip(),
        sender_email=str(raw.get("sender_email", "")).strip(),
        use_gmail_drafts=bool(raw.get("use_gmail_drafts", False)),
        gmail_credentials_path=str(raw.get("gmail_credentials_path", "credentials.json")).strip(),
        gmail_token_path=str(raw.get("gmail_token_path", "token.json")).strip(),
        domains=raw.get("domains", {})
    )


def read_companies_csv(path: str) -> List[CompanyInput]:
    companies: List[CompanyInput] = []
    with open(path, "r", encoding="utf-8") as handle:
        reader = csv.DictReader(handle)
        for row in reader:
            name = (row.get("company") or row.get("name") or "").strip()
            domain = normalize_domain(row.get("domain") or "")
            if not domain:
                continue
            companies.append(CompanyInput(name=name or domain, domain=domain))
    return companies


def require_env(name: str) -> str:
    value = os.getenv(name)
    if not value:
        raise RuntimeError(f"Missing required environment variable: {name}")
    return value.strip()


def normalize_role(role: str) -> str:
    return role.lower().strip()


def contains_role(target: Iterable[str], role: str) -> bool:
    normalized = normalize_role(role)
    for item in target:
        if item and normalize_role(item) in normalized:
            return True
    return False


def clean_multiline(text: str) -> str:
    return "\n".join([line.rstrip() for line in text.strip().splitlines() if line.strip()])


def to_safe_filename(value: str) -> str:
    cleaned = "".join(ch if ch.isalnum() or ch in "-_." else "_" for ch in value)
    return cleaned.lower()


def normalize_domain(domain: str) -> str:
    return "".join(domain.split()).lower().strip()


def log_action(message: str) -> None:
    print(f"[pm-outreach-agent] {message}")
