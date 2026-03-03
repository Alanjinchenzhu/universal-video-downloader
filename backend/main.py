# -*- coding: utf-8 -*-
"""
VideoDL FastAPI Backend
Video Downloader API Service - Based on yt-dlp
"""
import os
import re
import tempfile
import shutil

from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import StreamingResponse
from pydantic import BaseModel
from typing import Optional, List
import asyncio
from concurrent.futures import ThreadPoolExecutor
from urllib.parse import quote

from yt_dlp import YoutubeDL

app = FastAPI(
    title="VideoDL API",
    description="Video Downloader API based on yt-dlp",
    version="1.0.0",
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
    expose_headers=["Content-Disposition"],
)

executor = ThreadPoolExecutor(max_workers=4)


class DownloadRequest(BaseModel):
    """下载请求模型"""
    url: str
    format: Optional[str] = "best"
    audio_only: Optional[bool] = False


class VideoInfo(BaseModel):
    """视频信息模型"""
    title: str
    description: Optional[str] = None
    duration: Optional[int] = None
    thumbnail: Optional[str] = None
    uploader: Optional[str] = None
    view_count: Optional[int] = None
    like_count: Optional[int] = None
    formats: List[dict] = []


def normalize_url(url: str) -> str:
    """规范化 URL，处理特殊平台的 URL 格式"""
    # 抖音 jingxuan 页面 modal_id 格式
    douyin_match = re.search(r'douyin\.com/.*modal_id=(\d+)', url)
    if douyin_match:
        video_id = douyin_match.group(1)
        return f'https://www.douyin.com/video/{video_id}'

    # 抖音短链接
    if 'v.douyin.com' in url or 'douyin.com/share/video' in url:
        return url

    return url


def get_ydl_opts() -> dict:
    """获取 yt-dlp 配置选项"""
    return {
        'quiet': True,
        'no_warnings': True,
        'extract_flat': False,
        'cookiesfrombrowser': ('chrome',),
    }


def get_video_info_sync(url: str) -> dict:
    """获取视频信息"""
    url = normalize_url(url)
    
    ydl_opts = get_ydl_opts()

    with YoutubeDL(ydl_opts) as ydl:
        info = ydl.extract_info(url, download=False)

        formats = []
        for f in info.get('formats', [])[:15]:
            if f.get('vcodec') != 'none' or f.get('acodec') != 'none':
                formats.append({
                    'format_id': f.get('format_id'),
                    'ext': f.get('ext'),
                    'resolution': f.get('resolution'),
                    'filesize': f.get('filesize'),
                    'vcodec': f.get('vcodec'),
                    'acodec': f.get('acodec'),
                })

        # 获取缩略图，尝试多种字段
        thumbnail = info.get('thumbnail')
        if not thumbnail and info.get('thumbnails'):
            # 从thumbnails列表中找分辨率最高的缩略图
            thumbnails = info.get('thumbnails', [])
            if thumbnails:
                # 按优先级选择：优先选择width最大的
                best_thumb = max(thumbnails, key=lambda x: (x.get('width', 0), x.get('height', 0)))
                thumbnail = best_thumb.get('url')
        if not thumbnail:
            thumbnail = info.get('cover')
        if not thumbnail:
            # 尝试B站特定的字段
            thumbnail = info.get('pic')
        if not thumbnail:
            # 尝试从其他可能的字段获取
            for key in ['thumbnail_url', 'thumbnail_url_hd', 'thumbnail_url_2', 'thumbnail_url_3']:
                if key in info:
                    thumbnail = info[key]
                    break

        return {
            'title': info.get('title'),
            'description': info.get('description'),
            'duration': info.get('duration'),
            'thumbnail': thumbnail,
            'uploader': info.get('uploader') or info.get('channel') or info.get('author'),
            'view_count': info.get('view_count'),
            'like_count': info.get('like_count'),
            'formats': formats,
        }


def download_video_sync(url: str, format_id: str = None, audio_only: bool = False) -> tuple:
    """下载视频到临时目录，返回文件路径和标题"""
    url = normalize_url(url)
    
    # 创建临时目录
    temp_dir = tempfile.mkdtemp()
    
    ydl_opts = get_ydl_opts()
    ydl_opts['outtmpl'] = os.path.join(temp_dir, '%(title)s.%(ext)s')
    # 确保不重定向，直接下载到本地
    ydl_opts['noplaylist'] = True
    ydl_opts['no_warnings'] = True
    ydl_opts['quiet'] = True

    if audio_only:
        ydl_opts['format'] = 'bestaudio/best'
    elif format_id:
        ydl_opts['format'] = format_id
    else:
        # 优先下载已有的最佳质量，避免分离下载导致的问题
        ydl_opts['format'] = 'best/bestvideo[ext=mp4]+bestaudio[ext=m4a]/best'

    with YoutubeDL(ydl_opts) as ydl:
        info = ydl.extract_info(url, download=True)

        # 获取实际下载的文件名
        filename = None
        if 'requested_downloads' in info:
            for entry in info['requested_downloads']:
                if entry.get('filepath') and os.path.exists(entry['filepath']):
                    filename = entry['filepath']
                    break

        if not filename:
            # 遍历临时目录查找下载的文件
            for f in os.listdir(temp_dir):
                file_path = os.path.join(temp_dir, f)
                if os.path.isfile(file_path) and not f.endswith('.part'):
                    filename = file_path
                    break

        if not filename:
            filename = ydl.prepare_filename(info)

        # 从文件名中提取标题
        title = os.path.splitext(os.path.basename(filename))[0]

        return filename, title, temp_dir


@app.get("/")
async def root():
    """API 根路径"""
    return {
        "name": "VideoDL API",
        "version": "1.0.0",
        "description": "Video Downloader API based on yt-dlp",
        "endpoints": {
            "GET /": "API Info",
            "POST /info": "Get video info",
            "POST /download": "Download video (returns file stream)",
            "GET /platforms": "Supported platforms",
        }
    }


@app.get("/platforms")
async def get_platforms():
    """获取支持的平台列表"""
    return {
        "platforms": [
            {"name": "YouTube", "icon": "▶️", "color": "#FF0000"},
            {"name": "Bilibili", "icon": "📺", "color": "#00A1D6"},
            {"name": "Douyin", "icon": "🎵", "color": "#000000"},
            {"name": "Kuaishou", "icon": "⚡", "color": "#FF4906"},
            {"name": "Twitter/X", "icon": "🐦", "color": "#1DA1F2"},
            {"name": "Instagram", "icon": "📷", "color": "#E4405F"},
            {"name": "TikTok", "icon": "🎬", "color": "#000000"},
            {"name": "Weibo", "icon": "📱", "color": "#E6162D"},
            {"name": "Xiaohongshu", "icon": "📕", "color": "#FF2442"},
            {"name": "Youku", "icon": "🎥", "color": "#1F93FF"},
            {"name": "Tencent Video", "icon": "📺", "color": "#FF6600"},
        ],
        "total": "1000+",
    }


@app.post("/info", response_model=VideoInfo)
async def get_info(request: DownloadRequest):
    """获取视频信息"""
    try:
        loop = asyncio.get_event_loop()
        info = await loop.run_in_executor(executor, get_video_info_sync, request.url)
        return VideoInfo(**info)
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))


@app.post("/download")
async def download(request: DownloadRequest):
    """下载视频并返回文件流"""
    try:
        loop = asyncio.get_event_loop()
        filename, title, temp_dir = await loop.run_in_executor(
            executor,
            download_video_sync,
            request.url,
            request.format if request.format != "best" else None,
            request.audio_only
        )

        if not os.path.exists(filename):
            raise HTTPException(status_code=404, detail="File not found")

        # 获取文件扩展名
        ext = os.path.splitext(filename)[1]

        # 生成安全的文件名
        safe_title = re.sub(r'[\\/:*?"<>|]', '_', title)
        download_filename = f"{safe_title}{ext}"

        # 确定 MIME 类型
        mime_types = {
            '.mp4': 'video/mp4',
            '.webm': 'video/webm',
            '.mkv': 'video/x-matroska',
            '.mp3': 'audio/mpeg',
            '.m4a': 'audio/mp4',
            '.flac': 'audio/flac',
        }
        media_type = mime_types.get(ext.lower(), 'application/octet-stream')

        # 创建文件流响应
        def iterfile():
            with open(filename, 'rb') as f:
                yield from f
            # 清理临时文件
            shutil.rmtree(temp_dir, ignore_errors=True)

        # 编码文件名以支持中文
        encoded_filename = quote(download_filename)

        return StreamingResponse(
            iterfile(),
            media_type=media_type,
            headers={
                'Content-Disposition': f"attachment; filename*=UTF-8''{encoded_filename}"
            }
        )

    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
