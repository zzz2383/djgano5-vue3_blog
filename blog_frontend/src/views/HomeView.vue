<template>
    <!-- 整体布局容器 -->
    <div class="common-layout">
        <!-- Element Plus 容器组件 -->
        <el-container>
            <!-- 顶部导航栏 -->
            <el-header>
                <div class="header-content">
                    <!-- logo图片地址 -->
                    <img src="../assets/images/logo.jpg" alt="Logo" class="logo" /> <!-- 网站Logo -->
                    <el-breadcrumb separator="/">
                        <el-breadcrumb-item :to="{ path: '/' }">首页</el-breadcrumb-item>
                        <el-breadcrumb-item :to="{ path: '/articles/create' }">发布文章</el-breadcrumb-item>
                        <el-breadcrumb-item :to="{ path: '/myarticles' }">我的文章</el-breadcrumb-item>
                        <el-breadcrumb-item></el-breadcrumb-item>
                    </el-breadcrumb>

                    <!-- 用户信息区域 -->
                    <div class="user-info" v-if="authStore.isAuthenticated">
                        <el-dropdown>
                            <div class="user-avatar-name">
                                <div v-if="userAvatar">
                                    <el-avatar :size="40" :src="userAvatar" class="avatar">
                                    </el-avatar>
                                </div>
                                <span class="username">{{ authStore.user?.username }}</span>
                            </div>
                            <template #dropdown>
                                <el-dropdown-menu>
                                    <el-dropdown-item @click="goToAuthorProfile">个人中心</el-dropdown-item>
                                    <el-dropdown-item divided @click="handleLogout">退出登录</el-dropdown-item>
                                </el-dropdown-menu>
                            </template>
                        </el-dropdown>
                    </div>
                    <div class="login-register" v-else>
                        <el-button type="primary" size="small" @click="router.push('/login')">登录</el-button>
                        <el-button size="small" @click="router.push('/register')">注册</el-button>
                    </div>
                </div>
            </el-header>

            <!-- 主内容区域 -->
            <el-main>
                <!-- 用户欢迎信息 -->
                <span class="welcome-message">
                    <h1>欢迎，{{ username }}</h1><!-- 动态显示用户名 -->
                </span>
                <el-divider />
                <!-- 使用 router-view 嵌入 posts 视图 -->
                <ArticleListView v-if="$route.name === 'Articles'" />
                <MyArticleListView v-else-if="$route.name === 'Myarticles'" />
            </el-main>

            <!-- 底部信息栏 -->
            <el-footer>
                博客
            </el-footer>
        </el-container>
    </div>
</template>

<script setup lang="ts">
// 导入Vue相关API
import { computed, onMounted } from 'vue'
// 导入路由相关
import { useRouter } from 'vue-router'
// 导入Element Plus组件
import { ElMessage, ElMessageBox } from 'element-plus'
// 导入Pinia存储
import { useAuthStore } from '../stores/auth'



// ========== 初始化实例 ==========
const router = useRouter()          // 路由实例
const authStore = useAuthStore()    // 认证存储实例

// 初始化认证状态
onMounted(() => {
    console.log('初始化认证状态...')
    authStore.initialize()
    console.log('当前用户:', authStore.user)
})

// ========== 计算属性 ==========
// 获取当前用户名（未登录显示"未登录"）
const username = computed(() => authStore.user?.username || '未登录')

// 获取用户头像，如果没有则使用默认头像
const userAvatar = computed(() => {
    return authStore.user?.avatar
})

// ========== 方法定义 ==========
/**
 * 处理退出登录逻辑
 */
const handleLogout = async () => {
    try {
        // 1. 显示确认对话框
        await ElMessageBox.confirm('确定要退出登录吗？', '提示', {
            confirmButtonText: '确定',
            cancelButtonText: '取消',
            type: 'warning'  // 警告类型
        })

        // 2. 调用认证存储的logout方法
        await authStore.logout()

        // 3. 显示成功消息
        ElMessage.success('退出成功')

        // 4. 跳转到登录页
        router.push('/')
    } catch (error: any) {
        // 5. 错误处理（排除用户取消的情况）
        if (error !== 'cancel') {
            ElMessage.error('退出失败')
        }
    }
}

const goToAuthorProfile = () => {
    if (authStore.user?.id) {
        router.push(`/profile/${authStore.user?.id}`)
    }
}

</script>

<style scoped>
/* 
 * 定义CSS变量控制主题颜色
 * 便于统一管理和修改
 */
.common-layout {
    --header-footer-bg: #000000;
    /* 头部/底部背景色 - 黑色 */
    --header-link-color: #2db5e6;
    /* 头部链接默认颜色 - 浅蓝色 */
    --header-link-hover: #157db4;
    /* 头部链接悬停颜色 - 深蓝色 */
    --main-bg: #ffffff;
    /* 主内容区背景色 - 纯白 */
    --main-text: #333333;
    /* 主内容区文字色 - 深灰 */

    position: fixed;
    top: 0;
    left: 0;
    width: 100vw;
    height: 100vh;
    overflow: hidden;
}

/* 容器样式 - 填满父元素 */
.el-container {
    height: 100%;
}

/* 头部样式 */
.el-header {
    background-color: var(--header-footer-bg);
    height: 80px;
    font-size: 20px;
    font-weight: 500;
    display: flex;
    align-items: center;
    padding: 0 30px;
    box-shadow: 0 2px 10px rgba(0, 0, 0, 0.1);
}

.header-content {
    display: flex;
    align-items: center;
    justify-content: space-between;
    width: 100%;
}

.logo {
    height: 50px;
    width: auto;
    margin-right: 50px;
}


/* 面包屑导航样式 */
.el-breadcrumb {
    font-size: 16px;
}

.el-breadcrumb :deep(.el-breadcrumb__inner) {
    color: var(--header-link-color) !important;
    transition: color 0.3s ease;
}

.el-breadcrumb :deep(.el-breadcrumb__inner:hover) {
    color: var(--header-link-hover) !important;
    text-decoration: none;
}

.el-breadcrumb :deep(.el-breadcrumb__separator) {
    color: var(--header-link-color) !important;
}


/* 用户信息区域样式 */
.user-info {
    display: flex;
    align-items: center;
    margin-left: auto;
    cursor: pointer;
}

.user-avatar-name {
    display: flex;
    align-items: center;
    gap: 10px;
}

.user-avatar-name .username {
    color: white;
    font-size: 16px;
}

.avatar {
    background-color: #f5f7fa;
}

/* 登录注册按钮区域 */
.login-register {
    display: flex;
    gap: 10px;
    margin-left: auto;
}

/* 主内容区样式 */
.el-main {
    background-color: var(--main-bg);
    color: var(--main-text);
    flex: 1;
    overflow: auto;
    padding: 25px;
}

.welcome-message {
    display: block;
    margin-bottom: 20px;
}

/* 底部样式 */
.el-footer {
    background-color: var(--header-footer-bg);
    color: white;
    height: 50px;
    display: flex;
    align-items: center;
    justify-content: center;
    font-size: 14px;
    border-top: 1px solid rgba(255, 255, 255, 0.1);
}
</style>