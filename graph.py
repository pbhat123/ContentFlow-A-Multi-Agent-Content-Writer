# graph.py - Router → 3-way conditional edges.
# Agent ↔ tool loops using should_continue functions.
# General → END

from langgraph.checkpoint.memory import MemorySaver
from langgraph.graph import END, START, StateGraph
from langgraph.prebuilt import ToolNode

from general_handler import general_handler_node
from router import router_node
from seo_blog_writer import seo_blog_writer_node, seo_tools
from state import AgentState
from x_writer import x_blog_writer_node, x_tools

# Tool execution nodes
seo_tools_node = ToolNode(seo_tools)
x_tools_node = ToolNode(x_tools)

def route_from_router(state: AgentState) -> str:
    return state["route"]

def should_continue_seo(state: AgentState) -> str:
    last_message = state["messages"][-1]

    if getattr(last_message, "tool_calls", None):
        return "seo_tools"

    return END

def should_continue_x(state: AgentState) -> str:
    last_message = state["messages"][-1]

    if getattr(last_message, "tool_calls", None):
        return "x_tools"

    return END

builder = StateGraph(AgentState) # type: ignore[arg-type]

# Agent nodes
builder.add_node("router", router_node) # type: ignore[arg-type]
builder.add_node("seo_writer", seo_blog_writer_node) # type: ignore[arg-type]
builder.add_node("x_writer", x_blog_writer_node) # type: ignore[arg-type]
builder.add_node("general_handler", general_handler_node) # type: ignore[arg-type]

# Tool nodes
builder.add_node("seo_tools", seo_tools_node)
builder.add_node("x_tools", x_tools_node)

# Start → Router
builder.add_edge(START, "router")

# Router → Agent
builder.add_conditional_edges(
    "router",
    route_from_router,
    {
        "seo_blog_writer": "seo_writer",
        "x_blog_writer": "x_writer",
        "general": "general_handler",
    },
)

# SEO Writer ↔ Tools
builder.add_conditional_edges(
    "seo_writer",
    should_continue_seo,
    {
        "seo_tools": "seo_tools",
        END: END,
    },
)

builder.add_edge("seo_tools", "seo_writer")

# X Writer ↔ Tools
builder.add_conditional_edges(
    "x_writer",
    should_continue_x,
    {
        "x_tools": "x_tools",
        END: END,
    },
)

builder.add_edge("x_tools", "x_writer")

# General Handler → END
builder.add_edge("general_handler", END)

# Persistence
memory = MemorySaver()

graph = builder.compile(
    checkpointer=memory
)