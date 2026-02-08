import csv
from typing import List

from .models import Lead, EmailDraft, RankedLead
from .utils import clean_multiline


def write_markdown(path: str, ranked_leads: List[RankedLead], drafts: List[EmailDraft]) -> None:
    lines = ["# Send Sheet", ""]
    for idx, (ranked, draft) in enumerate(zip(ranked_leads, drafts), start=1):
        lead = ranked.lead
        lines.extend(
            [
                f"## Email {idx}: {lead.full_name} — {lead.company}",
                "",
                f"**Role:** {lead.role}",
                f"**Email:** {lead.email}",
                f"**Confidence:** {lead.confidence}",
                "",
                f"**Subject:** {draft.subject}",
                "",
                clean_multiline(draft.body),
                "",
                "---",
                "",
            ]
        )
    with open(path, "w", encoding="utf-8") as handle:
        handle.write("\n".join(lines).strip() + "\n")


def write_csv(path: str, ranked_leads: List[RankedLead], drafts: List[EmailDraft]) -> None:
    headers = ["Company", "Name", "Role", "Email", "Confidence", "Subject", "Email Body"]
    with open(path, "w", encoding="utf-8", newline="") as handle:
        writer = csv.writer(handle)
        writer.writerow(headers)
        for ranked, draft in zip(ranked_leads, drafts):
            lead = ranked.lead
            writer.writerow(
                [
                    lead.company,
                    lead.full_name,
                    lead.role,
                    lead.email,
                    lead.confidence,
                    draft.subject,
                    clean_multiline(draft.body),
                ]
            )


def format_summary(total: int, filtered: int, ranked: List[RankedLead], limit: int = 10) -> str:
    lines = [
        f"Total leads found: {total}",
        f"Leads after filtering: {filtered}",
        "Top prioritized contacts:",
    ]
    for ranked_lead in ranked[:limit]:
        lead = ranked_lead.lead
        lines.append(f"- {lead.full_name} | {lead.role} | {lead.email} | {lead.confidence}")
    return "\n".join(lines)
