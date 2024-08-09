import requests
from django.shortcuts import render
from django.conf import settings

def get_chatgpt_response(user_input):
    api_key = settings.OPENAI_API_KEY
    headers = {
        'Authorization': f'Bearer {api_key}',
        'Content-Type': 'application/json',
    }
    data = {
        'model': 'gpt-4',  # 使用するモデルを変更
        'messages': [
            {"role": "user", "content": user_input}
        ],
        'max_tokens': 150,
    }
    response = requests.post('https://api.openai.com/v1/chat/completions', headers=headers, json=data)

    if response.status_code == 200:
        try:
            return response.json()['choices'][0]['message']['content']
        except (KeyError, IndexError) as e:
            return f"Error processing response: {e}"
    else:
        return f"Request failed with status code {response.status_code}: {response.text}"

def index(request):
    if request.method == 'POST':
        user_input = request.POST.get('user_input')
        gpt_response = get_chatgpt_response(user_input)
        return render(request, 'mytestapp/index.html', {'user_input': user_input, 'gpt_response': gpt_response})
    return render(request, 'mytestapp/index.html')
