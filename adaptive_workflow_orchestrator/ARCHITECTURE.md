# Architecture Documentation

## System Overview

The Adaptive Workflow Orchestrator is a multi-module agentic system designed around the OODA (Observe-Orient-Decide-Act) loop. This document provides deep technical insight into the architecture.

## Core Principles

### 1. Continuous Learning
The system doesn't just execute tasks—it learns from every interaction and proposes improvements.

### 2. Human-in-the-Loop
Safety is paramount. A tiered permission system ensures humans maintain control while reducing friction for routine tasks.

### 3. Context Awareness
The system maintains both short-term (current session) and long-term (historical) memory to provide contextually relevant assistance.

### 4. Modularity
Each component is independent and can be upgraded or replaced without affecting others.

## Detailed Component Architecture

### The OODA Loop (`ooda_loop.py`)

The OODA loop is the central coordinator that orchestrates all four modules.

```python
class OODALoop:
    def run_cycle(self, context):
        observations = self.observe(context)      # Gather data
        orientation = self.orient(observations)   # Understand context
        decision = self.decide(orientation)       # Plan actions
        results = self.act(decision)              # Execute
        return cycle_result
```

**Data Flow:**
```
Environment → Perception → Cognitive → Action → Environment
                ↓             ↓          ↓
            Optimization ← ← ← ← ← ← ← ←
```

### Perception Module

**Purpose**: Sense the environment and filter noise

**Components:**

1. **SourceManager** (`source_manager.py`)
   - Manages connections to external data sources
   - Provides unified interfaces for heterogeneous APIs
   - Handles authentication and rate limiting

2. **DataFilter** (`data_filter.py`)
   - Applies multi-level filtering:
     - Priority-based (urgent vs. informational)
     - Pattern-based (recurring notifications)
     - User preference-based (learned filters)
   - Calculates noise reduction ratio

**Example Flow:**
```
Raw Email (1000 messages)
  → Spam Filter (200 filtered)
  → Priority Detection (50 urgent, 200 actionable, 550 informational)
  → Structured Output
```

### Cognitive Engine

**Purpose**: Understand, reason, and plan

**Components:**

1. **Memory System** (`memory_system.py`)

   **Short-term Memory:**
   - LRU cache with configurable capacity
   - Stores current conversation and session context
   - Fast retrieval (O(1))

   **Long-term Memory:**
   - Vector database for semantic search
   - Stores:
     - Past successful solutions
     - Email/document templates
     - Code snippets
     - User patterns
   - Enables "recall how you solved X 6 months ago"

2. **User Manual** (`user_manual.py`)
   - Persistent user preferences
   - Communication style (tone, verbosity)
   - Work patterns (peak hours, preferred task types)
   - Strategic goals (short-term and long-term)
   - Learning log (what works, what doesn't)

**Decision-Making Process:**
```
Input (Filtered Data)
  → Context Analysis (LLM-powered)
  → Priority Assignment (based on user preferences + deadlines)
  → Constraint Identification (time, resources, dependencies)
  → Action Plan Generation
  → Permission Check
  → Output (Actionable plan)
```

### Action Layer

**Purpose**: Execute tasks safely and effectively

**Components:**

1. **Executor** (`executor.py`)
   - Sandboxed code execution
   - API webhook triggers
   - File operations
   - Supports multiple action types:
     - Email (send, draft, reply)
     - Calendar (create, update events)
     - Code (execute Python/Bash)
     - Files (read, write, organize)

2. **PermissionManager** (`permission_manager.py`)

   **Tier 1 - Read Only:**
   ```python
   actions = ["search", "read", "analyze", "summarize"]
   # No approval needed
   ```

   **Tier 2 - Draft:**
   ```python
   actions = ["send_email", "create_event", "execute_code"]
   # User approval required
   ```

   **Tier 3 - Autonomous:**
   ```python
   actions = ["sort", "organize", "tag"]
   # Shadow mode: Runs in background after first approval
   ```

**Safety Mechanisms:**
- Sandboxing: Code runs in isolated environment
- Rollback: Reversible actions can be undone
- Audit trail: All actions logged
- User override: Can change permission tier for any action

### Optimization Loop

**Purpose**: Detect patterns and propose improvements

**Components:**

1. **PatternRecognizer** (`pattern_recognizer.py`)

   **Pattern Types:**

   - **Temporal**: `detect_temporal_patterns()`
     ```
     Example: "Every Friday at 3pm, compile status report"
     Detection: Group actions by (day_of_week, hour, action_type)
     Threshold: min_occurrences (default: 3)
     ```

   - **Sequential**: `detect_sequential_patterns()`
     ```
     Example: "Always git add → git commit → git push"
     Detection: Sliding window over action sequences
     Automation: Combine into single command
     ```

   - **Trigger**: `detect_trigger_patterns()`
     ```
     Example: "When email from X arrives, forward to Y"
     Detection: Action pairs within time window (5 min)
     Automation: If-this-then-that rule
     ```

   - **Bulk**: `detect_bulk_patterns()`
     ```
     Example: "Process 50 emails at once every Monday"
     Detection: Cluster similar actions in time
     Automation: Batch processing script
     ```

2. **ProposalSystem** (`proposal_system.py`)

   **Proposal Generation:**
   ```python
   def generate_proposal(pattern):
       proposal = {
           "title": "Automate X",
           "description": "I noticed you do X repeatedly...",
           "estimated_time_savings": calculate_savings(pattern),
           "risk_level": assess_risk(pattern),
           "automation_spec": generate_script(pattern),
           "requires_approval": check_tier(pattern)
       }
       return proposal
   ```

   **Learning from Feedback:**
   - Tracks accepted vs. rejected proposals
   - Adjusts future proposals based on user preferences
   - Avoids proposing similar automations if repeatedly rejected

## Interaction Modes

### Morning Briefer

**Execution Flow:**
```
1. Run OODA cycle to gather current state
2. Extract critical tasks (priority items)
3. Identify blockers (tasks waiting on others)
4. Get today's calendar
5. Calculate available time blocks
6. Generate recommendations
7. Format and present briefing
```

**Output Format:**
```
📊 TODAY'S OVERVIEW
  Critical Tasks: 3
  Meetings: 5
  Deep Work Time: 3.5 hours

🎯 CRITICAL TASKS
  1. Complete feature X (Priority: high, Est: 60min)
  2. Review PRs (Priority: medium, Est: 30min)

🚧 BLOCKERS
  • Waiting for API key from DevOps
```

### Co-Pilot

**Real-time Context Tracking:**
```python
class CoPilot:
    def __init__(self):
        self.current_context = None      # What user is working on
        self.active_document = None      # Current file/document
        self.conversation_history = []   # Dialogue history
```

**Micro-Delegation Handling:**
```
User: "Schedule a sync with dev team next week"
  ↓
Parse intent: SCHEDULE + MEETING
  ↓
Extract entities: dev team, next week
  ↓
Find available slots
  ↓
Draft calendar invite
  ↓
Request approval
```

### Architect

**Meta-Review Process:**
```
1. Define review period (week/month/quarter)
2. Analyze time allocation
   - By category (meetings, coding, email)
   - By day of week
3. Calculate productivity metrics
   - Tasks completed
   - Automation rate
   - Time saved
4. Get detected patterns
5. Get active proposals
6. Generate strategic recommendations
7. Review goal progress
```

## Data Flow Example

**Scenario**: User receives urgent email

```
1. PERCEPTION
   Email arrives → IMAP connector fetches
   → Spam filter (pass)
   → Priority detector (URGENT - contains "deadline" + high priority header)
   → Categorized as priority_item

2. COGNITIVE
   Priority item analyzed
   → Context: Email from manager about project deadline
   → Constraint: Deadline is tomorrow
   → User state: Currently in focused work
   → Decision: Interrupt user (high priority)

3. ACTION
   → Permission check: Notification = Tier 1 (allowed)
   → Execute: Show notification to user
   → Log action for pattern detection

4. OPTIMIZATION
   → Pattern detected: "Emails from manager are always urgent"
   → Proposal: "Auto-prioritize emails from manager"
   → Added to proposal queue
```

## Performance Considerations

### Memory Management
- Short-term memory: LRU eviction when capacity exceeded
- Long-term memory: Lazy loading, indexed search
- Pattern detection: Runs every N actions (configurable)

### Scalability
- Modular architecture allows horizontal scaling
- Each module can run as separate service
- Async execution for non-blocking operations
- Caching layer for frequently accessed data

### Optimization
- Batch processing where possible
- Incremental pattern analysis (not full re-scan)
- Smart scheduling (run heavy analysis during low-activity periods)

## Security Architecture

### Defense in Depth

1. **Input Validation**
   - All external data sanitized
   - Schema validation for configurations

2. **Sandboxing**
   - Code execution in isolated environment
   - Limited file system access
   - No network access from sandbox (configurable)

3. **Permission System**
   - Whitelist approach (explicit allow)
   - User override capability
   - Audit logging

4. **Data Encryption**
   - Sensitive data encrypted at rest
   - Secure credential storage
   - API keys in environment variables or vault

## Extension Points

### Adding New Modules

```python
# 1. Create module class
class MyCustomModule:
    def __init__(self, config):
        self.config = config

    def process(self, input_data):
        # Your logic here
        return output_data

# 2. Register in orchestrator
class AdaptiveWorkflowOrchestrator:
    def __init__(self, config):
        # ... existing modules ...
        self.custom_module = MyCustomModule(config.get("custom", {}))
```

### Adding New Pattern Types

```python
# In pattern_recognizer.py
def detect_custom_pattern(self, actions):
    # Your pattern detection logic
    patterns = []
    # ... analyze actions ...
    return patterns
```

### Adding New Action Types

```python
# In executor.py
def execute_custom_action(self, action):
    # Your execution logic
    result = perform_custom_action(action)
    return result
```

## Testing Strategy

1. **Unit Tests**: Each module independently tested
2. **Integration Tests**: OODA cycle end-to-end
3. **Pattern Tests**: Verify pattern detection accuracy
4. **Safety Tests**: Permission system enforcement
5. **Performance Tests**: Scalability and response time

## Deployment Considerations

### Local Deployment
```bash
# Single-process mode
python -m adaptive_workflow_orchestrator.main

# With config
python -m adaptive_workflow_orchestrator.main --config config/production.yaml
```

### Distributed Deployment
```
┌─────────────┐
│  API Gateway│
└──────┬──────┘
       │
   ┌───┴────────────────┬────────────┬──────────┐
   │                    │            │          │
┌──▼──────┐    ┌───────▼──┐   ┌────▼───┐  ┌──▼────────┐
│Perception│    │ Cognitive│   │ Action │  │Optimization│
└──────────┘    └──────────┘   └────────┘  └───────────┘
```

### Monitoring
- Logs: Structured JSON logs
- Metrics: Action counts, pattern detection rate, proposal acceptance rate
- Alerts: Failed actions, permission violations
- Dashboards: Real-time system health

## Future Architecture Enhancements

1. **Event Sourcing**: Store all events for complete audit trail
2. **CQRS**: Separate read/write models for better scalability
3. **Microservices**: Each module as independent service
4. **GraphQL API**: Flexible querying of system state
5. **Real-time Collaboration**: Multi-user support with operational transforms
6. **Federated Learning**: Privacy-preserving pattern learning across users

---

This architecture is designed to be **adaptive**, **safe**, and **continuously improving**—just like the system it describes.
