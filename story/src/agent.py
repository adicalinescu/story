from story.src.llm import get_google_model_pro, get_google_model_flash
from story.src.tools import DirectAnswer, WriterAnswer, CriticAnswer
from story.src.prompt import writer_prompt_template, critic_prompt_template

llm = get_google_model_flash()



writer_agent = writer_prompt_template.partial(
    response_tool=DirectAnswer.__name__,
) |  llm.bind_tools(tools=[DirectAnswer]).with_structured_output(WriterAnswer)


critic_agent = critic_prompt_template.partial() |  llm.with_structured_output(CriticAnswer)

