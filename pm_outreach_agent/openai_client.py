from dataclasses import dataclass

from .models import Lead, EmailDraft
from .utils import clean_multiline


@dataclass
class OpenAIDraftConfig:
    model: str


class OpenAIDraftClient:
    def __init__(self, api_key: str, config: OpenAIDraftConfig) -> None:
        from openai import OpenAI

        self._client = OpenAI(api_key=api_key)
        self._config = config

    def generate_email(self, lead: Lead, portfolio_url: str, background_summary: str, tone: str,
                      custom_subject: str = None, resume_url: str = None) -> EmailDraft:
        sender_name = background_summary.split(',')[0].strip() if background_summary else 'Anubhav'
        greeting_name = lead.first_name or "there"
        
        # Generate custom subject if not provided
        if not custom_subject:
            custom_subject = self._generate_subject(lead, sender_name)
        
        links = f"Portfolio: {portfolio_url}"
        if resume_url:
            links += f"\\nResume: {resume_url}"
        
        system_prompt = (
            "You are writing a professional cold email for a PM job seeker reaching out to a product leader. "
            "The email should be concise (under 120 words), genuine, and professional. "
            "Focus: Expressing interest in PM opportunities at their company. "
            "Do NOT mention: salary, resumes, urgency, or desperation. "
            "Return plain text only - no JSON, no markdown formatting, no brackets."
        )
        
        user_prompt = (
            f"Write a professional job-seeking email to {greeting_name}, {lead.role} at {lead.company}.\\n\\n"
            f"About sender:\\n"
            f"- Name: {sender_name}\\n"
            f"- Background: BITS Goa graduate, currently working as PM\\n"
            f"- Experience: Building AI-powered product analytics and decision-support tools\\n"
            f"- Goal: Exploring PM opportunities at {lead.company}\\n\\n"
            f"Email structure:\\n"
            f"1. Brief intro (who you are, what you do)\\n"
            f"2. Why {lead.company} (admiration for their work)\\n"
            f"3. Ask: Insights on PM roles or product leadership\\n"
            f"4. Close with links below\\n\\n"
            f"Links to include at end:\\n{links}\\n\\n"
            f"Tone: {tone}, confident but humble, job-seeking but not desperate.\\n"
            f"IMPORTANT: Return ONLY the email body text. Do NOT include 'Subject:' line. No markdown formatting."
        )
        
        try:
            response = self._client.chat.completions.create(
                model=self._config.model,
                messages=[
                    {"role": "system", "content": system_prompt},
                    {"role": "user", "content": user_prompt},
                ],
                temperature=0.6,
                max_tokens=350,
            )
            body = response.choices[0].message.content.strip()
            # Remove any markdown formatting and subject line if included
            body = body.replace('[', '').replace(']', '').replace('(', ' ').replace(')', '')
            # Remove "Subject:" line if OpenAI added it
            if body.startswith('Subject:'):
                body = '\n'.join(body.split('\n')[1:]).strip()
            # Remove any remaining "Subject: ..." patterns
            import re
            body = re.sub(r'^Subject:.*?\n', '', body, flags=re.IGNORECASE | re.MULTILINE)
            return EmailDraft(subject=custom_subject, body=clean_multiline(body))
        except Exception:
            # Fallback to template if OpenAI fails
            from .email_generator import build_subject, build_body
            subject = build_subject(lead, custom_subject)
            body = build_body(lead, portfolio_url, background_summary, tone, resume_url)
            return EmailDraft(subject=subject, body=body)
    
    def _generate_subject(self, lead: Lead, sender_name: str) -> str:
        """Generate a personalized email subject using OpenAI"""
        try:
            response = self._client.chat.completions.create(
                model=self._config.model,
                messages=[
                    {"role": "system", "content": "You write concise, professional email subject lines for job seekers. Keep it under 60 characters, professional, and intriguing."},
                    {"role": "user", "content": f"Write a subject line for a PM job seeker ({sender_name}) reaching out to {lead.role} at {lead.company}. Make it professional and genuine."}
                ],
                temperature=0.7,
                max_tokens=20,
            )
            subject = response.choices[0].message.content.strip()
            # Remove quotes if OpenAI adds them
            subject = subject.replace('"', '').replace("'", '')
            return subject
        except Exception:
            return f"PM opportunity inquiry - {sender_name}"
