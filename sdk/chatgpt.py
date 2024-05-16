from openai import OpenAI
from config import API_KEY, PROXY_URL, MODEL
from sdk.persisted_data import alloc, fetch

client = OpenAI(
    base_url=PROXY_URL,
    api_key=API_KEY
)

def ask(msg: list) -> str:
    ret = client.chat.completions.create(
      model=MODEL,
      messages=msg
    )
    # print(ret)
    token_usage = fetch('token_usage')
    if token_usage == None:
        alloc('token_usage', {
            "usage": 0
        })
        token_usage = fetch('token_usage')
    
    token = ret.usage.total_tokens
    token_usage.set('usage', token_usage.get('usage') + token)
    return ret.choices[0].message.content

def plain_msg(msg: str) -> list:
    return [
        { "role": "system", "content": "You are a helpful assistant." },
        { "role": "user", "content": msg }
    ]