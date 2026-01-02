"""
OODA Loop Implementation
The core decision-making cycle: Observe -> Orient -> Decide -> Act
"""

from typing import Dict, List, Any, Optional
from datetime import datetime
import logging
from enum import Enum


class LoopPhase(Enum):
    """Phases of the OODA loop"""
    OBSERVE = "observe"
    ORIENT = "orient"
    DECIDE = "decide"
    ACT = "act"


class OODALoop:
    """
    Implements the Observe-Orient-Decide-Act cycle for continuous improvement.

    This is the cognitive backbone of the agent, ensuring it perceives,
    understands, plans, and executes in a continuous cycle.
    """

    def __init__(self, perception_module, cognitive_engine, action_layer, optimization_loop):
        self.perception = perception_module
        self.cognitive = cognitive_engine
        self.action = action_layer
        self.optimization = optimization_loop

        self.logger = logging.getLogger(__name__)
        self.current_phase = LoopPhase.OBSERVE
        self.cycle_count = 0
        self.cycle_history: List[Dict[str, Any]] = []

    def observe(self, context: Optional[Dict[str, Any]] = None) -> Dict[str, Any]:
        """
        Phase 1: OBSERVE
        Gather data from all connected sources (email, calendar, code, etc.)

        Args:
            context: Optional context to guide observation

        Returns:
            Dict containing observed data and metadata
        """
        self.logger.info("🔍 OBSERVE: Gathering environmental data")
        self.current_phase = LoopPhase.OBSERVE

        observations = {
            "timestamp": datetime.now().isoformat(),
            "sources": {},
            "raw_data": {},
            "filtered_data": {}
        }

        # Collect data from all perception sensors
        observations["sources"] = self.perception.gather_all_sources(context)

        # Apply filters to reduce noise
        observations["filtered_data"] = self.perception.filter_and_structure(
            observations["sources"]
        )

        return observations

    def orient(self, observations: Dict[str, Any]) -> Dict[str, Any]:
        """
        Phase 2: ORIENT
        Understand context, priorities, deadlines, and user state

        Args:
            observations: Data from the observe phase

        Returns:
            Dict containing oriented understanding and context
        """
        self.logger.info("🧭 ORIENT: Analyzing context and priorities")
        self.current_phase = LoopPhase.ORIENT

        orientation = {
            "timestamp": datetime.now().isoformat(),
            "context": {},
            "priorities": [],
            "constraints": {},
            "user_state": {}
        }

        # Use cognitive engine to understand the situation
        orientation["context"] = self.cognitive.analyze_context(
            observations["filtered_data"]
        )

        # Determine priorities using user preferences and deadlines
        orientation["priorities"] = self.cognitive.prioritize_tasks(
            orientation["context"]
        )

        # Identify constraints (time, resources, dependencies)
        orientation["constraints"] = self.cognitive.identify_constraints(
            orientation["context"]
        )

        # Assess user state (energy, availability, preferences)
        orientation["user_state"] = self.cognitive.assess_user_state(
            observations["filtered_data"]
        )

        return orientation

    def decide(self, orientation: Dict[str, Any]) -> Dict[str, Any]:
        """
        Phase 3: DECIDE
        Plan the most efficient path forward

        Args:
            orientation: Context and priorities from orient phase

        Returns:
            Dict containing decision plan and action items
        """
        self.logger.info("🤔 DECIDE: Planning optimal action path")
        self.current_phase = LoopPhase.DECIDE

        decision = {
            "timestamp": datetime.now().isoformat(),
            "action_plan": [],
            "delegations": [],
            "automations": [],
            "user_confirmations_needed": []
        }

        # Generate action plan based on priorities and constraints
        decision["action_plan"] = self.cognitive.generate_action_plan(
            orientation["priorities"],
            orientation["constraints"],
            orientation["user_state"]
        )

        # Identify tasks that can be delegated to automation
        decision["automations"] = self.cognitive.identify_automatable_tasks(
            decision["action_plan"]
        )

        # Determine what needs user approval (based on permission tiers)
        decision["user_confirmations_needed"] = self.cognitive.check_permissions(
            decision["action_plan"]
        )

        return decision

    def act(self, decision: Dict[str, Any]) -> Dict[str, Any]:
        """
        Phase 4: ACT
        Execute the planned actions or prompt for minimum necessary input

        Args:
            decision: Action plan from decide phase

        Returns:
            Dict containing execution results and feedback
        """
        self.logger.info("⚡ ACT: Executing action plan")
        self.current_phase = LoopPhase.ACT

        results = {
            "timestamp": datetime.now().isoformat(),
            "executed_actions": [],
            "pending_approvals": [],
            "errors": [],
            "metrics": {}
        }

        # Execute each action in the plan
        for action in decision["action_plan"]:
            try:
                # Check if this action needs user approval
                if action["id"] in [c["action_id"] for c in decision["user_confirmations_needed"]]:
                    results["pending_approvals"].append(action)
                    continue

                # Execute the action
                execution_result = self.action.execute(action)
                results["executed_actions"].append({
                    "action": action,
                    "result": execution_result,
                    "status": "success"
                })

                # Log for optimization
                self.optimization.log_action(action, execution_result)

            except Exception as e:
                self.logger.error(f"Error executing action {action.get('id')}: {e}")
                results["errors"].append({
                    "action": action,
                    "error": str(e)
                })

        # Collect metrics for this cycle
        results["metrics"] = self._collect_cycle_metrics(results)

        return results

    def run_cycle(self, context: Optional[Dict[str, Any]] = None) -> Dict[str, Any]:
        """
        Execute a complete OODA cycle

        Args:
            context: Optional context to guide the cycle

        Returns:
            Dict containing complete cycle results
        """
        self.cycle_count += 1
        self.logger.info(f"🔄 Starting OODA cycle #{self.cycle_count}")

        cycle_result = {
            "cycle_number": self.cycle_count,
            "start_time": datetime.now().isoformat(),
            "phases": {}
        }

        # Execute each phase in sequence
        observations = self.observe(context)
        cycle_result["phases"]["observe"] = observations

        orientation = self.orient(observations)
        cycle_result["phases"]["orient"] = orientation

        decision = self.decide(orientation)
        cycle_result["phases"]["decide"] = decision

        action_results = self.act(decision)
        cycle_result["phases"]["act"] = action_results

        cycle_result["end_time"] = datetime.now().isoformat()

        # Store cycle for analysis
        self.cycle_history.append(cycle_result)

        # Trigger optimization analysis
        self.optimization.analyze_cycle(cycle_result)

        return cycle_result

    def _collect_cycle_metrics(self, results: Dict[str, Any]) -> Dict[str, Any]:
        """Collect metrics about cycle performance"""
        return {
            "actions_executed": len(results["executed_actions"]),
            "pending_approvals": len(results["pending_approvals"]),
            "errors": len(results["errors"]),
            "success_rate": len(results["executed_actions"]) / max(1, len(results["executed_actions"]) + len(results["errors"]))
        }

    def get_cycle_history(self, limit: Optional[int] = None) -> List[Dict[str, Any]]:
        """Get historical cycle data for analysis"""
        if limit:
            return self.cycle_history[-limit:]
        return self.cycle_history
