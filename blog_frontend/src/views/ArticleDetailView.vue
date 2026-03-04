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
                            <div class="author-avatar-name"
                                @click="goToAuthorProfile(articleStore.currentArticle.author?.id ?? 0)">
                                <span>作者:</span>
                                <img :src="articleStore.currentArticle.author?.avatar" class="avatar">
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

                        <!-- 操作按钮（仅作者可见) -->
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
                    <h3 class="section-title">评论 ({{ commentStore.comments.length }})</h3>

                    <!-- 发表评论表单 -->
                    <el-form v-if="authStore.isAuthenticated" :model="commentForm" :rules="commentRules"
                        ref="commentFormRef" @submit.prevent="submitComment" class="comment-form">
                        <el-form-item prop="content">
                            <el-input v-model="commentForm.content" :rows="3" type="textarea" placeholder="写下你的评论..."
                                resize="none" class="comment-input" />
                        </el-form-item>
                        <el-form-item>
                            <el-button type="primary" native-type="submit" class="submit-comment-btn"
                                :loading="isSubmitting">
                                发表评论
                            </el-button>
                        </el-form-item>
                    </el-form>
                    <div v-else class="login-prompt">
                        请<el-button type="text" @click="router.push('/login')">登录</el-button>后发表评论
                    </div>

                    <!-- 评论列表 -->
                    <div class="comment-list">
                        <div class="comment-item" v-for="comment in commentStore.comments" :key="comment.id">
                            <div class="comment-header">
                                <div class="comment-author-info" @click="goToAuthorProfile(comment.author.id)">
                                    <img :src="comment.author.avatar" class="comment-avatar">
                                    <span class="comment-author">{{ comment.author.username }}</span>
                                </div>
                                <span class="comment-date">{{ formatDate(comment.created_at) }}</span>
                                <el-button v-if="canDeleteComment(comment)" type="text" size="small"
                                    @click="deleteComment(comment.id)"
                                    :loading="commentStore.deletingCommentId === comment.id">
                                    删除
                                </el-button>
                            </div>
                            <div class="comment-content">
                                {{ comment.content }}
                            </div>
                        </div>

                        <div class="no-comments" v-if="!commentStore.isLoading && commentStore.comments.length === 0">
                            暂无评论，快来发表第一条评论吧~
                        </div>

                        <div class="loading-comments" v-if="commentStore.isLoading">
                            <el-skeleton :rows="2" animated />
                        </div>

                        <div class="load-more" v-if="commentStore.hasMoreComments && !commentStore.isLoading">
                            <el-button type="text" @click="loadMoreComments" :loading="commentStore.isLoadingMore">
                                加载更多评论
                            </el-button>
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
import { computed, onMounted, ref } from 'vue'
import { useRoute, useRouter } from 'vue-router'
import { ElMessage, type FormInstance, type FormRules } from 'element-plus'
import { MdPreview } from 'md-editor-v3'
import 'md-editor-v3/lib/style.css'
import { useArticleStore } from '../stores/article'
import { useAuthStore } from '../stores/auth'
import { useCommentStore } from '../stores/comment'
import type { Comment } from '../types/comment'

const route = useRoute()
const router = useRouter()
const articleStore = useArticleStore()
const authStore = useAuthStore()
const commentStore = useCommentStore()

// 评论表单相关
const commentFormRef = ref<FormInstance>()
const commentForm = ref({
    content: '',
    article: Number(route.params.id)
})

const commentRules = ref<FormRules>({
    content: [
        { required: true, message: '请输入评论内容', trigger: 'blur' },
        { min: 5, max: 1000, message: '评论长度在5到1000个字符之间', trigger: 'blur' }
    ]
})

// 评论提交状态
const isSubmitting = ref(false)

// 计算属性
const isAuthor = computed(() => {
    const userId = authStore.user?.id
    const authorId = articleStore.currentArticle?.author?.id
    return userId && authorId && String(userId) === String(authorId)
})

// 方法
const formatDate = (dateString: string) => {
    return new Date(dateString).toLocaleString()
}

const handleDelete = async () => {
    try {
        if (articleStore.currentArticle?.id) {
            await articleStore.deleteArticle(articleStore.currentArticle.id)
            router.push('/')
        }
    } catch (error) {
        console.error('删除文章失败:', error)
        ElMessage.error('删除文章失败')
    }
}

const goToAuthorProfile = (authorId: number) => {
    if (authorId) {
        router.push(`/profile/${authorId}`)
    }
}

const handleImageClick = () => {
    console.log('图片被点击')
}

const canDeleteComment = (comment: Comment) => {
    return authStore.isAuthenticated &&
        (authStore.user?.id === comment.author.id)
}

const submitComment = async () => {
    if (!commentFormRef.value) return

    try {
        await commentFormRef.value.validate()
        isSubmitting.value = true

        await commentStore.createComment(commentForm.value)
        commentForm.value.content = ''
        ElMessage.success('评论发表成功')
    } catch (error: any) {
        if (error.response?.status === 401) {
            ElMessage.warning('请先登录后再发表评论')
            router.push('/login')
        } else if (error.response?.status === 400) {
            // 处理字段验证错误
            const errors = error.response.data
            for (const field in errors) {
                ElMessage.error(`${field}: ${errors[field].join(', ')}`)
            }
        } else if (error !== 'validate') {
            console.error('发表评论失败:', error)
            ElMessage.error('发表评论失败')
        }
    } finally {
        isSubmitting.value = false
    }
}

const deleteComment = async (commentId: number) => {
    try {
        await commentStore.deleteComment(commentId)
        ElMessage.success('评论删除成功')
    } catch (error) {
        console.error('删除评论失败:', error)
        ElMessage.error('删除评论失败')
    }
}

const loadMoreComments = async () => {
    await commentStore.fetchComments(
        Number(route.params.id),
    )
}

// 生命周期钩子
onMounted(async () => {
    const articleId = Number(route.params.id)
    if (articleId) {
        await articleStore.fetchArticle(articleId)
        await commentStore.fetchComments(articleId)
    }
})
</script>

<style scoped>
/* 保持之前的样式不变 */
.article-detail-container {
    padding: 20px;
    max-width: 1200px;
    margin: 0 auto;
}

.article-header {
    text-align: center;
    margin-bottom: 20px;
    padding-bottom: 20px;
    border-bottom: 1px solid #eee;
}

.article-meta {
    display: flex;
    justify-content: center;
    align-items: center;
    gap: 20px;
    margin-top: 10px;
    color: #666;
    font-size: 14px;
    flex-wrap: wrap;
}

.author-avatar-name {
    display: flex;
    align-items: center;
    gap: 8px;
    cursor: pointer;
    transition: all 0.3s ease;
    padding: 4px 8px;
    border-radius: 4px;
}

.author-avatar-name:hover {
    background-color: #f5f5f5;
}

.avatar {
    width: 32px;
    height: 32px;
    border-radius: 50%;
    object-fit: cover;
    border: 1px solid #eee;
}

.author-name {
    font-weight: 500;
    color: #409eff;
}

.article-cover {
    margin: 0 auto 30px;
    width: 100%;
    max-width: 800px;
    border-radius: 8px;
    box-shadow: 0 4px 12px rgba(0, 0, 0, 0.1);
    overflow: hidden;
    transition: transform 0.3s ease, box-shadow 0.3s ease;
    cursor: pointer;
}

.cover-image {
    width: 100%;
    height: auto;
    display: block;
    transition: transform 0.3s ease;
}

.article-cover:hover {
    transform: translateY(-2px);
    box-shadow: 0 6px 16px rgba(0, 0, 0, 0.15);
}

.article-cover:hover .cover-image {
    transform: scale(1.02);
}

.article-excerpt {
    margin-bottom: 30px;
    padding: 15px;
    background-color: #f8f9fa;
    border-left: 4px solid #409eff;
}

.article-content {
    margin-top: 30px;
}

.article-actions {
    margin-top: 30px;
    display: flex;
    justify-content: center;
    gap: 20px;
    padding-top: 20px;
    border-top: 1px solid #eee;
}

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

.comment-section {
    margin-top: 40px;
}

.comment-form {
    margin-bottom: 30px;
}

.comment-input {
    margin-bottom: 15px;
}

.submit-comment-btn {
    width: 120px;
}

.login-prompt {
    margin-bottom: 30px;
    color: #666;
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

.comment-author-info {
    display: flex;
    align-items: center;
    cursor: pointer;
    transition: all 0.3s ease;
    padding: 4px 8px;
    border-radius: 4px;
}

.comment-author-info:hover {
    background-color: #f5f5f5;
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

.loading-comments {
    padding: 20px 0;
}

.load-more {
    text-align: center;
    margin-top: 20px;
}

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

    .comment-form {
        flex-direction: column;
    }

    .submit-comment-btn {
        width: 100%;
    }
}
</style>