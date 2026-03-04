// 导入Pinia相关方法和类型
import { defineStore } from 'pinia'
// 导入Vue响应式API
import { ref, computed } from 'vue'
// 导入API请求模块
import api from '../api/index'
// 导入评论类型定义
import type { Comment } from '../types/comment'

/**
 * 评论状态管理Store（组合式API）
 * 提供评论数据的获取、创建、删除等功能
 */
export const useCommentStore = defineStore('comment', () => {
    // ========== 状态定义 ==========
    const comments = ref<Comment[]>([]) // 评论列表数据
    const totalComments = ref(0)       // 评论总数
    const isLoading = ref(false)       // 是否正在加载（首次加载）
    const isLoadingMore = ref(false)   // 是否正在加载更多（分页加载）
    const deletingCommentId = ref<number | null>(null) // 当前正在删除的评论ID

    // ========== 计算属性 ==========
    /**
     * 判断是否还有更多评论可以加载
     * @returns {boolean} 如果已加载评论数小于总数则返回true
     */
    const hasMoreComments = computed(() => comments.value.length < totalComments.value)

    // ========== 操作方法 ==========
    /**
     * 获取评论列表
     * @param {number} articleId - 文章ID
     * @param {number} [page=1] - 当前页码，默认为1
     * @param {number} [pageSize=10] - 每页数量，默认为10
     */
    const fetchComments = async (articleId: number, page = 1, pageSize = 10) => {
        try {
            // 设置加载状态
            if (page === 1) {
                isLoading.value = true
                comments.value = []
            } else {
                isLoadingMore.value = true
            }

            // 发送API请求获取评论
            const response = await api.get('/api/comments/', {
                params: {
                    article_id: articleId,
                    page,
                    page_size: pageSize
                }
            })

            // 更新状态数据
            const responseData = response.data
            comments.value = page === 1 ? responseData : [...comments.value, ...responseData]
            totalComments.value = response.headers['x-total-count'] || responseData.length
        } catch (error) {
            console.error('获取评论失败:', error)
            throw error
        } finally {
            // 重置加载状态
            isLoading.value = false
            isLoadingMore.value = false
        }
    }

    /**
     * 创建新评论
     * @param {Object} commentData - 评论数据
     * @param {string} commentData.content - 评论内容
     * @param {number} commentData.article - 关联的文章ID
     * @returns {Promise<Comment>} 新创建的评论数据
     */
    const createComment = async (commentData: { content: string; article: number }) => {
        try {
            const response = await api.post('/api/comments/', commentData)
            // 将新评论添加到列表开头
            comments.value = [response.data, ...comments.value]
            totalComments.value += 1
            return response.data
        } catch (error) {
            console.error('发表评论失败:', error)
            throw error
        }
    }

    /**
     * 删除评论
     * @param {number} commentId - 要删除的评论ID
     */
    const deleteComment = async (commentId: number) => {
        try {
            deletingCommentId.value = commentId
            await api.delete(`/api/comments/${commentId}/`)
            // 从列表中过滤掉已删除的评论
            comments.value = comments.value.filter(c => c.id !== commentId)
            totalComments.value -= 1
        } catch (error) {
            console.error('删除评论失败:', error)
            throw error
        } finally {
            deletingCommentId.value = null
        }
    }

    // 返回所有需要暴露的状态和方法
    return {
        // 状态
        comments,
        totalComments,
        isLoading,
        isLoadingMore,
        deletingCommentId,

        // 计算属性
        hasMoreComments,

        // 方法
        fetchComments,
        createComment,
        deleteComment
    }
})