"""import requests
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
"""
import requests
from django.shortcuts import render
from django.conf import settings

# Function to interact with ChatGPT API
def get_chatgpt_response(messages):
    api_key = settings.OPENAI_API_KEY
    headers = {
        'Authorization': f'Bearer {api_key}',
        'Content-Type': 'application/json',
    }
    data = {
        'model': 'gpt-4',  # 使用するモデルを指定
        'messages': messages,  # ユーザーとこれまでの会話の履歴を送信
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

# View for handling user input and responses
def index(request):
    if request.method == 'POST':
        user_input = request.POST.get('user_input')

        # セッションから会話履歴を取得、存在しなければ新しく作成
        conversation = request.session.get('conversation', [])

        # デバッグ: セッション内容をコンソールに出力
        print("Current Conversation:", conversation)

        # 新しいユーザー入力を会話履歴に追加
        conversation.append({"role": "user", "content": user_input})

        # ChatGPTからの応答を取得
        gpt_response = get_chatgpt_response(conversation)

        # 応答を会話履歴に追加
        conversation.append({"role": "assistant", "content": gpt_response})

        # 更新した会話履歴をセッションに保存
        request.session['conversation'] = conversation

        return render(request, 'mytestapp/index.html', {'user_input': user_input, 'gpt_response': gpt_response})
    else:
        # GETリクエスト時にセッションをクリアするか、デフォルトで新しい会話を開始する
        request.session['conversation'] = []
        return render(request, 'mytestapp/index.html')
