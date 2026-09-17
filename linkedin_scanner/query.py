"""Turn a search brief into boolean strings and ready-to-open search URLs."""

from __future__ import annotations

from dataclasses import dataclass, field
from urllib.parse import quote_plus

from . import taxonomy


@dataclass
class Brief:
    """The four classifications, plus an optional explicit role title."""

    industry: str
    role: str = ""
    company: str = ""
    school: str = ""
    city: str = ""

    def __post_init__(self) -> None:
        if not self.industry.strip():
            raise ValueError("industry is required")


@dataclass
class SearchPlan:
    """Everything needed to actually run the search, in priority order."""

    boolean: str
    linkedin_people_url: str
    xray_google: str
    xray_bing: str
    company_people_url: str | None = None
    school_alumni_url: str | None = None
    notes: list[str] = field(default_factory=list)


def _or_group(terms: list[str]) -> str:
    """Quote each term and OR them together: ("a" OR "b")."""
    unique: list[str] = []
    for term in terms:
        cleaned = term.strip()
        if cleaned and cleaned not in unique:
            unique.append(cleaned)
    if not unique:
        return ""
    if len(unique) == 1:
        return f'"{unique[0]}"'
    return "(" + " OR ".join(f'"{t}"' for t in unique) + ")"


# Google stops honoring a query somewhere around 32 words and truncates the
# tail silently, so the X-ray form keeps only the strongest few terms per group.
XRAY_TERMS_PER_GROUP = 3


def _clauses(brief: Brief, terms_per_group: int | None = None) -> list[str]:
    """AND-joined clauses, most selective first so truncation degrades well."""

    def group(terms: list[str]) -> str:
        return _or_group(terms[:terms_per_group] if terms_per_group else terms)

    clauses = []
    if brief.role:
        clauses.append(group(taxonomy.seniority_terms(brief.role)))
    clauses.append(group(taxonomy.industry_terms(brief.industry)))
    if brief.company:
        aliases = taxonomy.company_profile(brief.company)["aliases"]
        clauses.append(group(list(aliases)))
    if brief.school:
        aliases = taxonomy.school_profile(brief.school)["aliases"]
        clauses.append(group(list(aliases)))
    if brief.city:
        clauses.append(group(taxonomy.city_terms(brief.city)))
    return [c for c in clauses if c]


def build(brief: Brief) -> SearchPlan:
    """Build the full search plan for a brief."""
    clauses = _clauses(brief)
    boolean = " AND ".join(clauses)

    # LinkedIn's own search bar takes the boolean directly. Location and current
    # company are better applied as native facets once the results load, so the
    # keyword string stays broad enough to leave those filters something to cut.
    people_url = (
        "https://www.linkedin.com/search/results/people/?keywords="
        + quote_plus(boolean)
    )

    # X-ray searches read public profiles only, so they skip LinkedIn's
    # commercial-use limit entirely and see people outside your network.
    xray_body = " ".join(_clauses(brief, terms_per_group=XRAY_TERMS_PER_GROUP))
    xray_google = f"site:linkedin.com/in {xray_body}"
    xray_bing = f'site:linkedin.com/in {xray_body}'

    notes: list[str] = []
    company_url = None
    school_url = None

    if brief.company:
        profile = taxonomy.company_profile(brief.company)
        slug = profile["slug"]
        if slug:
            company_url = f"https://www.linkedin.com/company/{slug}/people/"
            notes.append(
                "Company people tab is the highest-yield path: it filters by "
                "school and location natively, on employees LinkedIn has "
                "already confirmed work there."
            )
        else:
            notes.append(
                f"No known LinkedIn slug for {brief.company!r} — find the firm "
                "page by name, then open its People tab."
            )

    if brief.school:
        profile = taxonomy.school_profile(brief.school)
        slug = profile["slug"]
        if slug:
            school_url = f"https://www.linkedin.com/school/{slug}/people/"
            notes.append(
                "The school Alumni tab filters by employer, city, and field of "
                "study at once, and surfaces shared-connection paths."
            )
        else:
            notes.append(
                f"No known LinkedIn slug for {brief.school!r} — search the "
                "school by name, then open its Alumni tab."
            )

    if not brief.city:
        notes.append("No city set — results will span all geographies.")

    notes.append(
        f"X-ray keeps the top {XRAY_TERMS_PER_GROUP} terms per group; Google "
        "truncates past roughly 32 words. Widen by re-running a dropped term "
        "as its own search rather than lengthening this one."
    )
    notes.append(
        "Verify any /company/ or /school/ slug resolves; LinkedIn renames "
        "these, and a stale slug 404s rather than erroring loudly."
    )

    return SearchPlan(
        boolean=boolean,
        linkedin_people_url=people_url,
        xray_google=xray_google,
        xray_bing=xray_bing,
        company_people_url=company_url,
        school_alumni_url=school_url,
        notes=notes,
    )
