from flask import Flask, request, render_template, send_file
import os
import PyPDF2

app = Flask(__name__)
UPLOAD_FOLDER = 'static/uploads'
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        # Verifica se a pasta de uploads existe, se não cria
        if not os.path.exists(UPLOAD_FOLDER):
            os.makedirs(UPLOAD_FOLDER)

        # Salva os arquivos PDF enviados
        files = request.files.getlist('files')
        pdf_files = []  # Lista para armazenar os caminhos dos arquivos PDF

        for file in files:
            if file.filename.endswith('.pdf'):
                file_path = os.path.join(app.config['UPLOAD_FOLDER'], file.filename)
                file.save(file_path)
                pdf_files.append(file_path)  # Armazena o caminho do arquivo na lista

        # Inverte a lista para mesclar em ordem decrescente
        pdf_files.reverse()  # Inverte a lista para a mesclagem decrescente

        # Mescla os PDFs na ordem de seleção (invertida)
        merger = PyPDF2.PdfMerger()
        for pdf_file in pdf_files:  # Mescla na ordem decrescente
            merger.append(pdf_file)

        # Gera o arquivo mesclado
        merged_pdf_path = 'merged.pdf'
        merger.write(merged_pdf_path)
        merger.close()

        # (Opcional) Limpar os arquivos carregados após a mesclagem
        for pdf_file in pdf_files:
            os.remove(pdf_file)

        return send_file(merged_pdf_path, as_attachment=True)

    return render_template('index.html')

if __name__ == '__main__':
    app.run(debug=True)
