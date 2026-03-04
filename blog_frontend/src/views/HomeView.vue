<template>
    <!-- 整体布局容器 -->
    <div class="common-layout">
        <!-- Element Plus 容器组件 -->
        <el-container>
            <!-- 顶部导航栏 -->
            <el-header>
                <div class="header-content">
                    <img src="../assets/images/logo.jpg" alt="Logo" class="logo" />
                    <el-space :size="20" spacer="|">
                        <el-link underline="hover" href="/">首页</el-link>
                        <el-link underline="hover" href="/articles/create">发布文章</el-link>
                        <el-link underline="hover" href="/myarticles">我的文章</el-link>
                    </el-space>

                    <!-- 搜索框 -->
                    <div class="search-container">
                        <el-input v-model="searchQuery" placeholder="搜索文章..." clearable @clear="handleSearchClear"
                            @keyup.enter="handleSearch" class="search-input">
                            <template #append>
                                <el-button :icon="Search" @click="handleSearch" />
                            </template>
                        </el-input>
                    </div>

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
                    <h1>欢迎，{{ username }}</h1>
                </span>
                <el-divider />

                <!-- 使用ArticleListView组件并根据路由传递不同参数 -->
                <!--检查当前路由名称($route.name)是否为 'Myarticles'-->
                <!--如果是，传递 'myArticles'模式（显示当前用户的文章）-->
                <!--
如果不是，传递 'published'模式（显示所有已发布的文章）-->
                <ArticleListView :mode="$route.name === 'Myarticles' ? 'myArticles' : 'published'"
                    :search-query="searchQuery" />
            </el-main>

            <!-- 底部信息栏 -->
            <el-footer>
                博客
            </el-footer>
        </el-container>
    </div>
</template>

<script setup lang="ts">
// ============== 导入部分 ==============
import { computed, ref } from 'vue'
import { useRouter, useRoute } from 'vue-router'
import { ElMessage, ElMessageBox } from 'element-plus'
import { Search } from '@element-plus/icons-vue'
import { useAuthStore } from '../stores/auth'
import ArticleListView from './ArticleListView.vue'

const router = useRouter()
const route = useRoute()
const authStore = useAuthStore()

// ============== 搜索相关状态 ==============
const searchQuery = ref('') // 搜索关键词

// 初始化时检查路由中的搜索参数
if (route.query.search) {
    searchQuery.value = route.query.search as string
}

// ============== 计算属性 ==============
const username = computed(() => authStore.user?.username || '未登录')
const userAvatar = computed(() => authStore.user?.avatar)

// ============== 方法定义 ==============
/**
 * 处理搜索操作
 */
const handleSearch = () => {
    if (searchQuery.value.trim()) {
        // 更新路由查询参数
        router.push({
            query: { ...route.query, search: searchQuery.value }
        })
    } else {
        ElMessage.warning('请输入搜索关键词')
    }
}

/**
 * 处理搜索清除操作
 */
const handleSearchClear = () => {
    searchQuery.value = ''
    const query = { ...route.query }
    delete query.search
    router.push({ query })
}

/**
 * 处理退出登录逻辑
 */
const handleLogout = async () => {
    try {
        await ElMessageBox.confirm('确定要退出登录吗？', '提示', {
            confirmButtonText: '确定',
            cancelButtonText: '取消',
            type: 'warning'
        })

        await authStore.logout()
        ElMessage.success('退出成功')
        router.push('/')
    } catch (error: any) {
        if (error !== 'cancel') {
            ElMessage.error('退出失败')
        }
    }
}

/**
 * 跳转到作者个人资料页
 */
const goToAuthorProfile = () => {
    if (authStore.user?.id) {
        router.push(`/profile/${authStore.user?.id}`)
    }
}
</script>

<style scoped>
/* CSS变量定义 */
.common-layout {
    --header-footer-bg: #000000;
    --header-link-color: #2db5e6;
    --header-link-hover: #157db4;
    --main-bg: #ffffff;
    --main-text: #333333;

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

.el-header .el-link {
    color: var(--header-link-color) !important;
    font-size: 16px;
    transition: color 0.3s ease;
}

.el-header .el-link:hover {
    color: var(--header-link-hover) !important;
}

.el-header .el-space__spacer {
    color: var(--header-link-color) !important;
}

/* 搜索框样式 */
.search-container {
    flex: 1;
    max-width: 400px;
    margin: 0 30px;
}

.search-input {
    transition: all 0.3s ease;
}

.search-input:focus-within {
    box-shadow: 0 0 0 2px rgba(45, 181, 230, 0.2);
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

/* 响应式设计 */
@media (max-width: 992px) {
    .header-content {
        flex-wrap: wrap;
        gap: 15px;
    }

    .search-container {
        order: 3;
        width: 100%;
        max-width: 100%;
        margin: 10px 0 0 0;
    }
}

@media (max-width: 576px) {
    .el-header {
        height: auto;
        padding: 15px;
    }

    .logo {
        margin-right: 20px;
    }

    .el-space {
        display: flex;
        flex-wrap: wrap;
        gap: 10px;
    }

    .el-space__spacer {
        display: none;
    }
}
</style>