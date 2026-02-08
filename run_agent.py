import argparse
from typing import List
from dotenv import load_dotenv

from pm_outreach_agent.hunter_client import HunterClient
from pm_outreach_agent.lead_filter import filter_leads, rank_leads
from pm_outreach_agent.email_generator import generate_emails
from pm_outreach_agent.output_writer import write_markdown, write_csv, format_summary
from pm_outreach_agent.models import CompanyInput, Lead
from pm_outreach_agent.utils import load_config, read_companies_csv, require_env, log_action, normalize_domain
from pm_outreach_agent.openai_client import OpenAIDraftClient, OpenAIDraftConfig
from pm_outreach_agent.draft_writer import write_eml_drafts
from pm_outreach_agent.gmail_client import create_gmail_drafts


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="pm-outreach-agent: lead discovery and email drafting")
    parser.add_argument("--company", type=str, help="Company name")
    parser.add_argument("--domain", type=str, help="Company domain")
    parser.add_argument("--companies", type=str, help="CSV file with company and domain columns")
    parser.add_argument("--config", type=str, required=True, help="Path to config.yaml")
    parser.add_argument("--write-drafts", action="store_true", help="Write local .eml drafts (no sending)")
    parser.add_argument("--gmail-drafts", action="store_true", help="Create Gmail drafts (no sending)")
    return parser.parse_args()


def resolve_companies(args: argparse.Namespace) -> List[CompanyInput]:
    companies: List[CompanyInput] = []
    if args.companies:
        companies.extend(read_companies_csv(args.companies))
    if args.domain:
        domain = normalize_domain(args.domain)
        name = args.company or domain
        companies.append(CompanyInput(name=name, domain=domain))
    if not companies:
        raise RuntimeError("No companies provided. Use --domain or --companies.")
    return companies


def dedupe_leads(leads: List[Lead]) -> List[Lead]:
    seen = set()
    unique: List[Lead] = []
    for lead in leads:
        key = lead.email.lower().strip()
        if not key or key in seen:
            continue
        seen.add(key)
        unique.append(lead)
    return unique


def main() -> None:
    load_dotenv()
    args = parse_args()
    config = load_config(args.config)
    api_key = require_env("HUNTER_API_KEY")
    companies = resolve_companies(args)

    client = HunterClient(api_key=api_key)
    openai_client = None
    if config.use_openai_drafts:
        openai_key = require_env("OPENAI_API_KEY")
        openai_client = OpenAIDraftClient(openai_key, OpenAIDraftConfig(model=config.openai_model))

    all_leads: List[Lead] = []
    for company in companies:
        log_action(f"Searching domain {company.domain}")
        try:
            leads = client.domain_search(company.domain)
        except Exception as exc:
            log_action(f"Hunter API error for {company.domain}: {exc}")
            continue
        for lead in leads:
            if not lead.company:
                lead.company = company.name
        all_leads.extend(leads)

    total_leads = len(all_leads)
    all_leads = dedupe_leads(all_leads)
    filtered = filter_leads(all_leads, config.target_roles, config.excluded_roles, config.min_email_confidence)
    ranked = rank_leads(filtered)

    ordered_leads = [item.lead for item in ranked]
    drafts = generate_emails(
        ordered_leads,
        config.portfolio_url,
        config.candidate_background_summary,
        config.tone,
        openai_client=openai_client,
    )

    write_markdown("send_sheet.md", ranked, drafts)
    write_csv("send_sheet.csv", ranked, drafts)
    if args.write_drafts:
        sender_email = config.sender_email or "you@example.com"
        write_eml_drafts("drafts", ranked, drafts, sender_email)
    if args.gmail_drafts or config.use_gmail_drafts:
        sender_email = config.sender_email
        if not sender_email:
            raise RuntimeError("sender_email is required for Gmail drafts.")
        create_gmail_drafts(
            ranked,
            drafts,
            sender_email,
            config.gmail_credentials_path,
            config.gmail_token_path,
        )

    summary = format_summary(total_leads, len(filtered), ranked)
    log_action("Run complete. Summary:")
    print(summary)
    log_action("Files created: send_sheet.md, send_sheet.csv")
    if args.write_drafts:
        log_action("Drafts created in drafts/ (not sent).")
    if args.gmail_drafts or config.use_gmail_drafts:
        log_action("Gmail drafts created (not sent).")
    log_action("Reminder: human-in-the-loop review required before sending emails.")


if __name__ == "__main__":
    main()
