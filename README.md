一个基于Python Flask和mDNS的局域网文件共享解决方案，让你通过NFC标签实现“一碰即传”的文件传输体验，彻底告别微信文件传输助手的繁琐。

✨ 特性
🚀 一碰即传：使用NFC标签，手机一碰即可打开上传页面，体验极致流畅。
🌐 自动发现：基于mDNS（Bonjour）技术，无需关心IP地址变化，服务地址固定为 http://nfc-pc.local:18080。
🔒 安全访问：简单的密码保护机制，确保只有你能访问你的文件站。
📱 跨平台：支持任何带有NFC和现代浏览器的手机（Android、iOS）。
🖥️ 轻量级：纯Python实现，资源占用极小，可在后台静默运行。
⚙️ 开箱即用：代码结构清晰，配置简单，支持开机自启。
🤔 为什么需要它？
你是否厌倦了以下场景：

手机拍照/文档 -> 微信文件传输助手 -> 电脑微信 -> 手动下载…
文件过大传输缓慢，或被微信提示“文件已过期”。
想在局域网内快速分享文件，但配置FTP或NAS又太复杂。
NFC File Transfer Station 就是为了解决这些痛点而生。它为你提供了一个在局域网内专属、私密、高效的文件传输通道。

🛠️ 技术栈
后端: Python + Flask
网络发现: mDNS (via aiodiscover)
前端: HTML + CSS + JavaScript (原生)
触发: NFC (Near Field Communication)
📦 安装与使用
准备工作
安装Python: 确保你的电脑上安装了 Python 3.7 或更高版本。
安装Git: 用于克隆此项目。
一个NFC标签: NTAG213或更高规格的NFC贴纸即可。

### 安装依赖

使用pip安装所有必需的Python库：
pip install -r requirements.txt



### 配置与启动

1.  **创建共享文件夹** (如果不存在):
    项目根目录下的 `shared_files` 文件夹将用于存放所有上传的文件。
2.  **创建html文件夹**：
    项目根目录下，创建`templates`文件夹，将index.html和login.html这两个文件移动到该文件夹中。

3.  **(可选) 修改配置**:
    打开 `app.py`，你可以修改以下配置：
    -   `ACCESS_PASSWORD`: 修改访问密码。
    -   `SHARED_FOLDER`: 修改共享文件存放路径。
    -   `ALLOWED_EXTENSIONS`: 修改允许上传的文件类型。

4.  **启动服务**:
    在项目根目录下打开命令行，运行：
    python app.py
 <img width="1419" height="330" alt="image" src="https://github.com/user-attachments/assets/876c77fc-9fbd-44e1-aa4d-2e5379bb1ff3" />
5. **(可选) 设置开机自启**
  1.  按 `Win + R`，输入 `shell:startup` 并回车，打开Windows启动文件夹。
  2.  在该文件夹内创建一个新的批处理文件，例如 `start_nfc_service.bat`。
  3.  编辑该文件，输入以下内容（请将路径替换为你自己的项目路径）：
  batch
  @echo off
  cd /d “D:\path\to\your\nfc-file-transfer”
  python app.py
  4.  保存文件。现在，每次Windows启动时，该服务都会自动在后台运行。

## 📱 使用流程

1.  确保你的电脑和手机连接在同一个Wi-Fi网络下。
2.  用手机背部轻触已配置好的NFC标签。
3.  手机浏览器会自动打开 `http://nfc-pc.local:18080`。
4.  在登录页面输入你设置的密码。
5.  在文件上传页面，拖拽或选择文件进行上传。
6.  文件将即刻出现在电脑的 `shared_files` 文件夹中。


## 🙏 致谢

-   [Flask](https://flask.palletsprojects.com) - 强大的Python Web框架。
-   [aiodiscover](https://github.com/Digital-Sapphire/aiodiscover) - 简单易用的mDNS库。


    
