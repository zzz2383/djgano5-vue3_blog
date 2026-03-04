import { defineStore } from 'pinia'
import { ref, computed } from 'vue'
import api from '../api/index'
import type { User, UpdateProfileParams } from '../types/auth'


export const useAuthStore = defineStore('auth', () => {
    // ============== 状态定义 ==============
    const user = ref<User | null>(JSON.parse(localStorage.getItem('user') || 'null'))
    const accessToken = ref<string | null>(localStorage.getItem('accessToken'))
    const refreshToken = ref<string | null>(localStorage.getItem('refreshToken'))


    // ============== 计算属性 ==============
    const isAuthenticated = computed(() => !!user.value)

    // ============== 方法定义 ==============

    /**
     ◦ 用户登录方法
     ◦ @param username - 用户名
     ◦ @param password - 密码
     ◦ @throws {Error} 如果登录失败或token缺失  
     */
    const login = async (username: string, password: string) => {
        try {
            const response = await api.post('/api/user/login/', {
                username,
                password
            })

            console.log('登录响应数据:', response.data) // 调试日志

            // 确保响应中包含用户数据
            if (!response.data.user) {
                throw new Error('用户数据缺失')
            }

            // 更新状态
            user.value = {
                ...response.data.user,
                // 确保头像URL是完整路径
                avatar: formatAvatarUrl(response.data.user.avatar),
                bio: response.data.user.bio || '' // 添加bio字段
            }
            accessToken.value = response.data.access
            refreshToken.value = response.data.refresh

            console.log('登录后的用户数据:', user.value) // 调试日志

            // 持久化到 localStorage
            localStorage.setItem('user', JSON.stringify(user.value))
            if (accessToken.value) {
                localStorage.setItem('accessToken', accessToken.value)
            }
            if (refreshToken.value) {
                localStorage.setItem('refreshToken', refreshToken.value)
            }

            console.log('本地存储已更新') // 调试日志
        } catch (error) {
            console.error('登录失败:', error)
            throw error
        }
    }

    /**
     ◦ 格式化头像URL
     ◦ @param avatarUrl - 头像URL
     ◦ @returns 完整的头像URL
     */
    const defaultAvatar = '../assets/images/default-avatar.png'

    // 修改 formatAvatarUrl 方法
    const formatAvatarUrl = (avatarUrl: string | null): string => {
        if (!avatarUrl) return defaultAvatar;

        // 如果已经是完整URL则直接使用
        if (avatarUrl.startsWith('http') || avatarUrl.startsWith('data:')) {
            return avatarUrl;
        }

        // 处理相对路径（以/开头）
        if (avatarUrl.startsWith('/')) {
            const baseUrl = import.meta.env.VITE_API_BASE_URL?.replace(/\/$/, '') || '';
            // 避免重复拼接/media
            if (avatarUrl.startsWith('/media/')) {
                return `${baseUrl}${avatarUrl}`;
            }
            return `${baseUrl}/media${avatarUrl}`;
        }

        // 其他情况（如直接是文件名）
        const baseUrl = import.meta.env.VITE_API_BASE_URL?.replace(/\/$/, '') || '';
        return `${baseUrl}/media/${avatarUrl}`;
    }
    /**
     ◦ 刷新访问令牌
     */
    const refreshAccessToken = async () => {
        if (!refreshToken.value) {
            throw new Error('No refresh token available')
        }

        try {
            const response = await api.post('/api/user/refresh/', {
                refresh: refreshToken.value
            })

            accessToken.value = response.data.access
            if (!accessToken.value) {
                throw new Error('Access token is missing after refresh')
            }
            localStorage.setItem('accessToken', accessToken.value)
        } catch (error) {
            console.error('Token refresh failed:', error)
            logout()
            throw error
        }
    }

    /**
     ◦ 用户登出方法
     */
    const logout = async () => {
        try {
            if (!refreshToken.value) {
                throw new Error('没有可用的刷新令牌')
            }

            const response = await api.post(
                '/api/user/logout/',
                { refresh_token: refreshToken.value },
                {
                    headers: {
                        'Content-Type': 'application/json',
                        'Authorization': `Bearer ${accessToken.value}`
                    }
                }
            )

            if (response.status !== 200) {
                throw new Error(`退出失败: ${response.statusText}`)
            }
        } catch (error) {
            console.error('退出过程中出错:', error)
        } finally {
            clearAuthData()
        }
    }

    /**
     ◦ 用户注册方法
     */
    const register = async (username: string, email: string, password: string) => {
        try {
            const res = await api.post('/api/user/register/', { username, email, password })

            console.log('注册响应数据:', res.data) // 调试日志

            user.value = {
                ...res.data.user,
                avatar: formatAvatarUrl(res.data.user.avatar),
                bio: res.data.user.bio || '' // 添加bio字段
            }
            accessToken.value = res.data.access
            refreshToken.value = res.data.refresh

            if (accessToken.value) {
                localStorage.setItem('accessToken', accessToken.value)
                localStorage.setItem('refreshToken', refreshToken.value!)
                localStorage.setItem('user', JSON.stringify(user.value))
            }
            return res
        } catch (error) {
            clearAuthData()
            throw error
        }
    }

    /**
     * 更新用户资料
     * @param params - 更新参数
     */
    const updateProfile = async (params: UpdateProfileParams) => {
        if (!user.value) {
            throw new Error('用户未登录')
        }

        try {
            // 使用 FormData 处理可能包含文件的数据
            const formData = new FormData()

            if (params.username) formData.append('username', params.username)
            if (params.email) formData.append('email', params.email)
            if (params.password) formData.append('password', params.password)
            if (params.avatar) formData.append('avatar', params.avatar)

            const response = await api.patch(
                `/api/user/profile/${user.value.id}/`,
                formData,
                {
                    headers: {
                        'Content-Type': 'multipart/form-data',
                        'Authorization': `Bearer ${accessToken.value}`
                    }
                }
            )

            console.log('更新资料响应:', response.data) // 调试日志

            // 更新本地用户数据
            user.value = {
                ...user.value,
                ...response.data,
                avatar: formatAvatarUrl(response.data.avatar)
            }

            // 更新 localStorage
            localStorage.setItem('user', JSON.stringify(user.value))

            console.log('更新后的用户数据:', user.value) // 调试日志

            return response.data
        } catch (error) {
            console.error('更新用户资料失败:', error)
            throw error
        }
    }

    /**
     ◦ 清除认证数据
     */
    const clearAuthData = () => {
        user.value = null
        accessToken.value = null
        refreshToken.value = null
        localStorage.removeItem('accessToken')
        localStorage.removeItem('refreshToken')
        localStorage.removeItem('user')
    }

    /**
     ◦ 初始化认证状态(从localStorage恢复)
     */
    const initialize = () => {
        const storedUser = localStorage.getItem('user')
        const storedAccessToken = localStorage.getItem('accessToken')
        const storedRefreshToken = localStorage.getItem('refreshToken')

        if (!storedAccessToken || !storedRefreshToken || !storedUser) {
            clearAuthData()
            return
        }

        try {
            // 解析用户数据
            const parsedUser = JSON.parse(storedUser)

            // 更新状态
            user.value = {
                ...parsedUser,
                avatar: formatAvatarUrl(parsedUser.avatar),
                bio: parsedUser.bio || '' // 确保bio字段存在
            }
            accessToken.value = storedAccessToken
            refreshToken.value = storedRefreshToken

            console.log('初始化用户数据:', user.value) // 调试日志
        } catch (error) {
            console.error('初始化用户数据失败:', error)
            clearAuthData()
        }
    }

    // 获取用户资料
    const fetchUserProfile = async (userId?: string | number) => {
        try {
            const targetUserId = userId || user.value?.id
            if (!targetUserId) throw new Error('无法确定用户ID')

            const response = await api.get(`/api/user/profile/${targetUserId}`)
            return {
                ...response.data,
                avatar: formatAvatarUrl(response.data.avatar)
            }
        } catch (error) {
            console.error('获取用户资料失败:', error)
            return null
        }
    }



    // ============== 返回状态和方法 ==============
    return {
        // 状态
        user,
        accessToken,
        refreshToken,

        // 计算属性
        isAuthenticated,


        // 方法
        login,
        refreshAccessToken,
        logout,
        register,
        updateProfile,
        clearAuthData,
        initialize,
        formatAvatarUrl,
        fetchUserProfile,
    }
})