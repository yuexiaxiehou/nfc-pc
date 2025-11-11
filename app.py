import os
import time
import threading
import socket
from flask import Flask, request, send_file, jsonify, render_template, session, redirect, url_for
from werkzeug.utils import secure_filename
from zeroconf import ServiceBrowser, Zeroconf, ServiceInfo, IPVersion

# --- 配置 ---
app = Flask(__name__)
# 设置一个密钥，用于session加密
app.secret_key = b'_5#y2L"F4Q8z\n\xec]/' 

# 设置你想要共享的文件夹路径
SHARED_FOLDER = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'shared_files')

# 【优化点1：设置访问密码】
# 在这里修改你的密码
ACCESS_PASSWORD = "123456" 

# 允许上传的文件类型
ALLOWED_EXTENSIONS = {'txt', 'pdf', 'png', 'jpg', 'jpeg', 'gif', 'doc', 'docx', 'zip', 'mp4', 'mov', 'pptx', 'xlsx'}

# 确保共享文件夹存在
if not os.path.exists(SHARED_FOLDER):
    os.makedirs(SHARED_FOLDER)
    print(f"已创建共享文件夹: {SHARED_FOLDER}")

app.config['SHARED_FOLDER'] = SHARED_FOLDER
app.config['MAX_CONTENT_LENGTH'] = 100 * 1024 * 1024  # 限制上传文件大小为100MB

def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

# --- 路由 ---

# 登录页面
@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        password = request.form.get('password')
        if password == ACCESS_PASSWORD:
            session['logged_in'] = True
            return redirect(url_for('index'))
        else:
            # 密码错误，返回错误信息
            return render_template('login.html', error="密码错误，请重试。")
    return render_template('login.html')

# 登出
@app.route('/logout')
def logout():
    session.pop('logged_in', None)
    return redirect(url_for('login'))

# 主页：显示文件上传和下载界面 (需要登录)
@app.route('/')
def index():
    if not session.get('logged_in'):
        return redirect(url_for('login'))
    return render_template('index.html')

# API：获取文件列表 (需要登录)
@app.route('/api/files', methods=['GET'])
def list_files():
    if not session.get('logged_in'):
        return jsonify({'error': 'Unauthorized'}), 401
    try:
        files = []
        for filename in os.listdir(app.config['SHARED_FOLDER']):
            file_path = os.path.join(app.config['SHARED_FOLDER'], filename)
            if os.path.isfile(file_path):
                size_bytes = os.path.getsize(file_path)
                if size_bytes < 1024 * 1024:
                    size_str = f"{size_bytes / 1024:.2f} KB"
                else:
                    size_str = f"{size_bytes / (1024 * 1024):.2f} MB"
                files.append({'name': filename, 'size': size_str})
        return jsonify({'files': files})
    except Exception as e:
        return jsonify({'error': str(e)}), 500

# API：上传文件 (需要登录)
@app.route('/api/upload', methods=['POST'])
def upload_file():
    if not session.get('logged_in'):
        return jsonify({'error': 'Unauthorized'}), 401
    if 'file' not in request.files:
        return jsonify({'error': '请求中没有文件部分'}), 400
    file = request.files['file']
    if file.filename == '':
        return jsonify({'error': '未选择文件'}), 400
    if file and allowed_file(file.filename):
        filename = secure_filename(file.filename)
        save_path = os.path.join(app.config['SHARED_FOLDER'], filename)
        counter = 1
        base_name, extension = os.path.splitext(filename)
        while os.path.exists(save_path):
            filename = f"{base_name}_{counter}{extension}"
            save_path = os.path.join(app.config['SHARED_FOLDER'], filename)
            counter += 1
        file.save(save_path)
        return jsonify({'message': f'文件 {filename} 上传成功!'}), 200
    return jsonify({'error': '不允许的文件类型'}), 400

# API：下载文件 (需要登录)
@app.route('/api/download/<filename>', methods=['GET'])
def download_file(filename):
    if not session.get('logged_in'):
        return jsonify({'error': 'Unauthorized'}), 401
    try:
        safe_filename = secure_filename(filename)
        file_path = os.path.join(app.config['SHARED_FOLDER'], safe_filename)
        if os.path.isfile(file_path):
            return send_file(file_path, as_attachment=True)
        else:
            return jsonify({'error': '文件未找到'}), 404
    except Exception as e:
        return jsonify({'error': str(e)}), 500

# --- mDNS 服务注册 (IPv4强制版本) ---
def register_mdns_service():
    time.sleep(2) 
    zeroconf = Zeroconf(ip_version=IPVersion.V4Only)
    try:
        s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        s.connect(("8.8.8.8", 80))
        local_ip = s.getsockname()[0]
        s.close()
    except Exception:
        local_ip = socket.gethostbyname(socket.gethostname())

    service_info = ServiceInfo(
        "_http._tcp.local.",
        "NFC File Transfer._http._tcp.local.",
        addresses=[socket.inet_aton(local_ip)],
        port=18080, # 确保端口和你的设置一致
        properties={},
        server="nfc-pc.local.",
    )
    
    print("-" * 50)
    print(f"🚀 正在注册mDNS服务 (强制IPv4)...")
    print(f"   本地域名: nfc-pc.local")
    print(f"   本机IPv4: {local_ip}")
    print(f"   请在NFC标签中写入: http://nfc-pc.local:18080")
    print("-" * 50)
    
    zeroconf.register_service(service_info)
    
    try:
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        print("\n正在关闭mDNS服务...")
    finally:
        zeroconf.unregister_service(service_info)
        zeroconf.close()

# --- 主程序入口 ---
if __name__ == '__main__':
    mdns_thread = threading.Thread(target=register_mdns_service, daemon=True)
    mdns_thread.start()
    print("🌐 Flask服务正在启动...")
    app.run(host='0.0.0.0', port=18080, debug=False) # 确保端口是18080
