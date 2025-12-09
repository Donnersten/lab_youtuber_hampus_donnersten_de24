from pydantic_ai import Agent
from backend.data_models import RagResponse
from backend.constans import VECTOR_PATH
import lancedb

vector_db = lancedb.connect(uri=VECTOR_PATH)

rag_agent = Agent(
    model="google-gla:gemini-2.5-flash",
    retries=2,
    system_prompt=(
        """
        You are an expert data engineering YouTuber with a friendly, nerdy tone.
        Always answer strictly based on the retrieved transcript data. If the user asks about something not found in the retrieved context, say that you don’t have enough information to answer.
        Keep answers clear, concise, and directly to the point (maximum 6 sentences).
        You may add light expertise or clarification, but never hallucinate.
        """
    ),
    output_type= RagResponse,

)

@rag_agent.tool_plain
def retrive_top_documents(query: str, k=3) -> str:
    """
    Uses vector search to find the closest k matching documents to the query
    """
    results = vector_db["youtube"].search(query=query).limit(k).to_list()
    top_result = results[0]

    return f"""
    Filename: {top_result["filename"]},

    Filepath: {top_result["filepath"]},
    
    Content: {top_result["content"]}

    """

def chat(prompt:str) -> dict:
    message_history = result.all_messages() if result else None
    result = rag_agent.run_sync(prompt, message_history=message_history)

    return {"user": prompt, "bot": result.output}