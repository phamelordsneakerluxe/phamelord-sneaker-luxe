import os
import json
from flask import Flask, render_template, request, redirect, url_for, flash
from werkzeug.utils import secure_filename

app = Flask(__name__)
app.secret_key = 'supersecretkey'  # Change to your own secret for production

UPLOAD_FOLDER = 'static/uploads'
DATA_FILE = 'sneakers.json'
ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif'}

app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

def load_sneakers():
    if os.path.exists(DATA_FILE):
        with open(DATA_FILE, 'r') as f:
            return json.load(f)
    return []

def save_sneakers(data):
    with open(DATA_FILE, 'w') as f:
        json.dump(data, f, indent=4)

@app.route('/')
def index():
    sneakers = load_sneakers()
    return render_template('index.html', sneakers=sneakers)

@app.route('/admin', methods=['GET', 'POST'])
def admin():
    if request.method == 'POST':
        name = request.form.get('name')
        price = request.form.get('price')
        description = request.form.get('description')
        file = request.files.get('image')

        if not all([name, price, description, file]):
            flash('All fields are required.')
            return redirect(request.url)

        if file and allowed_file(file.filename):
            filename = secure_filename(file.filename)
            filepath = os.path.join(app.config['UPLOAD_FOLDER'], filename)
            file.save(filepath)

            sneakers = load_sneakers()
            sneakers.append({
                'name': name,
                'price': price,
                'description': description,
                'image': filepath.replace('\\', '/')
            })
            save_sneakers(sneakers)

            flash('Sneaker added successfully!')
            return redirect(url_for('index'))
        else:
            flash('Invalid image file type.')
            return redirect(request.url)

    return render_template('admin.html')

@app.route('/contact')
def contact():
    phone = "233XXXXXXXXX"  # Replace with your WhatsApp number including country code
    email = "youremail@example.com"  # Replace with your email
    sneaker_name = request.args.get('name')
    return render_template('contact.html', sneaker_name=sneaker_name, phone=phone, email=email)

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port)
