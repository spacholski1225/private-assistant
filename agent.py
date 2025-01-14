from smolagents import CodeAgent, DuckDuckGoSearchTool, LiteLLMModel

model = LiteLLMModel(model_id="gpt-4o-mini")
agent = CodeAgent(tools=[DuckDuckGoSearchTool()], model=model)

agent.run("Zjadłem 3 gryzy drożdzówki. Ile to będzie mialo kalorii?")