<script setup lang="ts">
import { ref, computed } from 'vue'
import { 
  DownloadOutlined, 
  SearchOutlined, 
  ThunderboltOutlined,
  SafetyCertificateOutlined,
  CloudDownloadOutlined,
  ApiOutlined,
  GithubOutlined,
  PlayCircleOutlined,
  GlobalOutlined,
  CheckCircleOutlined,
  CloseCircleOutlined
} from '@ant-design/icons-vue'

// API 基础地址
const API_BASE = 'http://localhost:8000'

// 支持的平台数据
const platforms = ref([
  { id: 1, name: 'YouTube', icon: '▶️', description: '支持视频、播放列表、直播回放下载', features: ['4K/8K画质', '字幕下载', '播放列表批量'], color: '#FF0000' },
  { id: 2, name: 'Bilibili', icon: '📺', description: '支持视频、番剧、课程下载', features: ['高清画质', '弹幕下载', '多P批量'], color: '#00A1D6' },
  { id: 3, name: '抖音', icon: '🎵', description: '支持短视频、直播、图集下载', features: ['无水印下载', '直播录制', '批量采集'], color: '#000000' },
  { id: 4, name: '快手', icon: '⚡', description: '支持短视频、直播回放下载', features: ['高清画质', '无水印', '批量下载'], color: '#FF4906' },
  { id: 5, name: 'Twitter/X', icon: '🐦', description: '支持视频、GIF、图片下载', features: ['高清视频', '原图下载', '多媒体'], color: '#1DA1F2' },
  { id: 6, name: 'Instagram', icon: '📷', description: '支持视频、Reels、Stories下载', features: ['高清视频', 'Stories保存', '批量下载'], color: '#E4405F' },
  { id: 7, name: 'TikTok', icon: '🎬', description: '支持国际版短视频下载', features: ['无水印', '高清画质', '音频提取'], color: '#000000' },
  { id: 8, name: '微博', icon: '📱', description: '支持视频、直播、图片下载', features: ['高清视频', '多图下载', 'Live回放'], color: '#E6162D' },
  { id: 9, name: '小红书', icon: '📕', description: '支持视频、图文笔记下载', features: ['无水印', '原图保存', '批量采集'], color: '#FF2442' },
  { id: 10, name: '优酷', icon: '🎥', description: '支持电视剧、电影、综艺下载', features: ['高清画质', '批量下载', '断点续传'], color: '#1F93FF' },
  { id: 11, name: '腾讯视频', icon: '📺', description: '支持会员视频、综艺、动漫下载', features: ['1080P', '批量下载', '字幕提取'], color: '#FF6600' },
  { id: 12, name: '更多平台', icon: '🌐', description: '支持 1000+ 视频网站', features: ['yt-dlp内核', '持续更新', '全网覆盖'], color: '#0EA5E9' },
])

// 搜索功能
const searchQuery = ref('')
const filteredPlatforms = computed(() => {
  if (!searchQuery.value) return platforms.value
  const query = searchQuery.value.toLowerCase()
  return platforms.value.filter(platform => 
    platform.name.toLowerCase().includes(query) ||
    platform.description.toLowerCase().includes(query) ||
    platform.features.some(f => f.toLowerCase().includes(query))
  )
})

// 下载相关状态
const videoUrl = ref('')
const isDownloading = ref(false)
const downloadStatus = ref<'idle' | 'success' | 'error'>('idle')
const statusMessage = ref('')
const videoInfo = ref<any>(null)
const downloadProgress = ref(0)
const downloadSpeed = ref(0)
const downloadSize = ref(0)
const totalSize = ref(0)

// 获取视频信息
const fetchVideoInfo = async () => {
  if (!videoUrl.value) return
  
  try {
    const response = await fetch(`${API_BASE}/info`, {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ url: videoUrl.value })
    })
    
    if (response.ok) {
      videoInfo.value = await response.json()
    }
  } catch (error) {
    console.error('获取视频信息失败:', error)
  }
}

// 下载视频
const handleDownload = async () => {
  if (!videoUrl.value) return
  
  isDownloading.value = true
  downloadStatus.value = 'idle'
  statusMessage.value = '正在解析视频...'
  downloadProgress.value = 0
  downloadSpeed.value = 0
  downloadSize.value = 0
  totalSize.value = 0
  
  try {
    const response = await fetch(`${API_BASE}/download`, {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ 
        url: videoUrl.value,
        format: 'best',
        audio_only: false
      })
    })
    
    if (!response.ok) {
      const errorData = await response.json()
      throw new Error(errorData.detail || '下载失败')
    }
    
    // 获取文件大小
    const contentLength = response.headers.get('Content-Length')
    if (contentLength) {
      totalSize.value = parseInt(contentLength, 10)
    }
    
    // 获取文件名
    const contentDisposition = response.headers.get('Content-Disposition')
    let filename = 'video.mp4'
    if (contentDisposition) {
      // 尝试多种匹配模式
      const patterns = [
        /filename\*=UTF-8''(.+?)(?:;|$)/,
        /filename\*=utf-8''(.+?)(?:;|$)/,
        /filename="(.+?)"/,
        /filename=(.+?)(?:;|$)/
      ]
      for (const pattern of patterns) {
        const match = contentDisposition.match(pattern)
        if (match && match[1]) {
          filename = decodeURIComponent(match[1].trim())
          break
        }
      }
    }
    
    // 下载文件流
    const reader = response.body?.getReader()
    const chunks: Uint8Array[] = []
    let startTime = Date.now()
    let lastUpdateTime = startTime
    
    if (reader) {
      while (true) {
        const { done, value } = await reader.read()
        
        if (done) break
        
        chunks.push(value)
        downloadSize.value += value.length
        
        // 更新进度
        if (totalSize.value > 0) {
          downloadProgress.value = (downloadSize.value / totalSize.value) * 100
        }
        
        // 计算下载速度
        const currentTime = Date.now()
        const timeElapsed = (currentTime - lastUpdateTime) / 1000
        if (timeElapsed >= 0.5) {
          const bytesPerSecond = (downloadSize.value / ((currentTime - startTime) / 1000))
          downloadSpeed.value = bytesPerSecond
          lastUpdateTime = currentTime
        }
      }
    }
    
    // 合并所有数据块
    const blob = new Blob(chunks as BlobPart[])
    const url = window.URL.createObjectURL(blob)
    const a = document.createElement('a')
    a.href = url
    a.download = filename
    document.body.appendChild(a)
    a.click()
    window.URL.revokeObjectURL(url)
    document.body.removeChild(a)
    
    downloadStatus.value = 'success'
    statusMessage.value = `下载成功！文件: ${filename}`
  } catch (error: any) {
    downloadStatus.value = 'error'
    statusMessage.value = error.message || '网络错误，请确保后端服务已启动'
  } finally {
    isDownloading.value = false
  }
}

// 监听 URL 变化，自动获取视频信息
let debounceTimer: ReturnType<typeof setTimeout>
const handleUrlChange = () => {
  clearTimeout(debounceTimer)
  debounceTimer = setTimeout(() => {
    if (videoUrl.value && videoUrl.value.length > 10) {
      fetchVideoInfo()
    }
  }, 500)
}

// 格式化文件大小
const formatSize = (bytes: number): string => {
  if (bytes === 0) return '0 B'
  const k = 1024
  const sizes = ['B', 'KB', 'MB', 'GB']
  const i = Math.floor(Math.log(bytes) / Math.log(k))
  return `${(bytes / Math.pow(k, i)).toFixed(2)} ${sizes[i]}`
}

// 格式化下载速度
const formatSpeed = (bytesPerSecond: number): string => {
  return `${formatSize(bytesPerSecond)}/s`
}
</script>

<template>
  <div class="app-container">
    <!-- 背景装饰 -->
    <div class="bg-decoration">
      <div class="bg-blob bg-blob-1"></div>
      <div class="bg-blob bg-blob-2"></div>
      <div class="bg-grid"></div>
    </div>

    <!-- Header -->
    <header class="header">
      <div class="header-inner">
        <div class="logo">
          <div class="logo-icon">
            <DownloadOutlined class="logo-icon-svg" />
          </div>
          <span class="logo-text">VideoDL</span>
        </div>
        
        <nav class="nav">
          <a href="#" class="nav-link active">首页</a>
          <a href="#platforms" class="nav-link">支持平台</a>
          <a href="#" class="nav-link">使用教程</a>
          <a href="#" class="nav-link">API文档</a>
        </nav>
        
        <a href="https://github.com/Alanjinchenzhu/universal-video-downloader" target="_blank" rel="noopener noreferrer" class="github-btn">
          <GithubOutlined />
          <span>GitHub</span>
        </a>
      </div>
    </header>

    <!-- Hero Section -->
    <section class="hero">
      <div class="hero-content">
        <div class="hero-badge">
          <PlayCircleOutlined />
          <span>支持 1000+ 视频网站</span>
        </div>
        <h1 class="hero-title">万能视频下载器</h1>
        <p class="hero-subtitle">
          一键下载高清视频，无水印保存，支持 YouTube、Bilibili、抖音、快手等主流平台
        </p>
        
        <!-- Download Box -->
        <div class="download-box">
          <div class="download-input-wrapper">
            <GlobalOutlined class="download-input-icon" />
            <input
              v-model="videoUrl"
              @input="handleUrlChange"
              type="text"
              placeholder="粘贴视频链接，支持 YouTube、Bilibili、抖音、快手等..."
              class="download-input"
            />
          </div>
          
          <!-- 视频信息预览 -->
          <div v-if="videoInfo" class="video-preview">
            <img v-if="videoInfo.thumbnail" :src="videoInfo.thumbnail" class="video-thumbnail" />
            <div class="video-meta">
              <h4 class="video-title">{{ videoInfo.title }}</h4>
              <p v-if="videoInfo.uploader" class="video-uploader">{{ videoInfo.uploader }}</p>
              <p v-if="videoInfo.duration" class="video-duration">
                时长: {{ Math.floor(videoInfo.duration / 60) }}:{{ String(videoInfo.duration % 60).padStart(2, '0') }}
              </p>
            </div>
          </div>
          
          <button 
            @click="handleDownload"
            :disabled="isDownloading || !videoUrl"
            class="download-btn"
          >
            <span v-if="!isDownloading" class="download-btn-content">
              <DownloadOutlined />
              <span>开始下载</span>
            </span>
            <span v-else class="download-btn-loading">
              <svg class="spinner" viewBox="0 0 24 24">
                <circle cx="12" cy="12" r="10" stroke="currentColor" stroke-width="3" fill="none" stroke-dasharray="31.4 31.4" />
              </svg>
              <span>{{ downloadProgress > 0 ? '下载中...' : '解析中...' }}</span>
            </span>
          </button>
          
          <!-- 下载进度条 -->
          <div v-if="isDownloading && downloadProgress > 0" class="download-progress">
            <div class="progress-info">
              <span class="progress-text">{{ downloadProgress.toFixed(1) }}%</span>
              <span class="speed-text">{{ formatSpeed(downloadSpeed) }}</span>
            </div>
            <div class="progress-bar">
              <div class="progress-fill" :style="{ width: `${downloadProgress}%` }"></div>
            </div>
            <div class="progress-size">
              <span>{{ formatSize(downloadSize) }} / {{ formatSize(totalSize) }}</span>
            </div>
          </div>
          
          <!-- 下载状态 -->
          <div v-if="downloadStatus !== 'idle' && !isDownloading" :class="['status-message', `status-${downloadStatus}`]">
            <CheckCircleOutlined v-if="downloadStatus === 'success'" />
            <CloseCircleOutlined v-else-if="downloadStatus === 'error'" />
            <span>{{ statusMessage }}</span>
          </div>
          
          <p class="download-hint">
            <span class="hint-icon">💡</span>
            直接粘贴视频页面链接即可，系统自动识别平台
          </p>
        </div>
      </div>
    </section>

    <!-- Features -->
    <section class="features">
      <div class="features-grid">
        <div class="feature-card" v-for="feature in [
          { icon: ThunderboltOutlined, title: '极速下载', desc: '多线程加速，断点续传', color: 'blue' },
          { icon: SafetyCertificateOutlined, title: '无水印', desc: '原画质量，高清保存', color: 'green' },
          { icon: CloudDownloadOutlined, title: '批量下载', desc: '播放列表一键下载', color: 'orange' },
          { icon: ApiOutlined, title: 'API 接口', desc: '开发者友好集成', color: 'purple' },
        ]" :key="feature.title">
          <div :class="['feature-icon', `feature-icon-${feature.color}`]">
            <component :is="feature.icon" />
          </div>
          <h3 class="feature-title">{{ feature.title }}</h3>
          <p class="feature-desc">{{ feature.desc }}</p>
        </div>
      </div>
    </section>

    <!-- Platforms Grid -->
    <section id="platforms" class="platforms">
      <div class="platforms-header">
        <h2 class="section-title">支持平台</h2>
        <p class="section-subtitle">搜索或浏览支持的视频平台</p>
      </div>
      
      <div class="search-wrapper">
        <SearchOutlined class="search-icon" />
        <input v-model="searchQuery" placeholder="搜索平台..." class="search-input" />
      </div>
      
      <div class="platforms-grid">
        <div v-for="platform in filteredPlatforms" :key="platform.id" class="platform-card">
          <div class="platform-header">
            <div class="platform-icon" :style="{ backgroundColor: platform.color + '15' }">
              {{ platform.icon }}
            </div>
            <div class="platform-info">
              <h3 class="platform-name">{{ platform.name }}</h3>
              <p class="platform-desc">{{ platform.description }}</p>
            </div>
          </div>
          <div class="platform-tags">
            <span v-for="feature in platform.features" :key="feature" class="platform-tag">
              {{ feature }}
            </span>
          </div>
        </div>
      </div>
      
      <div v-if="filteredPlatforms.length === 0" class="empty-state">
        <SearchOutlined class="empty-icon" />
        <p>没有找到相关平台</p>
      </div>
    </section>

    <!-- Tech Stack -->
    <section class="tech-stack">
      <h2 class="section-title">技术栈</h2>
      <div class="tech-tags">
        <span class="tech-tag" v-for="tech in [
          { icon: '🐍', name: 'FastAPI' },
          { icon: '📥', name: 'yt-dlp' },
          { icon: '💚', name: 'Vue 3' },
          { icon: '⚡', name: 'Vite' },
          { icon: '🎨', name: 'Tailwind CSS' },
          { icon: '🐜', name: 'Ant Design Vue' },
        ]" :key="tech.name">
          <span class="tech-icon">{{ tech.icon }}</span>
          <span>{{ tech.name }}</span>
        </span>
      </div>
    </section>

    <!-- Footer -->
    <footer class="footer">
      <div class="footer-inner">
        <div class="footer-brand">
          <div class="footer-logo">
            <DownloadOutlined />
          </div>
          <span>VideoDL</span>
        </div>
        <p class="footer-copyright">© 2026 VideoDL. 基于 yt-dlp 构建</p>
        <div class="footer-links">
          <a href="#">使用条款</a>
          <a href="#">隐私政策</a>
          <a href="#">联系我们</a>
        </div>
      </div>
    </footer>
  </div>
</template>

<style>
/* ===== 全局变量 ===== */
:root {
  --primary: #0EA5E9;
  --primary-hover: #38BDF8;
  --primary-light: #E0F2FE;
  --secondary: #0D9488;
  --cta: #F97316;
  --cta-hover: #FB923C;
  --bg: #F0F9FF;
  --bg-card: #FFFFFF;
  --text: #0C4A6E;
  --text-muted: #64748B;
  --border: #BAE6FD;
  --success: #10B981;
  --error: #EF4444;
  --shadow-sm: 0 1px 2px rgba(0, 0, 0, 0.05);
  --shadow-md: 0 4px 6px -1px rgba(0, 0, 0, 0.1);
  --shadow-lg: 0 10px 15px -3px rgba(0, 0, 0, 0.1);
  --shadow-xl: 0 20px 25px -5px rgba(0, 0, 0, 0.1);
  --radius-sm: 8px;
  --radius-md: 12px;
  --radius-lg: 16px;
  --radius-xl: 24px;
  --transition: all 0.2s cubic-bezier(0.4, 0, 0.2, 1);
}

/* ===== 基础样式 ===== */
.app-container {
  min-height: 100vh;
  background: var(--bg);
  position: relative;
  overflow-x: hidden;
}

/* ===== 背景装饰 ===== */
.bg-decoration {
  position: fixed;
  top: 0;
  left: 0;
  right: 0;
  bottom: 0;
  pointer-events: none;
  z-index: 0;
}

.bg-blob {
  position: absolute;
  border-radius: 50%;
  filter: blur(80px);
  opacity: 0.4;
}

.bg-blob-1 {
  width: 600px;
  height: 600px;
  background: linear-gradient(135deg, var(--primary-light) 0%, #BAE6FD 100%);
  top: -200px;
  right: -100px;
}

.bg-blob-2 {
  width: 500px;
  height: 500px;
  background: linear-gradient(135deg, #CCFBF1 0%, #99F6E4 100%);
  bottom: -150px;
  left: -100px;
}

.bg-grid {
  position: absolute;
  top: 0;
  left: 0;
  right: 0;
  bottom: 0;
  background-image: 
    linear-gradient(rgba(14, 165, 233, 0.03) 1px, transparent 1px),
    linear-gradient(90deg, rgba(14, 165, 233, 0.03) 1px, transparent 1px);
  background-size: 60px 60px;
}

/* ===== Header ===== */
.header {
  position: sticky;
  top: 0;
  z-index: 100;
  background: rgba(240, 249, 255, 0.8);
  backdrop-filter: blur(20px);
  border-bottom: 1px solid rgba(186, 230, 253, 0.5);
}

.header-inner {
  max-width: 1200px;
  margin: 0 auto;
  padding: 0 24px;
  height: 64px;
  display: flex;
  align-items: center;
  justify-content: space-between;
}

.logo {
  display: flex;
  align-items: center;
  gap: 10px;
}

.logo-icon {
  width: 36px;
  height: 36px;
  background: linear-gradient(135deg, var(--primary) 0%, var(--secondary) 100%);
  border-radius: var(--radius-sm);
  display: flex;
  align-items: center;
  justify-content: center;
  box-shadow: var(--shadow-md);
}

.logo-icon-svg {
  color: white;
  font-size: 18px;
}

.logo-text {
  font-size: 20px;
  font-weight: 700;
  color: var(--text);
  letter-spacing: -0.5px;
}

.nav {
  display: flex;
  gap: 32px;
}

.nav-link {
  font-size: 14px;
  font-weight: 500;
  color: var(--text-muted);
  text-decoration: none;
  transition: var(--transition);
  position: relative;
}

.nav-link:hover,
.nav-link.active {
  color: var(--primary);
}

.nav-link.active::after {
  content: '';
  position: absolute;
  bottom: -20px;
  left: 0;
  right: 0;
  height: 2px;
  background: var(--primary);
  border-radius: 1px;
}

.github-btn {
  display: flex;
  align-items: center;
  gap: 8px;
  padding: 8px 16px;
  font-size: 14px;
  font-weight: 500;
  color: var(--text);
  background: white;
  border: 1px solid var(--border);
  border-radius: var(--radius-md);
  text-decoration: none;
  transition: var(--transition);
}

.github-btn:hover {
  border-color: var(--primary);
  color: var(--primary);
  box-shadow: var(--shadow-md);
}

/* ===== Hero ===== */
.hero {
  position: relative;
  z-index: 1;
  padding: 80px 24px 60px;
}

.hero-content {
  max-width: 800px;
  margin: 0 auto;
  text-align: center;
}

.hero-badge {
  display: inline-flex;
  align-items: center;
  gap: 8px;
  padding: 8px 16px;
  background: var(--primary-light);
  color: var(--primary);
  font-size: 13px;
  font-weight: 600;
  border-radius: 100px;
  margin-bottom: 24px;
}

.hero-title {
  font-size: 56px;
  font-weight: 800;
  color: var(--text);
  line-height: 1.1;
  margin-bottom: 20px;
  letter-spacing: -1px;
}

.hero-subtitle {
  font-size: 18px;
  color: var(--text-muted);
  line-height: 1.6;
  margin-bottom: 40px;
}

/* ===== Download Box ===== */
.download-box {
  background: white;
  border-radius: var(--radius-xl);
  padding: 24px;
  box-shadow: var(--shadow-xl);
  border: 1px solid rgba(186, 230, 253, 0.3);
}

.download-input-wrapper {
  position: relative;
  margin-bottom: 16px;
}

.download-input-icon {
  position: absolute;
  left: 16px;
  top: 50%;
  transform: translateY(-50%);
  color: var(--text-muted);
  font-size: 18px;
}

.download-input {
  width: 100%;
  padding: 16px 16px 16px 48px;
  font-size: 15px;
  border: 2px solid var(--border);
  border-radius: var(--radius-lg);
  background: var(--bg);
  color: var(--text);
  transition: var(--transition);
}

.download-input:focus {
  outline: none;
  border-color: var(--primary);
  box-shadow: 0 0 0 4px rgba(14, 165, 233, 0.1);
}

.download-input::placeholder {
  color: var(--text-muted);
}

/* ===== 视频预览 ===== */
.video-preview {
  display: flex;
  gap: 16px;
  padding: 16px;
  background: var(--bg);
  border-radius: var(--radius-md);
  margin-bottom: 16px;
  text-align: left;
}

.video-thumbnail {
  width: 120px;
  height: 68px;
  object-fit: cover;
  border-radius: var(--radius-sm);
  flex-shrink: 0;
}

.video-meta {
  flex: 1;
  min-width: 0;
}

.video-title {
  font-size: 14px;
  font-weight: 600;
  color: var(--text);
  margin-bottom: 4px;
  display: -webkit-box;
  -webkit-line-clamp: 2;
  -webkit-box-orient: vertical;
  overflow: hidden;
}

.video-uploader {
  font-size: 12px;
  color: var(--text-muted);
  margin-bottom: 4px;
}

.video-duration {
  font-size: 11px;
  color: var(--primary);
}

/* ===== 下载按钮 ===== */
.download-btn {
  width: 100%;
  padding: 16px 32px;
  font-size: 16px;
  font-weight: 600;
  color: white;
  background: linear-gradient(135deg, var(--cta) 0%, #EA580C 100%);
  border: none;
  border-radius: var(--radius-lg);
  cursor: pointer;
  transition: var(--transition);
  box-shadow: 0 4px 14px rgba(249, 115, 22, 0.4);
}

.download-btn:hover:not(:disabled) {
  transform: translateY(-2px);
  box-shadow: 0 6px 20px rgba(249, 115, 22, 0.5);
}

.download-btn:disabled {
  opacity: 0.6;
  cursor: not-allowed;
}

.download-btn-content,
.download-btn-loading {
  display: flex;
  align-items: center;
  justify-content: center;
  gap: 8px;
}

.spinner {
  width: 18px;
  height: 18px;
  animation: spin 1s linear infinite;
}

@keyframes spin {
  from { transform: rotate(0deg); }
  to { transform: rotate(360deg); }
}

/* ===== 状态消息 ===== */
.status-message {
  display: flex;
  align-items: center;
  justify-content: center;
  gap: 8px;
  padding: 12px 16px;
  margin-top: 16px;
  border-radius: var(--radius-md);
  font-size: 14px;
  font-weight: 500;
}

.status-success {
  background: #D1FAE5;
  color: #059669;
}

.status-error {
  background: #FEE2E2;
  color: #DC2626;
}

.download-hint {
  margin-top: 16px;
  font-size: 13px;
  color: var(--text-muted);
  display: flex;
  align-items: center;
  justify-content: center;
  gap: 6px;
}

.hint-icon {
  font-size: 14px;
}

/* ===== 下载进度条 ===== */
.download-progress {
  margin-top: 16px;
  padding: 16px;
  background: var(--bg);
  border-radius: var(--radius-md);
}

.progress-info {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 8px;
}

.progress-text {
  font-size: 14px;
  font-weight: 600;
  color: var(--primary);
}

.speed-text {
  font-size: 12px;
  color: var(--text-muted);
  font-weight: 500;
}

.progress-bar {
  width: 100%;
  height: 8px;
  background: rgba(14, 165, 233, 0.1);
  border-radius: 4px;
  overflow: hidden;
  margin-bottom: 8px;
}

.progress-fill {
  height: 100%;
  background: linear-gradient(90deg, var(--primary) 0%, var(--primary-hover) 100%);
  border-radius: 4px;
  transition: width 0.3s ease;
  position: relative;
}

.progress-fill::after {
  content: '';
  position: absolute;
  top: 0;
  left: 0;
  right: 0;
  bottom: 0;
  background: linear-gradient(
    90deg,
    transparent 0%,
    rgba(255, 255, 255, 0.3) 50%,
    transparent 100%
  );
  animation: shimmer 2s infinite;
}

@keyframes shimmer {
  0% {
    transform: translateX(-100%);
  }
  100% {
    transform: translateX(100%);
  }
}

.progress-size {
  font-size: 12px;
  color: var(--text-muted);
  text-align: center;
}

/* ===== Features ===== */
.features {
  position: relative;
  z-index: 1;
  padding: 40px 24px;
  max-width: 1200px;
  margin: 0 auto;
}

.features-grid {
  display: grid;
  grid-template-columns: repeat(4, 1fr);
  gap: 24px;
}

.feature-card {
  background: white;
  border-radius: var(--radius-lg);
  padding: 32px 24px;
  text-align: center;
  border: 1px solid rgba(186, 230, 253, 0.3);
  transition: var(--transition);
}

.feature-card:hover {
  transform: translateY(-4px);
  box-shadow: var(--shadow-lg);
}

.feature-icon {
  width: 56px;
  height: 56px;
  margin: 0 auto 16px;
  border-radius: var(--radius-md);
  display: flex;
  align-items: center;
  justify-content: center;
  font-size: 24px;
}

.feature-icon-blue { background: linear-gradient(135deg, #DBEAFE 0%, #BFDBFE 100%); color: #2563EB; }
.feature-icon-green { background: linear-gradient(135deg, #D1FAE5 0%, #A7F3D0 100%); color: #059669; }
.feature-icon-orange { background: linear-gradient(135deg, #FFEDD5 0%, #FED7AA 100%); color: #EA580C; }
.feature-icon-purple { background: linear-gradient(135deg, #EDE9FE 0%, #DDD6FE 100%); color: #7C3AED; }

.feature-title {
  font-size: 16px;
  font-weight: 600;
  color: var(--text);
  margin-bottom: 8px;
}

.feature-desc {
  font-size: 13px;
  color: var(--text-muted);
}

/* ===== Platforms ===== */
.platforms {
  position: relative;
  z-index: 1;
  padding: 60px 24px;
  max-width: 1200px;
  margin: 0 auto;
}

.platforms-header {
  text-align: center;
  margin-bottom: 40px;
}

.section-title {
  font-size: 32px;
  font-weight: 700;
  color: var(--text);
  margin-bottom: 12px;
}

.section-subtitle {
  font-size: 16px;
  color: var(--text-muted);
}

.search-wrapper {
  position: relative;
  max-width: 400px;
  margin: 0 auto 40px;
}

.search-icon {
  position: absolute;
  left: 16px;
  top: 50%;
  transform: translateY(-50%);
  color: var(--text-muted);
  font-size: 16px;
}

.search-input {
  width: 100%;
  padding: 14px 16px 14px 44px;
  font-size: 15px;
  border: 2px solid var(--border);
  border-radius: 100px;
  background: white;
  color: var(--text);
  transition: var(--transition);
}

.search-input:focus {
  outline: none;
  border-color: var(--primary);
  box-shadow: 0 0 0 4px rgba(14, 165, 233, 0.1);
}

.platforms-grid {
  display: grid;
  grid-template-columns: repeat(4, 1fr);
  gap: 20px;
}

.platform-card {
  background: white;
  border-radius: var(--radius-lg);
  padding: 20px;
  border: 1px solid rgba(186, 230, 253, 0.3);
  transition: var(--transition);
  cursor: pointer;
}

.platform-card:hover {
  transform: translateY(-4px);
  box-shadow: var(--shadow-lg);
  border-color: var(--primary);
}

.platform-header {
  display: flex;
  align-items: flex-start;
  gap: 12px;
  margin-bottom: 16px;
}

.platform-icon {
  width: 48px;
  height: 48px;
  border-radius: var(--radius-md);
  display: flex;
  align-items: center;
  justify-content: center;
  font-size: 24px;
  flex-shrink: 0;
}

.platform-info {
  flex: 1;
  min-width: 0;
}

.platform-name {
  font-size: 15px;
  font-weight: 600;
  color: var(--text);
  margin-bottom: 4px;
}

.platform-desc {
  font-size: 12px;
  color: var(--text-muted);
  line-height: 1.4;
}

.platform-tags {
  display: flex;
  flex-wrap: wrap;
  gap: 6px;
}

.platform-tag {
  padding: 4px 10px;
  font-size: 11px;
  font-weight: 500;
  background: var(--bg);
  color: var(--text-muted);
  border-radius: 100px;
}

/* ===== Empty State ===== */
.empty-state {
  text-align: center;
  padding: 60px 20px;
  color: var(--text-muted);
}

.empty-icon {
  font-size: 48px;
  margin-bottom: 16px;
  display: block;
}

/* ===== Tech Stack ===== */
.tech-stack {
  position: relative;
  z-index: 1;
  padding: 60px 24px;
  text-align: center;
}

.tech-tags {
  display: flex;
  flex-wrap: wrap;
  justify-content: center;
  gap: 12px;
  margin-top: 24px;
}

.tech-tag {
  display: flex;
  align-items: center;
  gap: 8px;
  padding: 10px 18px;
  background: white;
  border: 1px solid var(--border);
  border-radius: var(--radius-md);
  font-size: 14px;
  font-weight: 500;
  color: var(--text);
}

.tech-icon {
  font-size: 18px;
}

/* ===== Footer ===== */
.footer {
  position: relative;
  z-index: 1;
  background: white;
  border-top: 1px solid rgba(186, 230, 253, 0.3);
  padding: 40px 24px;
}

.footer-inner {
  max-width: 1200px;
  margin: 0 auto;
  display: flex;
  align-items: center;
  justify-content: space-between;
}

.footer-brand {
  display: flex;
  align-items: center;
  gap: 10px;
  font-weight: 600;
  color: var(--text);
}

.footer-logo {
  width: 28px;
  height: 28px;
  background: linear-gradient(135deg, var(--primary) 0%, var(--secondary) 100%);
  border-radius: 6px;
  display: flex;
  align-items: center;
  justify-content: center;
  color: white;
  font-size: 14px;
}

.footer-copyright {
  font-size: 13px;
  color: var(--text-muted);
}

.footer-links {
  display: flex;
  gap: 24px;
}

.footer-links a {
  font-size: 13px;
  color: var(--text-muted);
  text-decoration: none;
  transition: var(--transition);
}

.footer-links a:hover {
  color: var(--primary);
}

/* ===== 响应式 ===== */
@media (max-width: 1024px) {
  .features-grid,
  .platforms-grid {
    grid-template-columns: repeat(2, 1fr);
  }
}

@media (max-width: 768px) {
  .nav { display: none; }
  .hero-title { font-size: 36px; }
  .hero-subtitle { font-size: 16px; }
  .features-grid,
  .platforms-grid { grid-template-columns: 1fr; }
  .footer-inner {
    flex-direction: column;
    gap: 16px;
    text-align: center;
  }
}
</style>
