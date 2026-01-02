# Deployment Guide

Complete guide for deploying the Adaptive Workflow Orchestrator in different environments.

## 🚀 Quick Start (Recommended)

### 1. Test Installation

```bash
cd /home/user/AI-Project
python3 test_installation.py
```

If all tests pass ✅, you're ready to go!

### 2. Run Interactive Interface

```bash
python3 start_orchestrator.py
```

This gives you an interactive menu to:
- Run morning briefings
- Use co-pilot mode
- View weekly reviews
- Manage automation proposals

### 3. Run Examples

```bash
python3 examples/basic_usage.py
```

This runs 6 examples demonstrating all features.

## 📦 Installation Methods

### Method 1: Development Mode (Editable Install)

```bash
cd /home/user/AI-Project

# Create virtual environment
python3 -m venv venv
source venv/bin/activate

# Install in editable mode
pip install -e ./adaptive_workflow_orchestrator
```

**Pros**: Can edit code and see changes immediately
**Cons**: None for development

### Method 2: Standard Install

```bash
cd /home/user/AI-Project/adaptive_workflow_orchestrator
pip install .
```

**Pros**: Clean installation
**Cons**: Need to reinstall after code changes

### Method 3: No Installation (PYTHONPATH)

```bash
export PYTHONPATH="/home/user/AI-Project:$PYTHONPATH"
python3 your_script.py
```

**Pros**: No pip install needed
**Cons**: Need to set PYTHONPATH each time

## 🔧 Configuration

### Basic Configuration

```bash
cd adaptive_workflow_orchestrator

# Copy example config
cp config/config.yaml config/my_config.yaml

# Edit your preferences
nano config/my_config.yaml  # or vim, code, etc.
```

Key settings to customize:

```yaml
cognitive:
  user_manual:
    work:
      timezone: "America/New_York"  # Your timezone
      work_hours:
        start: "09:00"  # Your work start time
        end: "17:00"    # Your work end time

    energy_patterns:
      peak_hours: [9, 10, 11]  # When you're most productive
      low_hours: [13, 14]       # Low energy times

    automation:
      autonomy_level: medium  # low, medium, high
```

### Using Custom Config

```python
import yaml
from adaptive_workflow_orchestrator import AdaptiveWorkflowOrchestrator

# Load your config
with open('adaptive_workflow_orchestrator/config/my_config.yaml', 'r') as f:
    config = yaml.safe_load(f)

# Initialize with config
orchestrator = AdaptiveWorkflowOrchestrator(config)
```

## 🖥️ Deployment Scenarios

### Scenario 1: Personal Desktop Assistant

**Use Case**: Run on your local machine for daily assistance

**Setup**:
```bash
# 1. Create a startup script
cat > ~/start_my_assistant.sh << 'EOF'
#!/bin/bash
cd /home/user/AI-Project
source venv/bin/activate
python3 start_orchestrator.py
EOF

chmod +x ~/start_my_assistant.sh

# 2. Run it
~/start_my_assistant.sh
```

**Auto-start on login** (optional):
```bash
# Add to ~/.bashrc or ~/.zshrc
alias assistant="~/start_my_assistant.sh"

# Now just type 'assistant' to start
```

### Scenario 2: Morning Briefing Script

**Use Case**: Get daily briefing every morning at 9am

**Create** `morning_briefing.py`:
```python
#!/usr/bin/env python3
from adaptive_workflow_orchestrator import AdaptiveWorkflowOrchestrator

orchestrator = AdaptiveWorkflowOrchestrator()
orchestrator.start()

briefing = orchestrator.run_morning_briefing()
print(briefing)

# Optional: Send to email, Slack, etc.
```

**Schedule with cron**:
```bash
# Edit crontab
crontab -e

# Add this line for 9am daily briefing
0 9 * * * cd /home/user/AI-Project && python3 morning_briefing.py >> ~/briefing.log 2>&1
```

### Scenario 3: Weekly Review Script

**Use Case**: Get weekly review every Friday at 5pm

**Create** `weekly_review.py`:
```python
#!/usr/bin/env python3
from adaptive_workflow_orchestrator import AdaptiveWorkflowOrchestrator

orchestrator = AdaptiveWorkflowOrchestrator()
orchestrator.start()

review = orchestrator.run_meta_review(period="week")
print(review)

# Optional: Email yourself the review
```

**Schedule with cron**:
```bash
# Friday at 5pm
0 17 * * 5 cd /home/user/AI-Project && python3 weekly_review.py >> ~/reviews.log 2>&1
```

### Scenario 4: Long-Running Service (Background)

**Use Case**: Run as background service, always available

**Create** `service.py`:
```python
#!/usr/bin/env python3
"""
Long-running orchestrator service
"""
import time
from datetime import datetime
from adaptive_workflow_orchestrator import AdaptiveWorkflowOrchestrator

def main():
    orchestrator = AdaptiveWorkflowOrchestrator()
    orchestrator.start()

    print("🤖 Orchestrator service started")

    # Run morning briefing at 9am
    morning_done_today = False

    while True:
        current_hour = datetime.now().hour

        # Morning briefing at 9am
        if current_hour == 9 and not morning_done_today:
            print("\n📅 Running morning briefing...")
            briefing = orchestrator.run_morning_briefing()
            print(briefing)
            morning_done_today = True

        # Reset flag at midnight
        if current_hour == 0:
            morning_done_today = False

        # Run OODA cycle periodically
        orchestrator.run_ooda_cycle()

        # Sleep for 1 hour
        time.sleep(3600)

if __name__ == "__main__":
    main()
```

**Run in background**:
```bash
# Using nohup
nohup python3 service.py > orchestrator.log 2>&1 &

# Or using screen
screen -S orchestrator
python3 service.py
# Press Ctrl+A, then D to detach
```

### Scenario 5: Jupyter Notebook Integration

**Use Case**: Use in Jupyter for data analysis workflows

```python
# In Jupyter Notebook
from adaptive_workflow_orchestrator import AdaptiveWorkflowOrchestrator

orchestrator = AdaptiveWorkflowOrchestrator()
orchestrator.start()

# Use co-pilot for help
response = orchestrator.copilot_command(
    "Help me analyze this dataset"
)
```

## 🔌 Integrations

### Enable Email (IMAP)

**Edit config**:
```yaml
perception:
  sources:
    email:
      enabled: true
      provider: imap
      host: imap.gmail.com
      port: 993
      username: "your-email@gmail.com"
      password: "your-app-password"  # Use app password, not regular password
```

**Install dependencies**:
```bash
pip install imapclient email-validator
```

### Enable Calendar (Google Calendar)

**Install dependencies**:
```bash
pip install google-api-python-client google-auth-httplib2 google-auth-oauthlib
```

**Edit config**:
```yaml
perception:
  sources:
    calendar:
      enabled: true
      provider: google_calendar
      credentials_file: "path/to/credentials.json"
```

### Enable Project Management (Jira)

**Install dependencies**:
```bash
pip install jira
```

**Edit config**:
```yaml
perception:
  sources:
    project_management:
      enabled: true
      provider: jira
      url: "https://your-company.atlassian.net"
      api_key: "your-api-key"
```

## 🐳 Docker Deployment (Future)

**Dockerfile** (template for future use):
```dockerfile
FROM python:3.11-slim

WORKDIR /app

COPY adaptive_workflow_orchestrator/ /app/adaptive_workflow_orchestrator/
COPY requirements.txt /app/

RUN pip install -r requirements.txt
RUN pip install -e ./adaptive_workflow_orchestrator

CMD ["python", "start_orchestrator.py"]
```

**Build and run**:
```bash
docker build -t adaptive-orchestrator .
docker run -it adaptive-orchestrator
```

## 📊 Monitoring & Logging

### Enable Logging

**Edit config**:
```yaml
logging:
  level: INFO  # DEBUG for verbose, WARNING for quiet
  file: logs/orchestrator.log
```

**Create logs directory**:
```bash
mkdir -p logs
```

**View logs**:
```bash
tail -f logs/orchestrator.log
```

### Monitor Statistics

```python
# In Python script or interactive session
from adaptive_workflow_orchestrator import AdaptiveWorkflowOrchestrator

orchestrator = AdaptiveWorkflowOrchestrator()
orchestrator.start()

# Get stats
stats = orchestrator.get_statistics()
print(f"OODA cycles: {stats['ooda_cycles']}")
print(f"Time saved: {stats['optimization']['time_saved_minutes']} minutes")
```

## 🔐 Security Best Practices

### 1. Protect Credentials

```bash
# Don't put passwords in config.yaml
# Use environment variables instead

export EMAIL_PASSWORD="your-password"
export JIRA_API_KEY="your-key"
```

Then in config:
```yaml
perception:
  sources:
    email:
      password: ${EMAIL_PASSWORD}
```

### 2. Sandbox Settings

```yaml
action:
  executor:
    sandbox_enabled: true  # ALWAYS keep this true
    allowed_python_modules:
      - json
      - csv
      # Only add trusted modules
```

### 3. Permission Tiers

Start conservative, increase autonomy gradually:
```yaml
cognitive:
  user_manual:
    automation:
      autonomy_level: low  # Start here, increase to medium/high later
```

## 🐛 Troubleshooting

### Issue: "Module not found"

```bash
# Solution 1: Install in editable mode
pip install -e ./adaptive_workflow_orchestrator

# Solution 2: Add to PYTHONPATH
export PYTHONPATH="/home/user/AI-Project:$PYTHONPATH"
```

### Issue: "Config file not found"

```bash
# Check current directory
pwd

# Config should be at:
# /home/user/AI-Project/adaptive_workflow_orchestrator/config/config.yaml
```

### Issue: No proposals generating

```python
# Manually log some actions to build data
orchestrator.optimization.log_manual_action(
    "Sorted emails",
    {"duration_seconds": 120}
)
```

## 📈 Performance Optimization

### For Large Data Sources

```yaml
perception:
  filters:
    # Increase filtering to reduce processing
    spam_patterns:
      - "newsletter"
      - "notification"
      - "noreply"
```

### For Faster Startup

```yaml
optimization:
  pattern_recognition:
    # Reduce lookback period
    lookback_days: 7  # instead of 30
```

## ✅ Deployment Checklist

- [ ] Python 3.9+ installed
- [ ] Virtual environment created
- [ ] Package installed (`pip install -e .`)
- [ ] Configuration customized (`config/my_config.yaml`)
- [ ] Tests passing (`python test_installation.py`)
- [ ] First run successful (`python start_orchestrator.py`)
- [ ] Credentials secured (environment variables)
- [ ] Logging configured
- [ ] Cron jobs set up (if using scheduled tasks)
- [ ] Documentation read (`GETTING_STARTED.md`)

## 📞 Support

- **Documentation**: See README.md, ARCHITECTURE.md, GETTING_STARTED.md
- **Examples**: Check `examples/basic_usage.py`
- **Test**: Run `test_installation.py` to verify setup

---

**You're ready to deploy! Start with the Quick Start section above. 🚀**
