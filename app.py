from cryptography.fernet import Fernet, InvalidToken
from flask import Flask, request, render_template
import openai
import os

app = Flask(__name__)

# Encryption key (replace with your actual encryption key)
encryption_key = b'V59yiO3MxO5LW0V0rZIHfE5R6-6IsLsYQPhMgRFQY3A='
cipher = Fernet(encryption_key)

def decrypt_api_key(encrypted_key):
    try:
        decrypted_key = cipher.decrypt(encrypted_key)
        return decrypted_key.decode()
    except InvalidToken:
        print("Invalid token or decryption key")
        return None

# Specify the absolute path to config.txt
config_path = 'C:/Users/PC/Documents/Work/Simple Chatbot/config.txt'

# Load encrypted API key from config.txt
with open(config_path, 'rb') as config_file:
    encrypted_api_key = config_file.read().strip()

# Decrypt API key
decrypted_api_key = decrypt_api_key(encrypted_api_key)
print("Decrypted API Key:", decrypted_api_key)  
if decrypted_api_key is not None:
    openai.api_key = decrypted_api_key
    print("openai.api_key set:", openai.api_key)  

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
