from typing import List, Optional

from .models import Lead, EmailDraft
from .utils import clean_multiline
from .openai_client import OpenAIDraftClient


def build_subject(lead: Lead, custom_subject: Optional[str] = None) -> str:
    if custom_subject:
        return custom_subject
    return f"BITS Goa PM exploring opportunities at {lead.company}"


def build_body(lead: Lead, portfolio_url: str, background_summary: str, tone: str, resume_url: Optional[str] = None) -> str:
    greeting_name = lead.first_name or "there"
    sender_name = background_summary.split(',')[0].strip() if background_summary else 'Anubhav'
    
    links = f"Portfolio: {portfolio_url}"
    if resume_url:
        links += f"\nResume: {resume_url}"
    
    body = f"""Hi {greeting_name},

I'm {sender_name}, a BITS Goa graduate currently working as a Product Manager building AI-powered product analytics and decision-support tools.

I've been following {lead.company}'s work and am genuinely impressed by your approach to product development and scaling. I'm actively exploring PM opportunities where I can contribute to meaningful product decisions and technical depth.

Would you be open to sharing insights about PM roles at {lead.company} or your approach to product leadership? I'd greatly value your perspective.

{links}

Best regards,
{sender_name}"""
    return clean_multiline(body)


def generate_email(lead: Lead, portfolio_url: str, background_summary: str, tone: str, 
                   custom_subject: Optional[str] = None, resume_url: Optional[str] = None) -> EmailDraft:
    subject = build_subject(lead, custom_subject)
    body = build_body(lead, portfolio_url, background_summary, tone, resume_url)
    return EmailDraft(subject=subject, body=body)


def generate_emails(
    leads: List[Lead],
    portfolio_url: str,
    background_summary: str,
    tone: str,
    openai_client: Optional[OpenAIDraftClient] = None,
    custom_subject: Optional[str] = None,
    resume_url: Optional[str] = None,
) -> List[EmailDraft]:
    drafts: List[EmailDraft] = []
    for lead in leads:
        if openai_client:
            try:
                drafts.append(openai_client.generate_email(lead, portfolio_url, background_summary, tone, 
                                                          custom_subject=custom_subject, resume_url=resume_url))
                continue
            except Exception:
                pass
        drafts.append(generate_email(lead, portfolio_url, background_summary, tone, custom_subject, resume_url))
    return drafts
