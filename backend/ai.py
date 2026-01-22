from api_keys import QWEN_key
from openai import OpenAI, OpenAIError


if __name__ == '__main__':
    key = QWEN_key
    client = OpenAI(
        # 若没有配置环境变量，请用百炼API Key将下行替换为：api_key="sk-xxx"
        # 新加坡/弗吉尼亚和北京地域的API Key不同。获取API Key：https://www.alibabacloud.com/help/zh/model-studio/get-api-key
        api_key=QWEN_key,
        # 以下为新加坡/弗吉尼亚地域base_url，若使用北京地域的模型，需将base_url替换为：https://dashscope.aliyuncs.com/compatible-mode/v1
        base_url="https://dashscope.aliyuncs.com/compatible-mode/v1",
    )
    # main.py
    try:
        # noinspection PyTypeChecker
        completion = client.chat.completions.create(
            model="qwen-plus",
            messages=[{'role': 'system', 'content': 'You are a helpful assistant.'},
                      {'role': 'user', 'content': r""" 
                      你是一个天气助手
                      {}"""}],
            stream=True,
            stream_options={"include_usage": True}
        )
        for chunk in completion:
            print(chunk.model_dump()['choices'][0]['delta']['content'], end='', flush=True)
            # print(chunk.model_dump())
    except Exception or OpenAIError as e:
        # print(f"API调用错误: {e}")
        pass
