import { defineStore } from 'pinia'
import { ref } from 'vue'
import api from '../api/index' // 导入API请求模块
import type { Article } from '../types/article' // 导入Post类型定义
import { ElMessageBox } from 'element-plus' // 导入Element Plus消息组件

/**
 * 定义文章(Post)的Pinia store
 * 集中管理所有与文章相关的状态和业务逻辑
 */
export const useArticleStore = defineStore('article', () => {
    // ==================== 状态定义 ====================

    // 文章列表数组，使用ref包装以实现响应式
    const articles = ref<Article[]>([])


    // 加载状态，用于显示加载中状态
    const loading = ref(false)

    // 当前查看/编辑的文章详情
    const currentArticle = ref<Article | null>(null)



    // ==================== 方法定义 ====================

    /**
     * 获取文章列表
     * @async
     * @function fetchPosts
     * @throws {Error} 当请求失败时抛出错误
     */
    const fetchArticles = async () => {
        loading.value = true // 开始加载
        try {
            // 发送GET请求获取文章列表
            const response = await api.get('/api/articles/', {
            })

            // 更新文章列表数据
            // 处理不同API返回格式的兼容性
            articles.value = response.data.results || response.data

        } catch (error) {
            console.error('获取文章列表错误:', error)
            throw error // 抛出错误以便组件处理
        } finally {
            loading.value = false // 无论成功失败，结束加载
        }
    }

    /**
     * 获取单个文章详情
     * @async
     * @function fetchPost
     * @param {number} id - 文章ID
     * @returns {Promise<Post>} 返回文章详情
     * @throws {Error} 当请求失败时抛出错误
     */
    const fetchArticle = async (id: number) => {
        try {
            // 发送GET请求获取指定ID的文章
            const response = await api.get(`/api/articles/${id}/`)

            // 更新当前文章状态
            currentArticle.value = response.data

            // 返回文章数据
            return response.data
        } catch (error) {
            console.error('获取文章详情错误:', error)
            throw error
        }
    }

    /**
     * 创建新文章
     * @async
     * @function createPost
     * @param {FormData} formData - 包含文章数据的表单数据
     * @returns {Promise<Post>} 返回新创建的文章
     * @throws {Error} 当请求失败时抛出错误
     */
    const createArticle = async (formData: FormData) => {
        try {
            // 发送POST请求创建文章
            const response = await api.post('/api/articles/', formData, {
                headers: {
                    'Content-Type': 'multipart/form-data' // 设置内容类型为表单数据
                }
            })
            console.log(formData)
            return response.data // 返回新创建的文章
        } catch (error) {
            console.error('创建文章错误:', error)
            throw error
        }
    }

    /**
     * 更新文章
     * @async
     * @function updatePost
     * @param {number} id - 要更新的文章ID
     * @param {FormData} formData - 包含更新数据的表单数据
     * @returns {Promise<Post>} 返回更新后的文章
     * @throws {Error} 当请求失败时抛出错误
     */
    const updateArticle = async (id: number, formData: FormData) => {
        try {
            // 发送PATCH请求更新文章
            const response = await api.patch(`/api/articles/${id}/`, formData, {
                headers: {
                    'Content-Type': 'multipart/form-data'
                }
            })
            return response.data
        } catch (error) {
            console.error('更新文章错误:', error)
            throw error
        }
    }

    /**
     * 删除文章
     * @async
     * @function deletePost
     * @param {number} id - 要删除的文章ID
     * @throws {Error} 当请求失败时抛出错误
     */
    const deleteArticle = async (id: number) => {
        try {
            // 显示确认对话框
            await ElMessageBox.confirm('确定要删除这篇文章吗？', '提示', {
                confirmButtonText: '确定',
                cancelButtonText: '取消',
                type: 'warning'
            })

            // 发送DELETE请求删除文章
            await api.delete(`/api/articles/${id}/`)

            // 删除成功后重新获取文章列表
            await fetchArticles()
        } catch (error) {
            // 如果用户点击了取消，不处理错误
            if (error !== 'cancel') {
                console.error('删除文章错误:', error)
                throw error
            }
        }
    }

    // ==================== 返回状态和方法 ====================
    return {
        // 状态
        articles,
        loading,
        currentArticle,
        // 方法
        fetchArticles,
        fetchArticle,
        createArticle,
        updateArticle,
        deleteArticle
    }
})