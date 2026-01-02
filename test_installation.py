#!/usr/bin/env python3
"""
Quick test to verify the Adaptive Workflow Orchestrator installation
"""

def test_installation():
    print("🧪 Testing Adaptive Workflow Orchestrator Installation")
    print("=" * 60)

    # Test 1: Import
    print("\n1️⃣  Testing imports...")
    try:
        from adaptive_workflow_orchestrator import AdaptiveWorkflowOrchestrator
        print("   ✅ Main module imported successfully")
    except ImportError as e:
        print(f"   ❌ Failed to import: {e}")
        return False

    # Test 2: Initialization
    print("\n2️⃣  Testing initialization...")
    try:
        orchestrator = AdaptiveWorkflowOrchestrator()
        print("   ✅ Orchestrator created successfully")
    except Exception as e:
        print(f"   ❌ Failed to initialize: {e}")
        return False

    # Test 3: Start
    print("\n3️⃣  Testing system startup...")
    try:
        info = orchestrator.start()
        print(f"   ✅ System started: {info['status']}")
        print(f"   📦 Version: {info['version']}")
    except Exception as e:
        print(f"   ❌ Failed to start: {e}")
        return False

    # Test 4: Modules
    print("\n4️⃣  Testing modules...")
    modules = ['perception', 'cognitive', 'action', 'optimization', 'ooda_loop']
    for module in modules:
        if hasattr(orchestrator, module):
            print(f"   ✅ {module} module loaded")
        else:
            print(f"   ❌ {module} module missing")
            return False

    # Test 5: Modes
    print("\n5️⃣  Testing interaction modes...")
    modes = ['morning_briefer', 'copilot', 'architect']
    for mode in modes:
        if hasattr(orchestrator, mode):
            print(f"   ✅ {mode} mode available")
        else:
            print(f"   ❌ {mode} mode missing")
            return False

    # Test 6: Run a simple OODA cycle
    print("\n6️⃣  Testing OODA cycle...")
    try:
        result = orchestrator.run_ooda_cycle()
        print(f"   ✅ OODA cycle #{result['cycle_number']} completed")
    except Exception as e:
        print(f"   ❌ OODA cycle failed: {e}")
        return False

    # Test 7: Statistics
    print("\n7️⃣  Testing statistics...")
    try:
        stats = orchestrator.get_statistics()
        print(f"   ✅ Statistics retrieved")
        print(f"   📊 OODA cycles: {stats['ooda_cycles']}")
    except Exception as e:
        print(f"   ❌ Statistics failed: {e}")
        return False

    print("\n" + "=" * 60)
    print("✅ All tests passed! System is ready to use.")
    print("=" * 60)
    print("\nNext steps:")
    print("  1. Run: python start_orchestrator.py")
    print("  2. Or run: python examples/basic_usage.py")
    print("  3. Read: adaptive_workflow_orchestrator/GETTING_STARTED.md")

    return True

if __name__ == "__main__":
    try:
        success = test_installation()
        exit(0 if success else 1)
    except Exception as e:
        print(f"\n❌ Unexpected error: {e}")
        import traceback
        traceback.print_exc()
        exit(1)
