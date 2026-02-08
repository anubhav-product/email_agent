# Multi-Domain Examples 🎯

This document shows how the PM Outreach Agent works across different career domains.

---

## Example 1: Product Management Search

**Input:**
- Domain: Product Management
- Company: Stripe
- Domain: stripe.com

**Target Roles Searched:**
- Founder
- Co-founder
- Head of Product
- Chief Product Officer
- VP Product
- Director of Product
- Group Product Manager
- Senior Product Manager
- Product Manager

**Sample Output:**
```
✅ Generated 3 Product Management leads!

1. Arielle Bail - Head of Product (arielle@stripe.com) - Confidence: 94%
2. John Smith - VP Product (john@stripe.com) - Confidence: 88%
3. Sarah Johnson - Senior Product Manager (sarah@stripe.com) - Confidence: 85%
```

---

## Example 2: Consulting Search

**Input:**
- Domain: Consulting
- Company: McKinsey
- Domain: mckinsey.com

**Target Roles Searched:**
- Partner
- Principal
- Director
- Senior Consultant
- Consultant
- Strategy Manager
- Business Analyst

**Sample Email Generated:**

```
Subject: BITS Goa grad exploring consulting opportunities

Hi [Name],

I'm Anubhav, a BITS Goa graduate with product and analytics experience, 
and I'm actively exploring consulting roles where strategic thinking and 
structured problem-solving create impact.

I've been following McKinsey's work in [industry] and would really 
appreciate learning about how you approach client problems and build 
consulting expertise.

Would you be open to a brief conversation?

Best regards,
Anubhav
Portfolio: https://portfolio-o5n7.onrender.com
```

---

## Example 3: Software Engineering Search

**Input:**
- Domain: Software Engineering
- Company: Google
- Domain: google.com

**Target Roles Searched:**
- CTO
- VP Engineering
- Engineering Manager
- Tech Lead
- Senior Software Engineer
- Software Engineer

**Use Case:** Great for PMs with technical backgrounds transitioning to engineering roles.

---

## Example 4: Data Science Search

**Input:**
- Domain: Data Science & Analytics
- Company: Netflix
- Domain: netflix.com

**Target Roles Searched:**
- Head of Data
- Data Science Manager
- Senior Data Scientist
- Data Scientist
- Analytics Manager

**Customization:**
The agent automatically adjusts email tone based on domain:
- **PM emails:** Focus on product thinking and user impact
- **Consulting emails:** Emphasize strategic problem-solving
- **Engineering emails:** Highlight technical skills and systems thinking
- **Data Science emails:** Showcase ML/analytics expertise

---

## Bulk Multi-Domain Strategy

**Scenario:** Send 50 emails across multiple domains in one day

**Approach:**

1. **Morning (10 emails):** Product Management
   - Companies: Stripe, Notion, Linear, Figma, Airbnb
   - Generate 10 PM leads

2. **Afternoon (15 emails):** Consulting
   - Companies: McKinsey, BCG, Bain, Deloitte
   - Generate 15 consultant leads

3. **Evening (10 emails):** Data Science
   - Companies: Netflix, Spotify, Meta
   - Generate 10 data science leads

4. **Review & Send:**
   - Review all Gmail drafts
   - Customize top 30 emails
   - Send in batches (10-15 per day max)

---

## Domain-Specific Email Tips

### Product Management
- ✅ Mention product you've shipped
- ✅ Show understanding of their product
- ✅ Highlight impact metrics

### Consulting
- ✅ Emphasize analytical skills
- ✅ Show structured thinking
- ✅ Reference case study experience

### Engineering
- ✅ Include GitHub/technical projects
- ✅ Mention tech stack expertise
- ✅ Show system design understanding

### Data Science
- ✅ Reference ML/AI projects
- ✅ Show statistical rigor
- ✅ Mention model deployment experience

---

## Configuration Customization

Want to add your own domain? Edit `config.yaml`:

```yaml
domains:
  marketing:  # New domain!
    name: "Marketing & Growth"
    target_roles:
      - CMO
      - Head of Marketing
      - Growth Manager
      - Marketing Manager
    background: "BITS Goa graduate with product and analytics experience in growth"
```

Then select "Marketing & Growth" from the web interface dropdown.

---

**Pro Tip:** Use different domains for different companies based on their hiring patterns. Tech companies → PM/Engineering, Consulting firms → Consulting, Data-heavy companies → Data Science.
