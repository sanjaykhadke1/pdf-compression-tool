from flask import Flask, render_template, request, send_file
import PyPDF2
import io

app = Flask(__name__)

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        uploaded_file = request.files['pdf_file']
        if uploaded_file.filename.endswith('.pdf'):
            reader = PyPDF2.PdfReader(uploaded_file)
            writer = PyPDF2.PdfWriter()

            for page in reader.pages:
                writer.add_page(page)

            output_stream = io.BytesIO()
            writer.write(output_stream)
            output_stream.seek(0)

            return send_file(
                output_stream,
                as_attachment=True,
                download_name='compressed.pdf',
                mimetype='application/pdf'
            )

    return render_template('index.html')

if __name__ == '__main__':
   import os
port = int(os.environ.get("PORT", 5000))
app.run(host='0.0.0.0', port=port)
