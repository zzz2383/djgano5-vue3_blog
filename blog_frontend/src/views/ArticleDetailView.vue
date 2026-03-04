<template>
    <!-- 页面容器，设置背景图 -->
    <div class="login-page">
        <!-- 文章详情容器，当文章数据加载完成时显示 -->
        <div class="article-detail-container" v-if="articleStore.currentArticle">
            <!-- Element Plus卡片组件 -->
            <el-card class="article-card">
                <!-- 卡片头部插槽 -->
                <template #header>
                    <div class="article-header">
                        <!-- 文章标题 -->
                        <h1>{{ articleStore.currentArticle.title }}</h1>

                        <!-- 文章元信息 -->
                        <div class="article-meta">
                            <!-- 作者信息 -->
                            <div class="author-avatar-name" @click="goToAuthorProfile">
                                <span>作者:</span>
                                <img v-if="articleStore.currentArticle.author?.avatar" :src="articleStore.currentArticle.author?.avatar" class="avatar">
                                <span class="author-name">{{ articleStore.currentArticle.author?.username }}</span>
                            </div>

                            <!-- 发布日期 -->
                            <span class="date">发布于: {{ formatDate(articleStore.currentArticle.created_at || '')
                                }}</span>

                            <!-- 发布状态标签 -->
                            <el-tag :type="articleStore.currentArticle.is_published ? 'success' : 'info'">
                                {{ articleStore.currentArticle.is_published ? '已发布' : '草稿' }}
                            </el-tag>
                        </div>

                        <!-- 操作按钮（仅作者可见） -->
                        <div class="article-actions">
                            <el-button type="primary" @click="router.push(`/`)">
                                首页
                            </el-button>
                            <el-button v-if="isAuthor" type="primary"
                                @click="router.push(`/articles/${articleStore.currentArticle.id}/edit`)">
                                编辑
                            </el-button>
                            <el-button v-if="isAuthor" type="danger" @click="handleDelete">
                                删除
                            </el-button>
                        </div>
                    </div>
                </template>

                <!-- 文章封面图片 -->
                <div class="article-cover" v-if="articleStore.currentArticle.cover_image">
                    <el-image :src="articleStore.currentArticle.cover_image" :alt="articleStore.currentArticle.title"
                        class="cover-image" :preview-src-list="[articleStore.currentArticle.cover_image]"
                        :initial-index="0" fit="cover" hide-on-click-modal preview-teleported
                        @click="handleImageClick" />
                </div>

                <!-- 文章摘要 -->
                <div class="article-excerpt" v-if="articleStore.currentArticle.excerpt">
                    <div class="section-divider"></div>
                    <h3 class="section-title">摘要</h3>
                    <p>{{ articleStore.currentArticle.excerpt }}</p>
                </div>

                <!-- 文章内容（Markdown渲染） -->
                <div class="article-content">
                    <div class="section-divider"></div>
                    <h3 class="section-title">文章内容</h3>
                    <MdPreview :modelValue="articleStore.currentArticle.content" />
                </div>

                <!-- 评论区块 -->
                <div class="comment-section">
                    <div class="section-divider"></div>
                    <h3 class="section-title">评论</h3>

                    <!-- 发表评论区域 -->
                    <div class="comment-input-area">
                        <el-input v-model="commentContent" :rows="3" type="textarea" placeholder="写下你的评论..."
                            resize="none" class="comment-input" />
                        <el-button type="primary" @click="submitComment" class="submit-comment-btn"
                            :disabled="!commentContent.trim()">
                            发表评论
                        </el-button>
                    </div>

                    <!-- 评论列表 -->
                    <div class="comment-list">
                        <div class="comment-item" v-for="comment in comments" :key="comment.id">
                            <div class="comment-header">
                                <img :src="comment.author.avatar" class="comment-avatar">
                                <span class="comment-author">{{ comment.author.username }}</span>
                                <span class="comment-date">{{ formatDate(comment.created_at) }}</span>
                            </div>
                            <div class="comment-content">
                                {{ comment.content }}
                            </div>
                        </div>

                        <div class="no-comments" v-if="comments.length === 0">
                            暂无评论，快来发表第一条评论吧~
                        </div>
                    </div>
                </div>
            </el-card>
        </div>

        <!-- 数据加载时的骨架屏 -->
        <el-skeleton v-else :rows="10" animated />
    </div>
</template>

<script setup lang="ts">
/**
 * 文章详情页组件 - 带详细注释版本
 * 功能：展示文章详情、评论列表，支持发表评论等操作
 */

// ============== 导入部分 ==============
// Vue 相关导入
import { computed, onMounted, ref } from 'vue' // Vue 组合式 API
import { useRoute, useRouter } from 'vue-router' // Vue Router 相关

// 第三方组件导入
import { ElMessage } from 'element-plus' // Element Plus 消息提示组件
import { MdPreview } from 'md-editor-v3' // Markdown 预览组件
import 'md-editor-v3/lib/style.css' // Markdown 编辑器样式

// 状态管理导入
import { useArticleStore } from '../stores/article' // 文章状态管理
import { useAuthStore } from '../stores/auth' // 认证状态管理

// ============== 初始化部分 ==============
// 初始化 Vue Router 相关
const route = useRoute() // 当前路由信息对象，包含 params、query 等
const router = useRouter() // 路由实例，用于编程式导航

// 初始化 Pinia 状态管理
const articleStore = useArticleStore() // 文章相关状态管理
const authStore = useAuthStore() // 认证相关状态管理

// ============== 组件状态定义 ==============
// 评论内容（使用 ref 创建响应式变量）
const commentContent = ref('')

// 评论列表（模拟数据）
const comments = ref([
    {
        id: 1, // 评论ID
        content: '这篇文章写得很好，对我帮助很大！', // 评论内容
        created_at: '2023-05-15T10:30:00Z', // 创建时间
        author: { // 评论作者信息
            id: 2, // 作者ID
            username: '评论用户1', // 用户名
            avatar: 'https://cube.elemecdn.com/3/7c/3ea6beec64369c2642b92c6726f1epng.png' // 头像
        }
    },
    {
        id: 2,
        content: '感谢作者的分享，期待更多精彩内容！',
        created_at: '2023-05-16T14:45:00Z',
        author: {
            id: 3,
            username: '评论用户2',
            avatar: 'https://cube.elemecdn.com/0/88/03b0d39583f48206768a7534e55bcpng.png'
        }
    }
])

// ============== 工具函数 ==============
/**
 * 格式化日期字符串
 * @param {string} dateString - ISO 格式的日期字符串
 * @returns {string} 格式化后的本地日期字符串
 * 
 * 示例：
 * 输入: '2023-05-15T10:30:00Z'
 * 输出: '2023/5/15 18:30:00' (根据本地时区)
 */
const formatDate = (dateString: string) => {
    return new Date(dateString).toLocaleString()
}

// ============== 计算属性 ==============
/**
 * 判断当前用户是否是文章作者
 * @returns {boolean} 是否是作者
 * 
 * 逻辑说明：
 * 1. 获取当前登录用户ID和文章作者ID
 * 2. 如果任一ID不存在，返回false
 * 3. 比较两个ID是否相同（转换为字符串后比较，避免类型不一致问题）
 */
const isAuthor = computed(() => {
    const userId = authStore.user?.id // 当前用户ID（可能为undefined）
    const authorId = articleStore.currentArticle?.author?.id // 文章作者ID（可能为undefined）

    // 如果任一ID不存在，返回false
    if (!userId || !authorId) return false

    // 比较用户ID和作者ID（转换为字符串比较，避免类型不一致问题）
    return String(userId) === String(authorId)
})

// ============== 操作方法 ==============
/**
 * 处理删除文章操作
 * 
 * 流程：
 * 1. 检查当前文章是否存在且有ID
 * 2. 调用store的删除方法
 * 3. 删除成功后跳转到文章列表页
 * 4. 捕获并处理可能的错误
 */
const handleDelete = async () => {
    try {
        // 确保当前文章存在且有ID
        if (articleStore.currentArticle?.id) {
            // 调用store的删除方法
            await articleStore.deleteArticle(articleStore.currentArticle.id)
            // 删除成功后跳转到文章列表页
            router.push('/')
        }
    } catch (error) {
        console.error('删除文章失败:', error)
        ElMessage.error('删除文章失败') // 显示错误提示
    }
}

/**
 * 跳转到作者个人资料页
 * 
 * 说明：
 * 根据文章作者的ID进行路由跳转
 */
const goToAuthorProfile = () => {
    // 检查文章作者ID是否存在
    if (articleStore.currentArticle?.author?.id) {
        // 跳转到作者个人资料页
        router.push(`/profile/${articleStore.currentArticle?.author?.id}`)
    }
}

/**
 * 处理图片点击事件
 * 
 * 当前仅打印日志，可根据需要扩展功能
 * 例如：打开图片预览、记录点击统计等
 */
const handleImageClick = () => {
    console.log('图片被点击') // 调试日志
    // 可扩展功能：打开图片预览、记录点击统计等
}

/**
 * 提交评论
 * 
 * 流程：
 * 1. 验证评论内容是否为空
 * 2. 检查用户是否已登录
 * 3. 创建新评论对象
 * 4. 添加到评论列表
 * 5. 清空评论输入框
 * 6. 显示成功提示
 */
const submitComment = () => {
    // 验证评论内容是否为空
    if (!commentContent.value.trim()) {
        ElMessage.warning('评论内容不能为空') // 显示警告提示
        return
    }

    // 检查用户是否已登录
    if (!authStore.isAuthenticated) {
        ElMessage.warning('请先登录后再发表评论') // 显示警告提示
        router.push('/login') // 跳转到登录页
        return
    }

    // 创建新评论对象（模拟数据）
    const newComment = {
        id: comments.value.length + 1, // 新评论ID（简单递增）
        content: commentContent.value, // 评论内容
        created_at: new Date().toISOString(), // 当前时间（ISO格式）
        author: {
            id: authStore.user?.id || 0, // 用户ID（默认为0）
            username: authStore.user?.username || '匿名用户', // 用户名（默认为匿名）
            avatar: authStore.user?.avatar || 'https://cube.elemecdn.com/9/c2/f0ee8a3c7c9638a54940382568c9dpng.png' // 默认头像
        }
    }

    // 将新评论添加到评论列表开头
    comments.value.unshift(newComment)
    // 清空评论输入框
    commentContent.value = ''
    // 显示成功提示
    ElMessage.success('评论发表成功')
}

// ============== 生命周期钩子 ==============
/**
 * 组件挂载时执行的逻辑
 * 
 * 流程：
 * 1. 从路由参数中获取文章ID
 * 2. 如果ID存在，获取文章详情
 */
onMounted(async () => {
    // 从路由参数中获取文章ID（转换为数字）
    const articleId = Number(route.params.id)

    // 如果ID存在，获取文章详情
    if (articleId) {
        await articleStore.fetchArticle(articleId)
    }
})
</script>

<!-- ============== 样式部分 ============== -->
<style scoped>
/* 文章详情容器 */
.article-detail-container {
    padding: 20px;
    max-width: 1200px;
    margin: 0 auto;
}

/* 文章头部样式 */
.article-header {
    text-align: center;
    margin-bottom: 20px;
    padding-bottom: 20px;
    border-bottom: 1px solid #eee;
}

/* 文章元信息样式 */
.article-meta {
    display: flex;
    justify-content: center;
    align-items: center;
    gap: 20px;
    margin-top: 10px;
    color: #666;
    font-size: 14px;
    flex-wrap: wrap;
    /* 允许在小屏幕上换行 */
}

/* 文章作者头像和名字容器 */
.author-avatar-name {
    display: flex;
    align-items: center;
    gap: 8px;
    cursor: pointer;
    transition: all 0.3s ease;
    padding: 4px 8px;
    border-radius: 4px;
}

/**作者信息悬浮样式 */
.author-avatar-name:hover {
    background-color: #f5f5f5;
}

/* 作者头像样式 */
.avatar {
    width: 32px;
    height: 32px;
    border-radius: 50%;
    object-fit: cover;
    border: 1px solid #eee;
}

/**作者名字样式 */
.author-name {
    font-weight: 500;
    color: #409eff;
}

/* 文章封面样式 */
.article-cover {
    margin: 0 auto 30px;
    width: 100%;
    max-width: 800px;
    /* 固定最大宽度 */
    border-radius: 8px;
    box-shadow: 0 4px 12px rgba(0, 0, 0, 0.1);
    overflow: hidden;
    /* 隐藏超出部分 */
    transition: transform 0.3s ease, box-shadow 0.3s ease;
    cursor: pointer;
}

/* 封面图片样式 */
.cover-image {
    width: 100%;
    /* 宽度填充容器 */
    height: auto;
    /* 高度自适应 */
    display: block;
    /* 消除图片底部间隙 */
    transition: transform 0.3s ease;
}

/* 悬停效果 */
.article-cover:hover {
    transform: translateY(-2px);
    box-shadow: 0 6px 16px rgba(0, 0, 0, 0.15);
}

.article-cover:hover .cover-image {
    transform: scale(1.02);
}

/* 文章摘要样式 */
.article-excerpt {
    margin-bottom: 30px;
    padding: 15px;
    background-color: #f8f9fa;
    border-left: 4px solid #409eff;
}

/* 文章内容样式 */
.article-content {
    margin-top: 30px;
}

/* 操作按钮区域样式 */
.article-actions {
    margin-top: 30px;
    display: flex;
    justify-content: center;
    gap: 20px;
    padding-top: 20px;
    border-top: 1px solid #eee;
}

/* 新增的分割线样式 */
.section-divider {
    height: 1px;
    background: linear-gradient(to right, transparent, #ddd, transparent);
    margin: 30px 0;
}

.section-title {
    margin-bottom: 20px;
    color: #333;
    font-size: 1.5rem;
    padding-bottom: 10px;
    border-bottom: 1px solid #eee;
}

/* 评论区块样式 */
.comment-section {
    margin-top: 40px;
}

.comment-input-area {
    display: flex;
    gap: 15px;
    margin-bottom: 30px;
}

.comment-input {
    flex: 1;
}

.submit-comment-btn {
    align-self: flex-end;
    height: 84px;
    /* 与输入框高度一致 */
}

.comment-list {
    margin-top: 20px;
}

.comment-item {
    padding: 15px 0;
    border-bottom: 1px solid #f0f0f0;
}

.comment-header {
    display: flex;
    align-items: center;
    margin-bottom: 10px;
}

.comment-avatar {
    width: 32px;
    height: 32px;
    border-radius: 50%;
    margin-right: 10px;
    object-fit: cover;
}

.comment-author {
    font-weight: 500;
    color: #409eff;
    margin-right: 15px;
}

.comment-date {
    color: #999;
    font-size: 0.9rem;
}

.comment-content {
    line-height: 1.6;
    color: #333;
}

.no-comments {
    text-align: center;
    color: #999;
    padding: 30px 0;
}

/* 响应式调整 */
@media (max-width: 768px) {
    .article-cover {
        margin: 20px 0;
        border-radius: 4px;
    }

    .section-divider {
        margin: 20px 0;
    }

    .section-title {
        font-size: 1.3rem;
    }

    .comment-input-area {
        flex-direction: column;
    }

    .submit-comment-btn {
        align-self: flex-end;
        height: auto;
        width: 100%;
    }
}
</style>