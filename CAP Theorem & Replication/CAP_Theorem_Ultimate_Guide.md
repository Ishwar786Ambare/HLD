# 🚀 CAP Theorem, PACELC & Replication — The Ultimate System Design Guide

> **Last Updated:** February 2026
> **Author:** System Design Study Notes (Scaler Academy — HLD Module)
> **Instructor:** Tarun Malhotra (Software Engineer at Google)
> **Topics:** Sharding, Replication, CAP Theorem, PACELC Theorem, Master-Slave Architecture, Consistency vs Availability

---

## 📋 Table of Contents

### Part 1: Foundations
1. [The Big Picture Architecture](#-the-big-picture-architecture)
2. [Sharding — Distributing Data](#-sharding--distributing-data)
3. [Replication — Copying Data](#-replication--copying-data)
4. [Sharding vs Replication — Side by Side](#-sharding-vs-replication--key-differences)

### Part 2: CAP Theorem
5. [What is CAP Theorem?](#-what-is-cap-theorem)
6. [Consistency (C)](#-c--consistency)
7. [Availability (A)](#-a--availability)
8. [Partition Tolerance (P)](#-p--partition-tolerance)
9. [CAP in Practice — The Hardep & Nikl Story](#-cap-in-practice--the-hardep--nikl-story)
10. [Choosing CP vs AP](#-choosing-cp-vs-ap)

### Part 3: PACELC Theorem
11. [What is PACELC Theorem?](#-what-is-pacelc-theorem)
12. [Latency vs Consistency Trade-off](#-latency-vs-consistency-trade-off)
13. [Real-World Examples](#-real-world-examples)

### Part 4: Master-Slave Replication
14. [Master-Slave Architecture](#-master-slave-architecture)
15. [Read Replicas](#-read-replicas)
16. [Failover & Recovery](#-failover--recovery)

### Part 5: Summary & Interview Prep
17. [Quick Reference Cheatsheet](#-quick-reference-cheatsheet)
18. [Practice Exercises & Interview Questions](#-practice-exercises--interview-questions)
19. [Solutions](#-solutions)
20. [References and Resources](#-references-and-resources)

---

# PART 1: FOUNDATIONS

---

## 🏗️ The Big Picture Architecture

Before diving into CAP Theorem, let's ground ourselves in how large-scale systems look:

```
                        ┌─────────────────────────────────┐
                        │         CLIENT (Browser)        │
                        └──────────────┬──────────────────┘
                                       │ DNS Resolution
                                       ▼
                        ┌─────────────────────────────────┐
                        │              DNS                │
                        └──────────────┬──────────────────┘
                                       │ IP Address returned
                                       ▼
                        ┌─────────────────────────────────┐
                        │       GATEWAY / LOAD BALANCER   │ ◄── SSL termination here
                        │   (First point of contact)      │     Protocol translation
                        └────────┬──────────┬─────────────┘     Rate limiting, etc.
                                 │          │
                    ┌────────────┘          └────────────┐
                    ▼                                    ▼
         ┌──────────────────┐                 ┌──────────────────┐
         │   App Server 1   │                 │   App Server 2   │
         │  (Compute Layer) │                 │  (Compute Layer) │
         └────────┬─────────┘                 └────────┬─────────┘
                  │                                    │
                  └────────────────┬───────────────────┘
                                   │
                    ┌──────────────▼───────────────────┐
                    │         GLOBAL CACHE             │ ◄── Redis / Memcached
                    └──────────────┬───────────────────┘
                                   │
                    ┌──────────────▼───────────────────┐
                    │       STORAGE / DATABASE         │ ◄── Source of Truth
                    └──────────────────────────────────┘
```

> **Key insight:** The Gateway box is called a "gateway" — not just a load balancer — because it does **much more** than load balancing: SSL termination, protocol translation, rate limiting, authentication, etc.

### Why Multiple App Servers?

| Scenario | Traffic Example |
|----------|----------------|
| Normal Day | Baseline load |
| Black Friday / Big Billion Day | 10-50x spike |
| India vs Pakistan Cricket (Hotstar) | 50-100x spike |
| Diwali Week | Sustained high load |

This is called **elasticity** — the ability to **scale up** (add more compute) when traffic is high and **scale down** (remove compute) when traffic is low. Cloud platforms like AWS support this via **Auto Scaling**.

> 💡 **Storage ≠ Compute** — Compute is highly elastic (scale up/down rapidly). Storage is **deliberately static** — you plan ahead, you don't rapidly add/remove DB boxes on the fly.

---

## 🔀 Sharding — Distributing Data

### The Problem: Too Much Data for One Machine

Consider Facebook's **User Database**:

```
Users Table (3 Billion Entries):
┌─────────┬────────┬────────┬─────────────────┬──────────┬───────────────┐
│ user_id │  name  │ gender │ relationship_st  │  DOB     │ last_updated  │
├─────────┼────────┼────────┼─────────────────┼──────────┼───────────────┤
│   107   │  Raju  │  Male  │    Married       │ 1990-01  │  2024-01-01   │
│   998   │  ...   │  ...   │    ...           │   ...    │     ...       │
│  1070   │  ...   │  ...   │    ...           │   ...    │     ...       │
└─────────┴────────┴────────┴─────────────────┴──────────┴───────────────┘

User Friends Table (Billions more entries):
┌─────────┬───────────┐
│ user_id │ friend_id │
├─────────┼───────────┤
│   107   │    998    │  ← Raju is friends with user 998
│   107   │   1070    │  ← Raju is friends with user 1070
│   107   │    66     │  ← Raju is friends with user 66
└─────────┴───────────┘
```

**A single machine CANNOT handle:**
- Storage: ~100 TB+ for billions of users (each with profile, posts, media links...)
- Load: Billions of requests per day

### What is Sharding?

> **Sharding** = Distributing data across multiple machines in a **Mutually Exclusive, Collectively Exhaustive (MECE)** way.

```
UNIVERSE OF ALL DATA
┌──────────────────────────────────────────────────────────────────┐
│  user:107  user:998  user:1070  user:66  user:442  user:5001 ... │
└──────────────────────────────────────────────────────────────────┘
                              │
               SHARDING splits this into:
                              │
       ┌──────────┬──────────┬──────────┬──────────┬──────────┐
       ▼          ▼          ▼          ▼          ▼
  ┌─────────┐ ┌─────────┐ ┌─────────┐ ┌─────────┐ ┌─────────┐
  │ SHARD A │ │ SHARD B │ │ SHARD C │ │ SHARD D │ │ SHARD E │
  │ u:107   │ │ u:998   │ │ u:1070  │ │ u:66    │ │ u:442   │
  │ u:28    │ │ u:319   │ │ u:2050  │ │ u:7123  │ │ u:9001  │
  └─────────┘ └─────────┘ └─────────┘ └─────────┘ └─────────┘
  
  ✅ All shards TOGETHER = ALL the data (Collectively Exhaustive)
  ✅ No two shards have the SAME data (Mutually Exclusive)
```

### Sharding Keys

The **sharding key** determines which shard a piece of data goes to.

| Sharding Key Type | Example | Used When |
|------------------|---------|-----------|
| **User ID** | `shard = hash(user_id) % num_shards` | User data |
| **Geography** | India → Shard India, US → Shard US | Regional services |
| **Time** | Jan data → Shard 1, Feb data → Shard 2 | Log/event data |
| **Consistent Hash** | Virtual ring with hash function | Distributed caches |

> 💡 **Connection to Consistent Hashing**: Remember the circle with servers placed around it? Each server on that circle **is a shard**. The request/user ID is hashed to a position on the ring, and you move clockwise to find the shard.

### Why Keep Related Data in the Same Shard?

This is the concept of **co-location**. Consider this example:

```
Query: "Get all friends of user 107"

❌ BAD (friends in different shards):
→ Query Shard A for 107's friends
→ Query Shard B for 107's friends
→ Query Shard C for 107's friends
→ Aggregate results
= INTERSHARD query (slow, network-heavy, inefficient)

✅ GOOD (user + their friends in same shard):
→ Query Shard A only (107 AND all his friend entries are here)
= INTRASHARD query (fast, single machine, efficient)
```

> **Rule of thumb:** Design your sharding key so that **frequently joined data lives in the same shard**. This converts expensive inter-shard queries into cheap intra-shard queries.

### Intrashard vs Intershard Requests

| Type | Description | Performance | Preferred? |
|------|-------------|-------------|------------|
| **Intrashard** | Query handled within a single shard | Fast ✅ | YES |
| **Intershard** | Query requires going to multiple shards | Slow ❌ | Avoid |

### The Hot Shard Problem 🔥

A **hot shard** occurs when one shard receives disproportionately more traffic than others.

```
Example: Justin Bieber's data on a celebrity-heavy shard

Shard A (celebrities):  💥💥💥💥💥💥💥  (millions of read requests)
Shard B (normal users): 💡             (low traffic)
Shard C (normal users): 💡             (low traffic)
```

**Solutions:**
1. **Hot-specific sharding** — Put popular users in dedicated shards with higher replication
2. **Caching** — Cache celebrity posts so DB is not hit every time (Facebook News Feed approach)

---

## 🔁 Replication — Copying Data

### The Problem: Too Many Requests for One Machine

```
Scenario: Justin Bieber's posts stored on a single machine

          User 1 ──┐
          User 2 ──┤
          User 3 ──┤──► Single DB Machine ◄── 💥 Overloaded!
          User 4 ──┤         (Millions of read requests)
          User 5 ──┘
```

Even after sharding, a **single machine per shard** may be overwhelmed by **read requests**.

### What is Replication?

> **Replication** = Creating **multiple identical copies** of the same data on different machines so more users can read from different copies simultaneously.

```
BEFORE Replication:
    Users ──► [Single Copy of Justin Bieber's Posts] ◄── 💥 Overloaded

AFTER Replication:
    Users 1-100M  ──► [Copy A — Original]       ◄── ✅ Manageable!
    Users 100M-200M ► [Copy B — Replica 1]      ◄── ✅ Manageable!
    Users 200M-300M ► [Copy C — Replica 2]      ◄── ✅ Manageable!
```

### Sharding + Replication Together

These two concepts can and **should** exist simultaneously:

```
3 Billion Facebook Users
           │
           ▼
    ┌──────────────────────────────────────────┐
    │              SHARDING                    │
    │  (Because storage is too large)          │
    └──────┬─────────────┬──────────────┬──────┘
           │             │              │
           ▼             ▼              ▼
      [SHARD 1]     [SHARD 2]     [SHARD 3]
      Users:1-1B    Users:1B-2B   Users:2B-3B
           │             │              │
           ▼             ▼              ▼
    ┌──────────────────────────────────────────┐
    │            REPLICATION                   │
    │  (Because request volume is too high)    │
    └──────────────────────────────────────────┘
           │             │              │
     ┌─────┤       ┌─────┤        ┌────┤
     │     │       │     │        │    │
  [S1 R1][S1 R2] [S2 R1][S2 R2] [S3 R1][S3 R2]
  Shard1  Shard1  Shard2 Shard2  Shard3 Shard3
  Replica1 Repl2  Repl1  Repl2   Repl1  Repl2
```

> 💡 Think of each **shard** as a subset of your data universe, and each **replica** as a clone of that shard.

---

## ⚖️ Sharding vs Replication — Key Differences

| Property | Sharding | Replication |
|----------|----------|-------------|
| **What it does** | Divides data across machines | Copies data to multiple machines |
| **Data on each machine** | DIFFERENT subsets | SAME data |
| **Primary Goal** | Handle too much **data (storage)** | Handle too many **requests (load)** |
| **Mutually Exclusive?** | YES — no two shards overlap | NO — all replicas are identical |
| **Driven by** | Storage requirements | Request volume / traffic |
| **Analogy** | Splitting a book into chapters | Printing multiple copies of the same book |
| **Scale dimension** | Horizontal **data** scale | Horizontal **read** scale |

```
SHARDING:                           REPLICATION:
┌─────┐ ┌─────┐ ┌─────┐           ┌─────┐ ┌─────┐ ┌─────┐
│ A-F │ │ G-M │ │ N-Z │           │ ALL │ │ ALL │ │ ALL │
│data │ │data │ │data │           │data │ │data │ │data │
└─────┘ └─────┘ └─────┘           └─────┘ └─────┘ └─────┘
Different data on each             Same data on each
```

---

# PART 2: CAP THEOREM

---

## 🧩 What is CAP Theorem?

> **CAP Theorem** states that in any **distributed system**, you can only guarantee **two out of these three properties simultaneously**:
>
> - **C** — Consistency
> - **A** — Availability
> - **P** — Partition Tolerance

```
              CONSISTENCY (C)
                   △
                  / \
                 /   \
                /  ⚠️  \
               /  Pick  \
              /   2 of 3 \
             /─────────────\
AVAILABILITY ───────────── PARTITION
    (A)                  TOLERANCE (P)
```

| Choice | Properties Guaranteed | Sacrificed |
|--------|----------------------|------------|
| **CA** | Consistent + Available | Partition Tolerance |
| **CP** | Consistent + Partition Tolerant | Availability |
| **AP** | Available + Partition Tolerant | Consistency |

> ⚠️ **Critical Insight:** In practice, **network partitions ALWAYS happen** (networks are unreliable). Therefore, partition tolerance is **non-negotiable** in distributed systems. The real choice is always between **CP or AP**.

---

## ✅ C — Consistency

> **Consistency** means every read returns the **latest write**, OR equivalently, every machine has the **same latest view of the truth**.

```
CONSISTENT System:
                   WRITE: "Raju's DOB = 1990"
                           │
                    ┌──────▼──────┐
                    │  Machine 1  │ ── "Raju DOB = 1990" ✅
                    └─────────────┘
                    ┌─────────────┐
                    │  Machine 2  │ ── "Raju DOB = 1990" ✅
                    └─────────────┘

READ from any machine → same answer ✅

INCONSISTENT System:
                   WRITE went to Machine 1 only:
                    ┌─────────────┐
                    │  Machine 1  │ ── "Raju DOB = 1990" ✅
                    └─────────────┘
                    ┌─────────────┐
                    │  Machine 2  │ ── "Raju DOB = ???"  ❌ (stale)
                    └─────────────┘

READ from Machine 2 → wrong/missing answer ❌
```

### Formal Definition

```
Every READ must return the result of the most recent WRITE
(or return an error — never stale data)
```

### Real-World Analogy

- 🏦 **Bank ATM**: You deposited ₹10 lakh. Your ATM must show ₹10 lakh when you check balance — not show ₹500. Consistency is **non-negotiable** here.
- 💹 **Zerodha (Stock Price)**: If Adani stock is ₹1200, showing ₹1800 to someone else is unacceptable. Wrong price = wrong trade decisions.

---

## ✅ A — Availability

> **Availability** means the system **always responds** to every request — even if the response isn't the most current data. A system is available if it responds **without error**.

> ⚠️ Availability does NOT guarantee the response is **correct** — just that there IS a response.

```
AVAILABLE System (even if stale):
    User asks: "How many views does this YouTube video have?"
    
    Machine 1 says: "10,242 views"   ← May not be exactly right
    Machine 2 says: "10,238 views"   ← May not be exactly right
    
    But BOTH respond! No error. = AVAILABLE ✅
    
NOT AVAILABLE System:
    User asks: "What is my ATM balance?"
    
    System says: "Sorry, try again later" ← ERROR response = NOT AVAILABLE ❌
```

### Real-World Analogy

- 📺 **YouTube view count**: Does not show exact real-time count, but ALWAYS shows *something*. Prioritizes availability.
- 📺 **Hotstar live viewers**: "2.4 million watching" might not be exact, but the count is always there.
- 🏦 **ATM**: Better to say "temporarily unavailable" than show wrong balance. Prioritizes consistency over availability.

---

## ✅ P — Partition Tolerance

> **Partition** = A **network partition** — a scenario where two machines **temporarily cannot communicate** with each other (the network link between them is broken).

```
NETWORK PARTITION:

┌─────────────┐         ✂️ BROKEN ✂️      ┌─────────────┐
│  Machine 1  │ ─────────── X ────────── │  Machine 2  │
└─────────────┘                          └─────────────┘

- M1 can still talk to clients ✅
- M2 can still talk to clients ✅
- M1 and M2 CANNOT talk to each other ❌
```

> **Partition Tolerance** = The system **continues to function** even when a network partition occurs.

### Why Partitions Always Happen

Networks are **always unreliable**. Even inside a single data center:
- Cables can fail
- Network ports can drop
- Packets can be lost
- Switches can fail
- Software bugs can block communication

> **Network is always unreliable.** This is a fundamental truth of distributed computing.

---

## 📖 CAP in Practice — The Hardep & Nikl Story

Let's walk through a concrete example to understand CP vs AP.

### The Scenario

**Hardep** runs an "Event Reminder Service" — people call in to register events; they call back later to recall them. As the service grows, Hardep hires **Nikl**. Now two people serve calls via a **load balancer**.

```
              CLIENTS
             /       \
            /         \
  ┌────────────────────────┐
  │     LOAD BALANCER      │
  └────────┬───────────────┘
           │
    ┌──────┴──────┐
    │             │
┌───▼───┐     ┌───▼───┐
│ HARDEP │     │  NIKL │
│(Diary)│     │(Diary)│
└───────┘     └───────┘
```

---

### Option 1 — AP System (Available, Partition Tolerant — NOT Consistent)

**Protocol**: Each person writes only in their own diary.

```
WRITE:
  Shiv calls in → Load balancer routes to Hardep
  Hardep writes: "Shiv: girlfriend's wedding, 28 Feb 7pm"
  ✅ Responds immediately

READ (later):
  Shiv calls back → Load balancer routes to Nikl (randomly!)
  Nikl checks his diary: "I have nothing for Shiv"
  ❌ Returns wrong answer — "No events found!"
```

**Result:**
- ✅ **Available** — Both Hardep and Nikl always respond (no errors)
- ❌ **Not Consistent** — Nikl returns wrong data
- ✅ **Partition Tolerant** — Even if they stop talking to each other, everything still "works"

---

### Option 2 — CP System (Consistent, Partition Tolerant — NOT Available)

**Protocol (updated)**: Before acknowledging any write, the receiver writes in BOTH diaries.

```
WRITE:
  Shiv calls in → routes to Hardep
  Hardep writes in his own diary ✓
  Hardep then calls Nikl: "Please write this too"
  Nikl writes ✓ and confirms
  ONLY THEN: Hardep tells Shiv "Your event is registered" ✅

READ (later):
  Shiv calls → routes to Nikl
  Nikl checks diary: "Shiv: girlfriend's wedding, 28 Feb 7pm"
  ✅ Returns correct answer
```

**Problem: What if Nikl goes on holiday (machine goes down)?**

```
Nikl is OFFLINE (vacation in Lonavala! 🏖️)

  Shiv calls in → routes to Hardep
  Hardep writes in his own diary ✓
  Hardep calls Nikl: [no answer] ❌
  
  HARDEP CANNOT ACKNOWLEDGE THE WRITE → 
  System is UNAVAILABLE for writes ❌
```

**Result:**
- ✅ **Consistent** — When working, every read returns latest write
- ❌ **Not Available** — If one machine is down, writes fail completely
- ✅ **Partition Tolerant** — Even during partition, the system rejects writes (stays consistent)

---

### Option 3 — AP System (with eventual sync)

**Protocol**: Write locally when partner is down; sync when they come back.

```
Nikl is OFFLINE:

  Shiv registers event → Hardep writes locally, acknowledges immediately ✅
  (Shiv is happy — quick response)
  
When Nikl comes BACK ONLINE:
  Hardep sends all pending entries to Nikl
  Nikl writes them ✓ — now both are synced
  
BUT: If network partition happens DURING sync:
  → Some entries may not reach Nikl
  → Nikl comes online, gets some requests
  → Nikl returns stale data ❌
```

**Result:**
- ✅ **Available** — Always responds even when partner is down
- ❌ **Not Consistent** — During partition window, stale data possible
- ✅ **Partition Tolerant** — Works through network outages

---

### Summary: The Three Options

```
┌──────────────────────────────────────────────────────────────────────┐
│  Option 1: AP  (each writes locally, no sync)                        │
│  ✅ Always responds (Available)                                       │
│  ✅ Handles partitions fine (Partition Tolerant)                     │
│  ❌ Different machines return different data (Not Consistent)         │
│                                                                      │
│  Option 2: CP  (write to both, fail if one is down)                  │
│  ✅ Every read returns latest write (Consistent)                      │
│  ✅ Handles partitions by refusing to accept inconsistency           │
│  ❌ System is unavailable when one machine is down (Not Available)   │
│                                                                      │
│  Option 3: AP with eventual consistency  (write locally, sync later) │
│  ✅ Always responds (Available)                                       │
│  ✅ Handles partitions (Partition Tolerant)                          │
│  ❌ Stale reads possible during/after partition (Not Consistent)     │
└──────────────────────────────────────────────────────────────────────┘
```

---

## 🎯 Choosing CP vs AP

> **In distributed systems, Partition Tolerance is always required.** Networks always fail sometimes. The choice is: **CP or AP**.

### Choose CP (Consistency + Partition Tolerance) when:
- **Banking / Financial systems** — Wrong balance is catastrophic
- **Stock Trading (Zerodha)** — Wrong price = bad trades
- **IRCTC / Flight Booking** — Double-booking a seat is unacceptable
- **User Authentication / Blacklisting** — If a user is blocked, they must be blocked everywhere

### Choose AP (Availability + Partition Tolerance) when:
- **YouTube view counts** — A slightly stale count is fine; going down is not
- **Hotstar live viewer count** — Approximate count is OK
- **Social media likes/comments** — A stale like count won't hurt anyone
- **Product catalog / Prices (non-critical)** — Slight staleness is acceptable
- **DNS** — Propagation delay is acceptable; being unavailable is not

### CA (without Partition Tolerance) — Only on Single Machines

| System | Why |
|--------|-----|
| Single SQL database | No network between machines |
| In-process cache | No inter-machine communication |
| SQLite | Single-node, no network partition possible |

> **CA systems exist in practice**, but only for specific use cases within a larger distributed system — e.g., a single MySQL box handling blacklist lookups (consistent + available, but no need for partition tolerance because it's ONE machine).

---

# PART 3: PACELC THEOREM

---

## ⚡ What is PACELC Theorem?

PACELC extends CAP theorem by adding a second trade-off that applies **even when there is no partition**.

> **PACELC** = **P**artition → **A**vailability or **C**onsistency; **E**lse → **L**atency or **C**onsistency

```
┌─────────────────────────────────────────────────────────┐
│               PACELC THEOREM                            │
├─────────────────────────────────────────────────────────┤
│                                                         │
│  IF Partition Happens:                                  │
│     → Choose between AVAILABILITY or CONSISTENCY       │
│        (this is the CAP theorem part)                   │
│                                                         │
│  ELSE (Normal operation, no partition):                 │
│     → Choose between LOW LATENCY or CONSISTENCY        │
│        (this is the NEW insight)                        │
│                                                         │
└─────────────────────────────────────────────────────────┘
```

---

## ⏱️ Latency vs Consistency Trade-off

### What is Latency?

> **Latency** = the time it takes for a request to be completed.
>
> - **Low Latency** = Fast (good ✅)
> - **High Latency** = Slow (bad ❌)

### Why Does Consistency Cost Latency?

Going back to the **Hardep & Nikl** example:

```
HIGH CONSISTENCY Protocol (CP):
  Client writes → Hardep writes locally → Hardep WAITS for Nikl to confirm
                                          ↑
                                   EXTRA TIME = EXTRA LATENCY

  Total Time: local write + network round trip + Nikl's write + confirmation
```

```
LOW LATENCY Protocol (AP):
  Client writes → Hardep writes locally → Hardep immediately responds ✅

  Total Time: just local write (fast!)
  But: consistency is sacrificed
```

### The Trade-off Visualized

```
                HIGH CONSISTENCY ←──────────────→ LOW LATENCY

  Banking ATM   Booking Systems   Social Feed    DNS      View Counts
      │               │                │           │           │
      ▼               ▼                ▼           ▼           ▼
   Must be         Must be         Eventual    Stale OK    Stale OK
   consistent      consistent      consistency  (TTL)       (approx)
   (slow ok)       (slow ok)                   (fast!)     (fast!)
```

---

## 🌍 Real-World Examples

### IRCTC / Flight Booking (CP + High Latency is OK)

```
User clicks "Book Seat 12A" on IRCTC:

→ Request goes to system
→ System must ensure NO TWO USERS book the same seat
→ Uses distributed lock / 2-phase commit
→ This takes 2-3 seconds ← HIGH LATENCY

But: ✅ Nobody ever gets double-booked
```

> You've experienced this! That 2-3 second wait on IRCTC after clicking "Book" — that's the system ensuring **consistency** at the cost of **latency**.

### YouTube Views (AP + Low Latency)

```
User visits video:
→ System returns view count immediately (maybe slightly stale)
→ No waiting for all replica counts to sync
→ Response in < 50ms ← LOW LATENCY

But: Different users may see slightly different view counts ❌ (Not consistent)
```

### Zerodha Stock Prices (CP even with latency)

```
Trader checks Adani stock price:
→ System MUST return latest price
→ Worth a small wait to ensure accuracy
→ Wrong data = wrong trades = financial loss
```

---

### PACELC Classification of Common Databases

| Database | Partition | Else | Classification |
|----------|-----------|------|----------------|
| **Cassandra** | A | L | PA/EL — Highly available, low latency, eventual consistency |
| **DynamoDB** | A | L | PA/EL — Always available, tunable consistency |
| **MongoDB** | C | L | PC/EL — Consistent reads, can tune for latency |
| **Zookeeper** | C | C | PC/EC — Strong consistency always |
| **MySQL (single node)** | N/A | C | E/C — No partition concern, strong consistency |
| **HBase** | C | C | PC/EC — Very strong consistency |

---

# PART 4: MASTER-SLAVE ARCHITECTURE

---

## 🏛️ Master-Slave Architecture

Master-Slave (also called **Primary-Replica**) is the most common replication pattern.

```
                    CLIENTS
                       │
              ┌────────▼────────┐
              │  LOAD BALANCER  │
              └────────┬────────┘
                       │
         ┌─────────────┼─────────────┐
         │             │             │
    READS │        READS │       READS │
         │             │             │
    ┌────▼────┐   ┌────▼────┐   ┌────▼────┐
    │ REPLICA │   │ REPLICA │   │ MASTER  │  ◄── WRITES go here ONLY
    │ (Slave) │   │ (Slave) │   │(Primary)│
    └────┬────┘   └────┬────┘   └────┬────┘
         │             │             │
         └─────────────┼─────────────┘
                       │
                    REPLICATION
                  (async/sync)
```

### Key Rules

| Operation | Goes To |
|-----------|---------|
| **WRITE** (INSERT, UPDATE, DELETE) | Master ONLY |
| **READ** (SELECT) | Any Replica (or Master) |

### Why Separate Reads from Writes?

In typical web applications:
- **80-90%** of traffic is **reads**
- **10-20%** of traffic is **writes**

By routing reads to replicas, we dramatically reduce master load.

---

## 📖 Read Replicas

### Synchronous vs Asynchronous Replication

```
SYNCHRONOUS REPLICATION (Strong Consistency):
  
  Client → WRITE → Master
                    │
                    ├─────────────► Replica 1 (write confirmed)
                    │                   │
                    └─────────────► Replica 2 (write confirmed)
                         ↑
                    Only THEN → ACK to Client
  
  ✅ All replicas always in sync
  ❌ Write latency = slowest replica's write time


ASYNCHRONOUS REPLICATION (Eventual Consistency):
  
  Client → WRITE → Master → ACK to Client immediately ✅
                    │
                    └──(async)──► Replica 1 (queued write)
                    └──(async)──► Replica 2 (queued write)
  
  ✅ Low write latency
  ❌ Replicas may lag — reads from replica may be stale
```

### Replication Lag

> **Replication Lag** = the time delay between a write to the master and that write appearing on all replicas.

```
Timeline:
  T+0ms  → User writes post
  T+0ms  → Master has the post ✅
  T+50ms → Replica 1 has the post ✅
  T+100ms → Replica 2 has the post ✅

During T+0ms to T+50ms:
  → If user's next READ goes to Replica 1, they DON'T see their own post! 😱
  → This is "Read Your Own Write" consistency violation
```

**Solutions to Replication Lag Issues:**

| Problem | Solution |
|---------|----------|
| User can't read their own write | Route same user's reads to master briefly after writes |
| Monotonic read violation | Always route same user to same replica |
| Lag growing too large | Use synchronous replication for critical data |

---

## 🔄 Failover & Recovery

### What Happens When Master Goes Down?

```
BEFORE FAILURE:
  Master ────(async)────► Replica 1
         ────(async)────► Replica 2

MASTER FAILS:
  Master ✗               Replica 1 ← Promoted to new Master!
                         Replica 2 ← Now replicates from Replica 1
```

### Failover Challenges

1. **Data Loss Risk**: If async replication, the failed master may have had some writes that never made it to replicas
2. **Split-Brain Problem**: Two nodes think they're both Master — can lead to conflicts
3. **Detection Time**: How quickly do you detect the master failed?
4. **Promotion Complexity**: Which replica becomes the new master? (Usually the most up-to-date one)

### Semi-Synchronous Replication

A middle ground:

```
WRITE → Master stores + sends to at least ONE replica
        → Gets ack from that ONE replica
        → Acknowledges to client

✅ At most one replica's worth of lag survived
✅ Better performance than full synchronous
✅ Better durability than full async
```

---

# PART 5: SUMMARY & INTERVIEW PREP

---

## 📋 Quick Reference Cheatsheet

### CAP Theorem Summary

```
┌──────────────────────────────────────────────────────────────┐
│                    CAP THEOREM CHEATSHEET                    │
├──────────────────────┬───────────────────────────────────────┤
│  C (Consistency)     │ Every read returns the latest write   │
│  A (Availability)    │ Every request gets a response (no err)│
│  P (Partition Tol.)  │ System works despite network failures │
├──────────────────────┼───────────────────────────────────────┤
│  CP System           │ Prioritizes accuracy over uptime      │
│  AP System           │ Prioritizes uptime over accuracy      │
│  CA System           │ Only possible on single machine       │
├──────────────────────┼───────────────────────────────────────┤
│  In Distributed?     │ P is always required! → CP or AP only │
└──────────────────────┴───────────────────────────────────────┘
```

### PACELC Summary

```
┌──────────────────────────────────────────────────────────────┐
│                   PACELC THEOREM CHEATSHEET                  │
├──────────────────────────┬───────────────────────────────────┤
│  P (Partition)           │ When partition: A vs C            │
│  E (Else / normal)       │ No partition: L vs C              │
│  A (Availability)        │ Respond even if stale             │
│  C (Consistency)         │ Only respond if data is current   │
│  L (Latency)             │ Respond fast (may not sync first) │
├──────────────────────────┼───────────────────────────────────┤
│  PA/EL  (Cassandra)      │ AP + fast, eventual consistency   │
│  PC/EC  (Zookeeper)      │ CP + always consistent, slower    │
└──────────────────────────┴───────────────────────────────────┘
```

### Sharding vs Replication Summary

```
┌────────────────┬──────────────────────┬──────────────────────┐
│                │      SHARDING        │     REPLICATION      │
├────────────────┼──────────────────────┼──────────────────────┤
│ What it does   │ Splits data across   │ Copies same data to  │
│                │ multiple machines    │ multiple machines    │
├────────────────┼──────────────────────┼──────────────────────┤
│ Data per box   │ DIFFERENT subsets    │ SAME full copy       │
├────────────────┼──────────────────────┼──────────────────────┤
│ Solves         │ Storage too large    │ Too many requests    │
├────────────────┼──────────────────────┼──────────────────────┤
│ MECE?          │ Yes — exclusive +    │ No — all are same    │
│                │ exhaustive           │                      │
├────────────────┼──────────────────────┼──────────────────────┤
│ Can coexist?   │ YES — a shard can    │ YES — a shard can    │
│                │ have replicas        │ also be sharded      │
└────────────────┴──────────────────────┴──────────────────────┘
```

---

## 🎯 Practice Exercises & Interview Questions

### Conceptual Questions

**Q1.** What is the CAP theorem? Explain with a real-world example.

**Q2.** Why can't a distributed system be simultaneously consistent, available, AND partition tolerant?

**Q3.** A social media platform shows slightly stale "likes" count on posts. Is this CP or AP? Why?

**Q4.** An online banking system must ensure that a user cannot withdraw money they don't have, even if two ATMs are used simultaneously. Is this CP or AP? Why?

**Q5.** Explain the difference between sharding and replication. Can they work together?

**Q6.** What is a "hot shard"? How would you solve it in the context of a social network like Instagram?

**Q7.** What is replication lag? When does it cause problems? How do you mitigate it?

**Q8.** What is the PACELC theorem? How does it extend CAP?

**Q9.** When would you choose synchronous replication vs asynchronous replication?

**Q10.** What is an intrashard query vs an intershard query? Which is preferred and why?

---

### System Design Application Questions

**Q11.** You are designing a chess game system. Should you use CP or AP for game state? Why?

**Q12.** You are designing a "recently viewed products" feature on Amazon. Would you use CP or AP? Why?

**Q13.** Design the sharding strategy for a WhatsApp chat system. What would be your sharding key?

**Q14.** You have a single MySQL master that's getting overwhelmed by read queries. What would you do? Walk through the trade-offs.

**Q15.** Facebook stores Justin Bieber's posts. Millions of users try to read his posts per second. How would you design this system? (Hint: hot shard + replication + caching)

---

## 📝 Solutions

### Q1 — CAP Theorem Explanation

CAP Theorem states that a distributed system can only guarantee two of three properties: Consistency (every read returns latest write), Availability (every request gets a response), and Partition Tolerance (system works despite network failures).

**Real-world example — IRCTC ticket booking:**
- **Consistency**: Two users cannot book the same seat (strong consistency required)
- **Availability**: The booking system should respond even during peak loads
- **Partition Tolerance**: Network issues between servers will inevitably happen

IRCTC chooses **CP**: It's better for the system to be temporarily slow or unavailable than to double-book a seat.

---

### Q2 — Why No CAP Together?

When a network partition occurs (which is inevitable), a node must decide: do I respond to the client (Availability) or do I wait until the other node confirms (Consistency)?

- If it responds immediately → Might return stale data → Not Consistent
- If it waits for confirmation → Might timeout → Not Available

There's no way to guarantee both during a partition. Hence: pick one.

---

### Q3 & Q4 — AP vs CP Classification

| System | Choice | Reason |
|--------|--------|--------|
| Social media likes count | **AP** | Stale count is fine; availability matters more |
| Bank ATM withdrawal | **CP** | Wrong balance data is catastrophic; prefer unavailability |

---

### Q5 — Sharding + Replication Together

Yes! They are complementary, not mutually exclusive.

- **Sharding** handles too much *data* → split across machines
- **Replication** handles too many *requests* → copy to multiple machines

Common pattern: Shard your data into N shards, then replicate each shard M times → N × M total machines.

---

### Q11 — Chess Game (CP)

Chess requires **CP** because:
- Both players must see the exact same game state
- An inconsistent view (e.g., player A sees different board than player B) would make the game unplayable
- Latency is acceptable (a few hundred ms is fine per move)

---

### Q12 — Recently Viewed Products (AP)

"Recently viewed" is **AP** because:
- Showing a product that was viewed 2 minutes ago instead of 1 minute ago is fine
- The system must ALWAYS respond (user is shopping; showing nothing is worse than showing slightly stale list)
- Consistency is not critical here

---

### Q13 — WhatsApp Chat Sharding Key

**Sharding Key: Chat Room ID (or Conversation ID)**

Why:
- All messages in a single chat belong together → intrashard queries for chat history
- Easy to route: hash(chat_id) → shard
- Avoids cross-shard joins for most common queries (fetch messages in a conversation)

Consideration: Group chats with millions of members could become hot shards → may need per-group-specific replication strategy.

---

### Q14 — MySQL Overwhelmed by Reads

1. **Add Read Replicas** — Route all read queries to replicas
2. **Add Caching Layer** — Redis in front of DB for hot queries
3. **Monitor Replication Lag** — Ensure replicas don't fall too far behind
4. **Read-Your-Own-Write Routing** — Route user's reads to master for N seconds after their write

Trade-off: Adding replicas with async replication → eventual consistency. If strong consistency needed → sync replication (higher latency) or always read from master.

---

### Q15 — Justin Bieber's Posts (Hot Shard + Replication + Caching)

Hot account problem (also called "celebrity problem"):

```
Solution layers:
1. Dedicated hot shard for celebrities (separate from normal users)
2. High replication factor for hot shards (e.g., 100 replicas vs 3 for normal users)
3. Aggressive caching — cache celebrity posts at CDN / application layer
4. Fan-out on read (pull model) — don't push to all followers; pull from celebrity shard when a follower loads feed
```

The Facebook News Feed solution: Use a **Recent Posts DB** (cache) that holds only the latest posts from celebrities, avoiding hitting the main shards on every feed load.

---

## 📚 References and Resources

### Academic & Formal References
- **CAP Theorem** — Originally proposed by Eric Brewer (2000), formalized by Gilbert & Lynch (2002)
  - Paper: [Brewer's Conjecture and the Feasibility of Consistent, Available, Partition-Tolerant Web Services](https://groups.csail.mit.edu/tds/papers/Gilbert/Brewer2.pdf)
- **PACELC Theorem** — Proposed by Daniel J. Abadi (2012)
  - Paper: [Consistency Tradeoffs in Modern Distributed Database System Design: CAP is Only Part of the Story](https://www.cs.umd.edu/~abadi/papers/abadi-pacelc.pdf)

### Database Documentation
- [Cassandra Architecture — Data Replication](https://cassandra.apache.org/doc/latest/cassandra/architecture/dynamo.html)
- [MongoDB Replication](https://www.mongodb.com/docs/manual/replication/)
- [MySQL Replication](https://dev.mysql.com/doc/refman/8.0/en/replication.html)
- [PostgreSQL High Availability](https://www.postgresql.org/docs/current/high-availability.html)

### Study Resources
- [Martin Kleppmann — Designing Data-Intensive Applications (DDIA)](https://dataintensive.net/) ← **Must Read**
  - Chapter 5: Replication
  - Chapter 6: Partitioning
  - Chapter 9: Consistency and Consensus
- [AWS — Eventual Consistency Primer](https://docs.aws.amazon.com/amazondynamodb/latest/developerguide/HowItWorks.ReadConsistency.html)
- [Cloudflare — Why Network Partitions Happen](https://blog.cloudflare.com/a-post-mortem-on-the-recent-cloudflare-outage/)

### Videos & Blogs
- [Martin Fowler — CAP Theorem](https://martinfowler.com/articles/distributed-failures.html)
- [ByteByteGo — CAP Theorem Simplified](https://blog.bytebytego.com/p/cap-theorem-and-distributed-systems)
- [System Design Primer (GitHub)](https://github.com/donnemartin/system-design-primer#cap-theorem)

---

> 📌 **Remember**: CAP Theorem and PACELC are frameworks for *thinking*, not rigid dogmas. Real-world databases often allow you to *tune* consistency vs availability per operation (e.g., DynamoDB's `ConsistentRead`, Cassandra's consistency levels). The key is understanding the **trade-offs** so you can make informed decisions.

