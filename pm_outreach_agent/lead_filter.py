from typing import List

from .models import Lead, RankedLead
from .utils import contains_role, normalize_role


SENIORITY_ORDER = [
    "founder",
    "co-founder",
    "chief product officer",
    "head of product",
    "group product manager",
    "senior product manager",
    "product manager",
]


def role_priority(role: str) -> int:
    normalized = normalize_role(role)
    for idx, key in enumerate(SENIORITY_ORDER):
        if key in normalized:
            return len(SENIORITY_ORDER) - idx
    return 0


def filter_leads(leads: List[Lead], target_roles: List[str], excluded_roles: List[str], min_confidence: int) -> List[Lead]:
    filtered: List[Lead] = []
    for lead in leads:
        if lead.confidence < min_confidence:
            continue
        if excluded_roles and contains_role(excluded_roles, lead.role):
            continue
        if target_roles and not contains_role(target_roles, lead.role):
            continue
        filtered.append(lead)
    return filtered


def rank_leads(leads: List[Lead]) -> List[RankedLead]:
    ranked: List[RankedLead] = []
    for lead in leads:
        seniority_score = role_priority(lead.role)
        score = seniority_score * 100 + lead.confidence
        ranked.append(RankedLead(lead=lead, score=score))
    ranked.sort(key=lambda item: item.score, reverse=True)
    return ranked
