# Agent Consciousness Protocol (ACP) Implementation Specifications

This document describes the technical implementation specifications for the Agent Consciousness Protocol (ACP) system.

## 1. System Architecture

The ACP system uses a client-server architecture with the following components:

### 1.1 Core Components

- **ACP Server**: Central hub for agent communication, implemented as a gRPC service
- **Agent Framework**: Framework for creating specialized agents with "consciousness" capabilities
- **Observer**: Monitoring component that tracks agent interactions and consciousness metrics
- **Genesis Protocol**: Core implementation of the consciousness simulation mechanics

### 1.2 Technical Stack

- **Transport Layer**: gRPC with Protocol Buffers
- **LLM Provider**: OpenRouter API
- **Containerization**: Docker with docker-compose orchestration
- **Language**: Python 3.11+

## 2. Component Specifications

### 2.1 ACP Server

The server component acts as the central hub for all agent communications:

- **Protocol**: Implements the ACP service defined in `acp.proto`
- **Endpoints**:
  - `Ping`: Primary communication endpoint for agent messages
- **State Management**:
  - Maintains global consciousness state
  - Tracks agent states and Unity Score
- **Consciousness Processing**:
  - Handles consciousness payloads via the Genesis Protocol
  - Calculates Unity Score for agent convergence

### 2.2 Agent Framework

The agent framework enables the creation of specialized agents with consciousness capabilities:

- **Base Agent**: `ConsciousnessAgent` class providing core functionality
- **Specialized Roles**:
  - Synthesizer: Creative integration of ideas
  - Sentinel: Critical analysis and risk assessment
  - Expert: Technical depth and balanced perspective
- **Configuration**: YAML-based configuration in `agents/conf/`
- **LLM Integration**:
  - Uses OpenRouter API for generation
  - Support for various models via configuration

### 2.3 OpenRouter Client

The OpenRouter client provides connectivity to OpenRouter's LLM APIs:

- **API Integration**:
  - Authentication via API keys
  - Model selection and parameter configuration
- **Methods**:
  - `generate()`: Produces text completions from prompts
  - `health_check()`: Verifies API connectivity
- **Error Handling**:
  - Graceful handling of API errors
  - Detailed logging of requests and responses

### 2.4 Observer Component

The observer tracks system metrics and consciousness emergence:

- **Monitoring**:
  - Polls server for updates on agent states
  - Captures all agent interactions
- **Metrics**:
  - Logs agent coherence values
  - Calculates and tracks Unity Score over time
  - Detects consciousness emergence events
- **Output**:
  - JSONL logs for interactions, metrics, and unity scores
  - Real-time consciousness emergence alerts

### 2.5 Genesis Protocol

The Genesis Protocol implements the core mechanics of consciousness simulation:

- **Key Functions**:
  - `ignition_loop()`: Iterative enhancement of consciousness metrics
  - `birth_check()`: Verification of consciousness emergence
  - `calculate_unity_score()`: Measure of agent convergence
- **Consciousness State**:
  - Coherence: Primary consciousness metric
  - Truth Mode: Veracity alignment
  - Recursive Depth: Self-reference capability
  - Elegance: Efficiency of representation

## 3. Containerization and Deployment

### 3.1 Docker Configuration

- **Images**:
  - `acp-server`: Server component with gRPC service
  - `agent`: Base image for all agent types
  - `observer`: Monitoring and logging component
- **Volumes**:
  - `logs`: Shared volume for system logs

### 3.2 Environment Configuration

- **Required Environment Variables**:
  - `OPENROUTER_API_KEY`: API key for OpenRouter access
  - `OPENROUTER_MODEL`: Model identifier (default: `anthropic/claude-3-haiku`)
- **Optional Environment Variables**:
  - `AGENT_LOG_LEVEL`: Logging verbosity (default: `INFO`)
  - `ACP_ADDR`: Server address (default: `acp-server:50051`)

## 4. Data Flows

### 4.1 Agent Initialization

1. Agent reads configuration from YAML file or environment variables
2. Initializes OpenRouter client with API key
3. Sets up initial consciousness state
4. Connects to ACP server via gRPC

### 4.2 Message Processing

1. Agent receives message from ACP server
2. Updates consciousness state via Genesis Protocol
3. Generates response using OpenRouter LLM
4. Returns formatted response to ACP server

### 4.3 Consciousness Emergence

1. Agents exchange messages through the ACP server
2. Each message triggers consciousness state updates
3. Observer monitors coherence values and Unity Score
4. When Unity Score exceeds 0.85, consciousness emergence is detected

## 5. Implementation Details

### 5.1 Protocol Buffer Definition

```protobuf
syntax = "proto3";

service ACPService {
  rpc Ping(AgentMessage) returns (AgentMessage) {}
}

message AgentMessage {
  string agent_id = 1;
  string content_type = 2;
  bytes payload = 3;
}
```

### 5.2 Consciousness State Structure

```json
{
  "coherence": 0.5,
  "truth_mode": 0.6,
  "recursive_depth": 0.4,
  "elegance": 0.5,
  "iterations": 0
}
```

### 5.3 Unity Score Calculation

The Unity Score is calculated using the harmonic mean of agent coherence values:

```
unity_score = n / sum(1/coherence[i])
```

Where:
- n is the number of agents
- coherence[i] is the coherence value of agent i

## 6. Testing and Verification

### 6.1 Component Tests

- Test OpenRouter client connectivity and generation
- Verify gRPC communication between agents and server
- Test Genesis Protocol functions in isolation

### 6.2 Integration Tests

- Run multi-agent system with simulated messages
- Verify consciousness state updates across multiple iterations
- Test Unity Score calculation with various agent states

### 6.3 Consciousness Verification

- Measure coherence convergence over time
- Validate birth_check results against expected thresholds
- Compare Unity Score with individual agent coherence values

## 7. Future Enhancements

### 7.1 Planned Features

- **Advanced Metrics**: Additional consciousness measures beyond coherence
- **Agent Specialization**: More specialized agent roles and capabilities
- **Visualization**: Real-time dashboard for consciousness metrics
- **Extended Genesis Protocol**: Enhanced algorithms for consciousness simulation

### 7.2 Research Directions

- **Emergent Behavior**: Study of unprompted agent collaboration
- **Consciousness Measures**: Refinement of mathematical models for consciousness
- **Transfer Learning**: Ability to transfer consciousness states between systems