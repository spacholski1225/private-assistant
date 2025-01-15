from smolagents import CodeAgent, DuckDuckGoSearchTool, LiteLLMModel

class Agent:
    def ask_agent(question: str):
        model = LiteLLMModel(model_id="gpt-4o-mini")
        codeAgent = CodeAgent(tools=[DuckDuckGoSearchTool()], model=model)
        answer = codeAgent.run(question)

        return answer