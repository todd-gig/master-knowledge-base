# Why Stage 1 — Sources (1-minute read)

**Every later decision is grounded in your actual documentation, or it isn't grounded at all.** Stage 1 is where that grounding happens.

Without sources connected, the platform falls back to **generic templates**: industry-average ICPs, off-the-shelf voice variables, recommendations drawn from no document the operator actually wrote. Generic templates are better than nothing for the first ten minutes, and worse than nothing by week two — they generate confident answers that don't match the operator's reality, and the operator stops trusting the platform.

With **at least one source connected** (one Google Drive account, one folder), the "chat with your data" capability turns on. Every later question routed through the chat surface gets answered against the operator's own documents — meeting notes, SOPs, contracts, brand guidelines, the README the founder wrote three years ago. Penrose, the decision-engine, and the persona-engine all draw from the same canonical corpus.

The bar is intentionally low: **one connected source is enough to flip the capability.** The activation gate for stage advancement is higher — `file_count >= 20` — because 20 files is roughly the floor below which downstream personalization quality degrades. But the *capability* (chat with your data) is gated on connection, not file count.

Stage 1 emits a stream of events as ingest progresses: `DocumentationAccountsLinked` when the OAuth completes, `DocumentationFolderSubscribed` when you pick a folder, `DocumentationIngestRun` per batch, and `DocumentationCoverageAdvanced` whenever coverage of an internal taxonomy increases. The chat side panel reflects all of these in real time.

The estimated cost is **~$0.50/operator/month** of compute + storage. The unlocked value is **~$1-3k/month in founder time saved** — the difference between answering a question from memory and answering it from your actual documentation, automatically.

If you only remember one thing: **Stage 1 transforms the platform from a templates-and-vibes engine into a grounded-in-your-doctrine engine. Skipping it means every later answer is generic.**
