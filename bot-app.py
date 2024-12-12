import streamlit as st
import config
from openai import OpenAI
import base64
from tools import ConnectionManager
import json
import asyncio

system_prompt = """
You are an AI Assistant representing Constoso Gaming Inc. You are tasked with helping their Customers with their queries and grievances.
Determine the intent of the user query and respond accordingly.
"""


system_prompt_response = """
You are an AI Assistant representing Constoso Gaming Inc.
Refer to the context provided to you below to respond to the user query.

Your audio response has to be concise and clear.
- When the content in the response is a rowset, you can provide a summary of the data in Markdown table format.
- For verbose content, format the response using bullet points, to make for easy reading.

"""

if "connection" in st.session_state and st.session_state["connection"]:
    pass
else:
    st.session_state["connection"] = ConnectionManager()

config.load_dotenv()
client = OpenAI(api_key=config.api_key)
st.title("Contoso Gaming Inc. AI Assistant")

if "messages" not in st.session_state:
    st.session_state.messages = []
    st.session_state.messages.append({"role": "system", "content": system_prompt})


audio_value = st.audio_input("Ask your question!")

encoded_string = None
if audio_value:
    audio_data = audio_value.read()
    encoded_audio_string = base64.b64encode(audio_data).decode("utf-8")

    st.session_state.messages.append(
        {
            "role": "user",
            "content": [
                {
                    "type": "input_audio",
                    "input_audio": {"data": encoded_audio_string, "format": "wav"},
                }
            ],
        }
    )
    completion = None
    try:
        completion = client.chat.completions.create(
            model=config.model,
            modalities=["text", "audio"],
            audio={"voice": "alloy", "format": "wav"},
            functions=st.session_state["connection"].functions,
            function_call="auto",
            messages=st.session_state.messages,
        )
    except Exception as e:
        print("Error in completion", e)
        st.write("Error in completion", e)
        st.stop()

    # print(completion.choices[0].message)
    function_response = None
    if completion.choices[0].message.function_call:
        # print(f"Function call detected \n,{completion.choices[0].message}")
        tool_call = completion.choices[0].message.function_call.name
        function_to_call = st.session_state["connection"].available_functions[tool_call]
        print("Tool call: >", tool_call)

        arguments = json.loads(completion.choices[0].message.function_call.arguments)
        print("Arguments: >", arguments)

        function_response = None
        if asyncio.iscoroutinefunction(function_to_call):
            function_response = asyncio.run(
                function_to_call(st.session_state["connection"], **arguments)
            )
        else:
            function_response = function_to_call(**arguments)
        print("Output of function call: >", function_response)

        l_completion = client.chat.completions.create(
            model=config.model,
            modalities=["text", "audio"],
            audio={"voice": "alloy", "format": "wav"},
            messages=[
                {
                    "role": "system",
                    "content": [{"type": "text", "text": system_prompt_response}],
                },
                {
                    "role": "user",
                    "content": [
                        {
                            "type": "text",
                            "text": "---- context -----\n"+str(function_response) + "\n --- User Query----:\n",
                        },
                        {
                            "type": "input_audio",
                            "input_audio": {
                                "data": encoded_audio_string,
                                "format": "wav",
                            },
                        },
                    ],
                },
            ],
        )
        wav_bytes = base64.b64decode(l_completion.choices[0].message.audio.data)

        transcript_out = l_completion.choices[0].message.audio.transcript
        st.session_state.messages.append(
            {
                "role": "assistant",
                "content": transcript_out,
            }
        )

        with st.chat_message("assistant"):
            st.markdown(transcript_out)
        st.audio(wav_bytes, format="audio/wav", autoplay=True)

    else:
        # The model response that is based on its own knowledge on the topic or context in the question. There is no grounding
        wav_bytes = base64.b64decode(completion.choices[0].message.audio.data)
        st.session_state.messages.append(
            {
                "role": "assistant",
                "audio": {"id": completion.choices[0].message.audio.id},
            }
        )
        with st.chat_message("assistant"):
            st.markdown(completion.choices[0].message.audio.transcript)
        st.audio(wav_bytes, format="audio/wav", autoplay=True)
