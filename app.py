from bottle import Bottle, run, static_file, request, default_app
import os
import json
import requests

app = Bottle()

root_dir = os.path.dirname(os.path.realpath(__file__))

@app.route('/')
def main():
    return static_file('app.html', root=root_dir)

@app.route('/static/<filename:re:.*>')
def static(filename):
    return static_file(filename, root=root_dir + '/static/')

@app.route('/chat/', method='POST')
def chat():
    content = request.body.read()
    content = str(content, 'utf-8')
    contents = json.loads(content) 
    messages = []
    for i, c in enumerate(contents):
        if i % 2 == 0:
            messages.append({"role": "user", "content": c});
        else:
            messages.append({"role": "system", "content": c});
    openaidata = {"model": "gpt-3.5-turbo", "messages": messages}
    try:
        req = requests.post('https://api.openai.com/v1/chat/completions', headers={'Content-Type': 'application/json', 'Authorization': 'Bearer sk-API KEI'}, json=openaidata, timeout=90)
        res = req.text
        res = json.loads(res)
        res = res['choices'][0]['message']['content'].strip()
        return {
            "stat": 1,
            "data": res
        }
    except Exception as e:
        return {
            "stat": 0,
            "data": None
        }

if __name__ == '__main__':
    run(app, host='127.0.0.1', port=8787)
