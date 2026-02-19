# CAP Theorem & Replication — HLD Study Notes

> Scaler Academy HLD Module | Instructor: Tarun Malhotra (Software Engineer, Google)

This folder covers three deeply related, often-confused topics that are **always tested in HLD interviews**:

---

## 📁 Files in this Folder

| File | Purpose | When to Use |
|------|---------|-------------|
| `CAP_Theorem_Ultimate_Guide.md` | Deep-dive notes with examples, diagrams, Q&A | First read, deep revision, interview prep |
| `CAP_Quick_Reference.md` | One-page cheatsheet for key definitions & choices | Last-minute revision before interview |

---

## 🎯 Topics Covered

### 1. Sharding
- What is sharding? Why is it needed?
- Facebook user DB example (3 billion users)
- Sharding keys (user ID, geography, time, consistent hash)
- Intrashard vs Intershard queries
- Hot Shard problem + solutions
- Connection to Consistent Hashing (from previous module)

### 2. Replication
- What is replication? Why is it needed?
- Sharding + Replication together
- Master-Slave architecture
- Synchronous vs Asynchronous replication
- Replication lag and its consequences

### 3. CAP Theorem
- Consistency, Availability, Partition Tolerance
- Why you can only pick 2 of 3
- The "Hardep & Nikl" story walkthrough (AP → CP → AP w/ sync)
- Network partitions and why they always happen
- CP vs AP decision guide with real examples

### 4. PACELC Theorem
- Extension of CAP — adds the Latency vs Consistency trade-off
- During normal operation: fast vs consistent
- IRCTC booking (high latency, high consistency) example
- YouTube views (low latency, eventual consistency) example
- Database classification: PA/EL vs PC/EC

---

## 🧠 Key Takeaways

1. **Sharding ≠ Replication** — sharding *splits* data; replication *copies* data
2. **In distributed systems, P is always required** → the real choice is CP or AP
3. **CAP Theorem + PACELC together**: when partition happens (CP/AP), when not (latency/consistency trade-off)
4. **Intrashard queries are always preferred** — design sharding key to keep related data together
5. **Eventual consistency** is fine for social feeds, view counts; **strong consistency** is needed for payments, bookings

---

## 📚 Prerequisite Knowledge

- ✅ Basics of distributed systems (app servers, load balancers)
- ✅ Consistent Hashing (from "Basics & Consistent Hashing" module)
- ✅ Caching basics (from "Caching" module)

---

*Notes compiled from Scaler Academy HLD Module Lecture*
*Date: February 2026*
