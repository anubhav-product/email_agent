import os
from typing import List

from .models import RankedLead, EmailDraft


def write_eml_drafts(output_dir: str, ranked_leads: List[RankedLead], drafts: List[EmailDraft], sender_email: str) -> None:
    os.makedirs(output_dir, exist_ok=True)
    for idx, (ranked, draft) in enumerate(zip(ranked_leads, drafts), start=1):
        lead = ranked.lead
        filename = f"draft_{idx:03d}_{lead.email.replace('@', '_')}.eml"
        path = os.path.join(output_dir, filename)
        content = (
            f"From: {sender_email}\n"
            f"To: {lead.email}\n"
            f"Subject: {draft.subject}\n"
            "MIME-Version: 1.0\n"
            "Content-Type: text/plain; charset=utf-8\n"
            "\n"
            f"{draft.body}\n"
        )
        with open(path, "w", encoding="utf-8") as handle:
            handle.write(content)
