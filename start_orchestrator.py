#!/usr/bin/env python3
"""
Simple script to start the Adaptive Workflow Orchestrator
"""

from adaptive_workflow_orchestrator import AdaptiveWorkflowOrchestrator

def main():
    print("🤖 Starting Adaptive Workflow Orchestrator...")
    print("=" * 60)

    # Initialize
    orchestrator = AdaptiveWorkflowOrchestrator()

    # Start the system
    info = orchestrator.start()
    print(f"✅ Status: {info['status']}")
    print(f"📦 Version: {info['version']}")
    print(f"⏰ Started at: {info['started_at']}")
    print()

    # Show available modes
    print("Available Modes:")
    for mode in info['modes_available']:
        print(f"  - {mode}")
    print()

    # Interactive menu
    while True:
        print("\n" + "=" * 60)
        print("What would you like to do?")
        print("1. Morning Briefing")
        print("2. Start Co-Pilot")
        print("3. Weekly Meta-Review")
        print("4. View Active Proposals")
        print("5. Run OODA Cycle")
        print("6. View Statistics")
        print("7. Exit")
        print("=" * 60)

        choice = input("Enter choice (1-7): ").strip()

        if choice == "1":
            print("\n📅 Running Morning Briefing...")
            briefing = orchestrator.run_morning_briefing()
            print(briefing)

        elif choice == "2":
            print("\n🤝 Starting Co-Pilot Mode...")
            session = orchestrator.start_copilot()
            print(f"{session['message']}\n")

            while True:
                command = input("Co-Pilot> ").strip()
                if command.lower() in ['exit', 'quit', 'back']:
                    break

                response = orchestrator.copilot_command(command)
                print(f"\nStatus: {response['status']}")
                print(f"Response: {response.get('message', response)}\n")

        elif choice == "3":
            print("\n📊 Running Weekly Meta-Review...")
            review = orchestrator.run_meta_review(period="week")
            print(review)

        elif choice == "4":
            print("\n💡 Active Optimization Proposals...")
            proposals = orchestrator.get_active_proposals()

            if not proposals:
                print("No active proposals yet.")
                print("Keep using the system and it will detect patterns!")
            else:
                for i, proposal in enumerate(proposals, 1):
                    print(f"\n{i}. {proposal['title']}")
                    print(f"   Description: {proposal['description']}")
                    print(f"   Time Savings: {proposal['estimated_time_savings_minutes']} min/week")
                    print(f"   Risk: {proposal['risk_level']}")

                # Ask if user wants to accept any
                accept = input("\nAccept a proposal? (enter number or 'n'): ").strip()
                if accept.isdigit() and 1 <= int(accept) <= len(proposals):
                    result = orchestrator.accept_proposal(proposals[int(accept)-1]['id'])
                    print(f"✅ {result['status']}: Automation enabled!")

        elif choice == "5":
            print("\n🔄 Running OODA Cycle...")
            result = orchestrator.run_ooda_cycle()
            print(f"Cycle #{result['cycle_number']} completed")
            print(f"  - Sources checked: {len(result['phases']['observe']['sources'])}")
            print(f"  - Actions executed: {len(result['phases']['act']['executed_actions'])}")
            print(f"  - Pending approvals: {len(result['phases']['act']['pending_approvals'])}")

        elif choice == "6":
            print("\n📊 System Statistics...")
            stats = orchestrator.get_statistics()
            print(f"Uptime: {stats['uptime_seconds']:.1f} seconds")
            print(f"Current Mode: {stats['current_mode']}")
            print(f"OODA Cycles: {stats['ooda_cycles']}")
            print(f"\nOptimization Stats:")
            opt = stats['optimization']
            print(f"  - Actions Logged: {opt['total_actions_logged']}")
            print(f"  - Patterns Detected: {opt['patterns_detected']}")
            print(f"  - Proposals Made: {opt['proposals_made']}")
            print(f"  - Proposals Accepted: {opt['proposals_accepted']}")
            print(f"  - Time Saved: {opt['time_saved_minutes']} minutes")

        elif choice == "7":
            print("\n👋 Goodbye!")
            break
        else:
            print("Invalid choice. Please try again.")

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\n\n👋 Shutting down gracefully...")
    except Exception as e:
        print(f"\n❌ Error: {e}")
        import traceback
        traceback.print_exc()
