# 🔍 Elasticsearch & Full-Text Search — The Ultimate HLD Guide

> **Last Updated:** March 2026
> **Author:** System Design Study Notes (Scaler Academy — HLD Module)
> **Topics:** Full-Text Search, Inverted Index, Stop Words, Stemming, Lemmatization, Sharding, Map Reduce, Replication, TF-IDF Ranking, Elasticsearch Architecture

---

![Elasticsearch Architecture Overview](./images/es_hero_diagram.png)

---

## 📋 Table of Contents

### Part 1: The Problem — Full-Text Search
1. [What Is Full-Text Search?](#-what-is-full-text-search)
2. [Real-World Use Cases](#-real-world-use-cases)
3. [Why SQL & NoSQL Databases Fail](#-why-sql--nosql-databases-fail)
4. [The Index Problem — Why Normal Indexes Don't Help](#-the-index-problem--why-normal-indexes-dont-help)

### Part 2: The Inverted Index — The Magic Data Structure
5. [What Is an Inverted Index?](#-what-is-an-inverted-index)
6. [Why Is It Called "Inverted"?](#-why-is-it-called-inverted)
7. [Storing Position Information](#-storing-position-information)
8. [Answering Single-Word Queries](#-answering-single-word-queries)
9. [Answering Multi-Word Queries](#-answering-multi-word-queries)

### Part 3: Text Processing Pipeline
10. [The Full Pipeline Overview](#-the-full-pipeline-overview)
11. [Stop Word Removal](#-stop-word-removal)
12. [Stemming — Fast but Imperfect](#-stemming--fast-but-imperfect)
13. [Lemmatization — Smart but Slow](#-lemmatization--smart-but-slow)
14. [Other Cleaning Steps](#-other-cleaning-steps)
15. [Applying the Pipeline to Queries Too](#-applying-the-pipeline-to-queries-too)

### Part 4: Scaling with Sharding
16. [Why We Need Sharding](#-why-we-need-sharding)
17. [CAP Theorem for Search Systems](#-cap-theorem-for-search-systems)
18. [Approach 1 — Document-ID Based Sharding (Recommended)](#-approach-1--document-id-based-sharding-recommended)
19. [Map Reduce — How Queries Run Across Shards](#-map-reduce--how-queries-run-across-shards)
20. [Pros of Document-ID Sharding](#-pros-of-document-id-sharding)
21. [Approach 2 — Word-Based Sharding](#-approach-2--word-based-sharding)
22. [Cons of Word-Based Sharding](#-cons-of-word-based-sharding)
23. [Zipf's Law — Why Word Sharding Is Structurally Broken](#-zipfs-law--why-word-sharding-is-structurally-broken)

### Part 5: Replication & Fault Tolerance
24. [Elasticsearch Replication Architecture](#-elasticsearch-replication-architecture)
25. [Master-Replica Placement Rules](#-master-replica-placement-rules)

### Part 6: Ranking & Relevance
26. [Beyond Matching — Why Ranking Matters](#-beyond-ranking--why-ranking-matters)
27. [TF-IDF — Term Frequency × Inverse Document Frequency](#-tf-idf--term-frequency--inverse-document-frequency)
28. [Other Ranking Signals](#-other-ranking-signals)
29. [Handling Misspellings & Synonyms](#-handling-misspellings--synonyms)

### Part 7: Summary & Interview Prep
30. [Elasticsearch vs Other Solutions](#-elasticsearch-vs-other-solutions)
31. [Complete Architecture Diagram](#-complete-architecture-diagram)
32. [Quick Reference Cheatsheet](#-quick-reference-cheatsheet)
33. [Practice Questions](#-practice-questions)
34. [References & Resources](#-references--resources)

---

# PART 1: THE PROBLEM — FULL-TEXT SEARCH

---

## 🎯 What Is Full-Text Search?

Full-text search is the ability to search **inside** the content of documents — not just match exact IDs or start-of-string prefixes.

```
THREE KINDS OF SEARCH (Different Complexity):
──────────────────────────────────────────────────────────────

  EXACT MATCH (Easy):
  → Query: "review_id = 10492"
  → Answer: a single row in the DB
  → Any database handles this ✅

  PREFIX MATCH (Medium):
  → Query: all products starting with "wom"
  → Answer: woman, women, wombat...
  → A sorted index (B+ tree) handles this ✅

  FULL-TEXT SEARCH (Hard — our problem today!):
  → Query: "value for money"
  → Answer: all documents that contain this ANYWHERE in the text
             beginning: "Value for money is great" ✅
             middle:    "This product gives great value for money" ✅
             end:       "I think it's good value for money" ✅
  → Normal indexes CANNOT handle this ❌
──────────────────────────────────────────────────────────────
```

> ⚠️ **What full-text search is NOT:**
> - **Ctrl+F in browser** — that scans one document for a string (a DSA problem)
> - **grep / regex** — a local file-system scan tool for developers
> - **Plagiarism detection** — fuzzy matching problem, not full-text search
> - **Google Search** — much more complex (PageRank, backlinks, etc.) though it does use full-text search internally

---

## 🌏 Real-World Use Cases

Any system where you store text and users need to search *within* that text:

| System | What Gets Searched |
|--------|-------------------|
| **Distributed Logs** (any large company) | Log message content — for debugging, security audits, tracing |
| **E-commerce** (Amazon, Flipkart) | Product titles + descriptions + **millions of reviews** |
| **Social Media** (Twitter, Quora, Reddit) | Posts, answers, profiles, comments |
| **Workplace Chat** (Slack, MS Teams) | All messages across all channels |
| **Cloud Storage** (Google Drive, Dropbox) | File contents — PDFs, Docs, Sheets |
| **Email** (Gmail) | Email subject + body |
| **Code Platforms** (GitHub, StackOverflow) | Code snippets, comments, answers |
| **Job Platforms** (LinkedIn, Naukri) | Profiles, job descriptions |
| **Scalar** | Problem descriptions, editorial content |

> 💡 **Key Insight:** In all these cases, you have a large collection of **documents** and a short **text query**. Your goal: find all (or top N) documents matching the query.

---

## 💥 Why SQL & NoSQL Databases Fail

Let's say Amazon reviews are stored in SQL:

```sql
CREATE TABLE product_reviews (
  review_id   BIGINT PRIMARY KEY,
  product_id  BIGINT,
  content     TEXT
);
```

A naive full-text search query would be:

```sql
SELECT * FROM product_reviews
WHERE content LIKE '%value for money%';
```

```
WHY THIS IS CATASTROPHICALLY SLOW:
──────────────────────────────────────────────────────────────
  If n = rows in table, m = average characters per review:

  → No index: O(n × m) — scans EVERY character of EVERY row
  → n = billions of reviews
  → m = hundreds of characters each
  → Result: query takes MINUTES TO HOURS
  → Amazon goes down for a single search request ❌
──────────────────────────────────────────────────────────────
```

The same problem exists for NoSQL — MongoDB, Cassandra, DynamoDB — **none of them support arbitrary mid-string text search efficiently**. They are key-value stores at heart.

---

## 📇 The Index Problem — Why Normal Indexes Don't Help

You might think "just add an index on the `content` column!"

```
WHAT A B+ TREE INDEX ON `content` GIVES YOU:
──────────────────────────────────────────────────────────────

  The index stores rows SORTED by the content column.
  
  ✅ It CAN answer: content LIKE 'value%'
     (prefix match — binary search works!)

  ❌ It CANNOT answer: content LIKE '%value for money%'
     (the % at the START means: could be ANYWHERE)
     → Binary search is impossible
     → Falls back to full table scan
     → Back to O(n × m) ❌

  KEY INSIGHT:
  "The moment you have a leading % in your LIKE query,
   the index becomes completely useless."
──────────────────────────────────────────────────────────────
```

Other data structures that **don't** help:
- **Tries** → Only prefix matches (same problem as sorted index)
- **Bloom Filters** → Only answer "does this string exist?" with YES/NO, can't retrieve documents
- **Hash Maps with exact keys** → Only exact lookups — no fuzzy/partial matching

We need something fundamentally different: an **Inverted Index**.

---

# PART 2: THE INVERTED INDEX — THE MAGIC DATA STRUCTURE

---

## 🗂️ What Is an Inverted Index?

An inverted index is a **hash map from word → list of documents that contain that word**.

![Inverted Index Concept](./images/inverted_index_diagram.png)

```
BUILDING AN INVERTED INDEX:
──────────────────────────────────────────────────────────────

  DOCUMENTS:
  ┌─────────────────────────────────────────────────┐
  │ Doc 1: "I ate at this restaurant food was nice" │
  │ Doc 2: "The ambience was awesome"               │
  │ Doc 3: "Service was great"                      │
  └─────────────────────────────────────────────────┘

  STEP 1: Split every document into individual words
  STEP 2: For every unique word, record which docs contain it
  STEP 3: Store as a hashmap (word → document list)

  INVERTED INDEX:
  ┌──────────────┬─────────────────────────────────────────┐
  │   Word (Key) │  Documents (Value)                      │
  ├──────────────┼─────────────────────────────────────────┤
  │ "ate"        │ [Doc1: pos=1]                           │
  │ "restaurant" │ [Doc1: pos=3]                           │
  │ "food"       │ [Doc1: pos=5]                           │
  │ "nice"       │ [Doc1: pos=7]                           │
  │ "ambience"   │ [Doc2: pos=1]                           │
  │ "awesome"    │ [Doc2: pos=3]                           │
  │ "service"    │ [Doc3: pos=0]                           │
  │ "great"      │ [Doc3: pos=2]                           │
  │ "was"        │ [Doc1: pos=6, Doc2: pos=2, Doc3: pos=1] │
  └──────────────┴─────────────────────────────────────────┘

  Now to answer query "awesome":
  → Look up "awesome" in hashmap → O(1) → [Doc2] ✅
──────────────────────────────────────────────────────────────
```

> 💡 **This is just a hashmap.** That's it. The genius is in what you store as the key (the word) and the value (documents + positions).

---

## 🔁 Why Is It Called "Inverted"?

The name makes sense when you compare it to the *regular* index:

```
REGULAR INDEX (forward index):
  Key   = Document ID
  Value = List of words in that document
  → "Find all words in document #42"

INVERTED INDEX (reverse/inverted):
  Key   = Word
  Value = List of document IDs that contain this word
  → "Find all documents that contain the word 'awesome'"

  This is exactly like the GLOSSARY at the back of a book!
  ─────────────────────────────────────────────────────────
  Front of book = Table of Contents (document → topics)
  Back of book  = Glossary (topic/word → page numbers)
                  ↑ This is the inverted index!
```

---

## 📍 Storing Position Information

In addition to the document ID, we also store **the position** (character or word index) where the word appears:

```
INVERTED INDEX WITH POSITIONS:
──────────────────────────────────────────────────────────────

  Entry format: { docId: X, position: Y }

  "was" → [
    { docId: 1, position: 6 },   ← position in Doc 1
    { docId: 2, position: 2 },   ← position in Doc 2
    { docId: 3, position: 1 }    ← position in Doc 3
  ]

  WHY POSITIONS MATTER:
  If query = "value for money" (a phrase search):
  → Find all docs where "value" is at position i
  → AND "for" is at position i+1
  → AND "money" is at position i+2
  → This is a PHRASE SEARCH — only possible with positions!
──────────────────────────────────────────────────────────────
```

> 💡 **Phrase queries** (like Google's quoted search: `"value for money"`) require positional information. Product search sites like Amazon/Flipkart usually DON'T need this — they're happy with any-order matching.

---

## 🔎 Answering Single-Word Queries

Simple. A single hashmap lookup:

```
QUERY: "awesome"
──────────────────────────────────────────────────────────────

  1. Clean query → stem it → "awesome" (stays the same)
  2. Look up "awesome" in the inverted index hashmap → O(1)
  3. Return: [Doc2]

  TIME COMPLEXITY: O(1) for lookup ✅
  Compare to SQL LIKE '%awesome%': O(n × m) ❌
──────────────────────────────────────────────────────────────
```

---

## 🔎 Answering Multi-Word Queries

For a query like **"woman white dress"** (after cleaning → 3 stemmed words):

```
MULTI-WORD QUERY HANDLING:
──────────────────────────────────────────────────────────────

  INTERPRETATION 1 — AND query (all words must be present):
  → Fetch docs for "woman": [D1, D5, D9, D12, D44...]
  → Fetch docs for "white":  [D1, D3, D9, D22, D44...]
  → Fetch docs for "dress":  [D1, D9, D44, D88...]
  → Take SET INTERSECTION → [D1, D9, D44]
  → Return documents that contain ALL 3 words ✅

  INTERPRETATION 2 — OR query (any word present):
  → Take SET UNION of all three lists
  → Return documents that contain ANY of the words

  INTERPRETATION 3 — Phrase query (exact order):
  → Use positional information
  → Find docs where "woman" is at position i,
    "white" at position i+1, "dress" at position i+2
  → Stricter matching — exact phrase

  WHICH INTERPRETATION TO USE?
  → This is the service layer's responsibility.
  → Elasticsearch provides the raw results.
  → You decide the logic based on your business use case.
──────────────────────────────────────────────────────────────
```

---

# PART 3: TEXT PROCESSING PIPELINE

---

## 🔧 The Full Pipeline Overview

Before building the inverted index, raw text must go through a **cleaning pipeline**. The same pipeline is applied to both **documents when indexing** AND **queries when searching**.

```
TEXT PROCESSING PIPELINE:
──────────────────────────────────────────────────────────────

  Raw Text / Raw Query
       │
       ▼
  ┌────────────────────┐
  │ 1. Stop Word       │  Remove: "the", "a", "is", "at"...
  │    Removal         │
  └────────┬───────────┘
           │
           ▼
  ┌────────────────────┐
  │ 2. Special Char    │  Remove: !, @, #, /, ?, . etc.
  │    Removal         │
  └────────┬───────────┘
           │
           ▼
  ┌────────────────────┐
  │ 3. Stemming /      │  "running" → "run", "dresses" → "dress"
  │    Lemmatization   │
  └────────┬───────────┘
           │
           ▼
  ┌────────────────────┐
  │ 4. Custom Rules    │  Remove abusive/sensitive words,
  │    (Optional)      │  handle abbreviations, synonyms
  └────────┬───────────┘
           │
           ▼
  Cleaned tokens → Build / Query Inverted Index
──────────────────────────────────────────────────────────────
```

> ⚠️ **Critical Rule:** The SAME pipeline must be applied to BOTH documents AND queries. If they differ, the queries will return no results because the indexed tokens and the query tokens won't match.

---

## 🛑 Stop Word Removal

```
WHAT ARE STOP WORDS?
──────────────────────────────────────────────────────────────

  Stop words = very common words that carry almost no meaning.
  Examples: the, a, an, is, at, of, in, on, and, or, I, was...

  WHY REMOVE THEM?
  • "the" alone appears in ~18% of ALL English text
  • Corresponding doc list for "the" → nearly EVERY document
  • Searching "the" is useless: returns everything
  • Wastes enormous amounts of storage and query time

  EXAMPLE — before vs after stop word removal:
  ─────────────────────────────────────────────
  Original: "I ate at this restaurant, food was really nice"
  After SW: "ate restaurant food really nice"

  Original: "The ambience was awesome"  
  After SW: "ambience awesome"
  
  Same information. Much less storage. ✅

  WHAT IS REMOVED BY STOP WORD REMOVAL:
  • Prepositions: in, on, at, by, for, with, about, against
  • Conjunctions: and, or, but, because, so, yet
  • Articles: the, a, an
  • Pronouns: I, you, he, she, it, we, they
  • Common verbs: is, are, was, were, be, been, have, had
──────────────────────────────────────────────────────────────
```

> 💡 **What about searching for stop words?** If a user searches "the", after cleaning the query the word "the" is removed. Since "the" is not in the inverted index, the query returns results based on other words. This is intentional — "the" alone tells us nothing useful.

---

## ✂️ Stemming — Fast but Imperfect

Stemming reduces words to their **root form** using a rule-based if-else ladder. It's extremely fast but not grammatically correct.

```
STEMMING — HOW IT WORKS:
──────────────────────────────────────────────────────────────

  Rule-based system: strip common suffixes
  
  SUFFIX RULES:
  ─ing  →  remove   │  running → runn   (normalized: run)
  ─ed   →  remove   │  escaped → escap  (normalized correctly)
  ─s    →  remove   │  dresses → dress  ✅
  ─tion →  remove   │  nation  → nat    ❌ (broken!)
  ─ion  →  remove   │  lion    → l      ❌ (broken badly!)
  
  EXAMPLE (stemming in action):
  ───────────────────────────────
  "develop"    → "develop"
  "developing" → "develop"   ← both map to same root ✅
  "developer"  → "develop"   ← same root ✅
  
  STEMMING FAILURES (notorious examples):
  ───────────────────────────────────────
  "caring"      → "car"      ❌ (confused with 'car'!)
  "nation"      → "nat"      ❌ (not a real word)
  "lion"        → "l"        ❌ (completely wrong)
  "ration"      → "rat"      ❌ (confused with 'rat')

  VERDICT:
  ✅ Extremely fast (simple if-else ladder → O(L) where L=word len)
  ✅ Good enough for most common words
  ❌ Fails on edge cases, irregular words, ambiguous suffixes
──────────────────────────────────────────────────────────────
```

---

## 🧠 Lemmatization — Smart but Slow

Lemmatization uses an **NLP/ML pipeline** to understand the *meaning* of a word in context before reducing it to its root (lemma).

```
LEMMATIZATION vs STEMMING:
──────────────────────────────────────────────────────────────

  Word: "caring"
  ────────────────────────────────────────────
  Stemming:      "car"         ← WRONG ❌
  Lemmatization: "care"        ← CORRECT ✅
  
  Word: "better"
  ────────────────────────────────────────────
  Stemming:      "better"      ← unchanged (misses the pattern)
  Lemmatization: "good"        ← CORRECT (it's the comparative) ✅

  HOW LEMMATIZATION WORKS:
  1. Create word vectors (ML embedding) for the word in context
  2. Look at previous 5 words and next 5 words (context window)
  3. Determine the grammatical role of the word (verb? noun? adj?)
  4. Look up lemma in a dictionary/morphological database
  5. Return the correct root form
  
  COMPARISON TABLE:
  ┌─────────────────┬──────────────┬──────────────────────────┐
  │   Feature       │  Stemming    │  Lemmatization           │
  ├─────────────────┼──────────────┼──────────────────────────┤
  │ Speed           │ Very fast    │ Very slow (ML pipeline)  │
  │ Accuracy        │ ~80%         │ ~98%                     │
  │ Context-aware?  │ No           │ Yes                      │
  │ Requires ML?    │ No           │ Yes                      │
  │ Used in ES?     │ Yes (default)│ Optional (custom plugin) │
  └─────────────────┴──────────────┴──────────────────────────┘

  INDUSTRY CHOICE: Stemming by default.
  At billions of documents, lemmatization's slowness
  becomes completely unacceptable.
──────────────────────────────────────────────────────────────
```

---

## 🧹 Other Cleaning Steps

```
ADDITIONAL CLEANING (company-specific):
──────────────────────────────────────────────────────────────

  1. SENSITIVE WORD REMOVAL:
     • Hate speech, slurs, dangerous phrases
     • Example: Amazon/YouTube removing slurs from search index
     • Also: terrorist, bomb, kill (in certain contexts)

  2. LANGUAGE NORMALIZATION:
     • British vs American spelling: colour → color
     • These are usually handled by stemming rules

  3. ABBREVIATION EXPANSION:
     • "cat" might be an abbreviation for a product name
     • Company-specific mappings in a hashmap/config

  4. SPECIAL CHARACTER REMOVAL:
     • !, @, #, $, %, ^, &, *, (, ), /
     • Unicode control characters, box-drawing chars
     • Emojis (may keep or remove depending on use case)

  5. MISSPELLING CORRECTION:
     • hashmap of known_misspelling → correct_spelling
     • Or: NFA (Non-deterministic Finite Automaton) for fuzzy match
     • Applied during BOTH indexing and query time

  ⚠️ All these are configurable in Elasticsearch.
     You can bring your own cleaning pipeline.
──────────────────────────────────────────────────────────────
```

---

## 🔃 Applying the Pipeline to Queries Too

This is **critical**. The same pipeline that cleans documents must also clean queries.

```
EXAMPLE: Query "The woman with the white dress"
──────────────────────────────────────────────────────────────

  Raw Query:    "The woman with the white dress"
  
  Step 1 (stop words removed): "woman white dress"
  Step 2 (special chars):      "woman white dress"  (unchanged)
  Step 3 (stemming):           "woman white dress"  (unchanged here)
  
  Final query tokens: ["woman", "white", "dress"]

  WHY ESSENTIAL?
  If query wasn't cleaned but documents were:
  → "the" is NOT in the inverted index (removed from docs)
  → Searching "the" returns nothing ❌
  → "dresses" (unstemmed) won't match "dress" in index ❌
  → System returns WRONG results
──────────────────────────────────────────────────────────────
```

> 💡 **Where does query cleaning happen?** At the backend/service layer — NOT the client side. The client doesn't know about your stemming rules.

---

# PART 4: SCALING WITH SHARDING

---

## 📐 Why We Need Sharding

The inverted index can be **enormous**:

```
SCALE ESTIMATES FOR A LARGE SEARCH INDEX:
──────────────────────────────────────────────────────────────

  Unique words in corpus:
  → English vocabulary alone: ~200k–400k words
  → Including foreign languages: 10s of millions of words
  → Including slang, typos, abbreviations: even more

  Documents in system:
  → Amazon reviews: hundreds of billions
  → logs at large companies: trillions per day

  Per word in index:
  → List of ALL documents that contain that word
  → Each entry: (docId, position) — ~16 bytes minimum
  → A word like "great" could appear in 100 billion docs
  → Storage for "great" alone: ~1.6 TB

  CONCLUSION:
  No single machine can hold this index.
  No single machine can handle the read load.
  → We must SHARD the inverted index.
──────────────────────────────────────────────────────────────
```

---

## ⚖️ CAP Theorem for Search Systems

Before sharding, decide: do we need consistency or availability?

```
CAP THEOREM ANALYSIS FOR FULL-TEXT SEARCH:
──────────────────────────────────────────────────────────────

  STRONG CONSISTENCY would mean:
  → If a document is added, it's immediately reflected in search
  → If a document is deleted/updated, search never shows stale data
  → Every query returns a 100% complete and accurate result set

  EVENTUAL CONSISTENCY means:
  → New documents may take seconds/minutes to appear in search
  → Updated documents may briefly show old content
  → A few documents might be temporarily missing from results

  WHAT DO WE ACTUALLY NEED?
  → If a review is added to Amazon and doesn't show in search
    for 30 seconds: almost nobody notices ✅
  → If a couple of reviews are temporarily invisible: fine ✅
  → The system doesn't need to be transactionally consistent

  VERDICT: Eventual consistency is more than sufficient.
  In fact, even weaker guarantees are often acceptable.
  → Elasticsearch is EVENTUALLY consistent by design.
──────────────────────────────────────────────────────────────
```

---

## 📦 Approach 1 — Document-ID Based Sharding (Recommended)

![Elasticsearch Sharding Architecture](./images/es_sharding_diagram.png)

This is what **Elasticsearch (and Apache Lucene) actually does**.

```
DOCUMENT-ID BASED SHARDING:
──────────────────────────────────────────────────────────────

  N shards are created. Each shard stores documents based on:
  shard_number = hash(document_id) % N

  EACH SHARD has its OWN inverted index, built on its subset of docs.

  Example: 3 shards, 12 docs total:
  
  ┌────────────────────────┐
  │       SHARD A          │
  │  Docs: 1, 4, 7, 10     │
  │  Inverted Index        │
  │  (for docs 1,4,7,10)   │
  └────────────────────────┘
  
  ┌────────────────────────┐
  │       SHARD B          │
  │  Docs: 2, 5, 8, 11     │
  │  Inverted Index        │
  │  (for docs 2,5,8,11)   │
  └────────────────────────┘

  ┌────────────────────────┐
  │       SHARD C          │
  │  Docs: 3, 6, 9, 12     │
  │  Inverted Index        │
  │  (for docs 3,6,9,12)   │
  └────────────────────────┘

  INSERT/UPDATE/DELETE QUERY:
  → hash(doc_id) → go to ONE shard → reindex content
  → Simple. Only 1 shard touched. ✅

  SEARCH QUERY: "woman white dress"
  → Send query to ALL shards in parallel
  → Each shard returns matching docs from ITS dataset
  → Collect (union) all results → return final result
──────────────────────────────────────────────────────────────
```

---

## 🔄 Map Reduce — How Queries Run Across Shards

Elasticsearch uses **Map Reduce** to distribute queries and collect results:

```
MAP REDUCE IN ELASTICSEARCH:
──────────────────────────────────────────────────────────────

  CONCEPT (from functional programming):

  MAP: apply(function, list_of_items)
  → Applies a function to every item in a list
  → In ES: apply(search_query, [Shard_A, Shard_B, Shard_C])
  → Every shard independently executes the query

  REDUCE: combine(results_from_all_shards)
  → Takes all partial results
  → Combines them into a final result
  → In ES: union of all returned document lists

  ──────────────────────────────────────────────────────────

  FLOW:
  Search query → ES Coordinator (Load Balancer)
                        │
          MAP operation: send query to all shards
                 ┌──────┼──────────┐
                 ▼      ▼          ▼
            Shard A   Shard B   Shard C
           (returns  (returns  (returns
           [D1,D9])  [D5,D44]) [D12,D88])
                 │      │          │
          REDUCE operation: collect + union all results
                        │
                        ▼
           Final Result: [D1, D5, D9, D12, D44, D88]

  No duplicate docs possible (each doc lives in ONE shard)
  → Simple concatenation (no deduplication needed) ✅
──────────────────────────────────────────────────────────────
```

---

## ✅ Pros of Document-ID Sharding

```
ADVANTAGES OF DOCUMENT-ID BASED SHARDING:
──────────────────────────────────────────────────────────────

  1. HIGHLY PREDICTABLE LATENCY:
     → Every shard has a RANDOM mix of documents
     → All shards look almost identical in terms of word distribution
     → All shards take roughly the same time to answer a query
     → Performance is HOMOGENEOUS across all shards
     → You can profile once and predict all queries ✅

  2. NO INTERSECTION NEEDED:
     → Each shard already gives you the matching docs
     → Just concatenate results — O(total results)
     → No expensive set intersection at query time ✅

  3. FAULT TOLERANCE WITH GRACEFUL DEGRADATION:
     → If one shard is slow/unresponsive: set a strict timeout
     → Example: "all shards must respond within 20ms"
     → If Shard C doesn't respond in 20ms → skip it
     → Still return results from Shards A and B ✅
     → Users get relevant results even during partial failures
     → (vs word-based: skipping a shard = catastrophically wrong results)

  4. SIMPLE WRITE PATH:
     → Insert = go to ONE shard (hash doc_id → one shard)
     → Delete = go to ONE shard
     → Update = go to ONE shard, reindex

  5. GRACEFUL SCALING:
     → Add more shards? Redistribute documents
     → Same query just fans out to more shards ✅
──────────────────────────────────────────────────────────────
```

---

## 🔡 Approach 2 — Word-Based Sharding

An alternative: each shard owns a group of words and their full document lists.

```
WORD-BASED SHARDING CONCEPT:
──────────────────────────────────────────────────────────────

  Shard 1: words "dress", "class", "design", "elastic"...
  Shard 2: words "woman", "system", "log", "review"...
  Shard 3: words "white", "drink", "cat", "fast"...

  INSERT QUERY for new document:
  → Process doc, extract all unique words
  → Go to EACH shard corresponding to EACH word in the doc
  → Update that shard's entry for the word
  → Writes touch MANY shards (one per word in the document)

  SEARCH QUERY: "woman white dress"
  → Go to Shard 2 (has "woman" → [D1, D3, D6, D8...])
  → Go to Shard 3 (has "white" → [D2, D5, D8, D11...])
  → Go to Shard 1 (has "dress" → [D1, D8, D44...])
  → Take INTERSECTION → [D8] ← documents with ALL 3 words
  
  Better than document sharding? Query touches only 3 shards
  (one per word in query) instead of ALL shards. Seems better!
──────────────────────────────────────────────────────────────
```

---

## ❌ Cons of Word-Based Sharding

```
WHY WORD-BASED SHARDING FAILS IN PRACTICE:
──────────────────────────────────────────────────────────────

  PROBLEM 1: MASSIVE RESULT SETS BEFORE INTERSECTION
  ───────────────────────────────────────────────────
  → Shard for "woman" returns: 20 BILLION document IDs
  → Shard for "white"  returns: 15 BILLION document IDs
  → Shard for "dress"  returns: 3 BILLION document IDs
  
  → Now take intersection of these massive lists
  → Final result: maybe 500 documents
  → ENORMOUS waste: process 38 billion entries to find 500 ❌
  → This is extremely CPU + memory intensive

  PROBLEM 2: UNPREDICTABLE LATENCY
  ──────────────────────────────────
  → If query has a rare word ("supercalifragilistic"):
    that shard returns tiny list → fast query ⚡
  → If query has a common word ("high"):
    that shard returns billions of docs → crawls 🐌
  → Latency is wildly unpredictable based on what words you search

  PROBLEM 3: CANNOT SKIP SLOW SHARDS
  ────────────────────────────────────
  → You NEED all 3 word shards to compute the intersection
  → If "dress" shard times out → you must wait OR return wrong results
  → If you skip it: you return docs with "woman" + "white" 
    (shoes! hair clips! everything except dresses!) → user confused ❌
  → Can't provide the graceful degradation that doc-sharding offers

  PROBLEM 4: WRITE COMPLEXITY
  ─────────────────────────────
  → A document with 200 unique words → touches 200 different shards on insert
  → Every write is a distributed multi-shard write operation
  → Much slower and more complex than doc-ID sharding's single-shard writes

  VERDICT: Word-based sharding sounds clever but fails at scale.
  Document-ID sharding is the industry standard.
──────────────────────────────────────────────────────────────
```

---

## 📉 Zipf's Law — Why Word Sharding Is Structurally Broken

Zipf's Law is a statistical law observed in all natural languages (and most datasets):

```
ZIPF'S LAW:
──────────────────────────────────────────────────────────────

  If the most frequent word appears N times,
  then the k-th most frequent word appears N/k times.

  Rank 1  (most frequent — "the"):  N occurrences
  Rank 2:                            N/2 occurrences
  Rank 3:                            N/3 occurrences
  ...
  Rank k:                            N/k occurrences

  This creates an extreme distribution:
  ┌──────────────────────────────────────────────────┐
  │ ████████████████████████████████  "the"          │
  │ ████████████████  "of"                           │
  │ ████████████  "and"                              │
  │ █████████  "to"                                  │
  │ ██  "awesome"                                    │
  │ █   "restaurant"                                 │
  │ .   "supercalifragilistic"                       │
  └──────────────────────────────────────────────────┘

  WHY THIS BREAKS WORD SHARDING:
  → Whichever shard contains "great" or "good" is MASSIVELY overloaded
  → Even after stop word removal, many common words remain
  → These words appear in billions of docs
  → Their shard becomes a hot spot — impossible to balance ❌

  Document-ID sharding avoids this entirely:
  → Documents are assigned uniformly by hash of doc ID
  → No shard is overloaded by popular words ✅
──────────────────────────────────────────────────────────────
```

> ⚠️ **Fun Fact:** Zipf's Law holds true even for completely random generated data. It's a universal statistical phenomenon, not just a language artifact.

---

# PART 5: REPLICATION & FAULT TOLERANCE

---

## 🔁 Elasticsearch Replication Architecture

Sharding handles capacity. Replication handles **fault tolerance** and **availability**.

```
ELASTICSEARCH REPLICATION MODEL:
──────────────────────────────────────────────────────────────

  Parameters (set ONCE at cluster creation — cannot change later!):
  → M = Number of shards
  → R = Replication factor (e.g., R=2 → 1 primary + 1 replica)
  → N = Number of server nodes

  Total data units = M × R
  Each server stores M × R / N shards/replicas

  EXAMPLE: M=3 shards, R=2 (1 master + 1 replica), N=3 nodes
  Total data units = 3 × 2 = 6

  Node 1 holds: [Shard A - PRIMARY], [Shard B - REPLICA]
  Node 2 holds: [Shard B - PRIMARY], [Shard C - REPLICA]
  Node 3 holds: [Shard C - PRIMARY], [Shard A - REPLICA]

  ┌──────────────────────────────────────────────────┐
  │  Node 1          │  Node 2          │  Node 3    │
  │  Shard A (P) ✅  │  Shard B (P) ✅  │  Shard C(P)│
  │  Shard B (R) 🔁  │  Shard C (R) 🔁  │  Shard A(R)│
  └──────────────────────────────────────────────────┘
  
  (P) = Primary/Master copy
  (R) = Replica copy
──────────────────────────────────────────────────────────────
```

---

## 🛡️ Master-Replica Placement Rules

```
ELASTICSEARCH PLACEMENT GUARANTEE:
──────────────────────────────────────────────────────────────

  RULE: The primary and all replicas of the SAME SHARD
        must NEVER be on the same server node.

  WHY?
  If Shard A primary and Shard A replica were both on Node 1:
  → Node 1 crashes → BOTH copies of Shard A are lost ❌
  → Replication factor = 2 but we lost BOTH copies

  WITH THE RULE ENFORCED:
  → Shard A primary (Node 1) + Shard A replica (Node 3)
  → Node 1 crashes → Shard A replica on Node 3 survives ✅
  → Node 3 replica is promoted to primary automatically ✅
  → System continues serving queries ✅

  REPLICATION SYNC:
  → Writes go to PRIMARY only
  → Primary syncs to replica asynchronously
  → Since ES is eventually consistent: async replication is fine ✅
  → Reads can go to EITHER primary or replica
  → (Replicas serve reads to distribute read load)

  ⚠️ ELASTICSEARCH LIMITATION:
  → You cannot change M (shard count) or R (replication factor)
     after the cluster is created without rebuilding the entire index.
  → Plan your cluster size carefully upfront.
──────────────────────────────────────────────────────────────
```

---

# PART 6: RANKING & RELEVANCE

---

## 🏆 Beyond Matching — Why Ranking Matters

Matching finds **all** documents. Ranking decides **which order** to show them.

```
THE RANKING PROBLEM:
──────────────────────────────────────────────────────────────

  Query: "quick"
  Matching returns:
  → Doc 1: "fire quick please quick call quick service"  (3 occurrences)
  → Doc 2: "quick brown fox"                             (1 occurrence)
  → Doc 3: "quick pain relief"                           (1 occurrence)

  All match. But which is most RELEVANT?
  → Doc 1: 3 occurrences → likely more about "quick"?
  → Or just padded text?

  For e-commerce, extra signals apply:
  → Title match > description match > review match
  → Recent reviews > old reviews
  → Verified purchases > unverified

  Elasticsearch provides TF-IDF scoring out of the box.
  You can add custom ranking signals on top.
──────────────────────────────────────────────────────────────
```

---

## 📊 TF-IDF — Term Frequency × Inverse Document Frequency

```
TF-IDF SCORING:
──────────────────────────────────────────────────────────────

  TERM FREQUENCY (TF):
  → How often does the word appear IN THIS document?
  → TF(word, doc) = count of word in this doc

  INVERSE DOCUMENT FREQUENCY (IDF):
  → How common is this word ACROSS ALL documents?
  → The rarer the word, the more informative it is
  → IDF(word) = 1 / (number of docs containing this word)
  → (in practice: log(N / df) + 1, where N=total docs, df=doc freq)

  FINAL SCORE:
  → score(doc, query_word) = TF × IDF

  ─────────────────────────────────────────────────────────

  EXAMPLE — Query: "quick"

  Corpus = 5 Documents. "quick" appears in D1, D2, D3.
  Document frequency for "quick" = 3
  IDF("quick") = 1/3

  Doc 1: "quick" appears 3 times → TF = 3
         Score = 3 × (1/3) = 1.0  ← HIGHEST

  Doc 2: "quick" appears 1 time  → TF = 1
         Score = 1 × (1/3) = 0.33

  Doc 3: "quick" appears 1 time  → TF = 1
         Score = 1 × (1/3) = 0.33

  Doc 1 ranks #1. Makes sense — most mentions of "quick".

  ─────────────────────────────────────────────────────────

  WHY IDF MATTERS — Multi-word queries:
  Query: "song supercalifragilistic"

  "song" → appears in billions of docs → IDF very low
  "supercalifragilistic" → appears in maybe 10 docs → IDF very high

  → Documents with "supercalifragilistic" get HIGH scores
  → Documents that only have "song" get LOW scores
  → The rare, specific word dominates the ranking ✅
  → The common, uninformative word is automatically down-weighted ✅
──────────────────────────────────────────────────────────────
```

---

## 🎯 Other Ranking Signals

Beyond TF-IDF, real production systems use many other signals:

```
ADDITIONAL RANKING SIGNALS (Industry):
──────────────────────────────────────────────────────────────

  FIELD IMPORTANCE:
  → Document field weights (configurable in ES)
  → Title match:       weight = 5.0  ← high importance
  → Description match: weight = 2.0
  → Review text match: weight = 1.0  ← lower importance
  
  TEMPORAL SIGNALS:
  → Newer documents get slightly higher scores (recency boost)
  → Trending topics get a boost

  USER SIGNALS:
  → Click-through rate: docs that users CLICK get ranked higher
  → Dwell time: docs that users READ FULLY rank higher
  → Purchase rate (for e-commerce)
  → Rating / review scores

  BUSINESS RULES:
  → Sponsored / promoted products always appear first
  → In-stock products rank above out-of-stock
  → Regional availability boosts (show local results)

  ML-BASED RANKERS:
  → Learning-to-Rank (LTR): train a model on click data
  → BM25: improved version of TF-IDF used in modern systems
  → BERT-based semantic ranking (understand meaning, not just words)

  EXAMPLE — Slack's Ranking (from engineering blog):
  → User-created content in subscribed channels ranks higher
  → Messages from people you interact with frequently rank higher
  → Recent messages rank higher than old messages
──────────────────────────────────────────────────────────────
```

---

## ✏️ Handling Misspellings & Synonyms

```
MISSPELLING HANDLING:
──────────────────────────────────────────────────────────────

  APPROACH 1 — Static Misspelling Dictionary:
  → Maintain a hashmap: { bad_spelling → correct_spelling }
  → "documnet" → "document"
  → "recieve"  → "receive"
  → "teh"      → "the"
  → Apply DURING cleaning pipeline before indexing/querying
  → PROS: O(1) lookup, simple to implement
  → CONS: Only catches known, pre-catalogued misspellings

  APPROACH 2 — NFA (Non-deterministic Finite Automaton):
  → Build a state machine for every word in vocabulary
  → State machine accepts not just the word, but all its
    1-character deletions, insertions, transpositions, substitutions
  → "documnet" — transposition of 'm' and 'e' → accepted ✅
  → More powerful than hashmap, handles arbitrary misspellings
  → CONS: Complex to implement and maintain

──────────────────────────────────────────────────────────────

  SYNONYM HANDLING:
  ──────────────────────────────────────────────────────────────

  APPROACH — Synonym Folding via Stemming Config:
  → Configure synonyms as a group with one canonical root
  → "good", "great", "awesome", "excellent" → all map to "good"
  → At index time: "awesome" in a doc → stored as "good"
  → At query time: "great" → stemmed to "good" → matches! ✅

  EXAMPLE in Elasticsearch config:
  synonyms: [
    "great, awesome, fantastic => good",
    "purchase, buy, order, checkout => buy",
    "cheap, affordable, budget => cheap"
  ]

  PROS: Automatic semantic matching without ML
  CONS: Must manually curate — misses context (not "great" as in "Great Wall")
──────────────────────────────────────────────────────────────
```

---

# PART 7: SUMMARY & INTERVIEW PREP

---

## 🛠️ Elasticsearch vs Other Solutions

| Solution | Type | Notes |
|----------|------|-------|
| **Apache Lucene** | Open Source | Core library; Elasticsearch is built on top of Lucene |
| **Apache Solr** | Open Source | Also built on Lucene; older, config-file-heavy |
| **Elasticsearch** | Proprietary (free tier) | Industry standard; REST API; scalable cluster mode |
| **OpenSearch** | Open Source | AWS fork of Elasticsearch |
| **Algolia** | Proprietary (paid) | Managed search-as-a-service; very fast; focus on UX |
| **Azure Cognitive Search** | Proprietary | Microsoft's managed search |
| **PostgreSQL FTS** | Open Source | Works for small to medium scale; not horizontally scalable |
| **Loki** | Open Source | Grafana's log aggregation and search |
| **Kibana** | Open Source | Dashboard UI on top of Elasticsearch |

---

## 🏗️ Complete Architecture Diagram

```
FULL ELASTICSEARCH ARCHITECTURE:
──────────────────────────────────────────────────────────────

  DATA INGESTION PATH (Write/Index):
  ─────────────────────────────────

  New Document (e.g., Amazon review)
       │
       ▼
  [Source DB — MongoDB/DynamoDB]
       │  change stream / event
       ▼
  [Kafka / Message Queue]         ← async decoupling
       │
       ▼
  [Indexer Service]
  1. Fetch document text
  2. Run cleaning pipeline:
     → Stop word removal
     → Stemming
     → Custom rules
  3. TokensSend to Elasticsearch API
       │
       ▼
  [Elasticsearch Cluster]
  → Coordinator node receives request
  → Routes to correct shard: hash(doc_id) % M
  → Shard updates its inverted index
  → Shard replicates to replica node (async)

  ─────────────────────────────────────────────────────────

  QUERY/SEARCH PATH (Read):
  ──────────────────────────

  User types search query "woman white dress"
       │
       ▼
  [API Gateway / Load Balancer]
       │
       ▼
  [Search Service Layer]
  1. Receive raw query string
  2. Run SAME cleaning pipeline on query:
     → Remove stop words
     → Stem tokens
  3. Send cleaned tokens to Elasticsearch
       │
       ▼
  [Elasticsearch Coordinator Node]
  → MAP: Fan out cleaned query to ALL shards in parallel
       │
       ├──► Shard A → runs inverted index lookup → returns doc IDs
       ├──► Shard B → runs inverted index lookup → returns doc IDs
       └──► Shard C → runs inverted index lookup → returns doc IDs
       │
  → REDUCE: Collect all doc IDs (union / concatenate)
  → RANK: Apply TF-IDF scores → sort by relevance
  → Return top-K results to Search Service
       │
       ▼
  [Search Service] → return ranked document IDs to API
       │
       ▼
  [Source DB] → fetch full document details from source DB
       │
       ▼
  User sees ranked results ✅
──────────────────────────────────────────────────────────────
```

---

## 📋 Quick Reference Cheatsheet

```
ELASTICSEARCH QUICK REFERENCE:
══════════════════════════════════════════════════════════════

  CORE CONCEPT:
  Inverted Index = hashmap { word → [(docId, position), ...] }

  CLEANING PIPELINE (ORDER MATTERS):
  1. Stop word removal  (the, a, is, at, and, of...)
  2. Special char removal (!, @, #, /, ?...)
  3. Stemming (running→run) OR Lemmatization (caring→care)
  4. Custom rules (synonyms, misspellings, sensitive words)
  Apply pipeline to BOTH documents and queries.

  SHARDING:
  Key:  hash(document_id) % num_shards → shard number
  NOT: word-based sharding (Zipf's law breaks it)
  Write: touches 1 shard (fast)
  Read:  fans out to ALL shards in parallel (predictable latency)

  QUERY EXECUTION:
  Map:    send query to all shards simultaneously
  Reduce: collect + union results from all shards
  Rank:   sort by TF-IDF (or BM25/custom) score
  Timeout: set strict timeout; ignore slow shards gracefully

  REPLICATION:
  Primary + R replicas per shard
  Rule: same shard's copies MUST be on DIFFERENT nodes
  ES is eventually consistent (async replication is fine)
  Writes go to PRIMARY only; reads can go to any replica

  CAP THEOREM:
  Elasticsearch = AP system (Available + Partition-tolerant)
  Consistency = eventual (acceptable for search use cases)

  TF-IDF SCORING:
  TF = occurrences of word in THIS document
  IDF = 1 / (documents containing this word)
  Score = TF × IDF  (higher = more relevant)
  Rare words carry MORE weight; common words less weight

  LIMITATIONS OF ELASTICSEARCH:
  - Shard count (M) cannot be changed after cluster init
  - Replication factor (R) cannot be changed after cluster init
  - Full cluster rebuild required to change either setting
══════════════════════════════════════════════════════════════
```

---

## 🎯 Interview Questions & Answers

> Questions are organized by difficulty. Each answer is written the way you'd explain it in a real system design or engineering interview.

---

### 🟢 TIER 1 — Basic Concepts (Entry Level / SE1–SE2)

---

**Q1. What is full-text search? How is it different from a normal database query?**

> **Answer:**
> Full-text search means finding all documents that contain a given word or phrase *anywhere* inside their content — not just in a specific column or as a prefix match.
>
> A normal database query does **exact match** (`WHERE id = 42`) or **prefix match** (`LIKE 'value%'`), both of which work with a sorted B+ tree index. But the moment you search for something that could appear *anywhere* in the text (`LIKE '%value for money%'`), the index is useless — the DB must scan every character of every row, which is O(n × m) and completely unscalable at billions of documents.
>
> Full-text search solves this with a specialized data structure — the **inverted index** — that maps each word to all documents containing it, giving O(1) lookup per word.

---

**Q2. What is an inverted index? Give a real-world analogy.**

> **Answer:**
> An inverted index is a **hashmap where the key is a word and the value is the list of all documents that contain that word**, optionally with the word's position inside each document.
>
> The real-world analogy is the **glossary at the back of a textbook**. The table of contents at the front maps *chapters → topics* (that's the forward index). The glossary at the back maps *terms → page numbers* (that's the inverted index). When you want to find every page that discusses "consistent hashing", you go to the glossary — not the table of contents.
>
> In Elasticsearch, instead of "pages" we have "document IDs", and instead of the glossary being manually curated, it's automatically built from every word in every document.

---

**Q3. What are stop words? Why do we remove them?**

> **Answer:**
> Stop words are extremely common words in a language that carry almost no meaningful information: *the, a, an, is, at, of, in, on, and, or, I, was, were…*
>
> We remove them because:
> 1. **They pollute the index** — the word "the" alone appears in ~18% of all English text. Its entry in the inverted index would point to nearly *every* document — making it useless for narrowing search results.
> 2. **They waste storage** — storing billions of (docId, position) pairs for "the" wastes massive disk space.
> 3. **They don't affect meaning** — "ate restaurant food nice" contains the same semantic information as "I ate at this restaurant, food was really nice".
>
> The same pipeline is applied to search queries, so if someone searches "the dress", the "the" is silently dropped and only "dress" is looked up.

---

**Q4. What is stemming? Give examples of where it works and where it fails.**

> **Answer:**
> Stemming is the process of reducing a word to its root form using a rule-based system (an if-else ladder of suffix-stripping rules). It's intentionally simple and fast.
>
> **Works well:**
> - "developing" → "develop" ✅
> - "developer" → "develop" ✅
> - "dresses" → "dress" ✅
> - "escaped" → "escap" ✅ (normalized correctly)
>
> **Fails:**
> - "caring" → "car" ❌ (strips "-ing" blindly, confused with "car")
> - "nation" → "nat" ❌ ("-ion" is not a suffix here)
> - "lion" → "l" ❌ (completely broken)
> - "ration" → "rat" ❌ (confused with "rat")
>
> Stemming is O(word_length), extremely fast, and good enough for ~80% of real-world cases. That's why Elasticsearch uses it by default despite its flaws.

---

**Q5. What is TF-IDF? How does it rank documents?**

> **Answer:**
> TF-IDF stands for **Term Frequency × Inverse Document Frequency**. It's a scoring formula that measures how relevant a document is for a given query word.
>
> - **TF (Term Frequency):** How many times does the query word appear *in this document*? More occurrences = more relevant.
> - **IDF (Inverse Document Frequency):** How rare is this word across *all documents*? The rarer the word, the more informative it is. IDF = log(N / df), where N = total docs, df = docs containing the word.
>
> **Score = TF × IDF**
>
> **Example:** Query = "quick"
> | Document | TF | IDF (3 docs have "quick") | Score |
> |----------|----|--------------------------|-------|
> | "quick quick quick call" | 3 | 1/3 | **1.0** ← ranked #1 |
> | "quick brown fox" | 1 | 1/3 | 0.33 |
> | "quick relief" | 1 | 1/3 | 0.33 |
>
> **Why IDF matters:** If someone searches "the dress", the word "the" has an IDF near zero (appears in every document), so it contributes almost nothing to the score. The word "dress" dominates. This automatically down-weights common words without needing to explicitly remove them.

---

**Q6. Why must the text cleaning pipeline be applied to both documents AND queries?**

> **Answer:**
> Because the inverted index stores **stemmed, cleaned tokens** — not the original words. If a document says "dresses" and the index stores the stemmed form "dress", then the query "dresses" must *also* be stemmed to "dress" before lookup. Otherwise, you'd search for "dresses" in the index, find no entry, and return zero results — even though thousands of documents are about dresses.
>
> Similarly, if the query contains stop words like "the", and those were removed from the index, searching for "the" would return nothing. Applying the same pipeline to the query silently drops it.
>
> **Rule:** Whatever transformation you apply to the document text before indexing, apply the *exact same* transformation to the query before searching.

---

**Q7. What is the difference between stemming and lemmatization?**

> **Answer:**
>
> | Feature | Stemming | Lemmatization |
> |---------|---------|---------------|
> | Method | Rule-based suffix stripping (if-else ladder) | NLP/ML pipeline using context |
> | Speed | Very fast — O(word length) | Very slow — requires neural network inference |
> | Accuracy | ~80% | ~98% |
> | Context-aware | No | Yes |
> | Example (correct) | "dresses" → "dress" ✅ | "better" → "good" ✅ |
> | Example (wrong) | "caring" → "car" ❌ | "caring" → "care" ✅ |
>
> **When to use what:** In production at scale (billions of documents), stemming is the standard choice — it's fast enough, and the errors are acceptable. Lemmatization is used when accuracy is critical and you can afford the ML inference cost (e.g., a small legal document search system).

---

### 🟡 TIER 2 — Intermediate (SE2–SE3)

---

**Q8. Why can't you use a SQL LIKE query with a leading `%` effectively? What's the alternative?**

> **Answer:**
> A SQL B+ tree index stores rows sorted by the indexed column. For a `LIKE 'value%'` query (prefix match), you can do binary search: find the first row that starts with "value" in O(log n). This is efficient.
>
> But for `LIKE '%value for money%'`, the word could appear at position 0, position 50, or position 500 in the text. There's no way to binary search for that — you don't know where to start. The database is forced to scan every single row character by character: O(n × m) where n = rows, m = avg text length. With billions of rows, this is completely impractical.
>
> **The alternative:** Build an inverted index. Pre-process all text, extract every word, and store a mapping of word → documents. Now any word lookup is O(1) instead of O(n × m).

---

**Q9. What positional information is stored in an inverted index and why?**

> **Answer:**
> Beyond just the document ID, the inverted index stores the **word position** (index of the word within the document):
> ```
> "was" → [
>     { docId: 1, position: 6 },
>     { docId: 2, position: 2 },
>     { docId: 3, position: 1 }
> ]
> ```
>
> **Why positions matter — phrase search:**
> If the query is "value for money" and you want documents where these words appear *in this exact order and consecutively*, you need positions. You'd look for all documents where "value" is at position i, "for" at i+1, and "money" at i+2. Without positions, you'd only know these words all exist in the document — not whether they're adjacent.
>
> Google's quoted search (`"value for money"`) uses this. Amazon and Flipkart typically don't require exact ordering — they use AND/OR matching without positions.

---

**Q10. Describe the two approaches to sharding an inverted index. Which does Elasticsearch use and why?**

> **Answer:**
> **Approach 1 — Document-ID Sharding (what Elasticsearch uses):**
> Each shard owns a random subset of documents (by hashing the doc ID). Every shard maintains its own local inverted index over its documents.
> - Write: route to ONE shard (by hash) — simple and fast.
> - Read: fan out to ALL shards in parallel, collect (union) results.
> - Advantage: predictable latency (all shards are homogeneous), graceful degradation (can skip slow shards).
>
> **Approach 2 — Word-Based Sharding:**
> Each shard owns a subset of words and all documents that contain them.
> - Write: touches one shard per unique word in the document (hundreds of shards per write).
> - Read: touches one shard per query word, then requires expensive intersection.
> - Problems: massive intersection over billions of entries, unpredictable latency (Zipf's law causes hot spots), can't skip any shard without corrupting results.
>
> **Why Elasticsearch chose doc-ID sharding:** The system is read-heavy. Writes are infrequent. Making reads predictable and fault-tolerant is the priority. Word-based sharding makes reads expensive, unpredictable, and non-degradable.

---

**Q11. What is Map Reduce? Explain how Elasticsearch uses it.**

> **Answer:**
> Map Reduce is a programming paradigm from functional programming adopted for distributed computing. It has two operations:
>
> - **Map:** Apply the same function independently to every item in a collection. Each item can be processed in parallel.
> - **Reduce:** Combine the outputs of the Map step into a single result (using an accumulator + combiner function).
>
> **In Elasticsearch:**
> 1. **MAP step:** The coordinator node receives a search query and sends it to ALL shards simultaneously. Each shard independently runs the query against its own local inverted index and returns a list of matching document IDs.
> 2. **REDUCE step:** The coordinator collects the results from all shards and concatenates them (since each document lives in exactly one shard, there are no duplicates — simple union/concatenation is enough).
>
> This is why search latency in doc-ID sharding is *not* affected by adding more shards — all shards run in parallel. The total latency is determined by the *slowest shard*, not the number of shards.

---

**Q12. Elasticsearch is eventually consistent. What does that mean in practice for search?**

> **Answer:**
> Eventual consistency in Elasticsearch means:
> 1. When you index a new document, it won't appear in search results *immediately*. There's a small delay (configurable, default ~1 second) before the new document's tokens are added to the inverted index on disk and replicated.
> 2. If a document is updated or deleted, search results may briefly reflect the old version.
> 3. Replicas may lag behind the primary momentarily.
>
> **Why this is acceptable for search:**
> - If a review posted on Amazon takes 30 seconds to show in search, that's invisible to the user.
> - If a deletion takes a few seconds to propagate, a stale result briefly appearing causes no data integrity issue.
> - Search systems don't need transactional guarantees.
>
> **Contrast with strong consistency** (what Zookeeper provides, for example): every read is guaranteed to reflect the latest write. This would be required if, say, a user was doing a financial transaction. For search, it's overkill and would hurt availability and latency.

---

**Q13. What is Zipf's Law? Why does it make word-based sharding fail?**

> **Answer:**
> Zipf's Law states that in any natural language corpus, the k-th most frequent word occurs approximately 1/k times as often as the most frequent word. The top 10 words account for a disproportionately huge fraction of all word occurrences.
>
> **Why it breaks word sharding:**
> Imagine assigning each word to a shard by hash. The shard that happens to get the word "good" might be responsible for storing 50 billion document IDs (one per document containing "good"). The shard that gets "supercalifragilistic" stores maybe 5.
>
> After stop word removal, the extreme tail of frequent words is trimmed — but words like "good", "new", "great", "product" still appear in billions of documents. The shards owning them become permanent hotspots: overloaded with data, overloaded with query traffic, and impossible to balance.
>
> No rebalancing strategy solves this because Zipf's distribution is inherent in the data, not an accident of bad key distribution.

---

**Q14. How does Elasticsearch ensure no two copies of the same shard land on the same server?**

> **Answer:**
> When you create an Elasticsearch cluster, you set the number of shards (M) and the replication factor (R). Elasticsearch's built-in **shard allocation mechanism** automatically places primary and replica shards across nodes following one key rule: **a node must never hold both the primary and any replica of the same shard**.
>
> **Why:** If both copies were on the same node and the node crashed, both would be lost simultaneously — defeating the entire purpose of replication. The rule guarantees that a single node failure can destroy at most *one* copy of any shard, leaving the other copy (on a different node) intact to serve as the new primary.
>
> In practice, Elasticsearch uses awareness attributes (rack awareness, zone awareness) to extend this further — ensuring copies are on different physical racks or availability zones for maximum resilience.

---

### 🔴 TIER 3 — Advanced (SE3–Senior)

---

**Q15. When a search query arrives at Elasticsearch, walk through the entire execution path — from raw query string to ranked results.**

> **Answer:**
>
> **Step 1 — Query received at service layer:**
> The user's raw query string ("The woman with the white dress") arrives at the backend Search Service.
>
> **Step 2 — Query cleaning (same pipeline as indexing):**
> - Stop words removed: "woman white dress"
> - Special characters removed (none here)
> - Stemmed: ["woman", "white", "dress"]
>
> **Step 3 — Fan out to all shards (MAP):**
> The Elasticsearch coordinator sends the cleaned tokens to all M shards in parallel.
>
> **Step 4 — Per-shard inverted index lookup:**
> Each shard looks up "woman", "white", and "dress" in its local inverted index. It finds all doc IDs common to all three postings lists (AND query = intersection). Returns its local matching document set.
>
> **Step 5 — Collect results (REDUCE):**
> Coordinator receives partial result lists from all shards. Since each doc lives in exactly one shard, it simply concatenates all lists. Applies a strict timeout (e.g., 20ms) — shards that don't respond in time are skipped.
>
> **Step 6 — Ranking:**
> TF-IDF scores (precomputed or computed at query time) are applied to sort the results by relevance. Top-K documents are selected.
>
> **Step 7 — Fetch full document data:**
> The Search Service takes the ranked document IDs and queries the source database (MongoDB/DynamoDB) to fetch the actual document content for display.
>
> **Step 8 — Return to user.**

---

**Q16. How does word-based sharding handle a case where a query shard doesn't respond? Compare this to document-ID sharding.**

> **Answer:**
>
> **Word-based sharding — catastrophic behavior on shard failure:**
> If the query is "woman white dress" and the "dress" shard doesn't respond:
> - You *cannot* compute the correct intersection without the "dress" posting list.
> - Option A: Wait indefinitely (completely unacceptable — latency explodes).
> - Option B: Skip the "dress" shard and return docs containing only "woman" + "white" — now you're showing shoes, hair accessories, anything white — completely wrong results.
> - There is no graceful option. The query either hangs or returns fundamentally incorrect results.
>
> **Document-ID sharding — graceful degradation:**
> If Shard C doesn't respond (set a 20ms timeout and move on):
> - You still have the results from Shards A and B.
> - Those results are valid — they just represent roughly 2/3 of the corpus.
> - The user still gets many relevant results. The missing results are random, not systematically biased.
> - You can even transparently retry or fall back to replicas.
>
> This graceful degradation property is one of the strongest arguments for document-ID sharding in a real production system.

---

**Q17. You need to support phrase search ("value for money" must appear as an exact phrase). How does Elasticsearch handle this?**

> **Answer:**
> Phrase search is solved using **positional information** stored in the inverted index.
>
> **During indexing:**
> For every (word, document) pair, store the word's position in the document:
> ```
> "value"  → [{ docId: D5, position: 12 }, { docId: D9, position: 4 }, ...]
> "for"    → [{ docId: D5, position: 13 }, { docId: D9, position: 1 }, ...]
> "money"  → [{ docId: D5, position: 14 }, { docId: D9, position: 7 }, ...]
> ```
>
> **During querying:**
> 1. Fetch all docs containing "value" (with positions).
> 2. Fetch all docs containing "for" (with positions).
> 3. Fetch all docs containing "money" (with positions).
> 4. Intersect on doc IDs.
> 5. For remaining docs, verify: is there a position i in the doc where "value" is at i, "for" at i+1, "money" at i+2?
> 6. Only return docs that pass this positional check.
>
> **Cost:** More storage (must store all positions, including duplicates for repeated words) and more query-time computation. This is why phrase search is slower than simple keyword search and not all platforms enable it (it's enabled in Google, not typically in Amazon product search).

---

**Q18. How would you handle misspelled queries at scale? What approaches exist?**

> **Answer:**
> Two main approaches:
>
> **Approach 1 — Static Misspelling Dictionary:**
> Build a hashmap `{ misspelling → correct_spelling }` from known common mistakes:
> `{ "accomodation" → "accommodation", "recieve" → "receive", ... }`
> Apply this during the cleaning pipeline on both documents and queries.
> - Pros: O(1) lookup, simple to implement, zero latency.
> - Cons: Only catches pre-catalogued misspellings; can't handle novel typos.
>
> **Approach 2 — NFA (Non-deterministic Finite Automaton):**
> For each word in the vocabulary, build a state machine that also accepts all words within edit distance 1 or 2 (transpositions, insertions, deletions, substitutions). Feed the raw query word through the NFA to find the canonical vocabulary word it matches.
> - Pros: Handles arbitrary (not just pre-catalogued) misspellings.
> - Cons: Complex to build and maintain; slower than hashmap lookup.
>
> **Approach 3 — Frequency-Based Correction (industry standard):**
> Maintain a frequency table of all correctly searched words. If a query word is rare (low frequency), check if a common word is within edit distance 1–2 and suggest it ("Did you mean…?"). This is what Google does. It exploits the fact that misspellings are rare in the frequency table, while correct spellings are common.

---

**Q19. Why can't you change the number of shards in an Elasticsearch cluster after creation? What are the implications?**

> **Answer:**
> In Elasticsearch, the number of primary shards (M) is fixed at index creation time and *cannot be changed without rebuilding the entire index*. Here's why:
>
> **Technical reason:** Documents are routed to shards using:
> ```
> shard_number = hash(document_id) % M
> ```
> If you change M, every document's assigned shard changes. A document that was on Shard 2 of 5 would now be on a different shard in the new 7-shard layout. There's no incremental migration possible — the entire index must be reindexed from scratch.
>
> **Implications for system design:**
> - You must **over-provision shards at cluster creation**. It's better to create 10 shards now and not fill them all immediately than to hit an upper bound in 6 months.
> - Changing shards requires: creating a new index, reindexing all data, switching aliases, then deleting the old index. This is expensive for billions of documents.
> - Modern solutions (like Elasticsearch 7.x's "shrink" and "split" APIs) allow limited changes but still require significant effort.
>
> **Interview takeaway:** This is a well-known limitation of Elasticsearch. When designing a cluster, plan for 2–3x expected data volume to avoid painful reindexing.

---

**Q20. How does replication in Elasticsearch differ from typical master-slave database replication?**

> **Answer:**
> In typical master-slave DB replication, there's usually one master node and N slave nodes. All writes go to the master; slaves receive replicated writes and handle reads.
>
> Elasticsearch replication has a more nuanced topology:
>
> 1. **Multiple primaries, not one master:** Each shard has its own primary copy. If you have 5 shards and 3 replicas, there are effectively **5 different "masters"** (one per shard), distributed across the cluster nodes.
>
> 2. **Node-level parallelism:** A single node can host multiple shards — both primaries for some and replicas for others. There's no single "master node" for data; there's a separate "cluster master" node just for cluster metadata/coordination.
>
> 3. **Placement constraint:** Elasticsearch guarantees no primary and its replica ever share a node. This is similar to a master-slave setup but enforced at the shard level, not the cluster level.
>
> 4. **Async replication, eventual consistency:** Writes go to the primary shard and are asynchronously replicated to replicas. Reads can be served from any copy (primary or replica), which allows load distribution. This is the same as typical async master-slave replication.

---

### 🔵 TIER 4 — System Design (Senior / Staff)

---

**Q21. Design a full-text log search system for a company with 500 microservices generating 100GB of logs per day. Support queries like "NullPointerException service=payment".**

> **Answer (structured):**
>
> **Requirements:**
> - Write: ~100GB/day = ~1.2 MB/sec of log data continuous ingestion
> - Read: engineers querying logs for debugging (low QPS, high value)
> - Retention: last 30 days (3TB total)
> - Query type: keyword + field-specific search ("service=payment")
>
> **Architecture:**
> ```
> Services → Fluentd/Logstash (agent) → Kafka → Indexer → Elasticsearch
>                                                              │
>                                                          Kibana UI
> ```
>
> **Components:**
> 1. **Log shipping:** Each microservice runs a log agent (Fluentd/Filebeat) that tails log files and ships structured JSON logs to Kafka. Kafka decouples the burst of logs from the indexing speed.
> 2. **Indexer Service:** Consumes from Kafka, runs the cleaning pipeline (no stop words for logs — error names and stack traces are meaningful), indexes into Elasticsearch.
> 3. **Elasticsearch Cluster:** 
>    - Shard count: 3TB / (target 30–50GB per shard) ≈ 60–100 shards
>    - Replication factor: 2 (1 primary + 1 replica) for fault tolerance
>    - Daily index rotation (time-based indexing) for easier retention management
> 4. **Kibana:** Dashboard + query UI on top of Elasticsearch for engineers
>
> **Cleaning pipeline for logs:** Minimal. Preserve field names, stack traces, error codes. No aggressive stop word removal (words like "null" matter). Use structured JSON fields (level, service, message, timestamp) with field-weighted search.
>
> **Retention:** Use ILM (Index Lifecycle Management) in Elasticsearch to automatically delete indices older than 30 days.

---

**Q22. Amazon has 10 billion product reviews in multiple languages. Design a review search system. How do you handle multilingual search?**

> **Answer:**
>
> **Core Design:**
> - Source DB: MongoDB (document store for reviews)
> - Change Stream → Kafka → Indexer → Elasticsearch
> - Each review = one document with fields: `productId`, `rating`, `language`, `title`, `body`, `date`
>
> **Multilingual handling:**
>
> The key challenge is that stop words, stemming rules, and character sets differ by language.
>
> 1. **Language detection:** After receiving the review, run a lightweight language detection model (e.g., `langdetect` library). Tag the review with its detected language.
>
> 2. **Per-language analyzers:** In Elasticsearch, configure different **analyzers** per language. An English analyzer uses English stop words + Porter stemmer. A French analyzer uses French stop words + French stemmer. Japanese uses a morphological analyzer (MeCab). Apply the correct analyzer during indexing based on the detected language.
>
> 3. **Per-language sub-indexes or index aliases:** Option A: separate ES indices per language (es_reviews_english, es_reviews_hindi…). Option B: single index with per-field language-specific analysis. Both work; separate indices are easier to manage.
>
> 4. **Query-side language detection:** Apply the same language detection + appropriate analyzer to the search query.
>
> **Ranking:**
> - TF-IDF base score
> - Field weights: title match > body match
> - Rating boost: verified 5-star reviews rank slightly higher
> - Recency boost: newer reviews surfaced slightly higher
> - Helpfulness signals: upvotes from other users

---

**Q23. How would you add real-time search to a system where new documents must appear in search results within 1 second of being written?**

> **Answer:**
> Elasticsearch's default refresh interval is **1 second** — which means documents are visible in search within 1 second of being indexed. This is already "near real-time" by design.
>
> **How the 1-second refresh works internally:**
> 1. When you index a document, it's written into an in-memory buffer in Elasticsearch's heap.
> 2. Every 1 second (configurable), Elasticsearch performs a **"refresh"**: it writes the in-memory buffer to a new Lucene segment (on disk, but still in OS file cache) and makes it searchable.
> 3. The segment is not yet fully flushed/committed to disk (that happens periodically via "flush"). But it IS searchable.
>
> **To guarantee sub-1-second visibility:**
> 1. Set `refresh_interval: 500ms` on the index (trades throughput for freshness).
> 2. Or call the `refresh API` explicitly after each write (`POST /index/_refresh`).
>
> **Trade-off:** More frequent refreshes = lower throughput (each refresh has overhead). For high-write systems (log ingestion), set refresh_interval to 30s or even 1m to maximize write throughput and accept longer indexing lag.

---

**Q24. A hot shard in Elasticsearch is causing query latency spikes. How do you diagnose and resolve it?**

> **Answer:**
>
> **Diagnosis:**
> 1. Use Elasticsearch's `_cat/shards?v` API to identify which shards are larger than others.
> 2. Check `_nodes/stats` to see CPU, heap, and indexing/search rates per node.
> 3. If a node hosting certain shards consistently shows higher CPU or longer query times → hot shard.
>
> **Root causes:**
> - **Uneven document size distribution:** Some documents are much larger, making their shard's inverted index disproportionately big.
> - **Temporal skew:** If sharding by timestamp (time-based indices), recent shards are always hotter.
> - **Non-random doc IDs:** If doc IDs are sequential integers and you use hash(docId) % M, some shards may receive more docs due to hash distribution (rare, but possible with poor hash functions).
>
> **Solutions:**
> 1. **Rebalance shards:** Increase the number of shards (requires reindexing) so each shard is smaller.
> 2. **Add replicas:** More replicas of the hot shard distribute read load across more nodes.
> 3. **Routing:** Use custom routing to distribute related documents more evenly.
> 4. **Force merge:** Merge small Lucene segments in the hot shard to reduce per-query overhead.
> 5. **New nodes:** Add more Elasticsearch nodes; ES will auto-rebalance shard placement.

---

**Q25. Compare Elasticsearch with PostgreSQL full-text search. When would you choose one over the other?**

> **Answer:**
>
> | Dimension | Elasticsearch | PostgreSQL FTS |
> |-----------|--------------|---------------|
> | **Scale** | Designed for billions of docs, horizontal sharding | Good up to ~100M rows on one machine |
> | **Query latency** | Sub-100ms at any scale (sharded) | Can degrade at high volume |
> | **Real-time indexing** | Near-real-time (1s refresh) | Synchronous (index updates on write) |
> | **Horizontal scaling** | Native — add nodes freely | Hard — requires manual partitioning |
> | **Query language** | Elasticsearch DSL (rich, complex) | SQL with `tsvector`/`tsquery` — familiar |
> | **Operational complexity** | High — separate cluster to manage | Low — already in your Postgres |
> | **Cost** | Significant (cluster of machines) | Near-zero (already paying for Postgres) |
> | **Language support** | Excellent — multilingual analyzers | Good — multiple language dictionaries |
> | **Ranking** | TF-IDF / BM25 + custom scoring | Basic `ts_rank` |
>
> **Choose PostgreSQL FTS when:**
> - Data volume is manageable within one Postgres instance (<50–100M rows).
> - You want to avoid operational overhead of a separate ES cluster.
> - Your search needs are moderate (simple keyword search, not heavy ranking).
> - You're a startup with a small team.
>
> **Choose Elasticsearch when:**
> - Billions of documents requiring horizontal scaling.
> - Advanced ranking, relevance tuning, and analytics.
> - Real-time log ingestion and search (ELK stack).
> - You need features like aggregations, faceted search, autocomplete at scale.

---

**Q26. How does Elasticsearch handle document updates? Is updating efficient?**

> **Answer:**
> Elasticsearch is built on **Apache Lucene**, which uses **immutable segments**. This makes updates inherently more expensive than in a traditional database.
>
> **How an update works:**
> 1. The "update" API fetches the current document, applies the changes, and re-indexes the entire document as a new version.
> 2. The old version is **marked as deleted** in the segment (a "tombstone" flag) — it's not immediately removed.
> 3. Queries skip tombstoned documents.
> 4. During segment **merges** (background process), deleted documents are actually purged and storage is reclaimed.
>
> **Why not in-place update?** Lucene segments are write-once, immutable data structures optimized for fast read access. Allowing in-place modification would break the segment's internal sorted structure and require complex locking.
>
> **Implication for system design:**
> - High update rates generate many deleted documents (tombstones) that bloat the index until the next merge.
> - Frequent updates hurt performance. If your use case has many updates (e.g., product inventory changes), consider if you need to re-index the full document or only maintain the changing fields in a separate faster store, and periodically reconcile.
> - Use the `_force_merge` API to clean up deleted docs proactively during low-traffic windows.

---

**Q27. What is BM25? How does it improve upon TF-IDF?**

> **Answer:**
> **BM25 (Best Match 25)** is the ranking function used by default in modern Elasticsearch (since version 5.0). It's a probabilistic improvement over TF-IDF.
>
> **Key improvements over TF-IDF:**
>
> 1. **Term frequency saturation:** In TF-IDF, if a word appears 100× in a doc, it scores 100× higher than a doc where it appears once. But intuitively, a word appearing 100× is not 100× more relevant than one appearing once. BM25 uses a saturation function — TF contribution grows quickly at first and then plateaus. Controlled by parameter `k1` (typically 1.2–2.0).
>
> 2. **Document length normalization:** In TF-IDF a long document scores higher just because it probably contains more occurrences of any word. BM25 normalizes for document length — a relevant mention in a short document is weighted more than the same mention in a very long document. Controlled by parameter `b` (typically 0.75).
>
> **BM25 formula (simplified):**
> ```
> BM25(d, q) = IDF(q) × (TF(q,d) × (k1 + 1)) / (TF(q,d) + k1 × (1 - b + b × |d|/avgdl))
>
> where |d| = document length, avgdl = average document length in corpus
> ```
>
> **In practice:** BM25 produces measurably better ranking quality than classic TF-IDF, especially for longer documents and high-frequency terms. It's the industry baseline for text ranking today.

---

**Q28. How would you implement autocomplete / typeahead suggestions on top of Elasticsearch?**

> **Answer:**
> Autocomplete requires returning suggestions after each keystroke, making it extremely latency-sensitive (<100ms end-to-end).
>
> **Option 1 — Prefix queries on a completion suggester:**
> Elasticsearch has a built-in **Completion Suggester** (backed by an in-memory FST — Finite State Transducer) that is optimized for prefix lookups. You index all valid suggestion strings (e.g., all product names) and query with the typed prefix. Returns suggestions in microseconds.
>
> **Option 2 — Edge n-gram tokenizer:**
> At index time, for each word/phrase, generate all prefix substrings (edge n-grams):
> "dress" → ["d", "dr", "dre", "dres", "dress"]
> Store these in the inverted index. Now a prefix query for "dre" hits the token "dre" and retrieves all documents whose title starts with "dre".
>
> **Option 3 — Redis-backed autocomplete (for simplest & highest QPS):**
> Store sorted sets in Redis with score = search frequency. For prefix "dre", do a `ZRANGEBYLEX` query for all strings starting with "dre". Fastest possible latency, no ES overhead.
>
> **Industry choice:** Large systems often use the Completion Suggester in ES for rich, weighted suggestions, combined with a Redis cache of the top-K common prefixes to absorb the highest-traffic keystrokes.

---

**Q29.  Elasticsearch says it's "near real-time" not "real-time". Explain the gap and when it matters.**

> **Answer:**
> "Near real-time" means there's a small, bounded delay (default: 1 second) between when a document is indexed and when it becomes visible in search.
>
> **Why the gap exists:**
> Elasticsearch writes new documents to an in-memory buffer. Every refresh interval (1s by default), the buffer is flushed to a new **Lucene segment** that is added to the searchable state. The segment is immediately searchable once created, but creating it has overhead — doing it after every *individual* document write would destroy throughput.
>
> **When the 1-second gap matters:**
> - **Doesn't matter:** Review search (users don't expect a review they just posted to immediately appear in global search). Log search (30s delay is fine for debugging). Product search.
> - **Matters:** Real-time chat message search (Slack expects your message to be searchable instantly). Financial event log search. Security intrusion detection (need to search logs as they arrive).
>
> **How to reduce the gap:**
> 1. Set `refresh_interval` to 500ms or 100ms (higher overhead).
> 2. Call `POST /index/_refresh` explicitly after indexing critical documents.
> 3. Use a **write-through cache** or maintain a secondary in-memory data structure for the most recent N seconds of documents, querying both ES and the in-memory store and merging the results.

---

**Q30. You're designing search for a legal document platform. Documents must be searchable immediately after upload, results must be 100% accurate (no missed documents), and the platform must handle 50 million 100-page PDFs. Walk through your full architecture.**

> **Answer:**
>
> **Unique requirements:**
> - Strong freshness: documents searchable within seconds (not 30s).
> - High accuracy: can't miss documents (legal discovery requires completeness).
> - Large documents: 100 pages each = ~100KB–1MB of text per document.
> - Volume: 50M × 1MB = ~50TB of text content in the index over time.
>
> **Ingestion Pipeline:**
> ```
> PDF Upload → S3 storage
>            → OCR/Text extraction job (Apache Tika or AWS Textract)
>            → Text cleaning & annotation service
>            → Kafka
>            → Elasticsearch Indexer
> ```
>
> **Elasticsearch Configuration:**
> - Shard count: 50TB / 30GB per shard ≈ 1,700 shards. Use 2,000 shards with room to grow.
> - Replication factor: 2 (primary + 1 replica) — legal firms need durability.
> - Refresh interval: 500ms (for near-instant searchability after upload).
>
> **Accuracy guarantee (no missed documents):**
> - Dual-write audit log: every document ID that gets sent to the indexer is logged. A reconciliation job periodically queries ES to verify each logged doc is retrievable. Any gap triggers an alert and re-index.
> - Kafka consumer group with `at-least-once` delivery + ES's idempotent indexing ensures no document is missed due to consumer failure.
>
> **Cleaning pipeline adjustments for legal text:**
> - No stop word removal (legal text: "the party to the contract" — "the" and "to" matter here).
> - Preserve case for proper nouns and legal citations.
> - Custom synonym expansion for legal terms (e.g., "plaintiff" = "claimant" in some jurisdictions).
> - Citation-aware tokenization (handle "12 U.S.C. § 1234" as a single token).
>
> **Ranking:**
> - Exact phrase matching carries very high weight (legal queries are precise).
> - Document date relevance (newer filings often more relevant).
> - Citation frequency (heavily cited docs rank higher).


---

## 📚 References & Resources

### Primary Sources
- **Apache Lucene** — The open-source foundation of Elasticsearch
  - https://lucene.apache.org/
- **Elasticsearch Documentation** — Official architecture docs
  - https://www.elastic.co/guide/en/elasticsearch/reference/current/index.html
- **OpenSearch** (AWS Elasticsearch fork)
  - https://opensearch.org/

### Engineering Blog Posts
- **[Slack Engineering — Search Architecture](https://slack.engineering/search-at-slack/)** — How Slack ranks and retrieves messages
- **[Elasticsearch Data Routing and Sharding](https://www.elastic.co/guide/en/elasticsearch/reference/current/scalability.html)**

### Concepts to Explore Further
- **BM25** — Modern successor to TF-IDF (default in newer Elasticsearch versions)
- **BERT-based Semantic Search** — Neural embeddings for meaning-based (not just keyword) search
- **Learning to Rank (LTR)** — ML models trained on click data for re-ranking
- **Zipf's Law video** — 3Blue1Brown / VSauce-style deep dive into why Zipf's law is universal
- **NFA / Automata Theory** — For understanding how misspelling correction works at scale
- **Apache Solr vs Elasticsearch** — Comparison of the two Lucene-based search platforms

---

*End of Elasticsearch & Full-Text Search — The Ultimate HLD Guide*
*Scaler Academy | HLD Module | Case Study 4*
