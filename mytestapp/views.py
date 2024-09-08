import requests
from django.shortcuts import render
from django.conf import settings
# from .utils import extract_text_from_predefined_pdf
from .forms import QueryForm
from .note import reference

# Function to interact with ChatGPT API
def get_chatgpt_response(messages):
    api_key = settings.OPENAI_API_KEY
    headers = {
        'Authorization': f'Bearer {api_key}',
        'Content-Type': 'application/json',
    }
    # data = {
    #     'model': 'gpt-4',  # 使用するモデルを指定
    #     'messages': messages,  # ユーザーとこれまでの会話の履歴を送信
    #     'max_tokens': 1000,
    # }
    payload = {
        "model": "gpt-4o-mini",
        "messages":[
            # {"role": "system", "content": f"以下のテキストからユーザーの質問に対応する番号を教えてください。複数ある場合は複数挙げてください。数字だけで結構です。{note.reference}"},
            {"role": "system", "content": f"以下のテキストからユーザーの質問に対応する文章を生成してください。{reference}"},
            {"role": "user", "content": f"{messages}"}
        ],
        "temperature":0.0,
        "max_tokens": 150
    }
    response = requests.post('https://api.openai.com/v1/chat/completions', headers=headers, json=payload)

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
        selected_check = request.POST.get('check')  # 選択されたチェックボックスの値を取得

        if selected_check == "check1":
            selected_text = "本科"
        elif selected_check == "check2":
            selected_text = "専攻科"
        else:
            selected_text = "None"

        # PDFからテキストを抽出
        # pdf_text = extract_text_from_predefined_pdf()
        # print(pdf_text)

        # # セッションから会話履歴を取得、存在しなければ新しく作成
        # conversation = request.session.get('conversation', [])

        # # 新しいユーザー入力を会話履歴に追加
        # conversation.append({"role": "user", "content": user_input})

        # # PDFのテキストとユーザーのクエリを組み合わせたプロンプトを作成
        # combined_prompt = f"以下のテキストから関連する情報を抽出してください:\n\n{pdf_text}\n\nユーザーの質問: {user_input}"
        combined_prompt = f"ユーザーの質問: {user_input}"

        # 新しいプロンプトを会話履歴に追加（オプション）
        # conversation.append({"role": "user", "content": combined_prompt})

        # ChatGPTからの応答を取得
        # gpt_response = get_chatgpt_response(conversation)
        gpt_response = get_chatgpt_response(user_input)

        # 応答を会話履歴に追加
        # conversation.append({"role": "assistant", "content": gpt_response})

        # 更新した会話履歴をセッションに保存
        # request.session['conversation'] = conversation

        context = {
            'user_input': user_input,
            'gpt_response': gpt_response,
            'selected_check': selected_text
        }

        return render(request, 'mytestapp/index.html', context)
    else:
        # GETリクエスト時にセッションをクリアするか、デフォルトで新しい会話を開始する
        request.session['conversation'] = []
        return render(request, 'mytestapp/index.html')
