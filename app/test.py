#type: ignore
from src.crud.dp import extract_text,handle_tool_call
from src.crud.dp import send_message
from promot import ds_pormpt
# from crud.dp import get_chat_by_id

import json


CHAT = [{"role": ds_pormpt.system_role, "content": ds_pormpt.system_content}]


def chat_loop_block(message,UserId:str):
    user_chat = CHAT
    #TODO: to make this func come to be real
    # user_chat = get_chat_by_id(UserId)

    user_chat.append(
        {
            "role" : "user",
            "content": message
        }
    )

    chat_completion = send_message(user_chat)
    response_result = extract_text(chat_completion)

    if response_result["type"] == "reply":
        user_chat.append({
                "role" : "assistant",
                "content" : response_result["content"]}
        )

        print("Assistant:", response_result["content"])   
    elif response_result["type"] == "tool_call":
        for call in response_result["tool_calls"]:
            user_chat.append({
                "role": "assistant",
                "tool_calls": [
                    {
                    "id":call.id,
                    "type": "function",
                    "function": {"name": call.function.name, "arguments": call.function.arguments} 
                    }
                ]
            })
            tool_result = handle_tool_call(call)   
            user_chat.append(
                {
                    "role": "tool",
                    "tool_call_id": call.id,
                    "content": f"{json.dumps(tool_result, ensure_ascii=False)}"
                }
            )
            
    elif response_result["type"] == "error":
        print("发生错误：", response_result["error"])


message = "请帮我规划一个在5.29日从重庆去北京的旅行，我比较想要有充足的时间来在故宫拍照以及游玩，我的预算大概是2000元，能否帮我规划一下？"
UserId = "12345"
chat_loop_block(message, UserId)