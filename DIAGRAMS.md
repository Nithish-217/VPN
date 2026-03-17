# Python VPN System - Visual Diagrams

## System Architecture Overview

```mermaid
graph TB
    subgraph "User Device"
        A[User Application] --> B[OS Network Stack]
        B --> C[TUN Interface tun0]
        C --> D[VPN Client]
    end
    
    subgraph "Encrypted Tunnel"
        D -->|AES-256 Encrypted| E[TCP Connection]
    end
    
    subgraph "VPN Server"
        E --> F[VPN Server]
        F --> G[Crypto Module]
        G --> H[Packet Handler]
    end
    
    subgraph "Internet"
        H --> I[Destination Server]
    end
    
    style D fill:#f9f,stroke:#333,stroke-width:4px
    style F fill:#9ff,stroke:#333,stroke-width:4px
    style E fill:#ffc,stroke:#333,stroke-width:2px
```

## Connection Flow Sequence

```mermaid
sequenceDiagram
    participant User
    participant Client
    participant Server
    participant Internet
    
    User->>Client: Start VPN
    activate Client
    Client->>Client: Create TUN Interface
    
    Client->>Server: Connect TCP (IP:PORT)
    activate Server
    Server->>Server: Accept Connection
    
    Client->>Server: Send Credentials
    Server->>Server: Verify Credentials
    Server-->>Client: Auth Response
    
    Client->>Server: Send Public Key (DH)
    Server->>Server: Generate Shared Secret
    Server->>Client: Send Public Key (DH)
    Client->>Client: Generate Shared Secret
    
    Client->>Server: Send Tunnel Config
    Server-->>Client: Tunnel Established
    
    loop Traffic Flow
        User->>Client: Packet to Internet
        Client->>Client: Encrypt (AES-256)
        Client->>Server: Send Encrypted
        Server->>Server: Decrypt
        Server->>Internet: Forward Packet
        
        Internet->>Server: Response
        Server->>Server: Encrypt Response
        Server->>Client: Send Encrypted
        Client->>Client: Decrypt
        Client->>User: Deliver Response
    end
    
    User->>Client: Stop VPN
    Client->>Server: Disconnect
    deactivate Server
    deactivate Client
```

## VPN Server Architecture

```mermaid
graph TB
    A[VPN Server Main] --> B[TCP Server]
    B --> C[Connection Listener]
    
    C --> D[Client 1 Handler]
    C --> E[Client 2 Handler]
    C --> F[Client N Handler]
    
    D --> D1[Authentication]
    D --> D2[Key Exchange]
    D --> D3[Crypto Manager]
    D --> D4[Packet Forwarder]
    
    E --> E1[Authentication]
    E --> E2[Key Exchange]
    E --> E3[Crypto Manager]
    E --> E4[Packet Forwarder]
    
    F --> F1[Authentication]
    F --> F2[Key Exchange]
    F --> F3[Crypto Manager]
    F --> F4[Packet Forwarder]
    
    D4 --> G[Internet Gateway]
    E4 --> G
    F4 --> G
    
    style A fill:#f9f,stroke:#333
    style G fill:#9ff,stroke:#333
```

## VPN Client Architecture

```mermaid
graph TB
    subgraph "VPN Client"
        A[Main Client] --> B[Connection Manager]
        B --> C[Auth Handler]
        B --> D[Key Exchange]
        B --> E[Traffic Handler]
        
        E --> F[Read from TUN Task]
        E --> G[Read from Server Task]
        
        F --> H[Crypto Manager]
        G --> H
        
        H --> I[TCP Connection]
    end
    
    subgraph "OS Level"
        J[User Applications] --> K[Network Stack]
        K --> L[TUN Interface]
        L --> F
        G --> L
    end
    
    style A fill:#f9f,stroke:#333
    style L fill:#9ff,stroke:#333
    style I fill:#ffc,stroke:#333
```

## Encryption/Decryption Flow

```mermaid
graph LR
    subgraph "Encryption (Sender)"
        A[Original IP Packet] --> B[Generate Random Nonce]
        B --> C[AES-256-CFB Cipher]
        C --> D[Shared Secret Key]
        D --> E[Encrypt]
        E --> F[Nonce + Ciphertext]
    end
    
    F -->|Transmit| G
    
    subgraph "Decryption (Receiver)"
        G[Nonce + Ciphertext] --> H[Extract Nonce]
        H --> I[Extract Ciphertext]
        I --> J[AES-256-CFB Cipher]
        J --> K[Shared Secret Key]
        K --> L[Decrypt]
        L --> M[Original Packet Restored]
    end
    
    style A fill:#f9f,stroke:#333
    style M fill:#9ff,stroke:#333
    style F fill:#ffc,stroke:#333
    style G fill:#ffc,stroke:#333
```

## Diffie-Hellman Key Exchange Visualization

```mermaid
sequenceDiagram
    participant Client
    participant Server
    
    Note over Client,Server: Goal: Generate shared secret without transmitting it
    
    Client->>Client: Generate Private Key A
    Client->>Client: Compute Public Key a = g^A mod p
    Client->>Server: Send Public Key a
    
    Server->>Server: Generate Private Key B
    Server->>Server: Compute Public Key b = g^B mod p
    Server->>Server: Compute Shared S = a^B mod p
    Server->>Client: Send Public Key b
    
    Client->>Client: Compute Shared S = b^A mod p
    
    Note over Client,Server: Both now have same shared secret S
    Note over Client,Server: S was never transmitted!
    
    style Client fill:#f9f,stroke:#333
    style Server fill:#9ff,stroke:#333
```

## Data Packet Journey

```mermaid
flowchart TD
    Start([User opens google.com]) --> A[DNS Query Generated]
    A --> B[IP Packet Created]
    B --> C{Routing Decision}
    C -->|Default Route| D[TUN Interface tun0]
    
    D --> E[VPN Client Reads Packet]
    E --> F[Add Length Prefix]
    F --> G[Encrypt with AES-256]
    G --> H[Send via TCP Socket]
    
    H --> I[Encrypted Tunnel]
    I --> J[VPN Server Receives]
    
    J --> K[Decrypt Packet]
    K --> L[Parse IP Header]
    L --> M[Extract Destination IP]
    M --> N[Forward to Internet]
    
    N --> O[Google Server Receives]
    O --> P[Google Sends Response]
    
    P --> Q[VPN Server Receives]
    Q --> R[Encrypt Response]
    R --> S[Send through Tunnel]
    
    S --> T[VPN Client Receives]
    T --> U[Decrypt Response]
    U --> V[Write to TUN Interface]
    
    V --> W[OS Delivers to Browser]
    W --> End([Webpage Displayed])
    
    style Start fill:#f9f,stroke:#333
    style End fill:#9ff,stroke:#333
    style G fill:#ffc,stroke:#333
    style K fill:#ffc,stroke:#333
    style U fill:#ffc,stroke:#333
    style I fill:#cfc,stroke:#333
```

## Authentication State Machine

```mermaid
stateDiagram-v2
    [*] --> Disconnected
    
    Disconnected --> Connecting: Client initiates
    Connecting --> Authenticating: TCP established
    Authenticating --> KeyExchange: Auth successful
    Authenticating --> Disconnecting: Auth failed
    
    KeyExchange --> Configuring: Keys exchanged
    KeyExchange --> Disconnecting: Key exchange failed
    
    Configuring --> Forwarding: Tunnel configured
    Configuring --> Disconnecting: Config failed
    
    Forwarding --> Forwarding: Traffic flowing
    Forwarding --> Disconnecting: Error or user request
    
    Disconnecting --> [*]: Connection closed
    
    note right of Forwarding
        All traffic encrypted
        with AES-256-CFB
    end note
    
    note right of KeyExchange
        X25519 DH exchange
        Perfect forward secrecy
    end note
```

## Network Topology Examples

### Home Network Deployment

```mermaid
graph TB
    A[Internet] --> B[Home Router]
    B --> C[Switch/WiFi]
    
    C --> D[Laptop with VPN Client]
    C --> E[Phone with VPN Client]
    C --> F[VPN Server PC]
    
    F --> G[Port Forwarding<br/>8080]
    G --> B
    
    style F fill:#f9f,stroke:#333,stroke-width:4px
    style D fill:#9ff,stroke:#333
    style E fill:#9ff,stroke:#333
```

### Cloud VPS Deployment

```mermaid
graph TB
    A[Internet] --> B[Cloud Provider]
    B --> C[VPS Instance]
    
    C --> D[VPN Server<br/>Ubuntu 22.04]
    D --> E[Firewall<br/>Port 8080]
    
    E --> B
    
    F[VPN Client - Home] -.->|Encrypted| D
    G[VPN Client - Mobile] -.->|Encrypted| D
    H[VPN Client - Office] -.->|Encrypted| D
    
    style D fill:#f9f,stroke:#333,stroke-width:4px
    style F fill:#9ff,stroke:#333
    style G fill:#9ff,stroke:#333
    style H fill:#9ff,stroke:#333
```

### Corporate HA Deployment

```mermaid
graph TB
    A[Internet] --> B[Corporate Firewall]
    B --> C[Load Balancer]
    
    C --> D[VPN Server 1<br/>Port 8080]
    C --> E[VPN Server 2<br/>Port 8081]
    C --> F[VPN Server 3<br/>Port 8082]
    
    D --> G[Active Directory<br/>LDAP Auth]
    E --> G
    F --> G
    
    D --> H[Central Logging<br/>ELK Stack]
    E --> H
    F --> H
    
    I[VPN Clients] --> B
    
    style C fill:#ffc,stroke:#333
    style D fill:#f9f,stroke:#333
    style E fill:#f9f,stroke:#333
    style F fill:#f9f,stroke:#333
```

## Security Layers

```mermaid
graph TB
    subgraph "Security Layers (Outside-In)"
        A[Firewall Rules] --> B[Authentication Layer]
        B --> C[Key Exchange Layer]
        C --> D[Encryption Layer]
        D --> E[Application Layer]
    end
    
    subgraph "Protection Provided"
        A --> A1[Port filtering<br/>IP whitelisting]
        B --> B1[Username/Password<br/>Failed attempt logging]
        C --> C1[X25519 DH<br/>Perfect forward secrecy]
        D --> D1[AES-256-CFB<br/>Random nonce per packet]
        E --> E1[Input validation<br/>Error handling]
    end
    
    style A fill:#ffc,stroke:#333
    style B fill:#f9f,stroke:#333
    style C fill:#9ff,stroke:#333
    style D fill:#cfc,stroke:#333
```

## Performance Characteristics

```mermaid
xychart-beta
    title "VPN Overhead by Operation"
    x-axis ["Base", "+Auth", "+Key Exchange", "+Encryption", "Total"]
    y-axis "Latency (ms)" 0 --> 50
    bar [5, 8, 15, 25, 35]
    line [5, 8, 15, 25, 35]
```

## Comparison with Other VPN Protocols

```mermaid
quadrantChart
    title "VPN Protocol Comparison"
    x-axis "Easy Setup" --> "Complex Setup"
    y-axis "Lower Performance" --> "Higher Performance"
    quadrant-1 "Modern & Fast"
    quadrant-2 "Mature & Robust"
    quadrant-3 "Educational & Simple"
    quadrant-4 "Legacy & Complex"
    "Our VPN": [0.2, 0.3]
    "WireGuard": [0.7, 0.9]
    "OpenVPN": [0.4, 0.7]
    "IPSec": [0.3, 0.8]
```

---

**Note:** These diagrams use Mermaid syntax for visualization. View in a Markdown editor that supports Mermaid diagrams for best experience.
