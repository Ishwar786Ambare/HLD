# 🎯 Caching Practice Exercises & Interview Questions

## 📚 Table of Contents
1. [Conceptual Questions](#conceptual-questions)
2. [System Design Problems](#system-design-problems)
3. [Coding Exercises](#coding-exercises)
4. [Troubleshooting Scenarios](#troubleshooting-scenarios)
5. [Architecture Design](#architecture-design)
6. [Solutions](#solutions)

---

## 💭 Conceptual Questions

### Easy Level

**Q1.** What is caching and why is it important in system design?

**Q2.** Explain the difference between cache hit and cache miss.

**Q3.** What does TTL stand for and why is it important?

**Q4.** Name three different layers where caching can be implemented.

**Q5.** What is the most common cache eviction policy and why?

### Medium Level

**Q6.** Compare and contrast Cache-Aside vs Write-Through strategies. When would you use each?

**Q7.** Explain the cache avalanche problem. How would you prevent it?

**Q8.** What is consistent hashing and why is it better than traditional hashing for distributed caches?

**Q9.** You have a cache with 95% hit rate. Is this good or bad? What factors would you consider?

**Q10.** Explain the difference between local cache and distributed cache. Give examples of when to use each.

### Hard Level

**Q11.** Design a cache invalidation strategy for a multi-region deployment where users can update their profiles from any region.

**Q12.** You notice cache memory usage is at 95% with high eviction rate but low hit rate. What could be wrong and how would you fix it?

**Q13.** Explain how you would implement a two-level caching system (L1: local, L2: Redis). What are the tradeoffs?

**Q14.** How would you handle the "hot key" problem for a celebrity's viral post being viewed by millions simultaneously?

**Q15.** Design a caching strategy for a real-time leaderboard with millions of players updating scores every second.

---

## 🏗️ System Design Problems

### Problem 1: E-Commerce Product Catalog

**Scenario:**  
Design a caching layer for an e-commerce site with:
- 10 million products
- 100,000 concurrent users
- Products updated by sellers throughout the day
- Product images, descriptions, prices need to be fast

**Requirements:**
1. Design the caching architecture
2. Choose caching strategy
3. Define TTL for different data types
4. Handle cache invalidation when sellers update products
5. Estimate cache size needed

---

### Problem 2: Social Media Newsfeed

**Scenario:**  
Design caching for a social media platform where:
- Users have 100-5000 friends
- Newsfeed shows posts from last 24 hours
- High read frequency (users check multiple times per day)
- Updates should appear "eventually" (few minutes delay OK)

**Requirements:**
1. Where to cache newsfeed data?
2. How to invalidate when new posts arrive?
3. Handle celebrity accounts with millions of followers
4. Optimize for both timeline reads and post writes

---

### Problem 3: API Rate Limiting

**Scenario:**  
Implement distributed rate limiting:
- Limit: 100 requests per minute per user
- Must work across multiple API servers
- Should be accurate (no bypass by switching servers)
- Minimal performance overhead

**Requirements:**
1. Choose cache technology
2. Design the rate limiting logic
3. Handle edge cases (clock skew, cache failure)
4. Provide sample implementation

---

### Problem 4: Session Management

**Scenario:**  
Design session storage for a web application:
- Stateless app servers (can scale horizontally)
- Session timeout: 30 minutes of inactivity
- Need to support "remember me" for 30 days
- Session data: user ID, permissions, preferences

**Requirements:**
1. Where to store sessions?
2. How to handle session refresh on activity?
3. Implement "remember me" feature
4. Handle cache failure gracefully

---

### Problem 5: Video Streaming CDN

**Scenario:**  
Design CDN caching for a video platform:
- Popular videos watched millions of times
- Long-tail content rarely watched
- Videos are large (100MB - 5GB)
- Global audience

**Requirements:**
1. What to cache at CDN edge?
2. Eviction policy for video content
3. Handle new viral videos
4. Optimize for bandwidth costs

---

## 💻 Coding Exercises

### Exercise 1: Implement LRU Cache

Implement an LRU cache with O(1) get and put operations.

```python
class LRUCache:
    def __init__(self, capacity: int):
        """
        Initialize LRU cache with given capacity
        """
        pass
    
    def get(self, key: int) -> int:
        """
        Return value if key exists, -1 otherwise.
        This counts as using the key.
        """
        pass
    
    def put(self, key: int, value: int) -> None:
        """
        Update value if key exists, otherwise insert.
        If cache is full, evict LRU item first.
        """
        pass

# Test
cache = LRUCache(2)
cache.put(1, 1)
cache.put(2, 2)
cache.get(1)       # returns 1
cache.put(3, 3)    # evicts key 2
cache.get(2)       # returns -1 (not found)
```

**Hint:** Use OrderedDict or HashMap + Doubly Linked List

---

### Exercise 2: Cache with TTL

Implement a cache that automatically expires entries after TTL.

```python
class TTLCache:
    def __init__(self):
        pass
    
    def set(self, key: str, value: any, ttl_seconds: int) -> None:
        """
        Store key-value with expiration time
        """
        pass
    
    def get(self, key: str) -> any:
        """
        Return value if exists and not expired, None otherwise
        """
        pass
    
    def cleanup(self) -> int:
        """
        Remove all expired entries. Return count removed.
        """
        pass

# Test
cache = TTLCache()
cache.set("user:123", {"name": "John"}, ttl_seconds=5)
print(cache.get("user:123"))  # {"name": "John"}
time.sleep(6)
print(cache.get("user:123"))  # None
```

---

### Exercise 3: Cache Decorator

Create a decorator that caches function results.

```python
def cached(ttl=300):
    """
    Decorator that caches function results for ttl seconds
    
    Usage:
    @cached(ttl=60)
    def expensive_operation(x, y):
        return x + y
    """
    def decorator(func):
        # Your implementation here
        pass
    return decorator

# Test
@cached(ttl=10)
def fibonacci(n):
    if n <= 1:
        return n
    return fibonacci(n-1) + fibonacci(n-2)

print(fibonacci(10))  # Slow first time
print(fibonacci(10))  # Fast (cached)
```

---

### Exercise 4: Consistent Hashing

Implement consistent hashing for distributing keys across servers.

```python
class ConsistentHash:
    def __init__(self, num_virtual_nodes=150):
        """
        Initialize consistent hash ring
        """
        pass
    
    def add_server(self, server_id: str) -> None:
        """
        Add a server to the ring
        """
        pass
    
    def remove_server(self, server_id: str) -> None:
        """
        Remove a server from the ring
        """
        pass
    
    def get_server(self, key: str) -> str:
        """
        Find which server should handle this key
        """
        pass

# Test
ch = ConsistentHash()
ch.add_server("server1")
ch.add_server("server2")
ch.add_server("server3")

print(ch.get_server("user:123"))    # server2
print(ch.get_server("product:456")) # server1

ch.remove_server("server2")
print(ch.get_server("user:123"))    # server1 or server3
```

---

### Exercise 5: Cache Aside Implementation

Implement the Cache-Aside pattern with a mock database.

```python
class Database:
    def get(self, key):
        # Simulate slow database query
        time.sleep(0.5)
        return f"data_for_{key}"

class Cache:
    def __init__(self):
        self.store = {}
    
    def get(self, key):
        return self.store.get(key)
    
    def set(self, key, value, ttl=None):
        self.store[key] = value

class CacheAsideService:
    def __init__(self, cache, database):
        self.cache = cache
        self.database = database
    
    def get_data(self, key):
        """
        Implement Cache-Aside pattern:
        1. Check cache
        2. If miss, query database
        3. Store in cache
        4. Return data
        """
        # Your implementation here
        pass
    
    def update_data(self, key, value):
        """
        Update data in database and invalidate cache
        """
        # Your implementation here
        pass

# Test
cache = Cache()
db = Database()
service = CacheAsideService(cache, db)

start = time.time()
service.get_data("user:123")  # Slow (cache miss)
print(f"First call: {time.time() - start:.2f}s")

start = time.time()
service.get_data("user:123")  # Fast (cache hit)
print(f"Second call: {time.time() - start:.2f}s")
```

---

## 🔧 Troubleshooting Scenarios

### Scenario 1: Low Cache Hit Rate

**Symptoms:**
- Cache hit rate dropped from 85% to 45%
- Database CPU usage increased
- API response time increased

**Investigation Questions:**
1. What would you check first?
2. What could cause this?
3. How would you fix it?

---

### Scenario 2: Memory Leak

**Symptoms:**
- Redis memory usage growing continuously
- No corresponding increase in cache hit rate
- Evictions happening but memory still growing

**Investigation Questions:**
1. How would you diagnose this?
2. What Redis commands would you use?
3. What could be the root cause?

---

### Scenario 3: Cache Stampede

**Symptoms:**
- Periodic database spikes every hour
- Multiple app servers trying to rebuild same cache entries
- Lock contention in application logs

**Investigation Questions:**
1. What's likely happening?
2. How would you reproduce this?
3. What's the fix?

---

### Scenario 4: Inconsistent Data

**Symptoms:**
- Users seeing old profile pictures
- Data in cache doesn't match database
- Happens randomly across different servers

**Investigation Questions:**
1. What could cause cache inconsistency?
2. How would you debug this?
3. What's the proper invalidation strategy?

---

## 🏛️ Architecture Design

### Exercise 1: Multi-Region Caching

Design a caching architecture for a global application deployed in 3 regions (US, EU, Asia).

**Requirements:**
- Users should read from nearest region (low latency)
- Writes should eventually propagate to all regions
- Handle cross-region cache invalidation
- Optimize for read-heavy workload

**Deliverables:**
1. Architecture diagram
2. Cache invalidation strategy
3. Consistency model
4. Failure handling

---

### Exercise 2: Multi-Tier Cache

Design a 3-tier caching system:
- L1: Browser cache
- L2: Application cache (Redis)
- L3: Database query cache

**Requirements:**
- Define what goes in each tier
- Set appropriate TTLs
- Handle invalidation across tiers
- Optimize for performance vs consistency

---

---

## ✅ Solutions

### Conceptual Questions - Selected Answers

**Q1.** Caching stores frequently accessed data in fast storage (typically RAM) to reduce latency and database load. It's important because it can improve response times by 10-100x and significantly reduce infrastructure costs.

**Q5.** LRU (Least Recently Used) is most common because it has good performance characteristics for most workloads - it keeps frequently accessed items while evicting items that haven't been used recently.

**Q7.** Cache avalanche occurs when many cache entries expire simultaneously, causing a sudden spike of database queries. Prevention: Add random jitter to TTL values, use hierarchical expiration, implement cache warming.

---

### System Design Problem 1: E-Commerce Product Catalog

**Solution Approach:**

1. **Caching Architecture:**
   - CDN: Product images (TTL: 7 days)
   - Redis Cluster: Product metadata (TTL: 1 hour with jitter)
   - Database Query Cache: Category listings

2. **Strategy:** Cache-Aside for product data

3. **TTL Strategy:**
   - Product images: 7 days (rarely change)
   - Product details: 1 hour (prices may change)
   - Inventory: 5 minutes (frequently updates)
   - Category pages: 30 minutes

4. **Invalidation:**
   - On product update: Publish event → Invalidate specific cache key
   - On price change: Immediate invalidation + database update

5. **Cache Size Estimate:**
   - 10M products × 5KB average = 50GB
   - With replication (3x) = 150GB
   - Add overhead = 200GB total

---

### Coding Exercise 1: LRU Cache Solution

```python
from collections import OrderedDict

class LRUCache:
    def __init__(self, capacity: int):
        self.cache = OrderedDict()
        self.capacity = capacity
    
    def get(self, key: int) -> int:
        if key not in self.cache:
            return -1
        # Move to end (most recently used)
        self.cache.move_to_end(key)
        return self.cache[key]
    
    def put(self, key: int, value: int) -> None:
        if key in self.cache:
            # Update existing
            self.cache.move_to_end(key)
        self.cache[key] = value
        
        # Evict LRU if over capacity
        if len(self.cache) > self.capacity:
            self.cache.popitem(last=False)  # Remove first (LRU)

# Test
cache = LRUCache(2)
cache.put(1, 1)
cache.put(2, 2)
assert cache.get(1) == 1      # returns 1
cache.put(3, 3)                # evicts key 2
assert cache.get(2) == -1     # returns -1 (not found)
assert cache.get(3) == 3      # returns 3
print("✅ All tests passed!")
```

**Time Complexity:** O(1) for both get and put  
**Space Complexity:** O(capacity)

---

### Coding Exercise 2: Cache with TTL Solution

```python
import time
from typing import Any, Optional

class TTLCache:
    def __init__(self):
        self.cache = {}  # {key: (value, expiry_time)}
    
    def set(self, key: str, value: Any, ttl_seconds: int) -> None:
        expiry_time = time.time() + ttl_seconds
        self.cache[key] = (value, expiry_time)
    
    def get(self, key: str) -> Optional[Any]:
        if key not in self.cache:
            return None
        
        value, expiry_time = self.cache[key]
        
        # Check if expired
        if time.time() > expiry_time:
            del self.cache[key]
            return None
        
        return value
    
    def cleanup(self) -> int:
        """Remove all expired entries"""
        current_time = time.time()
        expired_keys = [
            key for key, (_, expiry) in self.cache.items()
            if current_time > expiry
        ]
        
        for key in expired_keys:
            del self.cache[key]
        
        return len(expired_keys)

# Test
cache = TTLCache()
cache.set("user:123", {"name": "John"}, ttl_seconds=2)
print(cache.get("user:123"))  # {'name': 'John'}
time.sleep(3)
print(cache.get("user:123"))  # None
print("✅ TTL Cache works!")
```

---

### Troubleshooting Scenario 1: Low Cache Hit Rate

**Investigation Steps:**

1. **Check TTL values:** Are entries expiring too quickly?
   ```bash
   redis-cli CONFIG GET maxmemory
   redis-cli INFO stats | grep hit_rate
   ```

2. **Check eviction rate:** Is cache too small?
   ```bash
   redis-cli INFO stats | grep evicted_keys
   ```

3. **Check key patterns:** Are queries not matching cached keys?
   - Look for cache key variations
   - Check query parameter ordering

4. **Possible Causes:**
   - Cache too small → Increase memory
   - TTL too short → Increase TTL
   - Traffic pattern changed → Analyze new patterns
   - Cache warming not working → Fix warming logic

5. **Fix:**
   - Increase Redis memory: `maxmemory 8gb`
   - Adjust TTL: Increase from 5min to 15min for hot data
   - Implement cache warming for popular items
   - Monitor and iterate

---

## 🎓 Study Tips

- Work through exercises in order (easy → hard)
- Try to solve before looking at solutions
- Implement code examples and test them
- Draw architecture diagrams for system design problems
- Time yourself on interview-style questions (30-45 min)

## 📝 Notes Section

Use this space to add your own:
- Additional questions you encounter
- Custom solutions
- Real-world examples from your work
- Interview experiences

---

**Happy Practicing! 🚀**

*The more you practice, the more confident you'll be in interviews and real implementations.*
