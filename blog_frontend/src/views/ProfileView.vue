<template>
    <div class="profile-container">
        <!-- 加载状态 -->
        <div v-if="loading" class="loading">
            <span class="loader"></span>
            加载中...
        </div>

        <!-- 用户资料卡片 -->
        <div v-else-if="user" class="profile-card">
            <!-- 头像展示区域 -->
            <div class="avatar-section">
                <div class="avatar-wrapper">
                    <img :src="user.avatar" class="avatar-image" @error="handleAvatarError">
                </div>
                <h2 class="username">{{ user.username }}</h2>
            </div>

            <!-- 资料详情区域 -->
            <div class="profile-details">

                <div class="detail-item">
                    <span class="detail-label">个人简介:</span>
                    <span class="detail-value bio" v-if="user.bio">{{ user.bio }}</span>
                    <span class="detail-value no-bio" v-else>这个人很神秘，什么都没有说</span>
                </div>

                <!-- 编辑按钮（仅登录用户可见） -->
                <button v-if="authStore.isAuthenticated && authStore.user?.id === user.id" @click="navigateToEdit"
                    class="edit-button">
                    编辑资料
                </button>
                <button @click="router.push('/')" class="edit-button">回到首页</button>
            </div>
        </div>

        <!-- 未找到用户 -->
        <div v-else class="not-found">
            <h2>用户不存在</h2>
            <router-link to="/" class="home-link">返回首页</router-link>
        </div>
    </div>
</template>

<script setup lang="ts">
import { ref, onMounted } from 'vue'
import { useRoute, useRouter } from 'vue-router'
import { useAuthStore } from '../stores/auth'
import type { NullableUser } from '../types/auth'

const route = useRoute()
const router = useRouter()
const authStore = useAuthStore()

// 用户数据
const user = ref<NullableUser>(null)

// 加载状态
const loading = ref(true)

// 获取用户资料
const loadUserProfile = async () => {
    try {
        loading.value = true
        const userId = Number(route.params.id) // 从路由获取ID
        const profile = await authStore.fetchUserProfile(userId)
        user.value = profile
    } catch (error) {
        console.error('加载用户资料失败:', error)
        user.value = null
    } finally {
        loading.value = false
    }
}

// 头像加载失败处理
const handleAvatarError = (e: Event) => {
    const img = e.target as HTMLImageElement
    img.src = authStore.formatAvatarUrl(null)
}

// 跳转到编辑页面
const navigateToEdit = () => {
    router.push({ name: 'ProfileEdit' })
}

// 组件挂载时获取数据
onMounted(() => {
    loadUserProfile()
})
</script>

<style scoped>
/* 原有样式保持不变 */
.profile-container {
    max-width: 800px;
    margin: 0 auto;
    padding: 2rem;
}

.loading {
    display: flex;
    flex-direction: column;
    align-items: center;
    justify-content: center;
    height: 300px;
    color: #666;
}

.loader {
    width: 48px;
    height: 48px;
    border: 5px solid #f3f3f3;
    border-top: 5px solid #3498db;
    border-radius: 50%;
    animation: spin 1s linear infinite;
    margin-bottom: 1rem;
}

@keyframes spin {
    0% {
        transform: rotate(0deg);
    }

    100% {
        transform: rotate(360deg);
    }
}

.profile-card {
    background: white;
    border-radius: 12px;
    box-shadow: 0 4px 12px rgba(0, 0, 0, 0.1);
    overflow: hidden;
}

.avatar-section {
    display: flex;
    flex-direction: column;
    align-items: center;
    padding: 2rem;
    background: linear-gradient(135deg, #f5f7fa 0%, #c3cfe2 100%);
}

.avatar-wrapper {
    width: 150px;
    height: 150px;
    border-radius: 50%;
    overflow: hidden;
    border: 4px solid white;
    box-shadow: 0 4px 8px rgba(0, 0, 0, 0.1);
}

.avatar-image {
    width: 100%;
    height: 100%;
    object-fit: cover;
}

.username {
    margin-top: 1rem;
    color: #333;
    font-size: 1.8rem;
}

.profile-details {
    padding: 2rem;
}

.detail-item {
    display: flex;
    margin-bottom: 1.5rem;
    padding-bottom: 1.5rem;
    border-bottom: 1px solid #eee;
}

.detail-label {
    font-weight: bold;
    color: #555;
    width: 100px;
}

.detail-value {
    flex: 1;
    color: #333;
}

.bio {
    white-space: pre-line;
    line-height: 1.6;
}

.no-bio {
    color: #999;
    font-style: italic;
}

.edit-button {
    display: block;
    width: 100%;
    padding: 0.8rem;
    background-color: #3498db;
    color: white;
    border: none;
    border-radius: 6px;
    font-size: 1rem;
    cursor: pointer;
    transition: background-color 0.3s;
    margin-top: 2rem;
}

.edit-button:hover {
    background-color: #2980b9;
}

.not-found {
    text-align: center;
    padding: 2rem;
}

.home-link {
    display: inline-block;
    margin-top: 1rem;
    color: #3498db;
    text-decoration: none;
}

.home-link:hover {
    text-decoration: underline;
}

@media (max-width: 600px) {
    .profile-container {
        padding: 1rem;
    }

    .avatar-wrapper {
        width: 120px;
        height: 120px;
    }

    .detail-item {
        flex-direction: column;
    }

    .detail-label {
        width: 100%;
        margin-bottom: 0.5rem;
    }
}
</style>