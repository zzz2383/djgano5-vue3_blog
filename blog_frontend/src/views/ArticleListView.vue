<template>
    <!-- 文章列表容器 -->
    <div class="article-list-container">
        <!-- 列表头部区域 -->
        <div class="article-list-header">
            <h2>{{ listTitle }}</h2>
        </div>
        <el-divider />

        <!-- 文章网格布局 -->
        <div class="article-grid">
            <div v-for="article in filteredArticles" :key="article.id" class="article-card">
                <ArticleCard :article="article" @edit="handleEdit" @delete="handleDelete" />
            </div>
        </div>

        <!-- 空状态提示 -->
        <div v-if="filteredArticles.length === 0" class="empty-tip">
            <el-empty :description="emptyDescription" />
        </div>
    </div>
</template>

<script setup lang="ts">
// ============== 导入部分 ==============
// Vue 相关 API
import { computed, ref, watch, onMounted } from 'vue'
// 路由相关
import { useRouter } from 'vue-router'
// Pinia 状态管理
import { useArticleStore } from '../stores/article'
import { useAuthStore } from '../stores/auth'
import { ElMessage, ElMessageBox } from 'element-plus'
// 子组件
import ArticleCard from './ArticleCard.vue'

// ============== 组件 Props 定义 ==============
const props = defineProps({
    mode: {
        type: String,
        default: 'published', // 默认显示模式：'published' 或 'myArticles'
        validator: (value: string) => ['published', 'myArticles'].includes(value) // 验证器，确保传入正确的模式
    },
    searchQuery: {
        type: String,
        default: '' // 搜索关键词，默认为空
    }
})

// ============== 初始化实例 ==============
const router = useRouter()          // 路由实例
const articleStore = useArticleStore() // 文章状态管理
const authStore = useAuthStore()    // 认证状态管理

// ============== 响应式状态 ==============
const localSearchQuery = ref(props.searchQuery) // 本地搜索关键词（与props.searchQuery同步）
const isSearching = ref(false)      // 是否处于搜索状态

// ============== 计算属性 ==============
/**
 * 列表标题计算属性
 * 根据当前模式返回不同的标题
 */
const listTitle = computed(() => {
    return props.mode === 'myArticles' ? '我的文章' : '文章列表'
})

/**
 * 空状态描述计算属性
 * 根据当前模式返回不同的空状态提示
 */
const emptyDescription = computed(() => {
    return props.mode === 'myArticles'
        ? '您还没有发表过文章'
        : '暂无已发布的文章'
})

/**
 * 基础文章列表计算属性
 * 根据当前模式返回不同的文章列表：
 * - myArticles模式：返回当前用户的文章（无论是否发布）
 * - published模式：返回所有已发布的文章
 */
const baseArticles = computed(() => {
    if (props.mode === 'myArticles') {
        return articleStore.articles.filter(article =>
            article.author?.id === authStore.user?.id
        )
    } else {
        return articleStore.articles.filter(article => article.is_published)
    }
})

/**
 * 过滤后的文章列表计算属性
 * 如果有搜索关键词，返回匹配搜索的文章，否则返回基础文章列表
 */
const filteredArticles = computed(() => {
    if (isSearching.value && localSearchQuery.value.trim()) {
        const query = localSearchQuery.value.toLowerCase()
        return baseArticles.value.filter(article =>
            article.title.toLowerCase().includes(query) ||  // 匹配标题
            article.content.toLowerCase().includes(query) || // 匹配内容
            (article.excerpt && article.excerpt.toLowerCase().includes(query)) // 匹配摘要
        )
    }
    return baseArticles.value
})

// ============== 方法定义 ==============

/**
 * 处理编辑操作
 * @param id 文章ID
 */
const handleEdit = (id: number) => {
    router.push(`/articles/${id}/edit`) // 导航到文章编辑页
}

/**
 * 处理删除操作
 * @param id 文章ID
 */
const handleDelete = async (id: number) => {
    try {
        // 显示确认对话框
        await ElMessageBox.confirm('确定要删除这篇文章吗？', '提示', {
            confirmButtonText: '确定',
            cancelButtonText: '取消',
            type: 'warning'
        })
        // 调用store的删除方法
        await articleStore.deleteArticle(id)
        ElMessage.success('删除成功')
    } catch (error) {
        // 错误处理（排除用户取消的情况）
        if (error !== 'cancel') {
            ElMessage.error('删除失败')
        }
    }
}

// ============== 监听器 ==============
/**
 * 监听props.searchQuery变化
 * 当父组件传递的searchQuery变化时，更新本地状态
 */
watch(() => props.searchQuery, (newVal) => {
    localSearchQuery.value = newVal
    isSearching.value = !!newVal
}, { immediate: true }) // 立即执行一次

// ============== 生命周期钩子 ==============
/**
 * 组件挂载时执行的逻辑
 * 加载文章数据
 */
onMounted(async () => {
    await articleStore.fetchArticles() // 从API获取文章数据
})
</script>

<style scoped>
/* 样式保持不变 */
.article-list-container {
    padding: 20px;
    max-width: 1200px;
    margin: 0 auto;
}

.article-list-header {
    display: flex;
    justify-content: space-between;
    align-items: center;
    margin-bottom: 30px;
    flex-wrap: wrap;
    gap: 20px;
}

.article-grid {
    display: grid;
    grid-template-columns: repeat(auto-fill, minmax(500px, 1fr));
    gap: 20px;
    margin-bottom: 30px;
}

.empty-tip {
    margin-top: 50px;
}

@media (max-width: 768px) {
    .article-list-header {
        flex-direction: column;
        align-items: flex-start;
    }


    .article-grid {
        grid-template-columns: 1fr;
    }
}
</style>