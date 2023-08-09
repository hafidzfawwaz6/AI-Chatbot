from flask import Flask, request, render_template
import openai
import os

app = Flask(__name__)

openai.api_key = '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'

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/api', methods=['POST'])
def api():
    message = request.form.get("message")

    try:
        completion = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "user", "content": message}
            ]
        )

        if completion.choices[0].message != None:
            return completion.choices[0].message
        else:
            return 'Failed to Generate response!'

    except Exception as e:
        return f'Error: {str(e)}'



if __name__ == '__main__':
    app.run(debug=True)
