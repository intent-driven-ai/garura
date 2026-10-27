# ADR 039, Decision 4 (committed on plan/788/base) and the glossary row for Garura memory

### 4. The memory tool never copies a Phoenix file

- The tool reads Phoenix memory. It does not copy a file from it into the project.
- A project's Garura memory is built separately, from only the part the project needs: by `initialize`, and by promotion.
- The tool's `pull`, and its copy on `read`, go.

The product owner: "tool will not copy. it read the phoenix memory, and then it builds the project memry separately. For example, [Phoenix] has a memory about, let's say, a commerce domain, and let's say the project that we're working on only needs checkout in the commerce domain. You don't need to copy the entire file. You only need to bring in the context which is relevant to the checkout part of the commerce, so it cannot copy the file. It should not copy the file."

Glossary (core/grounding/glossary.md, line 37):

| **Garura memory** | The project's own memory, at `.garura/core/memory/` and kept in git; the product model at `.garura/product/` is part of it, not all of it. Built from only the part of Phoenix memory the project needs (by `initialize`) and from what people promote — never a copy of a Phoenix file (ADR 039). | `.garura/core/memory/`, `.garura/product/` | Second tier of a lookup (`.garura/core/memory/`, then the product model); filled by `initialize` and promotion; written as work only by plays built to write the product model | NOT: Phoenix memory. NOT: a copy of Phoenix memory — checkout, not all of commerce. |
