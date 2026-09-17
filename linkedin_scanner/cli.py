"""Command line entry point for the scanner."""

from __future__ import annotations

import argparse
import json
import sys
from dataclasses import asdict

from .query import Brief, build


def _parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        prog="scan",
        description="Build LinkedIn people-search queries from a brief.",
        epilog=(
            'example: scan.py --industry restructuring --role "managing director" '
            '--company Deloitte --school "Notre Dame" --city Chicago'
        ),
    )
    parser.add_argument("--industry", required=True,
                        help="field of work, e.g. restructuring, consulting, finance")
    parser.add_argument("--role", default="",
                        help="seniority or title, e.g. 'managing director', analyst")
    parser.add_argument("--company", default="",
                        help="specific firm; omit to search any employer")
    parser.add_argument("--school", default="",
                        help="required alma mater, e.g. 'Notre Dame'")
    parser.add_argument("--city", default="",
                        help="metro area; omit to search all geographies")
    parser.add_argument("--json", action="store_true",
                        help="emit the plan as JSON instead of formatted text")
    return parser


def _render(plan, brief: Brief) -> str:
    lines = [
        "BRIEF",
        f"  industry : {brief.industry}",
        f"  role     : {brief.role or '(any)'}",
        f"  company  : {brief.company or '(any)'}",
        f"  school   : {brief.school or '(any)'}",
        f"  city     : {brief.city or '(any)'}",
        "",
        "BOOLEAN",
        f"  {plan.boolean}",
        "",
        "SEARCH THESE IN ORDER",
    ]
    step = 1
    if plan.company_people_url:
        lines.append(f"  {step}. company people tab  {plan.company_people_url}")
        step += 1
    if plan.school_alumni_url:
        lines.append(f"  {step}. school alumni tab   {plan.school_alumni_url}")
        step += 1
    lines.append(f"  {step}. linkedin people     {plan.linkedin_people_url}")
    step += 1
    lines.append(f"  {step}. google x-ray        {plan.xray_google}")
    lines += ["", "NOTES"]
    lines += [f"  - {note}" for note in plan.notes]
    return "\n".join(lines)


def main(argv: list[str] | None = None) -> int:
    args = _parser().parse_args(argv)
    try:
        brief = Brief(
            industry=args.industry,
            role=args.role,
            company=args.company,
            school=args.school,
            city=args.city,
        )
    except ValueError as exc:
        print(f"error: {exc}", file=sys.stderr)
        return 2

    plan = build(brief)
    if args.json:
        print(json.dumps({"brief": asdict(brief), "plan": asdict(plan)}, indent=2))
    else:
        print(_render(plan, brief))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
