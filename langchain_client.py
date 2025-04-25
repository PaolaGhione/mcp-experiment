import asyncio
from dotenv import load_dotenv

from langchain_mcp_adapters.client import MultiServerMCPClient
from langgraph.prebuilt import create_react_agent
from langchain_openai import ChatOpenAI

load_dotenv()

llm = ChatOpenAI(model="gpt-4o-mini")


async def main():
    # print("Starting LangChain MCP Client")
    async with MultiServerMCPClient(
        {
            "math": {
                "command": "python",
                "args": ["C:/mcpprojects/mcp-experiment/servers/math_server.py"],
            },
            "weather": {
                "url": "http://localhost:8000/sse",
                "transport": "sse",
            },
        }
    ) as client:
        agent = create_react_agent(llm, client.get_tools())
        result = await agent.ainvoke(
            {"messages": "what is the weather in San Francisco?"}
        )
        print(result["messages"][-1].content)


if __name__ == "__main__":
    asyncio.run(main())
