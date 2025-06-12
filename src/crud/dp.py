#type: ignore
from sqlalchemy.ext.asyncio import AsyncSession
from typing import List
import json

from src.crud.user_db import get_user_by_id,reflush_user_chat
from .air_scraper import get_air_info
from config import get_ds_client
from src.schemas.base import DATE
from promot import ds_pormpt
from promot import tools_list

def send_message(message):
    ds_client = get_ds_client()
    response = ds_client.chat.completions.create(
        model="deepseek-chat",
        messages= message,
        stream=False,
        response_format={"type":"json_object"},
        tools= tools_list,
    )

    return response



# 可以根据你注册的其他 tools 继续添加 import
def handle_tool_call(tool_call):
    
    """
    根据 tool_call 信息分发到对应的函数执行。
    参数：
        tool_call: 一个 ToolCall 对象（来自 chat_completion.choices[0].message.tool_calls）
    返回：
        函数运行结果对象（建议为 dict，可被 json 序列化）
    """

    tool_name = tool_call.function.name
    try:
        arguments = json.loads(tool_call.function.arguments)
    except json.JSONDecodeError as e:
        raise ValueError(f"解析 tool 参数失败: {e}")

    # 根据 tool 名称路由到具体的函数
    if tool_name == "get_Air":
        return get_Air(**arguments)
    #TODO: 之后添加路由在此处
    
    else:
        raise NotImplementedError(f"未注册的工具函数: {tool_name}")


#CRUD：从ChatCompletion对象提取文本内容
def extract_text(chat_completion):
    try:
        # 尝试获取回复内容 - 适用于OpenAI的ChatCompletion对象
        msg = chat_completion.choices[0].message

        if msg.tool_calls:
            return {
                'type': 'tool_call',
                'tool_calls': chat_completion.choices[0].message.tool_calls
            }
        
        return {
            "type": "reply",
            "content": msg.content
        }
    
    except (AttributeError, IndexError, TypeError):
        try:
            return str(chat_completion)
        except:
            return "无法提取回复内容"
        
        
#CRUD：获取机票信息 TODO:实现函数
def get_Air(dep_air:str, des_air:str, date:str):
    """
        搜索获取[dep-des]日期的机票详情：
        Air{
            dep_air: str = Field(..., description="出发地点")
            des_air: str = Field(..., description="到达地点")
            price: float = Field(..., description="机票价格")
            dep_time: Itinerary_time = Field(..., description="出发时间")
            des_time: Itinerary_time = Field(..., description="到达时间")
            airline: str = Field(..., description="航空公司")
        }
    """
    year, month, day = map(int, date.split('-'))

    Date = DATE(year=str(year),month=str(month),day=str(day)) 
    Air_list = []
    Air_list = get_air_info(dep_air, des_air, Date)

    result = [air.model_dump() for air in Air_list]

    return result


#CRUD：获取指定地点附近酒店信息（10km？）TODO:实现函数
def get_Hotel_by_loc(location:str, date:DATE):
    """
    搜索指定酒店名称的酒店信息include：
        hotel_name: str, 酒店名称
        address: str, 地址
        star: str, 星级
        room:room = {
            room_type: str, 房型
            price: str, 价格
            free_room: bool, 指定时间内是否有房间   
        }
    """
    pass

#CRUD：获取指定酒店信息（10km？） TODO:实现函数
def get_Hotel_by_name(hotel_name:str,date:DATE):
    """
    搜索指定酒店名称的酒店信息include：
        hotel_name: str, 酒店名称
        address: str, 地址
        star: str, 星级
        room:room = {\
            room_type: str, 房型
            price: str, 价格
            free_room: bool, 指定时间内是否有房间   
        }
    """
    pass

#CRUD：获取指定地点天气信息 TODO:实现函数
def  get_weather_by_loc(location:str,date):
    """
    获取指定地点的天气信息
    """
    pass

#CRUD：获取指定用户对话历史 TODO:实现函数
CHAT = [{"role": ds_pormpt.system_role, "content": ds_pormpt.system_content}]
async def get_chat_by_id(UserId:str,db:AsyncSession)-> List[dict]:
    """
    获取指定用户的对话
    """
    try:
        user = await get_user_by_id(UserId,db)

        if user.ChatHistory == None or user.ChatHistory == "string":
            user.ChatHistory = json.dumps(CHAT)
        
        user_chat = json.loads(user.ChatHistory)

        return user_chat
    except Exception as e:
        return CHAT

async def chat_loop_block(message:str|None , UserId:str, db:AsyncSession):
    user_chat = await get_chat_by_id(UserId,db)
    if message:
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

        await reflush_user_chat(UserId,db,user_chat)
        return user_chat
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
            await reflush_user_chat(UserId,db,user_chat)

            return await chat_loop_block(None,UserId,db)
            
    elif response_result["type"] == "error":
        raise ValueError(f"工具调用失败: {response_result['error']}")