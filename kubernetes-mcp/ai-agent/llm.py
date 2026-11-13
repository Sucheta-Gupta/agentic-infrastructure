from google import genai
from google.genai.types import HttpOptions,GenerateContentConfig,AutomaticFunctionCallingConfig


genai_client = genai.Client(
    vertexai=True,
    project="dev-8fenak",
    location="global",
    http_options=HttpOptions(api_version="v1"),
)
# response = genai_client.models.generate_content(
#     model="gemini-3.8-flash",
#     contents="How does AI work?",
# )
# print(response.text)



async def ask_gemini(question, gemini_tool):
    

    response = await genai_client.aio.models.generate_content(
        model="gemini-3.8-flash",
        contents=question,
        config=GenerateContentConfig(
            tools= [gemini_tool],
            automatic_function_calling=AutomaticFunctionCallingConfig(
                disable=True
        ),
    ))
    return response


async def continue_conversation(question, content,tool_response_content,gemini_tool):
    response = await genai_client.aio.models.generate_content(
        model="gemini-3.8-flash",
        contents = [question, content, tool_response_content],
        config=GenerateContentConfig(
            tools= [gemini_tool],
            automatic_function_calling=AutomaticFunctionCallingConfig(
                disable=True
                ),
            )
    )
    return response
    