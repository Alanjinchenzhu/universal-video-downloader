# VideoDL - 万能视频下载器

一个功能强大、支持 1000+ 网站的视频下载工具，基于 yt-dlp 构建，采用 Vue3 + Vite + Tailwind CSS + FastAPI 技术栈。

## ✨ 功能特性

- 🎬 **支持 1000+ 平台**：YouTube、Bilibili、抖音、快手、Twitter、Instagram、TikTok 等主流视频网站
- 🚀 **极速下载**：多线程加速，支持高清晰度视频下载
- 🎵 **无水印保存**：原画质量，高清保存，无水印
- 💻 **现代化 UI**：采用 Vue3 + Tailwind CSS 构建的美观界面
- 🔒 **安全可靠**：无需登录，直接使用，保护用户隐私
- 📦 **一键下载**：简单易用，粘贴链接即可下载

## 🛠️ 技术栈

### 前端
- **框架**: Vue 3 (Composition API)
- **构建工具**: Vite
- **样式**: Tailwind CSS
- **UI 组件**: Ant Design Vue
- **语言**: TypeScript

### 后端
- **框架**: FastAPI
- **视频下载**: yt-dlp
- **语言**: Python 3.8+

## 📦 快速开始

### 环境要求

- Node.js 18+
- Python 3.8+
- FFmpeg (用于视频合并)

### 安装依赖

#### 前端

```bash
cd frontend
npm install
```

#### 后端

```bash
cd frontend/backend
pip install -r requirements.txt
```

### 运行项目

#### 启动后端服务

```bash
cd frontend/backend
python main.py
```

后端服务将运行在 http://localhost:8000

#### 启动前端开发服务器

```bash
cd frontend
npm run dev
```

前端将运行在 http://localhost:5173

## 📖 使用说明

1. 打开浏览器访问前端地址
2. 在输入框中粘贴视频链接
3. 系统自动识别平台并获取视频信息
4. 点击"开始下载"按钮
5. 等待下载完成，文件将自动保存

### 注意事项

- 下载抖音视频时，请确保 Chrome 浏览器已登录抖音账号（用于获取 cookies）
- 部分平台可能需要网络环境支持
- 请合理使用本工具，遵守相关法律法规

## 🔧 项目结构

```
.
├── frontend/              # 前端项目目录
│   ├── src/                 # 前端源码
│   │   ├── App.vue         # 主组件
│   │   ├── main.ts         # 入口文件
│   │   └── styles/         # 样式文件
│   └── package.json        # Node 依赖
│── backend/             # FastAPI 后端
│   ├── main.py         # 后端主文件
│   └── requirements.txt # Python 依赖
└── README.md               # 项目说明
```

## 🌐 支持的平台

- ✅ YouTube
- ✅ Bilibili (B站)
- ✅ 抖音
- ✅ 快手
- ✅ Twitter / X
- ✅ Instagram
- ✅ TikTok
- ✅ 微博
- ✅ 小红书
- ✅ 优酷
- ✅ 腾讯视频
- ✅ 以及 1000+ 其他视频网站

## 📜 许可证

本项目基于 yt-dlp 开发，请遵守相关许可证条款。

## ⚠️ 免责声明

本工具仅供学习和个人使用，请勿用于商业用途。下载视频时请遵守相关网站的服务条款和法律法规。

## 🤝 贡献

欢迎提交 Issue 和 Pull Request！

---

**VideoDL** - 让视频下载变得简单！🎉
