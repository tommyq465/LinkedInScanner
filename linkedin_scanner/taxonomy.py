"""Domain vocabulary for translating loose inputs into search terms.

The value of a people search lives almost entirely in synonym coverage: someone
doing restructuring work may never use the word "restructuring" in their
headline, but will say "turnaround", "distressed", or "Chapter 11".
"""

from __future__ import annotations

# Industry -> terms that actually appear in profiles doing that work.
INDUSTRIES: dict[str, list[str]] = {
    "restructuring": [
        "restructuring", "turnaround", "distressed", "special situations",
        "workout", "insolvency", "Chapter 11", "chief restructuring officer",
        "corporate renewal", "liability management",
    ],
    "big four strategy": [
        "Monitor Deloitte", "Strategy&", "EY-Parthenon", "KPMG Strategy",
        "Deloitte Consulting", "PwC Advisory", "Deal Advisory", "strategy",
        "management consulting",
    ],
    "consulting": [
        "consulting", "consultant", "strategy", "advisory",
        "management consulting", "transformation",
    ],
    "finance": [
        "finance", "investment banking", "capital markets", "corporate finance",
        "private equity", "credit", "asset management",
    ],
    "investment banking": [
        "investment banking", "M&A", "mergers and acquisitions", "coverage",
        "leveraged finance", "sponsors", "ECM", "DCM",
    ],
    "private equity": [
        "private equity", "buyout", "growth equity", "LBO", "sponsor",
        "portfolio operations",
    ],
    "transaction services": [
        "transaction services", "transaction advisory", "due diligence",
        "financial due diligence", "quality of earnings", "M&A advisory",
    ],
    "valuation": [
        "valuation", "fair value", "409A", "purchase price allocation",
        "financial modeling",
    ],
    "accounting": [
        "audit", "assurance", "tax", "CPA", "accounting", "controller",
    ],
    "legal": [
        "attorney", "counsel", "associate", "partner", "litigation",
        "bankruptcy", "corporate law",
    ],
    "technology": [
        "software engineer", "engineering", "product manager", "platform",
        "infrastructure", "data engineering",
    ],
    "healthcare": [
        "healthcare", "provider", "payer", "life sciences", "clinical",
        "health system",
    ],
    "real estate": [
        "real estate", "CRE", "acquisitions", "asset management",
        "development", "REIT",
    ],
}

# Seniority -> title variants, including abbreviations people actually type.
SENIORITY: dict[str, list[str]] = {
    "analyst": ["Analyst", "Business Analyst"],
    "associate": ["Associate", "Senior Associate"],
    "consultant": ["Consultant", "Senior Consultant"],
    "manager": ["Manager", "Engagement Manager"],
    "senior manager": ["Senior Manager", "Sr. Manager"],
    "director": ["Director", "Senior Director"],
    "vice president": ["Vice President", "VP", "SVP", "EVP"],
    "principal": ["Principal"],
    "big four junior": [
        "Consultant", "Senior Consultant", "Associate", "Senior Associate",
        "Analyst", "Business Analyst",
    ],
    "managing director": ["Managing Director", "MD"],
    "partner": ["Partner", "Managing Partner"],
    "founder": ["Founder", "Co-Founder", "Managing Member"],
    "c-suite": ["Chief Executive Officer", "CEO", "CFO", "COO", "CRO"],
}

# School -> the name strings LinkedIn education entries actually carry,
# including the business/professional school people often list instead.
SCHOOLS: dict[str, dict[str, object]] = {
    "notre dame": {
        "slug": "university-of-notre-dame",
        "aliases": ["University of Notre Dame", "Notre Dame", "Mendoza College of Business"],
    },
    "pitt": {
        "slug": "university-of-pittsburgh",
        "aliases": ["University of Pittsburgh", "Pitt", "Katz Graduate School of Business"],
    },
    "penn state": {
        "slug": "penn-state-university",
        "aliases": ["Penn State", "Pennsylvania State University", "Smeal College of Business"],
    },
    "michigan": {
        "slug": "university-of-michigan",
        "aliases": ["University of Michigan", "Ross School of Business"],
    },
    "wharton": {
        "slug": "university-of-pennsylvania",
        "aliases": ["Wharton", "University of Pennsylvania", "The Wharton School"],
    },
    "villanova": {
        "slug": "villanova-university",
        "aliases": ["Villanova University", "Villanova"],
    },
    "georgetown": {
        "slug": "georgetown-university",
        "aliases": ["Georgetown University", "McDonough School of Business"],
    },
    "ohio state": {
        "slug": "the-ohio-state-university",
        "aliases": ["The Ohio State University", "Ohio State", "Fisher College of Business"],
    },
    "indiana": {
        "slug": "indiana-university-bloomington",
        "aliases": ["Indiana University", "Kelley School of Business"],
    },
    "boston college": {
        "slug": "boston-college",
        "aliases": ["Boston College", "Carroll School of Management"],
    },
}

# Firm -> name variants plus the LinkedIn company slug where it is well known.
# Entities split across many legal names (Big Four especially) need the variants
# or the search misses whole practice groups.
COMPANIES: dict[str, dict[str, object]] = {
    "deloitte": {
        "slug": "deloitte",
        "aliases": ["Deloitte", "Deloitte & Touche", "Deloitte Consulting",
                    "Deloitte Corporate Finance", "Deloitte Transactions and Business Analytics"],
    },
    "pwc": {"slug": "pwc",
            "aliases": ["PwC", "PricewaterhouseCoopers", "Strategy&"]},
    "ey": {"slug": "ernstandyoung",
           "aliases": ["EY", "Ernst & Young", "EY-Parthenon",
                       "Strategy and Transactions"]},
    "kpmg": {"slug": "kpmg", "aliases": ["KPMG", "KPMG US", "KPMG Strategy",
                                        "Deal Advisory"]},
    "monitor deloitte": {"slug": "deloitte",
                         "aliases": ["Monitor Deloitte", "Deloitte Strategy"]},
    "strategy&": {"slug": "strategyand",
                  "aliases": ["Strategy&", "Strategy& part of the PwC network"]},
    "ey-parthenon": {"slug": "ernstandyoung",
                     "aliases": ["EY-Parthenon", "EY Parthenon", "Parthenon"]},
    "alvarez & marsal": {"slug": "alvarez-&-marsal", "aliases": ["Alvarez & Marsal", "A&M"]},
    "alixpartners": {"slug": "alixpartners", "aliases": ["AlixPartners", "Alix Partners"]},
    "fti consulting": {"slug": "fticonsulting", "aliases": ["FTI Consulting", "FTI"]},
    "huron": {"slug": "huron-consulting-group", "aliases": ["Huron", "Huron Consulting Group"]},
    "houlihan lokey": {"slug": "houlihan-lokey", "aliases": ["Houlihan Lokey", "HL"]},
    "mckinsey": {"slug": "mckinsey", "aliases": ["McKinsey & Company", "McKinsey"]},
    "bain": {"slug": "bain-and-company", "aliases": ["Bain & Company", "Bain"]},
    "bcg": {"slug": "boston-consulting-group", "aliases": ["Boston Consulting Group", "BCG"]},
    "accenture": {"slug": "accenture", "aliases": ["Accenture"]},
    "grant thornton": {"slug": "grant-thornton-llp", "aliases": ["Grant Thornton"]},
    "rsm": {"slug": "rsm-us-llp", "aliases": ["RSM", "RSM US LLP"]},
    "bdo": {"slug": "bdo-usa", "aliases": ["BDO", "BDO USA"]},
}

# Metro -> the location strings that show up on profiles for that market.
CITIES: dict[str, list[str]] = {
    "chicago": ["Chicago", "Greater Chicago Area", "Chicago, Illinois"],
    "new york": ["New York", "New York City", "NYC", "Greater New York City Area"],
    "pittsburgh": ["Pittsburgh", "Greater Pittsburgh Region", "Pittsburgh, Pennsylvania"],
    "philadelphia": ["Philadelphia", "Greater Philadelphia", "Philadelphia, Pennsylvania"],
    "boston": ["Boston", "Greater Boston", "Boston, Massachusetts"],
    "dallas": ["Dallas", "Dallas-Fort Worth Metroplex", "Dallas, Texas"],
    "houston": ["Houston", "Greater Houston", "Houston, Texas"],
    "atlanta": ["Atlanta", "Greater Atlanta Area", "Atlanta, Georgia"],
    "los angeles": ["Los Angeles", "Greater Los Angeles Area", "Los Angeles, California"],
    "san francisco": ["San Francisco", "San Francisco Bay Area", "SF Bay Area"],
    "washington dc": ["Washington DC", "Washington D.C.", "Washington DC-Baltimore Area"],
    "detroit": ["Detroit", "Detroit Metropolitan Area", "Detroit, Michigan"],
    "miami": ["Miami", "Miami-Fort Lauderdale Area", "Miami, Florida"],
    "denver": ["Denver", "Denver Metropolitan Area", "Denver, Colorado"],
    "charlotte": ["Charlotte", "Charlotte, North Carolina", "Charlotte Metro"],
}


def _normalize(value: str) -> str:
    return " ".join(value.strip().lower().replace("&", "&").split())


def industry_terms(industry: str) -> list[str]:
    """Terms for an industry, falling back to the raw input when unmapped."""
    key = _normalize(industry)
    if key in INDUSTRIES:
        return INDUSTRIES[key]
    for name, terms in INDUSTRIES.items():
        if key in name or name in key:
            return terms
    return [industry.strip()]


def seniority_terms(role: str) -> list[str]:
    """Title variants for a seniority level, falling back to the raw input."""
    key = _normalize(role)
    if key in SENIORITY:
        return SENIORITY[key]
    for name, terms in SENIORITY.items():
        if key == name or key in name:
            return terms
    return [role.strip()]


def school_profile(school: str) -> dict[str, object]:
    """Aliases and LinkedIn slug for a school; slug is None when unknown."""
    key = _normalize(school)
    if key in SCHOOLS:
        return dict(SCHOOLS[key])
    for name, profile in SCHOOLS.items():
        if key in name or name in key:
            return dict(profile)
    return {"slug": None, "aliases": [school.strip()]}


def company_profile(company: str) -> dict[str, object]:
    """Aliases and LinkedIn slug for a firm; slug is None when unknown."""
    key = _normalize(company)
    if key in COMPANIES:
        return dict(COMPANIES[key])
    for name, profile in COMPANIES.items():
        if key in name or name in key:
            return dict(profile)
    return {"slug": None, "aliases": [company.strip()]}


def city_terms(city: str) -> list[str]:
    """Location strings for a metro, falling back to the raw input."""
    key = _normalize(city)
    if key in CITIES:
        return CITIES[key]
    for name, terms in CITIES.items():
        if key in name or name in key:
            return terms
    return [city.strip()]
