# VideoDL API 文档

## 基础信息

- **Base URL**: `http://localhost:8000`
- **API 版本**: v1.0.0
- **内容类型**: `application/json`

## API 端点

### 1. 健康检查

检查后端服务是否正常运行。

**端点**: `GET /`

**响应**:
```json
{
  "status": "ok",
  "message": "VideoDL API is running"
}
```

**状态码**:
- `200 OK`: 服务正常

---

### 2. 获取视频信息

获取指定视频的详细信息，包括标题、时长、缩略图、可用格式等。

**端点**: `POST /info`

**请求头**:
```
Content-Type: application/json
```

**请求体**:
```json
{
  "url": "https://www.youtube.com/watch?v=dQw4w9WgXcQ"
}
```

**参数**:

| 参数 | 类型 | 必填 | 说明 |
|------|------|------|------|
| url | string | 是 | 视频URL |

**响应**:
```json
{
  "title": "视频标题",
  "description": "视频描述",
  "duration": 180,
  "thumbnail": "https://...",
  "uploader": "上传者名称",
  "view_count": 1000000,
  "like_count": 50000,
  "formats": [
    {
      "format_id": "best",
      "ext": "mp4",
      "resolution": "1920x1080",
      "filesize": 102400000,
      "vcodec": "h264",
      "acodec": "aac"
    }
  ]
}
```

**响应字段说明**:

| 字段 | 类型 | 说明 |
|------|------|------|
| title | string | 视频标题 |
| description | string | 视频描述（可选） |
| duration | integer | 视频时长（秒） |
| thumbnail | string | 缩略图URL |
| uploader | string | 上传者名称 |
| view_count | integer | 观看次数 |
| like_count | integer | 点赞数 |
| formats | array | 可用格式列表 |

**格式对象字段**:

| 字段 | 类型 | 说明 |
|------|------|------|
| format_id | string | 格式ID |
| ext | string | 文件扩展名 |
| resolution | string | 分辨率 |
| filesize | integer | 文件大小（字节） |
| vcodec | string | 视频编码 |
| acodec | string | 音频编码 |

**状态码**:
- `200 OK`: 成功获取视频信息
- `400 Bad Request`: 请求参数错误
- `404 Not Found`: 视频不存在或无法访问

**示例请求**:

```bash
curl -X POST http://localhost:8000/info \
  -H "Content-Type: application/json" \
  -d '{"url": "https://www.youtube.com/watch?v=dQw4w9WgXcQ"}'
```

---

### 3. 下载视频

下载指定视频并返回文件流。

**端点**: `POST /download`

**请求头**:
```
Content-Type: application/json
```

**请求体**:
```json
{
  "url": "https://www.youtube.com/watch?v=dQw4w9WgXcQ",
  "format": "best",
  "audio_only": false
}
```

**参数**:

| 参数 | 类型 | 必填 | 默认值 | 说明 |
|------|------|------|--------|------|
| url | string | 是 | - | 视频URL |
| format | string | 否 | "best" | 视频格式 |
| audio_only | boolean | 否 | false | 是否仅下载音频 |

**格式选项**:
- `"best"`: 最佳质量（默认）
- `"bestvideo"`: 最佳视频质量
- `"bestaudio"`: 最佳音频质量
- `"worst"`: 最低质量
- 其他 yt-dlp 支持的格式ID

**响应**:
- **Content-Type**: `video/mp4` 或其他视频格式
- **Content-Disposition**: 包含文件名的下载头
- **Content-Length**: 文件大小（字节）
- **Body**: 视频文件流

**响应头示例**:
```
Content-Type: video/mp4
Content-Disposition: attachment; filename*=UTF-8''视频标题.mp4
Content-Length: 102400000
```

**状态码**:
- `200 OK`: 下载成功
- `400 Bad Request`: 请求参数错误
- `404 Not Found`: 视频不存在或无法访问
- `500 Internal Server Error`: 服务器内部错误

**示例请求**:

```bash
curl -X POST http://localhost:8000/download \
  -H "Content-Type: application/json" \
  -d '{"url": "https://www.youtube.com/watch?v=dQw4w9WgXcQ"}' \
  --output video.mp4
```

**JavaScript 示例**:

```javascript
const response = await fetch('http://localhost:8000/download', {
  method: 'POST',
  headers: {
    'Content-Type': 'application/json',
  },
  body: JSON.stringify({
    url: 'https://www.youtube.com/watch?v=dQw4w9WgXcQ',
    format: 'best',
    audio_only: false
  })
});

const blob = await response.blob();
const url = window.URL.createObjectURL(blob);
const a = document.createElement('a');
a.href = url;
a.download = 'video.mp4';
a.click();
window.URL.revokeObjectURL(url);
```

---

## 错误响应

所有API端点在出错时返回统一的错误格式。

**错误响应格式**:
```json
{
  "detail": "错误描述信息"
}
```

**常见错误**:

| 状态码 | 错误信息 | 说明 |
|--------|----------|------|
| 400 | "URL is required" | 缺少必需的URL参数 |
| 400 | "Invalid URL format" | URL格式不正确 |
| 404 | "Video not found" | 视频不存在或无法访问 |
| 500 | "Internal server error" | 服务器内部错误 |

---

## 支持的平台

### 1. YouTube
- 支持视频、播放列表、直播回放
- 支持 4K/8K 画质
- 支持字幕下载

### 2. Bilibili
- 支持视频、番剧、课程
- 支持高清画质
- 支持弹幕下载

### 3. 抖音
- 支持短视频、直播、图集
- 无需 Cookie
- 无水印下载

### 4. 其他平台
- 快手
- Twitter/X
- Instagram
- TikTok
- 微博
- 小红书
- 优酷
- 腾讯视频
- 以及 1000+ 其他视频网站

---

## 限制与配额

### 请求限制
- 单次请求最大文件大小: 5GB
- 并发请求限制: 4 个
- 超时时间: 300 秒

### 下载限制
- 最大下载速度: 无限制
- 断点续传: 支持
- 重试次数: 3 次

---

## 最佳实践

### 1. 获取视频信息后再下载

```javascript
// 1. 先获取视频信息
const infoResponse = await fetch('http://localhost:8000/info', {
  method: 'POST',
  headers: { 'Content-Type': 'application/json' },
  body: JSON.stringify({ url: videoUrl })
});

const videoInfo = await infoResponse.json();

// 2. 检查视频是否可用
if (!videoInfo.title) {
  console.error('视频不可用');
  return;
}

// 3. 显示视频信息给用户确认
console.log(`视频标题: ${videoInfo.title}`);
console.log(`视频时长: ${videoInfo.duration}秒`);

// 4. 用户确认后下载
const downloadResponse = await fetch('http://localhost:8000/download', {
  method: 'POST',
  headers: { 'Content-Type': 'application/json' },
  body: JSON.stringify({ url: videoUrl })
});

// 5. 处理下载
const blob = await downloadResponse.blob();
// ... 保存文件
```

### 2. 处理大文件下载

```javascript
// 使用流式处理大文件
const response = await fetch('http://localhost:8000/download', {
  method: 'POST',
  headers: { 'Content-Type': 'application/json' },
  body: JSON.stringify({ url: videoUrl })
});

const reader = response.body.getReader();
const chunks = [];
let receivedLength = 0;

while (true) {
  const { done, value } = await reader.read();
  
  if (done) break;
  
  chunks.push(value);
  receivedLength += value.length;
  
  // 显示下载进度
  console.log(`已下载: ${receivedLength} 字节`);
}

// 合并所有数据块
const blob = new Blob(chunks);
// ... 保存文件
```

### 3. 错误处理

```javascript
try {
  const response = await fetch('http://localhost:8000/download', {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify({ url: videoUrl })
  });

  if (!response.ok) {
    const errorData = await response.json();
    throw new Error(errorData.detail || '下载失败');
  }

  // 处理成功响应
  const blob = await response.blob();
  // ... 保存文件

} catch (error) {
  console.error('下载失败:', error.message);
  // 显示错误信息给用户
}
```

---

## 更新日志

### v1.0.0 (2026-03-04)
- 初始版本发布
- 支持基础视频下载功能
- 支持视频信息获取
- 实现抖音无Cookie解析
- 添加文件名清理功能
- 实现实时下载进度

---

## 技术支持

如有问题或建议，请访问：
- GitHub: https://github.com/Alanjinchenzhu/universal-video-downloader
- Gitee: https://gitee.com/z-jinchen/universal-video-downloader
