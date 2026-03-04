# -*- coding: utf-8 -*-
"""
VideoDL FastAPI Backend
Video Downloader API Service - Based on yt-dlp
"""
import os
import re
import tempfile
import shutil
import json
import requests

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


def parse_douyin_video(url: str) -> dict:
    """解析抖音视频信息（无需Cookie）"""
    try:
        # 提取视频ID
        video_id = None
        
        # 处理短链接
        if 'v.douyin.com' in url:
            response = requests.get(url, allow_redirects=False)
            url = response.headers.get('Location', url)
        
        # 从URL中提取视频ID
        patterns = [
            r'/video/(\d+)',
            r'/share/video/(\d+)',
            r'modal_id=(\d+)',
            r'/aweme/v1/play/\?video_id=(\w+)',
        ]
        
        for pattern in patterns:
            match = re.search(pattern, url)
            if match:
                video_id = match.group(1)
                break
        
        if not video_id:
            return None
        
        # 使用移动端接口获取视频信息
        headers = {
            'User-Agent': 'Mozilla/5.0 (Linux; Android 8.0.0; SM-G955U Build/R16NW) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/116.0.0.0 Mobile Safari/537.36',
            'Referer': 'https://www.douyin.com/?is_from_mobile_home=1&recommend=1'
        }
        
        # 尝试使用iesdouyin接口
        share_url = f'https://www.iesdouyin.com/share/video/{video_id}/'
        response = requests.get(share_url, headers=headers)
        
        # 从页面源码中提取JSON数据
        match = re.search(r'window\._ROUTER_DATA\s*=\s*(\{.*?\});?</', response.text)
        if not match:
            return None
        
        data = json.loads(match.group(1))
        
        # 解析视频信息
        try:
            item_list = data['loaderData']['video_(id)/page']['videoInfoRes']['item_list'][0]
        except (KeyError, IndexError):
            return None
        
        # 提取视频信息
        title = item_list.get('desc', '抖音视频')
        nickname = item_list.get('author', {}).get('nickname', '未知用户')
        aweme_id = item_list.get('aweme_id', video_id)
        
        # 获取视频URL
        video_uri = item_list.get('video', {}).get('play_addr', {}).get('uri')
        if video_uri:
            if 'mp3' not in video_uri:
                video_url = f'https://www.douyin.com/aweme/v1/play/?video_id={video_uri}'
            else:
                video_url = video_uri
        else:
            video_url = None
        
        # 获取封面图
        cover_url = None
        try:
            cover_url = item_list.get('video', {}).get('cover', {}).get('url_list', [None])[0]
        except (KeyError, IndexError):
            pass
        
        # 检查是否为图集
        images = item_list.get('images')
        is_image_set = images is not None
        
        if is_image_set:
            image_urls = []
            for img in images:
                try:
                    image_urls.append(img['url_list'][0])
                except (KeyError, IndexError):
                    pass
        else:
            image_urls = []
        
        return {
            'title': title,
            'uploader': nickname,
            'thumbnail': cover_url,
            'description': f'来自 {nickname} 的抖音视频',
            'duration': None,
            'view_count': None,
            'like_count': None,
            'formats': [{
                'format_id': 'best',
                'ext': 'mp4',
                'resolution': 'unknown',
                'filesize': None,
                'vcodec': 'h264',
                'acodec': 'aac',
            }],
            'video_url': video_url,
            'images': image_urls,
            'is_image_set': is_image_set,
            'platform': 'douyin',
        }
        
    except Exception as e:
        print(f"抖音解析错误: {e}")
        return None


def clean_filename(filename: str) -> str:
    """清理文件名，移除可能导致播放问题的特殊字符"""
    # 移除话题标签（#开头的内容）
    filename = re.sub(r'#\S+', '', filename)
    # 移除其他特殊字符
    filename = re.sub(r'[\\/:*?"<>|]', '_', filename)
    # 移除连续的下划线
    filename = re.sub(r'_+', '_', filename)
    # 移除首尾空格和下划线
    filename = filename.strip('_ ')
    # 如果文件名为空，使用默认名称
    if not filename:
        filename = '抖音视频'
    return filename


def download_douyin_video(video_url: str, title: str) -> tuple:
    """下载抖音视频"""
    max_retries = 3
    retry_delay = 2
    
    for attempt in range(max_retries):
        try:
            headers = {
                'User-Agent': 'Mozilla/5.0 (Linux; Android 8.0.0; SM-G955U Build/R16NW) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/116.0.0.0 Mobile Safari/537.36',
                'Referer': 'https://www.douyin.com/',
                'Accept': '*/*',
                'Accept-Language': 'zh-CN,zh;q=0.9,en;q=0.8',
                'Accept-Encoding': 'gzip, deflate, br',
                'Connection': 'keep-alive',
            }
            
            # 使用session来处理重定向，保持Referer头
            session = requests.Session()
            session.verify = False  # 禁用SSL验证
            
            # 手动处理重定向，保持Referer头
            response = session.get(video_url, headers=headers, stream=True, allow_redirects=False, timeout=30)
            
            # 如果是重定向，跟随重定向并保持Referer
            redirect_count = 0
            max_redirects = 5
            while response.status_code in (301, 302, 303, 307, 308) and redirect_count < max_redirects:
                redirect_url = response.headers.get('Location')
                if not redirect_url:
                    break
                
                print(f"重定向 {redirect_count + 1}: {redirect_url}")
                response = session.get(redirect_url, headers=headers, stream=True, allow_redirects=False, timeout=30)
                redirect_count += 1
            
            if response.status_code != 200:
                raise Exception(f"下载失败，状态码: {response.status_code}")
            
            # 检查内容类型
            content_type = response.headers.get('Content-Type', '')
            if 'video' not in content_type.lower():
                print(f"警告：响应内容类型不是视频: {content_type}")
                print(f"响应头: {dict(response.headers)}")
                print(f"响应内容前200字节: {response.content[:200]}")
            
            # 创建临时文件
            temp_dir = tempfile.mkdtemp()
            # 清理文件名
            clean_title = clean_filename(title)
            filename = os.path.join(temp_dir, f"{clean_title}.mp4")
            
            # 写入文件
            with open(filename, 'wb') as f:
                downloaded = 0
                total_size = int(response.headers.get('Content-Length', 0))
                for chunk in response.iter_content(chunk_size=8192):
                    if chunk:
                        f.write(chunk)
                        downloaded += len(chunk)
                        if total_size > 0:
                            progress = (downloaded / total_size) * 100
                            if downloaded % 100000 == 0:  # 每100KB打印一次进度
                                print(f"下载进度: {progress:.1f}% ({downloaded}/{total_size})")
            
            # 验证文件大小
            file_size = os.path.getsize(filename)
            if file_size < 1024:
                raise Exception(f"下载的文件太小: {file_size} 字节，可能下载失败")
            
            print(f"抖音视频下载成功: {filename}, 大小: {file_size} 字节")
            return filename, clean_title, temp_dir
            
        except Exception as e:
            print(f"抖音下载错误 (尝试 {attempt + 1}/{max_retries}): {e}")
            if attempt < max_retries - 1:
                print(f"等待 {retry_delay} 秒后重试...")
                import time
                time.sleep(retry_delay)
            else:
                raise e


def get_ydl_opts() -> dict:
    """获取 yt-dlp 配置选项"""
    return {
        'quiet': True,
        'no_warnings': True,
        'extract_flat': False,
        'cookiesfrombrowser': ('chrome',),
        # 下载优化选项
        'concurrent_fragment_downloads': 4,  # 并发下载片段
        'buffersize': 1024 * 16,  # 缓冲区大小 16KB
        'nocheckcertificate': True,  # 不检查证书
        'retries': 3,  # 重试次数
        'fragment_retries': 3,  # 片段重试次数
        'skip_unavailable_fragments': True,  # 跳过不可用片段
        'keepvideo': False,  # 不保留中间文件
    }


def get_video_info_sync(url: str) -> dict:
    """获取视频信息"""
    url = normalize_url(url)
    
    # 优先尝试抖音解析
    if 'douyin.com' in url:
        douyin_info = parse_douyin_video(url)
        if douyin_info:
            return douyin_info
    
    # 使用yt-dlp解析其他平台
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
    
    # 优先尝试抖音下载
    if 'douyin.com' in url:
        douyin_info = parse_douyin_video(url)
        if douyin_info and douyin_info.get('video_url'):
            try:
                return download_douyin_video(douyin_info['video_url'], douyin_info['title'])
            except Exception as e:
                print(f"抖音下载失败，尝试使用yt-dlp: {e}")
    
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

        # 从文件名中提取标题并清理
        title = os.path.splitext(os.path.basename(filename))[0]
        clean_title = clean_filename(title)

        return filename, clean_title, temp_dir


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
