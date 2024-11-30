from langchain_google_vertexai import ChatVertexAI

def get_google_model_pro():
    return ChatVertexAI(
    temperature=0,
    model_name="gemini-1.5-pro-002",
    max_retries=2,
    max_tokens=8192,
    # top_p=0.01,
    # top_k=1,
)

def get_google_model_flash():
    return ChatVertexAI(
        temperature=0,
        model_name="gemini-1.5-flash-002",
        max_retries=2,
        max_tokens=8192,
        # top_p=0.01,
        # top_k=1,
    )
