from langgraph.graph import END, StateGraph
from src.state import ReleaseState
from src.nodes.context_aggregator import aggregate_context
from src.nodes.risk_analyzer import analyze_risk
from src.nodes.release_gate import evaluate_release_gate
from src.nodes.telemetry_monitor import monitor_telemetry
from src.nodes.health_evaluator import evaluate_health
from src.nodes.rollback_orchestrator import orchestrate_rollback


def build_graph():
    graph = StateGraph(ReleaseState)
    graph.add_node("context_aggregator", aggregate_context)
    graph.add_node("risk_analyzer", analyze_risk)
    graph.add_node("release_gate", evaluate_release_gate)
    graph.add_node("telemetry_monitor", monitor_telemetry)
    graph.add_node("health_evaluator", evaluate_health)
    graph.add_node("rollback_orchestrator", orchestrate_rollback)
    graph.set_entry_point("context_aggregator")
    graph.add_edge("context_aggregator", "risk_analyzer")
    graph.add_edge("risk_analyzer", "release_gate")
    graph.add_conditional_edges("release_gate", lambda s: "approved" if s.deployment_approved else "halted", {"approved": "telemetry_monitor", "halted": END})
    graph.add_edge("telemetry_monitor", "health_evaluator")
    graph.add_edge("health_evaluator", "rollback_orchestrator")
    graph.add_edge("rollback_orchestrator", END)
    return graph.compile()


release_graph = build_graph()

