"""Create a non-destructive evidence packet for US frontier research."""

from __future__ import annotations

import argparse
from pathlib import Path


FILES = {
    "README.md": "# {project}: US Frontier Evidence Packet\n\nDecision: {decision}\n",
    "decision-contract.md": "# Decision Contract\n\n## Job and user\n\n## Metrics and failure criteria\n\n## Data, compute, rights, and budget\n\n## Human-gated actions\n",
    "capability-graph.md": "# Capability Graph\n\n| Need | US lane | Global comparison lane | Why relevant | Status |\n| --- | --- | --- | --- | --- |\n",
    "source-ledger.csv": "source_url,date,owner,source_role,ecosystem,language,claim,evidence_tier,limitations\n",
    "repository-audit.csv": "candidate,upstream_url,commit,license,model_terms,data_terms,tests,security_notes,reproduction_status,decision\n",
    "provider-test-log.csv": "provider,model_version,datetime_region,input_class,parameters,quality,safety,p50_ms,p95_ms,cost,data_boundary,fallback,decision\n",
    "global-comparison.csv": "job,candidate,ecosystem,version_or_commit,quality,calibration,safety,latency,throughput,cost,rights,explainability,operator_load,decision\n",
    "experiment-plan.md": "# Experiment Plan\n\n## Frozen split and metrics\n\n## Baselines and negative control\n\n## Adversarial and outage cases\n\n## Reproduction results\n",
    "commercialization-gate.md": "# Commercialization Reality Gate\n\n## Buyer and painful job\n\n## Measured outcome and paid-pilot test\n\n## Moat, data rights, and route to market\n",
    "decision-log.md": "# Decision Log\n\n## Adopted\n\n## Rejected\n\n## Inconclusive\n\n## Unresolved risks\n",
}


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--project", required=True)
    parser.add_argument("--decision", required=True)
    parser.add_argument("--output", required=True, type=Path)
    return parser.parse_args()


def main() -> None:
    args = parse_args()
    output = args.output.resolve()
    if output.exists():
        raise SystemExit(f"Refusing to overwrite existing output: {output}")
    output.mkdir(parents=True)
    for name, template in FILES.items():
        (output / name).write_text(
            template.format(project=args.project, decision=args.decision),
            encoding="utf-8",
        )
    print(f"Created US frontier packet: {output}")
    print(f"Created {len(FILES)} evidence files.")


if __name__ == "__main__":
    main()
