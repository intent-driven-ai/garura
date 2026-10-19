#!/usr/bin/env python3
"""Make real decision records for the review tool's Agent decisions screen (#659).

    python3 make_decisions.py <scratch folder> <Phoenix memory clone> <out folder>

A fresh shop project (issue 613, the Kickoff sample) and a clone of Phoenix memory. The real
memory tool records the decisions /intent, /vision and /understand would make, each with its
trace: the steps the agent took, in order. A step reads the shop's own Garura memory (its
product profile — who the users are, the surfaces, the security level, the compliance regimes —
and its product model), or real Phoenix memory lines (the domain knowledge those values select),
or a memory update a person approved. Then memory moves on, the way it does: one Phoenix line is edited,
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
MARK = ".made-by-make_decisions"  # this script only ever deletes a folder it made
if os.path.exists(work):
    if not os.path.isfile(os.path.join(work, MARK)):
        raise SystemExit(f"{work} exists and was not made by this script; give a new folder.")
    shutil.rmtree(work)
os.makedirs(work)
open(os.path.join(work, MARK), "w").close()
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


# The shop's own Garura memory: its product profile (the product-profile schema in Phoenix
# memory) and two pages of its product model.
write("product/product-os/profile.yaml",
      "profile:\n  product_ref: shop\n  state: set\n  shape:\n    stage: public\n    users: public\n"
      "    monetization: paywall\n    surfaces: [web, mobile]\n  nfr:\n"
      '    performance:   { level: high, gate: "p95 page load under 2 s" }\n'
      '    security:      { level: high, gate: "OWASP ASVS L2; no P1/P2" }\n'
      '    accessibility: { level: high, gate: "WCAG 2.1 AA" }\n'
      '    privacy:       { level: high, gate: "PII encrypted at rest and in transit" }\n'
      "  compliance: [PCI-DSS, GDPR]\n")
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


def step(asked, found, tier, path, start, end):
    """One step of a trace: read the lines the way an agent would, and name them with their
    fingerprint."""
    a = tool("read", {"issue": 613, "tier": tier, "path": path, "start": start, "end": end})
    return {"asked": asked, "found": found,
            "source": {"tier": tier, "path": path, "start": start, "end": end, "fingerprint": a["fingerprint"]}}


def cite(play, by, question, answer, trace, **extra):
    tool("cite", {"issue": 613, "play": play, "decided_by": by, "question": question, "answer": answer,
                  "trace": trace, **extra})


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
PROFILE = "product/product-os/profile.yaml"
CHECKOUT, LIMITS = "product/product-os/checkout/checkout/capability.md", "product/product-os/checkout/limits.md"
INTENT, VISION, UNDERSTAND = "intent-resolver (/intent)", "product-os-keeper (/vision)", "product-os-keeper (/understand)"
USERS_ARE = step("Who are the shop's users, and where do they use it?", "The public, on web and mobile.",
                 "garura", PROFILE, 6, 8)
SECURITY = step("What security level and compliance does the profile set?",
                "Security is high; PCI-DSS and GDPR are in force.", "garura", PROFILE, 11, 14)

cite("/intent", INTENT, "What path does a shopper take from the storefront to paying?",
     "Home, category pages, product listing, product detail, cart, then checkout.", [
         step("Which domain is this product in?", "Ecommerce: the shop sells goods — catalog, cart, orders, storefront.",
              "phoenix", SHOP, 5, 5),
         step("What journey must an ecommerce product always have?",
              "The core journey: home, category pages, product listing, product detail, cart, checkout handoff.",
              "phoenix", SHOP, 87, 88)])
cite("/vision", VISION, "How does the shop take card payments?",
     "Through a payment provider with hosted fields, so card data never touches our servers.", [
         step("Does the shop take money?", "Yes: monetization is paywall.", "garura", PROFILE, 7, 7),
         step("Which domain covers taking money?", "Payments, not ecommerce.", "phoenix", SHOP, 22, 22),
         step("What is the payments stance?", "Never hold card data you don't have to: charge through a PSP "
              "with hosted fields and tokenisation.", "phoenix", PAY, 19, 21),
         step("What is the floor for card payments?", "Card via PSP with hosted fields.", "phoenix", PAY, 44, 44)])
cite("/vision", VISION, "Can a returning shopper pay with a saved card?",
     "Yes, as a provider token only — never the card number.", [
         SECURITY,
         step("What does a saved card need under PCI-DSS?", "Tokenised vaulting is the floor and mandatory under "
              "PCI-DSS: store the PSP token, never the card.", "phoenix", PAY, 63, 65)])
cite("/vision", VISION, "Are Apple Pay and Google Pay part of launch?",
     "Yes. The shop has a mobile app, so wallets are in.", [
         USERS_ARE,
         step("When are wallets included?", "Add wallets when the surfaces include mobile.", "phoenix", PAY, 47, 47)])
cite("/vision", VISION, "Is guest checkout allowed at launch?",
     "Yes. An account is offered after payment.", [
         USERS_ARE,
         step("What has the product model decided for checkout?", "Guest checkout is allowed at launch; an account "
              "is offered after payment.", "garura", CHECKOUT, 12, 12)])
cite("/vision", VISION, "How long is a guest's cart kept?",
     "Seven days, then it is cleared and the guest is told.", [
         step("Do guests have carts?", "Yes: guest checkout is allowed at launch.", "garura", CHECKOUT, 12, 12),
         step("How long is a guest cart kept?", "Seven days, then cleared; the guest is told.",
              "short-term", "613/context/answers/guest-cart.md", 1, 1)], from_update=u["id"])
cite("/vision", VISION, "Is there a cap on items in a cart?", "No cap at launch.", [
         step("What limits has the product model set for checkout?", "Cart size: no cap at launch.",
              "garura", LIMITS, 3, 3)])
cite("/understand", UNDERSTAND, "How do shoppers sign in?",
     "Email and password, social login, and MFA.", [
         USERS_ARE,
         step("Which domain covers sign-in, and what decides its parts?", "User management. Its parts are picked by "
              "the profile: the users, the surfaces, security, accessibility and compliance.", "phoenix", USERS, 4, 6),
         SECURITY,
         step("Which sign-in methods do those values select?", "Email and password is the floor; social login "
              "because the users are public; MFA because security is high and PCI-DSS is in force.",
              "phoenix", USERS, 44, 47)])
cite("/understand", UNDERSTAND, "Does the shop need MFA at launch?",
     "Yes. Security is high and PCI-DSS is in force; either one brings MFA.", [
         SECURITY,
         step("When is MFA included?", "When security is high or more, or compliance includes PCI-DSS.",
              "phoenix", USERS, 47, 47)])
cite("/understand", UNDERSTAND, "Which refunds are in launch?",
     "Full and partial refunds through the payment provider. Chargeback handling waits.", [
         step("What is the refunds floor?", "Full and partial refunds through the PSP.", "phoenix", PAY, 60, 60),
         step("Does the shop's monetization call for more?", "Monetization is paywall.", "garura", PROFILE, 7, 7),
         step("When is chargeback handling added?", "When monetization is monetized — not this shop, yet.",
              "phoenix", PAY, 61, 61)])
cite("/understand", UNDERSTAND, "How does a shopper get back into a locked account?",
     "Password reset, unlock, and timed self-service auto-unlock.", [
         SECURITY,
         step("Which recovery do those values select?", "Password reset is the floor; unlock at medium security; "
              "auto-unlock at high.", "phoenix", USERS, 61, 64)])

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
                         "trace": [], "from_update": None}) + "\n")

for name, command, request in (("decisions.json", "citations", {"issue": 613, "check": True}),
                               ("updates.json", "updates", {})):
    with open(os.path.join(out, name), "w", encoding="utf-8") as fh:
        json.dump(tool(command, request), fh, indent=2, ensure_ascii=False)
        fh.write("\n")
shutil.rmtree(work)
