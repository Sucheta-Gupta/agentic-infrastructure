from contextlib import asynccontextmanager
import asyncio
import pprint
from mcp import ClientSession
from mcp.client.streamable_http import streamable_http_client
from google.genai import types
import json
from llm import ask_gemini , continue_conversation


mcp_server = "http://127.0.0.1:8000/mcp"


@asynccontextmanager
async def connect_mcp():
    async with streamable_http_client(url=mcp_server) as (read_stream, write_stream):
        async with ClientSession(read_stream,write_stream) as session:
            await session.initialize()
            yield session


async def call_mcp_tool(session, name, **kwargs):
    response = await session.call_tool(name, kwargs)
    return response
     


async def list_mcp_tools(session) ->list:
        available_tools = []
        response = await session.list_tools()
        if response:
            for tool in response.tools:
                available_tools.append({
                    "name": tool.name,
                    "description": tool.description, 
                    "input_schema" : tool.input_schema
                    }
                    )
                
            return available_tools
        return []


def convert_mcp_tools_to_gemini(mcp_tools):
    
    gemini_functions = []

    for tool in mcp_tools:
        function = types.FunctionDeclaration( 
            name = tool.get("name"),
            description = tool.get("description"),
            parameters_json_schema = tool.get("input_schema"),
        )

        gemini_functions.append(function)

    return gemini_functions

            
async def ask_kubernetes(question: str) -> str:
    async with connect_mcp() as session:
        tools=await list_mcp_tools(session)
        # print("MCP TOOLS:")
        #pprint.pp(tools)
        
        gemini_functions = convert_mcp_tools_to_gemini(tools)
        gemini_tool = types.Tool(
            function_declarations=gemini_functions
        )
        # if gemini_tool.function_declarations is not None:
        #     for function in gemini_tool.function_declarations:
        #         print("Name:", function.name)
        #         print("Description:", function.description)
        #         print("Parameters:", function.parameters_json_schema)
        #         print("-" * 50)


        response = await ask_gemini(question, gemini_tool) 
        if not response.candidates:
            raise RuntimeError("Gemini returned no candidates")
        function_call_content=response.candidates[0].content
        # print("Gemini function calls:")
        function_calls = response.function_calls
        function_response_parts = []
        
        
        for function in function_calls or []:

            func_name = function.name
            func_args = function.args or {}
            if func_name is None:
                continue
            mcp_result = await call_mcp_tool(session,func_name,**func_args)
  
            # print(type(response))

            contents = mcp_result.content
            results = []

            for content in contents:
                text = json.loads(content.text)
                results.append(text)
            # print(type(response.content[0])
            # print(results)


            part_response = types.Part.from_function_response(name=func_name,response={"results":results})
            function_response_parts.append(part_response)

        tool_response_content=types.Content(
            role = "tool",
            parts = function_response_parts
        )

    
        final_response = await continue_conversation(question,function_call_content,tool_response_content,gemini_tool)


        if not final_response.candidates:
            raise RuntimeError("Gemini returned no candidates")

        content = final_response.candidates[0].content

        if not content or not content.parts:
            raise RuntimeError("Gemini returned no content")

        answer = content.parts[0].text

        if answer is None:
            raise RuntimeError("Gemini returned no text")

        return answer
    
if __name__ == "__main__":
    answer = asyncio.run(
        ask_kubernetes("List all pods in the mcp-demo namespace")
    )
    print(answer)