#!/usr/bin/env python3
"""Make real decision records for the review tool's Agent decisions screen (#659).

    python3 make_decisions.py <scratch folder> <Phoenix memory clone> <out folder>

A fresh shop project (issue 613, the Kickoff sample) and a clone of Phoenix memory. The real
memory tool records the decisions /intent, /vision and /understand would make — each source
read from real Phoenix memory lines, or from the project's own Garura memory, or from a memory
update a person approved. Then memory moves on, the way it does: one Phoenix line is edited,
one Garura memory file is removed, and one old record names no memory. The tool's own answers
are written to the out folder, exactly as the contract shapes them: decisions.json is
`citations --check` (the records and the problems), updates.json is `updates` (the memory update
a decision came from, with who approved it). The reviewer named below is a sample, not a
person's real answer.
"""

import json
import os
import shutil
import subprocess
import sys

TOOL = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "..", "..", "..", "..",
                                    "core", "tools", "memory", "memory.py"))
work, phoenix_src, out = os.path.abspath(sys.argv[1]), os.path.expanduser(sys.argv[2]), os.path.abspath(sys.argv[3])
if os.path.exists(work):
    shutil.rmtree(work)
project, phoenix = os.path.join(work, "shop"), os.path.join(work, "phoenix-memory")
short = os.path.join(project, ".garura", "project", "issues")
garura = os.path.join(project, ".garura")
os.makedirs(os.path.join(short, "613"))
subprocess.run(["git", "clone", "-q", phoenix_src, phoenix], check=True)
subprocess.run(["git", "-C", phoenix, "checkout", "-q", "-B", "main", "origin/main"], check=True)
with open(os.path.join(project, "memory-settings.json"), "w") as fh:
    json.dump({"short-term": ".garura/project/issues", "garura": ".garura", "phoenix": "../phoenix-memory",
               "phoenix_ref": "main", "garura_pull_dir": "core/memory"}, fh)


def write(rel, text):
    path = os.path.join(garura, rel)
    os.makedirs(os.path.dirname(path), exist_ok=True)
    with open(path, "w") as fh:
        fh.write(text)


# The shop's own Garura memory: two pages of its product model.
write("product/product-os/checkout/checkout/capability.md",
      "# Checkout\n\nDomain: checkout\nLevel: detailed\n\n## What it does\nTakes a shopper from the cart to a paid order.\n\n"
      "## Decisions\n- Payment through a PSP; card data never touches our servers.\n\n"
      "Guest checkout: allowed at launch; an account is offered after payment.\n")
write("product/product-os/checkout/limits.md", "# Checkout limits\n\nCart size: no cap at launch.\n")

env = dict(os.environ, MEMORY_SETTINGS=os.path.join(project, "memory-settings.json"))
for k in ("MEMORY_SHORT_TERM_ROOT", "MEMORY_GARURA_ROOT", "MEMORY_PHOENIX_ROOT", "MEMORY_PHOENIX_REF"):
    env.pop(k, None)


def tool(command, request):
    run = subprocess.run([sys.executable, TOOL, command, "--request", json.dumps(request)],
                         capture_output=True, text=True, env=env, cwd=project)
    answer = json.loads(run.stdout.splitlines()[0])
    if not answer["ok"]:
        raise SystemExit(f"{command} failed: {answer['error']}")
    return answer


def source(tier, path, start, end):
    """Read the lines the way an agent would, and name them with their fingerprint."""
    a = tool("read", {"issue": 613, "tier": tier, "path": path, "start": start, "end": end})
    return {"tier": tier, "path": path, "start": start, "end": end, "fingerprint": a["fingerprint"]}


def cite(play, by, question, answer, sources, **extra):
    tool("cite", {"issue": 613, "play": play, "decided_by": by, "question": question, "answer": answer,
                  "sources": sources, **extra})


# A memory update a person approved: how long a guest cart is kept.
u = tool("propose", {"issue": 613, "missing": "How long a guest's cart is kept before it is cleared.",
                     "target_tier": "short-term", "target_path": "613/context/answers/guest-cart.md",
                     "draft": "A guest cart is kept for 7 days, then cleared. The guest is told when they come back.\n",
                     "draft_source": "web", "sources": [], "requested_by": "product-os-keeper (/vision)",
                     "blocking": True})["update"]
tool("decide", {"id": u["id"], "verdict": "approve", "by": "sample reviewer", "reply": "Yes, 7 days.",
                "decided_in": "review-tool"})
tool("apply", {"id": u["id"]})

PAY, USERS, SHOP = "knowledge/domains/payments.md", "knowledge/domains/user-management.md", "knowledge/domains/ecommerce.md"
CHECKOUT, LIMITS = "product/product-os/checkout/checkout/capability.md", "product/product-os/checkout/limits.md"
cite("/intent", "intent-resolver (/intent)", "What path does a shopper take from the storefront to paying?",
     "Home, category pages, product listing, product detail, cart, then checkout.", [source("phoenix", SHOP, 87, 88)])
cite("/vision", "product-os-keeper (/vision)", "How does the shop take card payments?",
     "Through a payment provider with hosted fields, so card data never touches our servers.",
     [source("phoenix", PAY, 19, 21), source("phoenix", PAY, 44, 44)])
cite("/vision", "product-os-keeper (/vision)", "Can a returning shopper pay with a saved card?",
     "Yes, as a provider token only — never the card number.", [source("phoenix", PAY, 63, 65)])
cite("/vision", "product-os-keeper (/vision)", "Are Apple Pay and Google Pay part of launch?",
     "Yes. The shop has a mobile app, so wallets are in.", [source("phoenix", PAY, 47, 47)])
cite("/vision", "product-os-keeper (/vision)", "Is guest checkout allowed at launch?",
     "Yes. An account is offered after payment.", [source("garura", CHECKOUT, 12, 12)])
cite("/vision", "product-os-keeper (/vision)", "How long is a guest's cart kept?",
     "Seven days, then it is cleared and the guest is told.",
     [source("short-term", "613/context/answers/guest-cart.md", 1, 1)], from_update=u["id"])
cite("/vision", "product-os-keeper (/vision)", "Is there a cap on items in a cart?",
     "No cap at launch.", [source("garura", LIMITS, 3, 3)])
cite("/understand", "product-os-keeper (/understand)", "How do shoppers sign in?",
     "Email and password, with social login for public shoppers.", [source("phoenix", USERS, 45, 46)])
cite("/understand", "product-os-keeper (/understand)", "Does the shop need MFA at launch?",
     "Yes. Taking card payments brings PCI-DSS, and MFA comes with it.", [source("phoenix", USERS, 47, 47)])
cite("/understand", "product-os-keeper (/understand)", "Which refunds are in launch?",
     "Full and partial refunds through the payment provider.", [source("phoenix", PAY, 60, 60)])
cite("/understand", "product-os-keeper (/understand)", "How does a shopper get back into a locked account?",
     "Password reset, the floor for any password login.", [source("phoenix", USERS, 61, 62)])

# Memory moves on. A Phoenix line is edited (approved outside Garura), a Garura file is removed,
# and one old record, written before every decision had to name its memory, has no source.
path = os.path.join(phoenix, PAY)
with open(path) as fh:
    lines = fh.read().split("\n")
lines[46] = "  - Wallets — Apple Pay / Google Pay one-tap. Add when `shape.surfaces` includes mobile and the PSP supports wallets in every launch region."
with open(path, "w") as fh:
    fh.write("\n".join(lines))
subprocess.run(["git", "-C", phoenix, "-c", "user.name=sample", "-c", "user.email=sample@example.com",
                "commit", "-qam", "wallets need PSP support in every launch region"], check=True)
os.remove(os.path.join(garura, LIMITS))
with open(os.path.join(short, "613", "context", "citations.jsonl"), "a") as fh:
    fh.write(json.dumps({"citation_id": "cite-20261009-001", "issue": 613, "play": "/understand",
                         "question": "Does checkout need an address book?", "answer": "Not at launch.",
                         "decided_by": "product-os-keeper (/understand)", "decided_at": "2026-10-09T11:20:00Z",
                         "sources": [], "from_update": None}) + "\n")

for name, command, request in (("decisions.json", "citations", {"issue": 613, "check": True}),
                               ("updates.json", "updates", {})):
    with open(os.path.join(out, name), "w", encoding="utf-8") as fh:
        json.dump(tool(command, request), fh, indent=2, ensure_ascii=False)
        fh.write("\n")
shutil.rmtree(work)
