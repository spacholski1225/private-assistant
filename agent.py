from smolagents import CodeAgent, DuckDuckGoSearchTool, LiteLLMModel

from tools.download import HFModelDownloadsTool

class Agent:
    def ask_agent(question: str):
        model = LiteLLMModel(model_id="gpt-4o-mini")
        codeAgent = CodeAgent(tools=[DuckDuckGoSearchTool(), HFModelDownloadsTool()], model=model)
        answer = codeAgent.run(question)

        return answer