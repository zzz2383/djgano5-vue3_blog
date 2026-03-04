// 导入axios库
import axios from 'axios'
// 导入Pinia认证存储
import { useAuthStore } from '../stores/auth'

/**
 * 创建自定义axios实例
 * 配置全局默认参数
 */
const api = axios.create({
    baseURL: import.meta.env.VITE_API_BASE_URL || 'http://localhost:8000', // API基础路径
    timeout: 10000, // 请求超时时间（10秒）
    headers: {
        'Content-Type': 'application/json', // 默认请求头
    }
})

/**
 * 请求拦截器
 * 在发送请求前统一处理
 */
api.interceptors.request.use(
    (config) => {
        // 获取认证存储实例
        const authStore = useAuthStore()

        // 如果存在accessToken，添加到请求头
        if (authStore.accessToken) {
            config.headers.Authorization = `Bearer ${authStore.accessToken}`
        }

        return config
    },
    (error) => {
        // 请求错误处理（通常发生在请求发送前）
        return Promise.reject(error)
    }
)

/**
 * 响应拦截器
 * 统一处理API响应
 */
api.interceptors.response.use(
    (response) => {
        // 2xx范围内的状态码都会触发此函数
        return response
    },
    async (error) => {
        // 超出2xx范围的状态码都会触发此函数
        const originalRequest = error.config // 原始请求配置
        const authStore = useAuthStore()

        /**
         * 处理401未授权错误（token过期）
         * 且该请求未被重试过
         */
        if (error.response.status === 401 && !originalRequest._retry) {
            originalRequest._retry = true // 标记请求已重试

            try {
                // 尝试刷新accessToken
                await authStore.refreshAccessToken()

                // 更新请求头中的Authorization
                originalRequest.headers.Authorization = `Bearer ${authStore.accessToken}`

                // 重新发送原始请求
                return api(originalRequest)
            } catch (refreshError) {
                // 刷新token失败，执行登出
                authStore.logout()
                return Promise.reject(refreshError)
            }
        }

        // 其他错误直接拒绝
        return Promise.reject(error)
    }
)

// 导出配置好的axios实例
export default api