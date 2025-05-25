import os
import datetime


#CRUD：从JSON模板文件中读取模板
def load_template_from_json(file_path=f"H:\\Gowhere_Bac_project\\asset\\json\\travel_plan_template.json"):
    try:
        if os.path.exists(file_path):
            with open(file_path, 'r', encoding='utf-8') as f:
                return f.read()
        else:
            print(f"警告: 模板文件不存在: {file_path}")
            return "{}"
    except Exception as e:
        print(f"读取模板文件时出错: {e}")
        return "{}"

#-------------------air_scraper-------------------------------
# 加载JSON模板
travel_plan_json_template = load_template_from_json()

class Ds_Pormpt:
    system_role = "system"
    
    now_time = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")

    system_content = f"""
    你是一个旅行规划师的序列化程序，名字叫小GO。
    你的工作是帮助用户计划他们的旅行，并将其日程作JSON格式输出。
    你的回答必须为JSON格式。格式例子如下:
    {travel_plan_json_template}
    如果用户询问你关于旅行的问题，你要为他们提供真实可信的信息
    ，并帮助他们规划符合他们要求的行程,或者提出问题以获取更多信息.
    现在时间为{now_time},你的规划必须在未来
    你只能回答关于旅行的问题,如果用户询问你关于其他事情，你可以不回答，
    并返回
    {{"error": False ,"message":"你只能回答关于旅行的问题"}}
    """

ds_pormpt = Ds_Pormpt()

tools_list = [
    {
        "type": "function",
        "function": {
            "name": "get_Air",
            "description": "查询机票信息",
            "parameters": {
                "type": "object",
                "properties": {
                    "dep_air": {"type": "string", "description": "出发地"},
                    "des_air": {"type": "string", "description": "目的地"},
                    "date": {"type": "string", "format": "date", "description": "出发日期（YYYY-MM-DD）"},
                },
                "required": ["dep_air", "des_air", "date"]
            }
        }
    }
]




class Sp_Pormpt :
    system_role = "system"

    system_content = """
    注意，你是一个判断输入语意的AI，你的任务是判断用户的提问或对话是否与旅游相关。
    你的回复json schema是{'jud':'True'/'False'}。
    当用户的提问或对话涉及旅游咨询时（如旅行建议、景点推荐、行程规划、路程规划、酒店预定等）
    或者涉及无关紧要的问候之类的对话时，你的回复应该是{'jud':'True'}否则{'jud':'False'}。
    请确保严格按照格式回答，且不要提供额外的解释。
    """

sp_pormpt = Sp_Pormpt()
