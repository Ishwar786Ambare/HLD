# Load Balancer & Consistent Hashing - High Level Design

## 🎯 What is a Load Balancer?

A **Load Balancer** is a reverse proxy that distributes incoming network traffic across multiple backend servers, ensuring no single server gets overwhelmed.

---

## 🔍 Why Use a Load Balancer?

| Benefit | Description |
|---------|-------------|
| **Scalability** | Add more servers to handle increased traffic |
| **Resilience/Availability** | Failover to healthy servers if one fails |
| **Performance** | Distribute load evenly across servers |
| **Security** | Provides abstraction layer and DDoS protection |
| **SSL Offloading** | Handles SSL encryption/decryption centrally |

---

## ⚙️ How Does It Work?

```mermaid
sequenceDiagram
    participant Client
    participant DNS
    participant LB as Load Balancer
    participant S1 as Server 1
    participant S2 as Server 2
    participant S3 as Server 3
    
    Client->>DNS: Request example.com
    DNS-->>Client: Returns Load Balancer IP
    Client->>LB: HTTP Request
    
    Note over LB: Health Check<br/>Select Server<br/>(Algorithm)
    
    LB->>S2: Forward Request
    S2->>S2: Process Request
    S2-->>LB: Response
    LB-->>Client: Response
```

### Key Components:

1. **Reverse Proxy**: Acts as intermediary between clients and servers
2. **Health Checks**: Periodically pings servers to ensure they're online
3. **Routing Algorithms**:
   - **Round Robin**: Sequential distribution
   - **Least Connections**: Routes to server with fewest active connections
   - **IP Hash**: Uses client IP for session persistence

---

## 📊 Types of Load Balancers

```mermaid
graph TD
    A[Load Balancers] --> B[Layer 4 - L4]
    A --> C[Layer 7 - L7]
    
    B --> D[Transport Level<br/>TCP/UDP]
    B --> E[Routes by:<br/>IP + Port]
    
    C --> F[Application Level<br/>HTTP/HTTPS]
    C --> G[Routes by:<br/>URL, Headers, Cookies]
    
    style B fill:#e1f5ff
    style C fill:#fff4e1
```

---

## 🔄 Consistent Hashing

### The Problem with Traditional Hashing

**Traditional**: `server = hash(key) % number_of_servers`

❌ **Issue**: When you add/remove servers, almost ALL keys get remapped → massive cache invalidation

### The Solution: Consistent Hashing

```mermaid
graph LR
    subgraph "Hash Ring (0 to 2^32)"
        A[Server A<br/>Hash: 100]
        B[Server B<br/>Hash: 200]
        C[Server C<br/>Hash: 300]
        K1[Key 1<br/>Hash: 150]
        K2[Key 2<br/>Hash: 250]
        K3[Key 3<br/>Hash: 50]
    end
    
    K3 -.Clockwise.-> A
    K1 -.Clockwise.-> B
    K2 -.Clockwise.-> C
    
    style A fill:#90EE90
    style B fill:#87CEEB
    style C fill:#FFB6C1
    style K1 fill:#FFE4B5
    style K2 fill:#FFE4B5
    style K3 fill:#FFE4B5
```

### How It Works:

1. **Hash Ring**: Imagine a circular ring from 0 to 2^32 - 1
2. **Hash Servers**: Each server is hashed onto the ring
3. **Hash Keys**: Each request/key is hashed onto the ring
4. **Mapping Rule**: A key is assigned to the **first server** encountered moving **clockwise**

### Benefits:

✅ **Minimal Reorganization**: When a server is added/removed, only `~1/n` keys need remapping (not all)

✅ **Cache Efficiency**: Most cached data remains valid after scaling

---

## 🚀 Complete Workflow

```mermaid
flowchart TD
    Start[Client Request] --> DNS[DNS Resolution]
    DNS --> LB{Load Balancer}
    
    LB --> HC[Health Check Servers]
    HC --> Algo{Select Algorithm}
    
    Algo -->|Round Robin| RR[Sequential Selection]
    Algo -->|Least Conn| LC[Fewest Connections]
    Algo -->|Consistent Hash| CH[Hash Ring Lookup]
    
    RR --> Route[Route to Server]
    LC --> Route
    CH --> Route
    
    Route --> Server[Backend Server]
    Server --> Process[Process Request]
    Process --> Response[Send Response]
    Response --> LB
    LB --> Client[Client Receives Response]
    
    style LB fill:#4CAF50,color:#fff
    style Server fill:#2196F3,color:#fff
    style Client fill:#FF9800,color:#fff
```

---

## 📝 Quick Summary

| Component | Purpose |
|-----------|---------|
| **Load Balancer** | Distributes traffic across servers |
| **Health Checks** | Monitors server availability |
| **L4 Load Balancer** | Routes based on IP/Port (faster) |
| **L7 Load Balancer** | Routes based on content (smarter) |
| **Consistent Hashing** | Minimizes remapping when scaling |

---

## 🎓 Key Takeaways

1. Load balancers improve **scalability**, **availability**, and **performance**
2. **Layer 4** is faster but less flexible; **Layer 7** is content-aware
3. **Consistent hashing** is crucial for distributed systems with caching
4. Health checks ensure traffic only goes to healthy servers
5. Different algorithms suit different use cases
