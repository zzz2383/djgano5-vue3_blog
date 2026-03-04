<template>
    <div class="article-card">
        <!-- 文章封面图片 -->
        <div class="article-cover" @click="router.push(`/articles/${article.id}`)">
            <img v-if="article.cover_image" :src="article.cover_image" :alt="article.title" class="cover-image" />
            <div v-else class="cover-placeholder">
                <el-icon>
                    <Picture />
                </el-icon>
            </div>
        </div>

        <!-- 文章内容区域 -->
        <div class="article-content">
            <h3 class="article-title" @click="router.push(`/articles/${article.id}`)">
                {{ article.title }}
            </h3>

            <div class="article-meta">
                <el-tag :type="article.is_published ? 'success' : 'info'" size="small">
                    {{ article.is_published ? '已发布' : '草稿' }}
                </el-tag>
                <span class="article-date">{{ formatDate(article.created_at ?? '') }}</span>
            </div>

            <p class="article-excerpt">{{ article.excerpt || '暂无摘要' }}</p>

            <!-- 操作按钮 -->
            <div class="article-actions">
                <el-button size="small" @click="router.push(`/articles/${article.id}`)">
                    查看
                </el-button>
                <el-button v-if="isAuthor(article)" size="small" type="primary" @click="$emit('edit', article.id)">
                    编辑
                </el-button>
                <el-button v-if="isAuthor(article)" size="small" type="danger" @click="$emit('delete', article.id)">
                    删除
                </el-button>
            </div>
        </div>
    </div>
</template>

<script setup lang="ts">
// ============== 导入部分 ==============
// Vue Router 相关
import { useRouter } from 'vue-router'
// Pinia 状态管理
import { useAuthStore } from '../stores/auth'
// Element Plus 图标
import { Picture } from '@element-plus/icons-vue'

// ============== 初始化实例 ==============
const router = useRouter()          // 路由实例，用于编程式导航
const authStore = useAuthStore()    // 认证状态管理

// ============== 组件 Props 定义 ==============
const props = defineProps({
    article: {
        type: Object,               // 文章数据对象
        required: true,             // 必需属性
    }
})

// ============== 工具函数 ==============
/**
 * 格式化日期字符串
 * @param {string} dateString - ISO格式的日期字符串
 * @returns {string} 格式化后的本地日期字符串
 * 
 * 示例：
 * 输入: '2023-05-15T10:30:00Z'
 * 输出: '2023/5/15 18:30:00' (根据本地时区)
 */
const formatDate = (dateString: string) => {
    return new Date(dateString).toLocaleString()
}

/**
 * 判断当前用户是否是文章作者
 * @param {Object} article - 文章对象
 * @returns {boolean} 是否是作者
 * 
 * 逻辑说明：
 * 1. 获取当前用户ID和文章作者ID
 * 2. 如果任一ID不存在，返回false
 * 3. 比较两个ID是否相同（转换为字符串比较，避免类型不一致问题）
 */
const isAuthor = (article: any) => {
    const userId = authStore.user?.id      // 当前用户ID（可能为undefined）
    const authorId = article.author?.id    // 文章作者ID（可能为undefined）

    // 如果任一ID不存在，返回false
    if (!userId || !authorId) return false

    // 比较用户ID和作者ID（转换为字符串比较）
    return String(userId) === String(authorId)
}
</script>

<style scoped>
/* 文章卡片样式 */
.article-card {
    border: 1px solid #ebeef5;
    border-radius: 8px;
    overflow: hidden;
    transition: all 0.3s ease;
    background: #fff;
    box-shadow: 0 2px 12px 0 rgba(0, 0, 0, 0.1);
}

.article-card:hover {
    transform: translateY(-5px);
    box-shadow: 0 6px 16px 0 rgba(0, 0, 0, 0.1);
}

/* 文章封面样式 */
.article-cover {
    height: 250px;
    background: #f5f7fa;
    cursor: pointer;
    overflow: hidden;
    position: relative;
}

.cover-image {
    width: 100%;
    height: 100%;
    object-fit: cover;
    transition: transform 0.3s ease;
}

.article-cover:hover .cover-image {
    transform: scale(1.05);
}

.cover-placeholder {
    width: 100%;
    height: 100%;
    display: flex;
    align-items: center;
    justify-content: center;
    color: #c0c4cc;
    font-size: 48px;
}

/* 文章内容区域 */
.article-content {
    padding: 20px;
}

.article-title {
    margin: 0 0 10px 0;
    font-size: 18px;
    cursor: pointer;
    color: #303133;
    transition: color 0.2s;
}

.article-title:hover {
    color: #409eff;
}

.article-meta {
    display: flex;
    align-items: center;
    gap: 10px;
    margin-bottom: 15px;
}

.article-date {
    font-size: 14px;
    color: #909399;
}

.article-excerpt {
    margin: 0 0 15px 0;
    color: #606266;
    font-size: 14px;
    line-height: 1.6;
    display: -webkit-box;
    -webkit-line-clamp: 3;
    line-clamp: 3;
    -webkit-box-orient: vertical;
    overflow: hidden;
    text-overflow: ellipsis;
}

/* 操作按钮区域 */
.article-actions {
    display: flex;
    gap: 10px;
}
</style>