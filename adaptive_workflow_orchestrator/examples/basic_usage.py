"""
Basic usage examples for the Adaptive Workflow Orchestrator
"""

import sys
import os

# Add parent directory to path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from orchestrator import AdaptiveWorkflowOrchestrator


def example_1_morning_briefing():
    """Example: Run a morning briefing"""
    print("=" * 70)
    print("EXAMPLE 1: Morning Briefing")
    print("=" * 70)

    # Initialize orchestrator
    orchestrator = AdaptiveWorkflowOrchestrator()

    # Start the system
    startup_info = orchestrator.start()
    print(f"System started: {startup_info['status']}")
    print()

    # Run morning briefing
    briefing = orchestrator.run_morning_briefing()
    print(briefing)


def example_2_copilot_mode():
    """Example: Use co-pilot for real-time assistance"""
    print("\n" + "=" * 70)
    print("EXAMPLE 2: Co-Pilot Mode")
    print("=" * 70)

    orchestrator = AdaptiveWorkflowOrchestrator()
    orchestrator.start()

    # Start co-pilot session
    session = orchestrator.start_copilot()
    print(f"Co-pilot session started: {session['session_id']}")
    print(session['message'])
    print()

    # Send some commands
    commands = [
        "Schedule a sync with the dev team next week and draft an agenda",
        "Find all TODO comments in the codebase",
        "Draft an email to the project manager about our progress"
    ]

    for command in commands:
        print(f"\n> {command}")
        response = orchestrator.copilot_command(command)
        print(f"Status: {response['status']}")
        print(f"Response: {response['message']}")


def example_3_meta_review():
    """Example: Run a weekly meta-review"""
    print("\n" + "=" * 70)
    print("EXAMPLE 3: Meta-Review (Architect Mode)")
    print("=" * 70)

    orchestrator = AdaptiveWorkflowOrchestrator()
    orchestrator.start()

    # Run weekly review
    review = orchestrator.run_meta_review(period="week")
    print(review)


def example_4_ooda_cycle():
    """Example: Run a manual OODA cycle"""
    print("\n" + "=" * 70)
    print("EXAMPLE 4: Manual OODA Cycle")
    print("=" * 70)

    orchestrator = AdaptiveWorkflowOrchestrator()
    orchestrator.start()

    # Run an OODA cycle
    result = orchestrator.run_ooda_cycle({
        "context": "user_requested_analysis",
        "focus": "productivity"
    })

    print(f"Cycle #{result['cycle_number']} completed")
    print(f"\nOBSERVE Phase:")
    print(f"  Sources checked: {len(result['phases']['observe']['sources'])}")

    print(f"\nORIENT Phase:")
    orientation = result['phases']['orient']
    print(f"  Urgency level: {orientation['context'].get('urgency_level', 'N/A')}")

    print(f"\nDECIDE Phase:")
    decision = result['phases']['decide']
    print(f"  Action plan items: {len(decision['action_plan'])}")

    print(f"\nACT Phase:")
    action_results = result['phases']['act']
    print(f"  Actions executed: {len(action_results['executed_actions'])}")
    print(f"  Pending approvals: {len(action_results['pending_approvals'])}")


def example_5_optimization_proposals():
    """Example: Review and manage optimization proposals"""
    print("\n" + "=" * 70)
    print("EXAMPLE 5: Optimization Proposals")
    print("=" * 70)

    orchestrator = AdaptiveWorkflowOrchestrator()
    orchestrator.start()

    # Simulate some actions to generate patterns
    # (In real usage, these would come from actual work)
    for i in range(5):
        orchestrator.optimization.log_manual_action(
            action_description="Manually sort emails by sender",
            metadata={"category": "email_management", "duration_seconds": 120}
        )

    # Get active proposals
    proposals = orchestrator.get_active_proposals()

    if proposals:
        print(f"You have {len(proposals)} optimization proposal(s):\n")

        for i, proposal in enumerate(proposals, 1):
            print(f"{i}. {proposal['title']}")
            print(f"   {proposal['description']}")
            print(f"   Estimated savings: {proposal['estimated_time_savings_minutes']} min/week")
            print(f"   Risk level: {proposal['risk_level']}")
            print()

            # Accept first proposal as example
            if i == 1:
                print(f"Accepting proposal #{proposal['id']}...")
                result = orchestrator.accept_proposal(proposal['id'])
                print(f"Result: {result['status']}")
                print()
    else:
        print("No active proposals yet. Keep working and the system will detect patterns!")


def example_6_statistics():
    """Example: Get system statistics"""
    print("\n" + "=" * 70)
    print("EXAMPLE 6: System Statistics")
    print("=" * 70)

    orchestrator = AdaptiveWorkflowOrchestrator()
    orchestrator.start()

    # Run a few cycles
    for _ in range(3):
        orchestrator.run_ooda_cycle()

    # Get statistics
    stats = orchestrator.get_statistics()

    print("System Statistics:")
    print(f"  Uptime: {stats['uptime_seconds']:.1f} seconds")
    print(f"  Current mode: {stats['current_mode']}")
    print(f"  OODA cycles completed: {stats['ooda_cycles']}")
    print()

    print("Optimization Stats:")
    opt_stats = stats['optimization']
    print(f"  Actions logged: {opt_stats['total_actions_logged']}")
    print(f"  Patterns detected: {opt_stats['patterns_detected']}")
    print(f"  Proposals made: {opt_stats['proposals_made']}")
    print(f"  Proposals accepted: {opt_stats['proposals_accepted']}")
    print(f"  Time saved: {opt_stats['time_saved_minutes']} minutes")


if __name__ == "__main__":
    print("\n🤖 Adaptive Workflow Orchestrator - Examples\n")

    # Run all examples
    example_1_morning_briefing()
    example_2_copilot_mode()
    example_3_meta_review()
    example_4_ooda_cycle()
    example_5_optimization_proposals()
    example_6_statistics()

    print("\n" + "=" * 70)
    print("All examples completed!")
    print("=" * 70)
