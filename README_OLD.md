# pm-outreach-agent

Local automation agent for PM outbound outreach. It discovers PM leaders, fetches verified work emails via Hunter.io, generates personalized email drafts, and produces clean send sheets for Gmail. It **never sends emails** and always keeps a human-in-the-loop.

## Features
- Domain-based lead discovery using Hunter.io Domain Search and Email Finder APIs
- Role-based filtering and confidence scoring
- Prioritized lead ranking (Founder → CPO/Head of Product → GPM → SPM → PM)
- Drafts calm, professional, curiosity-driven outreach emails
- Outputs Markdown and CSV send sheets (no daily cap)
- Transparent logs and safety constraints

## Setup
1. Create and activate a Python virtual environment.
2. Install dependencies:
	 - requests
	 - pyyaml
	- openai (optional for LLM drafts)
3. Export your Hunter.io API key:
	 - `export HUNTER_API_KEY="your_key"`
4. (Optional) Export your OpenAI API key for LLM drafts:
	- `export OPENAI_API_KEY="your_key"`
5. (Optional) Gmail drafts setup:
	- Enable Gmail API in Google Cloud.
	- Create OAuth client credentials (Desktop).
	- Download credentials JSON to `credentials.json` in the project root.

## Configuration
Edit [config.yaml](config.yaml) to customize role filters, confidence threshold, portfolio URL, background summary, and tone.

## Usage
Single company:

python run_agent.py \
	--company "BrowserStack" \
	--domain "browserstack.com" \
	--config config.yaml

To write local .eml drafts (no sending):

python run_agent.py \
	--company "BrowserStack" \
	--domain "browserstack.com" \
	--config config.yaml \
	--write-drafts

To create Gmail drafts (no sending):

python run_agent.py \
	--company "BrowserStack" \
	--domain "browserstack.com" \
	--config config.yaml \
	--gmail-drafts

Multiple companies (CSV):

python run_agent.py \
	--companies companies.csv \
	--config config.yaml

## Outputs
- [send_sheet.md](send_sheet.md): Ready-to-copy emails for Gmail
- [send_sheet.csv](send_sheet.csv): Structured send sheet for bulk Gmail import
- drafts/ (optional): Local .eml drafts (not sent)
- Gmail drafts (optional): Created via Gmail API, never sent

Terminal summary includes:
- Total leads found
- Leads after filtering
- Top 10 prioritized contacts

## Safety & Compliance
- No LinkedIn scraping
- No automated sending
- Respects Hunter.io rate limits
- Human review required for every email

## Example Files
- [config.yaml](config.yaml)
- [companies.csv](companies.csv)