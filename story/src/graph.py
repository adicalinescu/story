from langchain_core.messages import  HumanMessage, AIMessage
from langgraph.graph import END, StateGraph, START
from langgraph.prebuilt import ToolNode
from langgraph.graph import MessagesState
from typing import Literal

from story.src.agent import  writer_agent, critic_agent
from story.src.tools import  DirectAnswer, WriterAnswer


def call_writer(state: MessagesState):
    last_message = state["messages"][-1]
    if isinstance(last_message.content, list):
        feedback = last_message.content[0]["feedback"]
        last_message.content = f"Fix your story based on the remarks:\n{feedback}"
        state["messages"][-1].content = last_message.content
    response = writer_agent.invoke(state["messages"])
    return {"messages": AIMessage(content=response.to_list())}


def call_critic(state: MessagesState):
    last_message = state["messages"][-1]
    state["messages"][-1] = HumanMessage(content=f"{last_message.content[0]["story"]}")
    response = critic_agent.invoke({"messages": state["messages"]})
    return {"messages": AIMessage(content=response.to_list())}


def call_final_answer(state: MessagesState):
    story_message = state["messages"][-2]
    answer = WriterAnswer(story=story_message.content, general_answer="")
    answer.general_answer = ""
    answer.story = story_message.content
    return {"messages": AIMessage(content=answer.to_list())}


def writer_router(state: MessagesState) -> Literal["end", "continue"]:
    messages = state["messages"]
    last_message = messages[-1]
    if last_message.content[0]["story"] == '':
        return "end"
    else:
        return "continue"


def critic_router(state: MessagesState) -> Literal["feedback", "end"]:
    last_message =  state["messages"][-1]
    if last_message.content[0]["story_ok"]:
        return "end"
    else:
        return "feedback"


workflow = StateGraph(MessagesState)

workflow.add_node("writer", call_writer)
workflow.add_node("direct_answer", ToolNode(tools=[DirectAnswer]))
workflow.add_node("critic", call_critic)
workflow.add_node("final_answer", call_final_answer)

workflow.add_edge(START, "writer")
workflow.add_edge("direct_answer", END)
workflow.add_edge("final_answer", END)

workflow.add_conditional_edges(
    "writer",
    writer_router,
    {
        "continue": "critic",
        "end": "direct_answer"
    }
)

workflow.add_conditional_edges(
    "critic",
    critic_router,
    {
        "feedback": "writer",
        "end": "final_answer"
    }
)

graph = workflow.compile()

graph.get_graph().draw_mermaid_png(output_file_path='story.png')

out = graph.invoke(
    {"messages": "Please write a story, choose the topic"},
    debug=True
)

print(out["messages"][-1].content[0])
