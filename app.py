from flask import Flask, request, jsonify
import base64
import magic

app = Flask(__name__)

USER_ID = "john_doe_17091999"
EMAIL = "john@xyz.com"
ROLL_NUMBER = "ABCD123"

def is_prime(n):
    if n < 2:
        return False
    for i in range(2, int(n**0.5)+1):
        if n % i == 0:
            return False
    return True

@app.route('/bfhl', methods=['GET', 'POST'])
def bfhl():
    if request.method == 'GET':
        return jsonify({"operation_code": 1}), 200

    if request.method == 'POST':
        data = request.json.get('data', [])
        file_b64 = request.json.get('file_b64')

        numbers = [item for item in data if item.isdigit()]
        alphabets = [item for item in data if item.isalpha()]
        lowercase_letters = [c for c in data if c.islower()]
        highest_lowercase = [max(lowercase_letters)] if lowercase_letters else []

        prime_found = any(is_prime(int(num)) for num in numbers)

        file_valid = False
        mime_type = None
        file_size_kb = None

        if file_b64:
            try:
                file_data = base64.b64decode(file_b64)
                file_valid = True
                mime_type = magic.from_buffer(file_data, mime=True)
                file_size_kb = round(len(file_data) / 1024, 2)
            except Exception:
                file_valid = False

        response = {
            "is_success": True,
            "user_id": USER_ID,
            "email": EMAIL,
            "roll_number": ROLL_NUMBER,
            "numbers": numbers,
            "alphabets": alphabets,
            "highest_lowercase_alphabet": highest_lowercase,
            "is_prime_found": prime_found,
            "file_valid": file_valid,
            "file_mime_type": mime_type,
            "file_size_kb": file_size_kb
        }
        return jsonify(response), 200

if __name__ == '__main__':
    app.run(debug=True)
