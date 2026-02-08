from dataclasses import dataclass
from typing import Optional


@dataclass
class Lead:
    first_name: str
    last_name: str
    role: str
    email: str
    confidence: int
    company: str

    @property
    def full_name(self) -> str:
        full = f"{self.first_name} {self.last_name}".strip()
        return full if full.strip() else "Unknown"


@dataclass
class CompanyInput:
    name: str
    domain: str


@dataclass
class EmailDraft:
    subject: str
    body: str


@dataclass
class RankedLead:
    lead: Lead
    score: int
    rank_reason: Optional[str] = None
