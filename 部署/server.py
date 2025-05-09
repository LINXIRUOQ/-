from flask import Flask, request, send_from_directory  # 新增 send_from_directory
import os

app = Flask(__name__)
UPLOAD_FOLDER = 'uploads'

if not os.path.exists(UPLOAD_FOLDER):
    os.makedirs(UPLOAD_FOLDER)

app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

# 文件上传路由（原有代码）
@app.route('/upload', methods=['POST'])
def upload_file():
    if 'file' not in request.files:
        return "Error: No file uploaded", 400

    file = request.files['file']
    if file.filename == '':
        return "Error: Empty filename", 400

    try:
        file.save(os.path.join(app.config['UPLOAD_FOLDER'], file.filename))
        return "Success: File uploaded", 200
    except Exception as e:
        return f"Error: {str(e)}", 500

# 新增文件下载路由
@app.route('/download/<filename>', methods=['GET'])
def download_file(filename):
    try:
        # 检查文件是否存在
        if not os.path.isfile(os.path.join(app.config['UPLOAD_FOLDER'], filename)):
            return "Error: File not found", 404

        # 返回文件内容（浏览器会自动下载）
        return send_from_directory(
            app.config['UPLOAD_FOLDER'],
            filename,
            as_attachment=True  # 可选：强制下载而非预览
        )
    except Exception as e:
        return f"Error: {str(e)}", 500

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
