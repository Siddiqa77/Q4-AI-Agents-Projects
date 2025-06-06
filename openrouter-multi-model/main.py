# import chainlit as cl
# from models import MODEL_LIST
# from openrouter_client import fetch_model_response

# @cl.on_message
# async def on_message(message: cl.Message):
#     prompt = message.content
#     await cl.Message(content="⏳ Fetching responses...").send()

#     responses = []
#     for model in MODEL_LIST:
#         try:
#             response = await fetch_model_response(model["name"], prompt)
#             responses.append((model["name"], response))
#         except Exception as e:
#             responses.append((model["name"], f"❌ Error: {str(e)}"))

#     for model_name, response in responses:
#         await cl.Message(
#             content=f"**{model_name}**\n\n{response}"
#         ).send()


import chainlit as cl
from models import MODEL_LIST
from openrouter_client import fetch_model_response

# Convert model names into a list for easy matching
MODEL_NAMES = [model["name"] for model in MODEL_LIST]

@cl.on_chat_start
async def start():
    model_list_str = "\n".join(f"- {name}" for name in MODEL_NAMES)

    await cl.Message(
        f"👋 Welcome! Please select a model by typing its name from the following list:\n\n{model_list_str}"
    ).send()

@cl.on_message
async def on_message(message: cl.Message):
    user_input = message.content.strip()

    selected_model = cl.user_session.get("model_choice")

    # If no model selected yet, treat the first message as model selection
    if not selected_model:
        if user_input in MODEL_NAMES:
            cl.user_session.set("model_choice", user_input)
            await cl.Message(f"✅ Model set to **{user_input}**. Now send your prompt!").send()
        else:
            await cl.Message("❌ Invalid model name. Please type a valid model name from the list.").send()
        return

    # If model is already selected, treat message as prompt
    await cl.Message(f"⏳ Fetching response from **{selected_model}**...").send()

    try:
        response = await fetch_model_response(selected_model, user_input)
        await cl.Message(f"**{selected_model} says:**\n\n{response}").send()
    except Exception as e:
        await cl.Message(f"❌ Error: {str(e)}").send()
