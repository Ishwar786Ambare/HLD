# ⚡ Caching Quick Reference & Cheatsheet

## 🎯 When to Use Caching

✅ **DO Cache:**
- Frequently read data
- Computation-heavy results
- Database query results
- API responses
- Session data
- Static content (images, CSS, JS)
- Configuration data

❌ **DON'T Cache:**
- Highly personalized data
- Sensitive information (passwords, credit cards)
- Data that changes frequently
- Large objects (>1MB)
- Real-time data

---

## 📊 Quick Strategy Selector

```
Read-Heavy + Eventually Consistent → Cache-Aside (Lazy Loading)
Read-Heavy + Need Consistency → Write-Through
Write-Heavy + Can tolerate loss → Write-Back
General Purpose → Cache-Aside
```

---

## 🔄 Strategies Cheatsheet

### Cache-Aside (Lazy Loading)
```python
data = cache.get(key)
if not data:
    data = db.query(key)
    cache.set(key, data, ttl=3600)
return data
```
**Use:** 90% of cases

### Write-Through
```python
def update(key, data):
    cache.set(key, data)    # 1. Cache
    db.update(key, data)    # 2. Database
```
**Use:** When consistency matters

### Write-Back
```python
def update(key, data):
    cache.set(key, data)           # 1. Cache (fast)
    queue.enqueue('db_update', key, data)  # 2. Async DB
```
**Use:** Write-heavy workloads

---

## 🗑️ Eviction Policies Quick Guide

| Policy | Best For | Avoid For |
|--------|----------|-----------|
| **LRU** | General purpose | Time-sensitive data |
| **LFU** | Stable workloads | Dynamic patterns |
| **FIFO** | Simple caching | Production systems |
| **TTL** | Time-sensitive data | Data that doesn't expire |

### Redis Configuration:
```
maxmemory-policy allkeys-lru    # Most common
maxmemory-policy allkeys-lfu    # Frequency-based
maxmemory-policy volatile-lru   # Only evict keys with TTL
```

---

## ⏰ TTL Quick Reference

```python
# Hot data (frequently changing)
cache.set(key, data, ttl=300)       # 5 minutes

# Warm data (moderate changes)
cache.set(key, data, ttl=3600)      # 1 hour

# Cold data (rarely changes)
cache.set(key, data, ttl=86400)     # 24 hours

# Static data
cache.set(key, data, ttl=604800)    # 1 week

# No expiration (manual invalidation)
cache.set(key, data, ttl=None)
```

---

## 🚨 Problem-Solution Matrix

| Problem | Quick Solution |
|---------|----------------|
| **Cache Penetration** | Cache null values + Bloom filter |
| **Cache Avalanche** | Random TTL jitter |
| **Hot Key** | Local cache + Replication |
| **Stampede** | Locking + Probabilistic refresh |
| **Stale Data** | TTL + Event-based invalidation |

### Implementation Examples:

#### Cache Penetration Fix:
```python
user = db.get_user(user_id)
if user is None:
    cache.set(f"user:{user_id}", "NULL", ttl=60)
```

#### Cache Avalanche Fix:
```python
import random
jitter = random.randint(0, 300)
cache.set(key, data, ttl=3600 + jitter)
```

#### Hot Key Fix:
```python
# Local cache layer
local_data = local_cache.get(key)
if local_data:
    return local_data
    
data = redis_cache.get(key)
local_cache.set(key, data, ttl=60)
```

---

## 📈 Performance Metrics

### Target Goals:
```
Cache Hit Rate:    >80% ✅
                   60-80% ⚠️
                   <60% ❌

Cache Latency:     <5ms ✅
                   5-20ms ⚠️
                   >20ms ❌

Memory Usage:      <75% ✅
                   75-85% ⚠️
                   >85% ❌
```

### Monitoring Commands (Redis):
```bash
# Stats
redis-cli INFO stats

# Hit rate calculation
hits / (hits + misses)

# Memory usage
redis-cli INFO memory

# Slow queries
redis-cli SLOWLOG GET 10
```

---

## 🔧 Redis Common Commands

### Basic Operations:
```bash
# Set with TTL
SET user:123 "John Doe" EX 3600

# Get
GET user:123

# Delete
DEL user:123

# Check TTL
TTL user:123

# Set if not exists
SETNX lock:resource "locked"

# Increment
INCR counter:pageviews
```

### Data Structures:
```bash
# Hash (for objects)
HSET user:123 name "John" age 30
HGETALL user:123

# List
LPUSH queue:jobs "job1"
RPOP queue:jobs

# Set
SADD tags:post:1 "python" "redis"
SMEMBERS tags:post:1

# Sorted Set (leaderboard)
ZADD leaderboard 100 "player1"
ZREVRANGE leaderboard 0 9 WITHSCORES
```

---

## 🌐 Cache Layer Selection

```
┌─────────────────────────────────────────────┐
│ Browser Cache (Client)                      │
│ • HTML, CSS, JS, Images                     │
│ • Latency: 0ms (instant)                    │
│ • Control: Low                              │
└─────────────────────────────────────────────┘
                    ↓
┌─────────────────────────────────────────────┐
│ CDN (Edge)                                  │
│ • Static assets, API responses              │
│ • Latency: 10-50ms                          │
│ • Control: Medium                           │
└─────────────────────────────────────────────┘
                    ↓
┌─────────────────────────────────────────────┐
│ Application Cache (Redis/Memcached)        │
│ • Database queries, computed data           │
│ • Latency: 1-5ms                            │
│ • Control: High                             │
└─────────────────────────────────────────────┘
                    ↓
┌─────────────────────────────────────────────┐
│ Database Cache (Query cache)                │
│ • Frequent queries, indexes                 │
│ • Latency: 10-100ms                         │
│ • Control: Medium                           │
└─────────────────────────────────────────────┘
```

---

## 🎨 Cache Key Naming Conventions

### Best Practices:
```python
✅ GOOD:
"user:123"
"product:456:details"
"session:abc123"
"leaderboard:daily:2026-02-18"
"api:v1:users:list:page:1"

❌ BAD:
"123"                    # No context
"userdata"               # No ID
"cache_temp"             # Unclear
"x"                      # Meaningless
```

### Pattern:
```
{entity}:{id}:{attribute}:{version}
```

---

## 🔐 Security Checklist

- [ ] Enable Redis AUTH/ACL
- [ ] Use TLS for cache connections
- [ ] Don't cache PII without encryption
- [ ] Set firewall rules (only app servers can access)
- [ ] Regular security updates
- [ ] Monitor for unusual access patterns
- [ ] Use separate cache for sensitive data

---

## 💡 Pro Tips

### 1. Cache warming
```python
# Pre-populate cache before traffic
def warm_cache():
    popular_items = get_top_100_products()
    for item in popular_items:
        cache.set(f"product:{item.id}", item, ttl=3600)
```

### 2. Graceful degradation
```python
def get_data(key):
    try:
        return cache.get(key) or db.get(key)
    except CacheError:
        logger.warning("Cache down, using DB")
        return db.get(key)
```

### 3. Cache versioning
```python
# Easy to invalidate entire version
CACHE_VERSION = "v2"
key = f"user:{user_id}:{CACHE_VERSION}"
```

### 4. Compression for large values
```python
import zlib
compressed = zlib.compress(pickle.dumps(large_data))
cache.set(key, compressed)
```

### 5. Multi-get optimization
```python
# Instead of N queries
users = cache.mget([f"user:{id}" for id in user_ids])
```

---

## 📚 One-Liner Definitions

**Cache Hit:** Data found in cache (fast ✅)  
**Cache Miss:** Data not in cache, fetch from source (slow ❌)  
**TTL (Time To Live):** How long data stays in cache  
**Eviction:** Removing data from cache (when full)  
**Invalidation:** Deleting stale data from cache  
**Cache Warming:** Pre-loading cache with data  
**Cache Stampede:** Multiple requests rebuilding cache simultaneously  
**Hot Key:** Single popular key causing bottleneck  
**Distributed Cache:** Cache shared across multiple servers  
**Consistent Hashing:** Efficient key distribution across cache nodes  

---

## 🚀 Quick Start - Redis Cache Example

### Installation:
```bash
# Docker
docker run -d -p 6379:6379 redis:latest

# Python client
pip install redis
```

### Code:
```python
import redis
from functools import wraps
import time

# Connect to Redis
cache = redis.Redis(host='localhost', port=6379, db=0)

# Decorator for caching
def cached(ttl=3600):
    def decorator(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            # Create cache key from function name and args
            cache_key = f"{func.__name__}:{str(args)}:{str(kwargs)}"
            
            # Try cache first
            cached_value = cache.get(cache_key)
            if cached_value:
                print(f"Cache HIT: {cache_key}")
                return eval(cached_value)  # Deserialize
            
            # Cache miss - call function
            print(f"Cache MISS: {cache_key}")
            result = func(*args, **kwargs)
            
            # Store in cache
            cache.setex(cache_key, ttl, str(result))
            return result
        return wrapper
    return decorator

# Usage
@cached(ttl=300)
def get_user(user_id):
    # Simulate expensive database query
    time.sleep(2)
    return {"id": user_id, "name": "John Doe"}

# First call: Cache MISS (2 seconds)
user = get_user(123)

# Second call: Cache HIT (instant!)
user = get_user(123)
```

---

## 📞 When to Call for Help

### Signs You Need Better Caching:

🚨 **Critical Issues:**
- Database is overwhelmed (>80% CPU)
- Response times >1 second
- Frequent timeouts

⚠️ **Warning Signs:**
- Cache hit rate <60%
- High eviction rate
- Memory constantly at 100%

### Scaling Checklist:

1. **Overwhelmed?** → Add more cache nodes
2. **Out of memory?** → Increase maxmemory or evict more aggressively
3. **Low hit rate?** → Increase TTL or warm cache
4. **Slow queries?** → Add indexes or pre-compute
5. **Hot keys?** → Replicate or use local cache

---

**Keep this cheatsheet handy for quick reference! 🎯**
