"""Generate the project SVG diagrams without third-party dependencies."""

from __future__ import annotations

import argparse
import html
import math
import textwrap
from dataclasses import dataclass
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]


@dataclass(frozen=True)
class Box:
    key: str
    title: str
    detail: str
    x: int
    y: int
    width: int
    height: int
    fill: str = "#1168bd"
    stroke: str = "#0b4f8a"
    color: str = "#ffffff"
    dashed: bool = False


@dataclass(frozen=True)
class Edge:
    source: str
    target: str
    label: str
    points: tuple[tuple[int, int], ...]
    color: str = "#52616b"
    dashed: bool = False


def esc(value: str) -> str:
    return html.escape(value, quote=True)


def text_lines(value: str, width: int, size: int) -> list[str]:
    max_chars = max(8, int(width / (size * 0.56)))
    lines: list[str] = []
    for paragraph in value.split("\n"):
        lines.extend(textwrap.wrap(paragraph, max_chars) or [""])
    return lines


def svg_text(lines: list[str], x: float, y: float, size: int, color: str,
             anchor: str = "middle", weight: str = "normal") -> str:
    parts = [
        f'<text x="{x}" y="{y}" text-anchor="{anchor}" '
        f'font-family="Arial, Helvetica, sans-serif" font-size="{size}" '
        f'font-weight="{weight}" fill="{color}">'
    ]
    for index, line in enumerate(lines):
        dy = 0 if index == 0 else int(size * 1.25)
        parts.append(f'<tspan x="{x}" dy="{dy}">{esc(line)}</tspan>')
    parts.append("</text>")
    return "".join(parts)


def title_block(title: str, subtitle: str, width: int) -> str:
    return (
        svg_text([title], width / 2, 38, 28, "#17212b", weight="bold")
        + svg_text([subtitle], width / 2, 66, 14, "#52616b")
    )


def render_box(box: Box) -> str:
    dash = ' stroke-dasharray="9 6"' if box.dashed else ""
    shape = (
        f'<rect x="{box.x}" y="{box.y}" width="{box.width}" height="{box.height}" '
        f'rx="16" fill="{box.fill}" stroke="{box.stroke}" stroke-width="2"{dash}/>'
    )
    title = text_lines(box.title, box.width - 24, 14)
    detail = text_lines(box.detail, box.width - 28, 12) if box.detail else []
    total = len(title) * 18 + len(detail) * 15 + (9 if detail else 0)
    start = box.y + (box.height - total) / 2 + 14
    body = svg_text(title, box.x + box.width / 2, start, 14, box.color, weight="bold")
    if detail:
        body += svg_text(
            detail,
            box.x + box.width / 2,
            start + len(title) * 18 + 4,
            12,
            box.color,
        )
    return f'<g filter="url(#shadow)">{shape}{body}</g>'


def render_edge(edge: Edge) -> str:
    points = " ".join(f"{x},{y}" for x, y in edge.points)
    dash = ' stroke-dasharray="8 6"' if edge.dashed else ""
    path = (
        f'<polyline points="{points}" fill="none" stroke="{edge.color}" '
        f'stroke-width="2.5" marker-end="url(#arrow)"{dash}/>'
    )
    if not edge.label:
        return path
    mid = edge.points[len(edge.points) // 2]
    lines = text_lines(edge.label, 220, 11)
    width = min(230, max(80, max(len(line) for line in lines) * 6.3 + 18))
    height = len(lines) * 14 + 12
    label = (
        f'<rect x="{mid[0] - width / 2:.1f}" y="{mid[1] - height / 2:.1f}" '
        f'width="{width}" height="{height}" rx="6" fill="#ffffff" fill-opacity="0.95"/>'
        + svg_text(lines, mid[0], mid[1] - (len(lines) - 1) * 7 + 4, 11, edge.color)
    )
    return path + label


def svg_document(width: int, height: int, body: list[str]) -> str:
    return "\n".join(
        [
            f'<svg xmlns="http://www.w3.org/2000/svg" width="{width}" height="{height}" '
            f'viewBox="0 0 {width} {height}">',
            "<defs>",
            '<marker id="arrow" markerWidth="10" markerHeight="10" refX="9" refY="3" '
            'orient="auto" markerUnits="strokeWidth"><path d="M0,0 L0,6 L9,3 z" fill="#52616b"/></marker>',
            '<filter id="shadow" x="-10%" y="-10%" width="120%" height="125%">'
            '<feDropShadow dx="0" dy="2" stdDeviation="2" flood-opacity="0.16"/></filter>',
            "</defs>",
            f'<rect width="{width}" height="{height}" fill="#f8fafc"/>',
            *body,
            "</svg>",
            "",
        ]
    )


def c4_container() -> str:
    width, height = 2200, 1420
    boxes = (
        Box("business", "Бизнес-пользователь", "конструирует отчёты", 35, 165, 230, 100, "#08427b", "#062f59"),
        Box("analyst", "Доменный аналитик", "публикует data products", 35, 445, 230, 100, "#08427b", "#062f59"),
        Box("owner", "Data Product Owner", "contract, SLO, quality", 35, 725, 230, 100, "#08427b", "#062f59"),
        Box("portal", "Self-Service Data Portal", "catalog, query builder, saved reports", 340, 140, 290, 115),
        Box("gateway", "API Gateway / BFF", "OIDC, quotas, request validation", 720, 140, 285, 115, "#2e7d32", "#1f5b24"),
        Box("iam", "IAM + Policy Engine", "MFA; RBAC + ABAC; purpose", 1100, 120, 290, 115, "#2e7d32", "#1f5b24"),
        Box("catalog", "Catalog + Data Product Registry", "owner, contract, classification, lineage", 1100, 315, 315, 125, "#d88c00", "#9a6200", "#17212b"),
        Box("query", "Query & Semantic Service", "governed SQL, KPI model, result limits", 720, 350, 300, 125),
        Box("engine", "Distributed Query Engine", "independent compute pools and queues", 720, 570, 300, 115, "#5b4b9a", "#443575"),
        Box("lakehouse", "Domain Lakehouse", "object storage + Iceberg; curated products", 1120, 570, 330, 120, "#0b5f91", "#08476c"),
        Box("orchestrator", "Orchestrator + Quality Gates", "batch/stream pipelines, quarantine, retries", 1120, 785, 330, 120),
        Box("events", "Event Streaming + Schema Registry", "domain topics, outbox/CDC, DLQ", 720, 785, 300, 120, "#7b3fa1", "#5c2f78"),
        Box("observability", "Observability + Audit", "data SLO, traces, query/export audit", 1510, 330, 300, 120, "#2e7d32", "#1f5b24"),
        Box("products", "Domain Data Products", "Clinic Ops | Fintech | Corporate | Partners", 1510, 570, 300, 120, "#0b5f91", "#08476c"),
        Box("systems", "Domain Operational Systems", "DB per domain; versioned API and events", 1880, 570, 280, 120, "#5f6b76", "#414a52"),
        Box("legacy", "Legacy SQL Server 2008 + Camel", "read-only bridge during migration; no new logic", 1510, 805, 300, 120, "#8b3a3a", "#662929"),
        Box("clinical", "Clinical & AI PHI Zone", "medical records and studies; operational use only", 1850, 960, 310, 130, "#8b3a3a", "#662929"),
        Box("rule", "Жёсткая граница", "Медкарты, истории болезни и результаты исследований не передаются в Lakehouse и портал.", 1150, 1125, 1010, 115, "#fff4cc", "#b88900", "#17212b"),
    )
    edges = (
        Edge("business", "portal", "OIDC / HTTPS", ((265, 215), (340, 198))),
        Edge("analyst", "catalog", "поиск и публикация", ((265, 495), (550, 495), (550, 378), (1100, 378)), "#d88c00"),
        Edge("owner", "catalog", "contract + SLO", ((265, 775), (600, 775), (600, 415), (1100, 415)), "#d88c00"),
        Edge("portal", "gateway", "REST/JSON", ((630, 198), (720, 198))),
        Edge("gateway", "iam", "authorize each request", ((1005, 198), (1100, 178)), "#2e7d32"),
        Edge("gateway", "query", "logical query", ((862, 255), (862, 350))),
        Edge("query", "catalog", "schema + policy", ((1020, 410), (1100, 390)), "#d88c00"),
        Edge("query", "engine", "approved SQL + quota", ((870, 475), (870, 570))),
        Edge("engine", "lakehouse", "columnar reads", ((1020, 628), (1120, 630))),
        Edge("events", "orchestrator", "validated events", ((1020, 845), (1120, 845)), "#7b3fa1"),
        Edge("orchestrator", "lakehouse", "publish curated table", ((1285, 785), (1285, 690))),
        Edge("products", "lakehouse", "versioned product", ((1510, 630), (1450, 630)), "#0b5f91"),
        Edge("systems", "products", "outbox / CDC", ((1880, 630), (1810, 630)), "#7b3fa1"),
        Edge("systems", "events", "domain events", ((2020, 690), (2020, 880), (1020, 880)), "#7b3fa1"),
        Edge("legacy", "events", "anti-corruption layer", ((1510, 865), (1020, 865)), "#8b3a3a", True),
        Edge("catalog", "observability", "lineage / access metadata", ((1415, 378), (1510, 390)), "#2e7d32", True),
        Edge("query", "observability", "query/export audit", ((1020, 445), (1510, 445)), "#2e7d32", True),
    )
    body = [
        title_block("C4 Container — целевая архитектура «Будущего 2.0»", "Через год: доменные дата-продукты, Lakehouse и портал самообслуживания", width),
        '<rect x="300" y="90" width="1545" height="990" rx="22" fill="none" stroke="#59636e" stroke-width="2" stroke-dasharray="10 7"/>',
        svg_text(["Облачная data platform"], 325, 120, 16, "#334155", "start", "bold"),
    ]
    body.extend(render_edge(edge) for edge in edges)
    body.extend(render_box(box) for box in boxes)
    body.append(svg_text(["Синий — приложение/data; зелёный — security/audit; фиолетовый — events; красный — legacy/PHI isolation."], 35, 1365, 13, "#52616b", "start"))
    return svg_document(width, height, body)


def data_flow() -> str:
    width, height = 2220, 1450
    boxes = (
        Box("clinic", "Clinic Operations", "appointments, capacity, inventory", 40, 150, 260, 105),
        Box("fintech", "Fintech", "accounts, loans, transactions", 40, 340, 260, 105),
        Box("corporate", "Corporate", "HR, finance, procurement", 40, 530, 260, 105),
        Box("partners", "Partners", "pharma and medtech contracts", 40, 720, 260, 105),
        Box("outbox", "Outbox / CDC", "atomic event; replayable log", 405, 340, 270, 115, "#7b3fa1", "#5c2f78"),
        Box("broker", "Event Backbone", "domain topics + Schema Registry + DLQ", 790, 340, 290, 115, "#7b3fa1", "#5c2f78"),
        Box("ingest", "Ingestion + Quality", "schema, PII tags, freshness, quarantine", 1175, 340, 300, 120),
        Box("catalog", "Catalog + Policy", "owner, lineage, purpose, ABAC", 1175, 145, 300, 115, "#d88c00", "#9a6200", "#17212b"),
        Box("lakehouse", "Domain Lakehouse", "raw → validated → curated Iceberg", 1580, 340, 315, 120, "#0b5f91", "#08476c"),
        Box("query", "Query + Semantic Layer", "governed SQL, KPI, quotas", 1580, 605, 315, 115),
        Box("portal", "Self-Service Portal / BI", "catalog, report builder, export", 1960, 605, 240, 115),
        Box("audit", "Audit + Data SLO", "query/export/access, quality alerts", 1580, 805, 315, 110, "#2e7d32", "#1f5b24"),
        Box("legacy", "SQL Server 2008 + Camel", "temporary read-only migration source", 405, 930, 310, 115, "#8b3a3a", "#662929"),
        Box("acl", "Anti-Corruption Layer", "legacy schema → versioned contract", 790, 930, 290, 115, "#8b3a3a", "#662929"),
        Box("clinical", "Clinical System", "medical records and studies", 405, 1180, 300, 115, "#8b3a3a", "#662929"),
        Box("ai", "Medical AI Services", "operational inference; mTLS; treatment purpose", 850, 1180, 330, 115, "#8b3a3a", "#662929"),
        Box("phi", "PHI boundary: no flow to portal/Lakehouse", "Карты, истории болезни и результаты исследований остаются здесь.", 1280, 1165, 610, 145, "#fff4cc", "#b88900", "#17212b"),
    )
    edges = (
        Edge("clinic", "outbox", "non-clinical events", ((300, 202), (350, 202), (350, 382), (405, 382))),
        Edge("fintech", "outbox", "banking events", ((300, 392), (405, 392))),
        Edge("corporate", "outbox", "business events", ((300, 582), (350, 582), (350, 420), (405, 420))),
        Edge("partners", "outbox", "validated API events", ((300, 772), (370, 772), (370, 440), (405, 440))),
        Edge("outbox", "broker", "at-least-once + idempotency key", ((675, 398), (790, 398)), "#7b3fa1"),
        Edge("broker", "ingest", "versioned schema", ((1080, 398), (1175, 398)), "#7b3fa1"),
        Edge("catalog", "ingest", "contract + classification", ((1325, 260), (1325, 340)), "#d88c00", True),
        Edge("ingest", "lakehouse", "accepted data product", ((1475, 400), (1580, 400)), "#0b5f91"),
        Edge("lakehouse", "query", "curated tables", ((1738, 460), (1738, 605))),
        Edge("query", "portal", "policy-filtered result", ((1895, 662), (1960, 662))),
        Edge("portal", "audit", "query/export event", ((2080, 720), (2080, 860), (1895, 860)), "#2e7d32", True),
        Edge("query", "audit", "SLI + access decision", ((1738, 720), (1738, 805)), "#2e7d32", True),
        Edge("legacy", "acl", "CDC", ((715, 988), (790, 988)), "#8b3a3a", True),
        Edge("acl", "broker", "temporary contract", ((935, 930), (935, 455)), "#8b3a3a", True),
        Edge("clinical", "ai", "PHI request (mTLS)", ((705, 1238), (850, 1238)), "#8b3a3a"),
        Edge("ai", "clinical", "signed inference result", ((850, 1280), (760, 1280), (760, 1270), (705, 1270)), "#8b3a3a"),
    )
    body = [
        title_block("Data Flow Diagram — доменные потоки", "Бизнес-сценарии обеспечиваются контрактами, событиями и изолированными data products", width),
        '<rect x="370" y="1120" width="850" height="225" rx="20" fill="none" stroke="#b3261e" stroke-width="3" stroke-dasharray="10 7"/>',
        svg_text(["Clinical & AI PHI zone"], 395, 1150, 16, "#8b3a3a", "start", "bold"),
    ]
    body.extend(render_edge(edge) for edge in edges)
    body.extend(render_box(box) for box in boxes)
    body.append(svg_text(["Пунктир — control/migration; фиолетовый — event flow; красный — legacy/PHI; синий — данные."], 40, 1395, 13, "#52616b", "start"))
    return svg_document(width, height, body)


def tech_radar() -> str:
    width, height = 2050, 1450
    cx, cy = 690, 735
    rings = ((155, "Adopt"), (285, "Trial"), (410, "Assess"), (540, "Hold"))
    body = [title_block("Технологический радар «Будущего 2.0»", "Целевой горизонт — 12 месяцев; номера соответствуют таблице tech-radar.md", width)]
    fills = ("#e4f5e8", "#e8f0ff", "#fff4cc", "#fde8e8")
    for (radius, label), fill in reversed(list(zip(rings, fills))):
        body.append(f'<circle cx="{cx}" cy="{cy}" r="{radius}" fill="{fill}" stroke="#64748b" stroke-width="2"/>')
        body.append(svg_text([label], cx, cy - radius + 24, 14, "#334155", weight="bold"))
    body.extend(
        [
            f'<line x1="{cx - 540}" y1="{cy}" x2="{cx + 540}" y2="{cy}" stroke="#64748b" stroke-width="2"/>',
            f'<line x1="{cx}" y1="{cy - 540}" x2="{cx}" y2="{cy + 540}" stroke="#64748b" stroke-width="2"/>',
            svg_text(["Платформы"], 360, 175, 18, "#17212b", weight="bold"),
            svg_text(["Инструменты"], 1020, 175, 18, "#17212b", weight="bold"),
            svg_text(["Методы"], 360, 1320, 18, "#17212b", weight="bold"),
            svg_text(["Языки / фреймворки"], 1020, 1320, 18, "#17212b", weight="bold"),
        ]
    )
    entries = {
        1: (600, 630), 2: (780, 610), 3: (610, 850), 4: (520, 815), 5: (780, 835), 6: (805, 760),
        7: (480, 525), 8: (570, 460), 9: (400, 630), 10: (850, 490), 11: (980, 620), 12: (940, 790), 13: (850, 940), 14: (495, 980),
        15: (330, 420), 16: (270, 700), 17: (1070, 435), 18: (360, 1080),
        19: (300, 430), 20: (1030, 1090), 21: (290, 1040), 22: (1030, 390), 23: (980, 1125),
    }
    ring_color = {range(1, 7): "#1f7a36", range(7, 15): "#1c57cd", range(15, 19): "#b77900", range(19, 24): "#b3261e"}
    for number, (x, y) in entries.items():
        color = next(value for key, value in ring_color.items() if number in key)
        body.append(f'<circle cx="{x}" cy="{y}" r="17" fill="{color}" stroke="#ffffff" stroke-width="2"/>')
        body.append(svg_text([str(number)], x, y + 5, 13, "#ffffff", weight="bold"))
    legend = [
        "1 Landing zone / Object Storage", "2 Terraform + policy-as-code", "3 GitOps / CI/CD / ADR",
        "4 Data contracts / ownership", "5 OIDC + MFA + RBAC/ABAC", "6 Python, Go, Java",
        "7 Kubernetes", "8 Kafka + Schema Registry", "9 S3 + Apache Iceberg", "10 Trino",
        "11 dbt + Airflow/Dagster", "12 Catalog + data quality", "13 OpenTelemetry + data SLO", "14 Data Mesh pilot",
        "15 Apache Flink", "16 Serverless query/ETL", "17 Data virtualization", "18 FinOps showback",
        "19 SQL Server 2008 as DWH", "20 PowerBuilder for new UI", "21 Logic in DWH/shared DB",
        "22 Point-to-point Camel", "23 Logic in custom Power BI",
    ]
    body.append('<rect x="1270" y="130" width="735" height="1210" rx="18" fill="#ffffff" stroke="#cbd5e1" stroke-width="2"/>')
    body.append(svg_text(["Легенда"], 1637, 170, 20, "#17212b", weight="bold"))
    for index, value in enumerate(legend):
        y = 215 + index * 46
        number, name = value.split(" ", 1)
        body.append(f'<circle cx="1305" cy="{y - 5}" r="13" fill="#334155"/>')
        body.append(svg_text([number], 1305, y, 11, "#ffffff", weight="bold"))
        body.append(svg_text([name], 1332, y, 13, "#334155", "start"))
    return svg_document(width, height, body)


def roadmap() -> str:
    width, height = 2100, 1120
    left, top, month_w, lane_h = 330, 170, 135, 115
    lanes = ["Foundation", "Platform", "Security & governance", "Domains", "Portal & BI", "Migration / change"]
    body = [title_block("Роадмап трансформации", "12 месяцев: от согласованной архитектуры до портала и read-only legacy", width)]
    for month in range(13):
        x = left + month * month_w
        body.append(f'<line x1="{x}" y1="{top}" x2="{x}" y2="{top + len(lanes) * lane_h}" stroke="#cbd5e1" stroke-width="1"/>')
        if month < 12:
            body.append(svg_text([f"M{month + 1}"], x + month_w / 2, top - 20, 13, "#334155", weight="bold"))
    for index, lane in enumerate(lanes):
        y = top + index * lane_h
        body.append(f'<rect x="20" y="{y}" width="{left + 12 * month_w - 20}" height="{lane_h}" fill="{("#ffffff" if index % 2 == 0 else "#f1f5f9")}"/>')
        body.append(svg_text([lane], 30, y + 65, 15, "#17212b", "start", "bold"))
        body.append(f'<line x1="20" y1="{y + lane_h}" x2="{left + 12 * month_w}" y2="{y + lane_h}" stroke="#cbd5e1"/>')
    bars = [
        (0, 0, 2, "C4/DFD, domains, baseline", "#1c57cd"), (0, 2, 2, "Terraform modules + landing zone", "#1c57cd"),
        (1, 1, 3, "Lakehouse, Kafka, catalog, query", "#5b4b9a"), (1, 4, 4, "HA, quotas, observability", "#5b4b9a"),
        (2, 0, 4, "classification, IAM/ABAC, data contracts", "#2e7d32"), (2, 4, 5, "audit, DLP, DR game days", "#2e7d32"),
        (3, 2, 3, "Clinic + Fintech pilots", "#d88c00"), (3, 5, 3, "Corporate + Partners", "#d88c00"), (3, 8, 4, "Pharma + medtech onboarding", "#d88c00"),
        (4, 3, 4, "portal MVP + 10 reports", "#1168bd"), (4, 7, 5, "self-service rollout", "#1168bd"),
        (5, 1, 4, "CDC + reconciliation", "#8b3a3a"), (5, 5, 4, "report migration + training", "#8b3a3a"), (5, 9, 3, "read-only DWH; exit plan", "#8b3a3a"),
    ]
    for lane, start, length, label, color in bars:
        x = left + start * month_w + 6
        y = top + lane * lane_h + 28
        w = length * month_w - 12
        body.append(f'<rect x="{x}" y="{y}" width="{w}" height="58" rx="12" fill="{color}" filter="url(#shadow)"/>')
        body.append(svg_text(text_lines(label, int(w - 18), 12), x + w / 2, y + 26, 12, "#ffffff", weight="bold"))
    milestones = [(2, "Архитектура согласована"), (4, "Platform MVP"), (7, "Portal MVP"), (10, "M&A template"), (12, "Legacy read-only")]
    for month, label in milestones:
        x = left + month * month_w
        y = top + len(lanes) * lane_h + 35
        body.append(f'<polygon points="{x},{y - 14} {x + 14},{y} {x},{y + 14} {x - 14},{y}" fill="#17212b"/>')
        body.append(svg_text(text_lines(label, 210, 12), x, y + 38, 12, "#334155", weight="bold"))
    body.append(svg_text(["Go/no-go на каждом milestone: reconciliation, SLO, security, DR и adoption. Legacy остаётся rollback-путём до прохождения gate."], 30, 1070, 13, "#52616b", "start"))
    return svg_document(width, height, body)


def deployment() -> str:
    width, height = 2050, 1220
    boxes = (
        Box("git", "Git repository", "reviewed Terraform code", 40, 250, 230, 100, "#5f6b76", "#414a52"),
        Box("ci", "CI pipeline", "fmt → validate → security scan", 355, 250, 260, 105, "#5b4b9a", "#443575"),
        Box("plan", "Terraform plan", "immutable plan artifact", 700, 250, 250, 105, "#5b4b9a", "#443575"),
        Box("approve", "Manual go/no-go", "separation of duties", 1035, 250, 250, 105, "#fff4cc", "#b88900", "#17212b"),
        Box("apply", "Terraform apply", "service account; audited execution", 1370, 250, 270, 105, "#5b4b9a", "#443575"),
        Box("vpc", "VPC Network", "Terraform-managed", 120, 545, 250, 100),
        Box("subnet", "Subnet 10.42.10.0/24", "Terraform-managed", 460, 545, 270, 100),
        Box("sg", "Security Group", "HTTP; optional SSH; egress", 820, 545, 260, 100, "#2e7d32", "#1f5b24"),
        Box("vm", "Compute VM", "2 vCPU / 2 GiB; Ubuntu; preemptible", 1170, 545, 300, 115),
        Box("boot", "Boot Disk", "10 GiB network-hdd", 1170, 770, 240, 100, "#0b5f91", "#08476c"),
        Box("data", "Data Disk", "10 GiB; separate lifecycle", 1510, 770, 250, 100, "#0b5f91", "#08476c"),
        Box("nat", "Public NAT", "demo validation only", 1550, 545, 250, 100, "#d88c00", "#9a6200", "#17212b"),
        Box("cloudinit", "cloud-init", "install Nginx + health page", 1170, 970, 300, 105, "#2e7d32", "#1f5b24"),
        Box("manual", "Outside Terraform", "billing, cloud/folder, bootstrap SA, credential rotation, business access approval, production data", 80, 930, 780, 155, "#fff4cc", "#b88900", "#17212b"),
    )
    edges = (
        Edge("git", "ci", "push / pull request", ((270, 300), (355, 300))),
        Edge("ci", "plan", "validated code", ((615, 300), (700, 300))),
        Edge("plan", "approve", "plan review", ((950, 300), (1035, 300))),
        Edge("approve", "apply", "approved plan", ((1285, 300), (1370, 300))),
        Edge("apply", "vpc", "provider API creates graph", ((1505, 355), (1505, 430), (245, 430), (245, 545)), "#1c57cd"),
        Edge("vpc", "subnet", "network_id", ((370, 595), (460, 595))),
        Edge("subnet", "sg", "network boundary", ((730, 595), (820, 595))),
        Edge("sg", "vm", "security_group_ids", ((1080, 595), (1170, 600))),
        Edge("subnet", "vm", "subnet_id", ((595, 645), (595, 690), (1320, 690), (1320, 660))),
        Edge("nat", "vm", "public IPv4", ((1550, 600), (1470, 600)), "#d88c00"),
        Edge("boot", "vm", "boot_disk", ((1290, 770), (1290, 660))),
        Edge("data", "vm", "secondary_disk", ((1510, 820), (1450, 820), (1450, 660))),
        Edge("cloudinit", "vm", "user-data", ((1320, 970), (1320, 660)), "#2e7d32", True),
    )
    body = [
        title_block("Автоматизация IaaS-развёртывания", "Terraform управляет графом ресурсов; ручные шаги ограничены bootstrap и одобрениями", width),
        '<rect x="40" y="480" width="1840" height="440" rx="22" fill="none" stroke="#59636e" stroke-width="2" stroke-dasharray="10 7"/>',
        svg_text(["Yandex Cloud folder — Terraform managed resources"], 70, 515, 16, "#334155", "start", "bold"),
    ]
    body.extend(render_edge(edge) for edge in edges)
    body.extend(render_box(box) for box in boxes)
    body.append(svg_text(["Синий — Terraform resource; зелёный — security/bootstrap; жёлтый — осознанный ручной gate."], 40, 1165, 13, "#52616b", "start"))
    return svg_document(width, height, body)


GENERATED = {
    ROOT / "Task1" / "c4-container.svg": c4_container,
    ROOT / "Task2" / "data-flow-diagram.svg": data_flow,
    ROOT / "Task3" / "tech-radar.svg": tech_radar,
    ROOT / "Task3" / "roadmap.svg": roadmap,
    ROOT / "Task4" / "deployment-automation.svg": deployment,
}


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--check", action="store_true", help="Fail if generated SVGs differ from files")
    args = parser.parse_args()
    failures: list[str] = []
    for path, factory in GENERATED.items():
        content = factory()
        if args.check:
            if not path.exists() or path.read_text(encoding="utf-8") != content:
                failures.append(str(path.relative_to(ROOT)))
        else:
            path.write_text(content, encoding="utf-8")
            print(path.relative_to(ROOT))
    if failures:
        raise SystemExit("Outdated generated files: " + ", ".join(failures))


if __name__ == "__main__":
    main()
