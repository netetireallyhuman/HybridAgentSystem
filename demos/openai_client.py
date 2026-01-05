# openai_client.py    !This is a demo for a paid model!
# Register on https://platform.openai.com/ and obtain a free api-key (or pay if you like).
# Set an environment variable named "OPENAI_API_KEY" to the value of your API key.
# pip install pyautogen
# pip install "autogen-ext[openai]"
import asyncio
from autogen_agentchat.agents import AssistantAgent
from autogen_ext.models.openai import OpenAIChatCompletionClient
async def main() -> None:
    agent = AssistantAgent("assistant", OpenAIChatCompletionClient(model="gpt-4o"))
    print(await agent.run(task="Say 'Hello World!'"))

asyncio.run(main())
