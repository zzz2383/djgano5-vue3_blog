// 导入Vue Router相关功能
import { createRouter, createWebHistory } from 'vue-router'
// 导入认证状态管理
import { useAuthStore } from '../stores/auth'

/**
 * 路由配置数组
 * 每个路由对象包含以下属性：
 * - path: 路由路径
 * - name: 路由名称（唯一标识）
 * - component: 路由组件（使用懒加载）
 * - meta: 路由元信息（如权限要求）
 * - children: 嵌套子路由
 */
const routes = [
    {
        // 根路径
        path: '/',
        name: 'Home',
        // 首页组件（懒加载）
        component: () => import('../views/HomeView.vue'),
        // 默认重定向到文章列表
        redirect: { name: 'Articles' },
        // 嵌套子路由
        children: [
            {
                // 空路径匹配父路由
                path: '',
                name: 'Articles',
                // 命名视图配置
                component: () => import('../views/ArticleListView.vue'),
            },
            {
                // 我的文章路径（注意：子路由不要前导斜线）
                path: 'myarticles',
                name: 'Myarticles',
                // 命名视图配置
                component: () => import('../views/ArticleListView.vue'),
                // 路由元信息：需要登录
                meta: { requiresAuth: true }
            },
        ]
    },
    {
        // 登录页路径
        path: '/login',
        name: 'Login',
        // 登录组件（懒加载）
        component: () => import('../views/LoginView.vue'),
        // 路由元信息：需要未登录状态
        meta: { requiresGuest: true }
    },
    {
        // 注册页路径
        path: '/register',
        name: 'Register',
        // 注册组件（懒加载）
        component: () => import('../views/RegisterView.vue'),
        // 路由元信息：需要未登录状态
        meta: { requiresGuest: true }
    },
    {
        // 文章详情页（动态路由参数）
        path: '/articles/:id',
        name: 'Article-detail',
        // 文章详情组件（懒加载）
        component: () => import('../views/ArticleDetailView.vue')
    },
    {
        // 创建文章页
        path: '/articles/create',
        name: 'Article-create',
        // 创建文章组件（懒加载）
        component: () => import('../views/ArticleCreateView.vue'),
        // 路由元信息：需要登录
        meta: { requiresAuth: true }
    },
    {
        // 编辑文章页（动态路由参数）
        path: '/articles/:id/edit',
        name: 'Article-edit',
        // 编辑文章组件（懒加载）
        component: () => import('../views/ArticleEditView.vue'),
        // 路由元信息：需要登录
        meta: { requiresAuth: true }
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

/**
 * 创建路由实例
 * 配置项：
 * - history: 使用HTML5历史模式
 * - routes: 路由配置数组
 */
const router = createRouter({
    // 使用HTML5历史模式
    history: createWebHistory(),
    // 路由配置
    routes
})

/**
 * 全局前置路由守卫
 * 在每次导航前执行
 * @param to 即将进入的路由
 * @param from 当前导航正要离开的路由
 * @param next 执行跳转的函数
 */
router.beforeEach(async (to, from, next) => {
    // 获取认证存储实例
    const authStore = useAuthStore()

    /**
     * 初始化认证状态
     * 如果store中未认证但localStorage有token，则尝试初始化
     */
    if (!authStore.isAuthenticated && localStorage.getItem('accessToken')) {
        // 从localStorage初始化用户状态
        authStore.initialize()
    }

    // 检查目标路由是否需要认证
    if (to.meta.requiresAuth && !authStore.isAuthenticated) {
        // 重定向到登录页，并携带原路径作为查询参数
        next({
            name: 'Login',
            query: {
                redirect: to.fullPath
            }
        })
    }
    // 检查目标路由是否需要未认证状态（如登录/注册页）
    else if (to.meta.requiresGuest && authStore.isAuthenticated) {
        // 已登录用户访问登录/注册页时重定向到首页
        next({ name: 'Articles' })
    }
    // 其他情况正常放行
    else {
        next()
    }
})

// 导出路由实例
export default router