<template>
    <!-- 登录页面容器 -->
    <div class="login-page">
        <!-- 登录表单容器 -->
        <div class="login-container">
            <!-- 使用Element Plus的卡片组件包裹表单 -->
            <el-card class="login-card">
                <!-- 登录标题 -->
                <h2 class="login-title">登录</h2>

                <!-- 登录表单 -->
                <el-form ref="loginFormRef" :model="loginForm" :rules="loginRules" @submit.prevent="handleLogin">
                    <!-- 用户名输入框 -->
                    <el-form-item prop="username">
                        <el-input v-model="loginForm.username" placeholder="用户名" prefix-icon="User" clearable
                            @keyup.enter="handleLogin" />
                    </el-form-item>

                    <!-- 密码输入框 -->
                    <el-form-item prop="password">
                        <el-input v-model="loginForm.password" type="password" placeholder="密码" prefix-icon="Lock"
                            show-password @keyup.enter="handleLogin" />
                    </el-form-item>

                    <!-- 登录按钮 -->
                    <el-form-item>
                        <el-button type="primary" native-type="submit" :loading="loading" class="login-button">
                            登录
                        </el-button>
                    </el-form-item>
                </el-form>

                <!-- 注册引导链接 -->
                <div class="login-footer">
                    <span>还没有账号？</span>
                    <router-link to="/register">立即注册</router-link>
                </div>
            </el-card>
        </div>
    </div>
</template>

<script setup lang="ts">
// ========== 导入部分 ==========
// Vue响应式API
import { ref } from 'vue'
// Vue路由相关
import { useRouter, useRoute } from 'vue-router'
// Pinia认证存储
import { useAuthStore } from '../stores/auth'
// Element Plus组件
import { ElMessage, type FormInstance } from 'element-plus'
//登录表单
import type { LoginForm } from '../types/auth'


// ========== 实例获取 ==========
const router = useRouter()  // 获取路由实例，用于页面跳转
const route = useRoute()    // 获取当前路由信息，用于读取查询参数
const authStore = useAuthStore()  // 获取Pinia认证存储实例
const loginFormRef = ref<FormInstance>()  // 表单引用，用于调用表单方法

// ========== 响应式数据 ==========
// 登录表单数据
const loginForm = ref<LoginForm>({
    username: '',  // 初始为空用户名
    password: ''   // 初始为空密码
})

// ========== 表单验证规则 ==========
const loginRules = {
    username: [
        // 必填验证规则
        {
            required: true,  // 必填字段
            message: '请输入用户名',  // 错误提示信息
            trigger: 'blur'  // 触发验证的时机（失去焦点时）
        }
    ],
    password: [
        // 必填验证规则
        {
            required: true,  // 必填字段
            message: '请输入密码',  // 错误提示信息
            trigger: 'blur'  // 触发验证的时机（失去焦点时）
        }
    ]
}

// ========== 状态管理 ==========
const loading = ref(false)  // 加载状态，用于控制登录按钮的loading效果

// ========== 核心方法 ==========
/**
 * 处理登录提交
 * 1. 表单验证
 * 2. 调用认证接口
 * 3. 处理登录结果
 */
const handleLogin = async () => {
    // 1. 表单验证
    // 调用Element表单的validate方法进行验证
    const valid = await loginFormRef.value?.validate()
    if (!valid) return  // 如果验证失败，直接返回不继续执行

    // 2. 开始加载，显示loading状态
    loading.value = true

    try {
        // 3. 调用认证存储的login方法进行登录
        // trim()去除用户名前后空格
        await authStore.login(
            loginForm.value.username.trim(),
            loginForm.value.password
        )

        // 4. 登录成功后获取重定向路径
        // 从路由查询参数中获取redirect参数，如果没有则跳转到首页
        const redirect = route.query.redirect as string || '/'

        // 5. 跳转到目标页面
        router.push(redirect)

        // 6. 显示成功消息
        ElMessage.success('登录成功')
    } catch (error: unknown) {
        // 7. 错误处理
        // 默认错误消息
        let message = '登录失败，请检查用户名和密码'

        // 如果是Error实例且有message，则使用错误消息
        if (error instanceof Error) {
            message = error.message || message
        }

        // 显示错误提示
        ElMessage.error(message)
    } finally {
        // 8. 结束加载，无论成功失败都要取消loading状态
        loading.value = false
    }
}
</script>

<style scoped>
/* 登录页面整体样式 */
.login-page {
    background-image: url('../assets/images/login.jpg');
    /* 背景图片 */
    background-size: cover;
    /* 背景图覆盖整个容器 */
    background-position: center;
    /* 背景图居中 */
    background-repeat: no-repeat;
    /* 不重复背景图 */
    width: 100vw;
    /* 视口宽度 */
    height: 100vh;
    /* 视口高度 */
    display: flex;
    /* 弹性布局 */
    justify-content: center;
    /* 水平居中 */
    align-items: center;
    /* 垂直居中 */
}

/* 登录容器样式 */
.login-container {
    display: flex;
    justify-content: center;
    align-items: center;
    min-height: 100vh;
    /* 最小高度为视口高度 */
}

/* 登录卡片样式 */
.login-card {
    width: 400px;
    /* 固定宽度 */
    padding: 20px;
    /* 内边距 */
}

/* 登录标题样式 */
.login-title {
    text-align: center;
    /* 文字居中 */
    margin-bottom: 30px;
    /* 底部外边距 */
    color: #409eff;
    /* 主题蓝色 */
}

/* 登录按钮样式 */
.login-button {
    width: 100%;
    /* 宽度100% */
}

/* 登录页脚样式（注册引导） */
.login-footer {
    text-align: center;
    /* 文字居中 */
    margin-top: 20px;
    /* 顶部外边距 */
    color: #909399;
    /* 次要文字颜色 */
}

/* 注册链接样式 */
.login-footer a {
    color: #409eff;
    /* 主题蓝色 */
    text-decoration: none;
    /* 去除下划线 */
}
</style>