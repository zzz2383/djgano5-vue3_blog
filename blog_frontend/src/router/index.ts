// src/router/index.ts
import { createRouter, createWebHistory } from 'vue-router'
import Home from '../views/HomeView.vue'
import { useAuthStore } from '../stores/auth' // 引入认证状态管理

const routes = [
    //主页
    {
        path: '/',
        name: 'Home',
        component: Home
    },
    //登录
    {
        path: '/login',
        name: 'Login',
        component: () => import('../views/LoginView.vue'), // 异步加载组件
        meta: { requiresGuest: true }, // 元信息：需要未登录状态
    },
    //注册
    {
        path: '/register',
        name: 'Register',
        component: () => import('../views/RegisterView.vue'), // 异步加载组件
        meta: { requiresGuest: true }, // 需要未登录状态
    },
    // 查看他人资料（通过ID）
    {
        path: '/profile/:id',
        name: 'ProfileView',
        component: () => import('../views/ProfileView.vue'),
    },
    //修改资料
    {
        path: '/profile/edit',
        name: 'ProfileEdit',
        component: () => import('../views/ProfileEdit.vue'),
        meta: { requiresAuth: true },
    },

]

const router = createRouter({
    history: createWebHistory(),
    routes
})


/**
 * 全局前置路由守卫
 * 在每次导航前执行
 */
router.beforeEach(async (to, from, next) => {
    // 获取认证存储实例
    const authStore = useAuthStore()

    /**
     * 初始化认证状态
     * 如果store中未认证但localStorage有token，则尝试初始化
     */
    if (!authStore.isAuthenticated && localStorage.getItem('accessToken')) {
        authStore.initialize()
    }

    // 检查目标路由是否需要认证
    if (to.meta.requiresAuth && !authStore.isAuthenticated) {
        // 重定向到登录页，并携带原路径作为查询参数
        next({ name: 'Login', query: { redirect: to.fullPath } })
    }
    // 检查目标路由是否需要未认证状态（如登录/注册页）
    else if (to.meta.requiresGuest && authStore.isAuthenticated) {
        // 已登录用户访问登录/注册页时重定向到首页
        next({ name: 'Home' })
    }
    // 其他情况正常放行
    else {
        next()
    }
})


export default router