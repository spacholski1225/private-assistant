from smolagents import CodeAgent, DuckDuckGoSearchTool, LiteLLMModel

from tools.utils import stretching_video_link

class Agent:
    def ask_agent(question: str):
        model = LiteLLMModel(model_id="gpt-4o-mini")
        codeAgent = CodeAgent(tools=[DuckDuckGoSearchTool(), stretching_video_link], model=model)
        answer = codeAgent.run(question)

        return answer