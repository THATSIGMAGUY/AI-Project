# Getting Started with Adaptive Workflow Orchestrator

This guide will walk you through setting up and using your Adaptive Workflow Orchestrator.

## Table of Contents
1. [Installation](#installation)
2. [First Run](#first-run)
3. [Configuration](#configuration)
4. [Basic Usage](#basic-usage)
5. [Common Workflows](#common-workflows)
6. [Troubleshooting](#troubleshooting)

## Installation

### Prerequisites
- Python 3.9 or higher
- pip package manager

### Install from Source

```bash
# Clone the repository
git clone <your-repo-url>
cd adaptive_workflow_orchestrator

# Create a virtual environment (recommended)
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Install the package
pip install -e .
```

## First Run

### Quick Test

Let's verify everything works:

```python
# test_basic.py
from adaptive_workflow_orchestrator import AdaptiveWorkflowOrchestrator

# Create orchestrator
orchestrator = AdaptiveWorkflowOrchestrator()

# Start it
info = orchestrator.start()
print(f"System status: {info['status']}")

# Run a simple OODA cycle
result = orchestrator.run_ooda_cycle()
print(f"Cycle completed: #{result['cycle_number']}")
```

Run it:
```bash
python test_basic.py
```

If you see "System status: running", you're good to go!

## Configuration

### Step 1: Copy the Example Config

```bash
cp config/config.yaml config/my_config.yaml
```

### Step 2: Edit Your Preferences

Open `config/my_config.yaml` and customize:

#### User Manual (Most Important!)

```yaml
cognitive:
  user_manual:
    communication:
      tone: professional  # or: casual, formal
      verbosity: balanced  # or: terse, detailed

    work:
      timezone: America/New_York  # Your timezone
      work_hours:
        start: "09:00"
        end: "17:00"

    energy_patterns:
      peak_hours: [9, 10, 11]  # When you're most productive
      low_hours: [13, 14]       # Post-lunch dip

    automation:
      autonomy_level: medium  # low, medium, high
      require_approval_for:
        - send_email
        - schedule_meeting
```

#### Enable Data Sources

Start with local sources (safest):

```yaml
perception:
  sources:
    filesystem:
      enabled: true
      watch_paths:
        - ~/Documents
        - ~/Projects

    # Enable others as needed
    email:
      enabled: false  # Set to true when ready
    calendar:
      enabled: false
```

### Step 3: Load Your Config

```python
import yaml

with open('config/my_config.yaml', 'r') as f:
    config = yaml.safe_load(f)

orchestrator = AdaptiveWorkflowOrchestrator(config)
```

## Basic Usage

### 1. Morning Briefing

Start your day right:

```python
from adaptive_workflow_orchestrator import AdaptiveWorkflowOrchestrator

orchestrator = AdaptiveWorkflowOrchestrator()
orchestrator.start()

# Get your morning briefing
briefing = orchestrator.run_morning_briefing()
print(briefing)
```

**What you'll see:**
```
============================================================
  Good Morning! Here's your briefing for Monday, January 02
============================================================

📊 TODAY'S OVERVIEW
------------------------------------------------------------
Critical Tasks: 3
Meetings: 2
Available Deep Work Time: 5.5 hours
Urgency Level: NORMAL

🎯 CRITICAL TASKS
------------------------------------------------------------
1. Complete project proposal
   Priority: critical | Est: 60min
...
```

### 2. Co-Pilot Mode

Work with real-time assistance:

```python
# Start co-pilot
session = orchestrator.start_copilot()
print(session['message'])  # "Co-pilot ready. How can I help you?"

# Send commands
response = orchestrator.copilot_command(
    "Schedule a team sync next Tuesday at 2pm"
)

print(response['status'])  # "draft_created"
print(response['message'])  # Shows the draft for approval
```

### 3. Pattern Detection & Automation

Let the system learn from you:

```python
# Log a manual action
orchestrator.optimization.log_manual_action(
    action_description="Sorted emails by project",
    metadata={"duration_seconds": 180}
)

# After doing this a few times, check proposals
proposals = orchestrator.get_active_proposals()

for proposal in proposals:
    print(f"\n{proposal['title']}")
    print(f"Description: {proposal['description']}")
    print(f"Est. time savings: {proposal['estimated_time_savings_minutes']} min/week")

    # Accept if you like it
    # orchestrator.accept_proposal(proposal['id'])
```

### 4. Weekly Meta-Review

End of week retrospective:

```python
# Run architect mode
review = orchestrator.run_meta_review(period="week")
print(review)
```

**What you'll see:**
```
======================================================================
  META-REVIEW: WEEK
  2026-01-02 to 2026-01-09
======================================================================

⏱️  TIME ALLOCATION
----------------------------------------------------------------------
Total Work Time: 40.0 hours

Breakdown:
  Meetings: 12.0h (30.0%)
  Coding: 15.0h (37.5%)
  Email: 5.0h (12.5%)
  ...

💡 OPTIMIZATION PROPOSALS
----------------------------------------------------------------------
1. Automate email sorting
   I noticed you spend 15 minutes every Friday sorting emails...
   Estimated savings: 60 min/week
...
```

## Common Workflows

### Workflow 1: Daily Routine

```python
# Morning
briefing = orchestrator.run_morning_briefing()
# Review critical tasks

# During work
orchestrator.start_copilot()
# Use commands as needed

# End of day
stats = orchestrator.get_statistics()
# Review what was accomplished
```

### Workflow 2: Accepting an Automation

```python
# 1. Review proposals
proposals = orchestrator.get_active_proposals()

# 2. Pick one
proposal = proposals[0]
print(f"Title: {proposal['title']}")
print(f"Risk: {proposal['risk_level']}")
print(f"Savings: {proposal['estimated_time_savings_minutes']} min/week")

# 3. Accept it
result = orchestrator.accept_proposal(proposal['id'])
print(f"Status: {result['status']}")
print(f"Automation enabled!")
```

### Workflow 3: Custom Command in Co-Pilot

```python
orchestrator.start_copilot()

# Various command examples
commands = [
    # Scheduling
    "Schedule a 1-on-1 with my manager next week",

    # Drafting
    "Draft an email to the client about the project delay",

    # Searching
    "Find all TODO comments in the Python files",

    # Analysis
    "Analyze my time spent in meetings this week",
]

for cmd in commands:
    response = orchestrator.copilot_command(cmd)
    # Handle response
```

## Troubleshooting

### Issue: "Module not found"

**Solution:**
```bash
# Make sure you installed the package
pip install -e .

# Or add to PYTHONPATH
export PYTHONPATH="${PYTHONPATH}:/path/to/adaptive_workflow_orchestrator"
```

### Issue: "No proposals being generated"

**Reason**: Not enough pattern data yet.

**Solution:**
```python
# Manually log some actions to build up data
for i in range(10):
    orchestrator.optimization.log_manual_action(
        action_description="Checked email",
        metadata={"timestamp": "2026-01-02T09:00:00"}
    )

# Now check again
proposals = orchestrator.get_active_proposals()
```

### Issue: Config file not loading

**Solution:**
```python
import yaml
import os

config_path = "config/my_config.yaml"

# Verify file exists
print(f"Config exists: {os.path.exists(config_path)}")

# Try loading
with open(config_path, 'r') as f:
    config = yaml.safe_load(f)
    print("Config loaded successfully!")
```

### Issue: Permission errors

**Solution:**
Check your permission settings in config:

```yaml
action:
  permissions:
    user_overrides:
      # Force specific action to Tier 1 (no approval)
      sort_emails: tier_1
```

## Next Steps

1. **Customize Your User Manual**: The more you configure your preferences, the better the system understands you.

2. **Enable Data Sources**: Start with safe sources (filesystem) and gradually enable others (email, calendar).

3. **Use Daily**: The more you use the system, the more patterns it detects.

4. **Review Proposals Weekly**: Check the Architect mode every Friday to see optimization opportunities.

5. **Provide Feedback**: Accept/reject proposals to train the system.

## Advanced Usage

### Creating Custom Modes

```python
class MyCustomMode:
    def __init__(self, orchestrator):
        self.orchestrator = orchestrator

    def run(self):
        # Your custom logic using orchestrator components
        result = self.orchestrator.run_ooda_cycle({
            "custom_context": "my_use_case"
        })
        return result

# Register it
orchestrator.custom_mode = MyCustomMode(orchestrator)
```

### Integrating with External Tools

```python
# Example: Slack integration
def send_slack_notification(message):
    # Your Slack webhook logic
    pass

# Hook into the orchestrator
original_act = orchestrator.action.execute

def execute_with_slack(action):
    result = original_act(action)
    if action.get('type') == 'critical':
        send_slack_notification(f"Critical action completed: {action['id']}")
    return result

orchestrator.action.execute = execute_with_slack
```

## Support

- **Documentation**: See [README.md](README.md) and [ARCHITECTURE.md](ARCHITECTURE.md)
- **Examples**: Check `examples/` directory
- **Issues**: [GitHub Issues](your-repo-url/issues)

---

**Happy orchestrating! 🎭**
