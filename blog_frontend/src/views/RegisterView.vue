<template>
    <!-- 注册页面主容器 -->
    <div class="register-container">
        <!-- 使用Element Plus的卡片组件作为注册表单容器 -->
        <el-card class="register-card">
            <!-- 注册标题 -->
            <h2 class="register-title">用户注册</h2>

            <!-- 注册表单 -->
            <el-form ref="registerFormRef" :model="registerForm" :rules="registerRules"
                @submit.prevent="handleRegister">
                <!-- 用户名输入框 -->
                <el-form-item prop="username">
                    <el-input v-model="registerForm.username" placeholder="用户名" prefix-icon="User" clearable
                        @keyup.enter="handleRegister" />
                </el-form-item>

                <!-- 邮箱输入框 -->
                <el-form-item prop="email">
                    <el-input v-model="registerForm.email" placeholder="邮箱" prefix-icon="Message" clearable
                        @keyup.enter="handleRegister" />
                </el-form-item>

                <!-- 密码输入框 -->
                <el-form-item prop="password">
                    <el-input v-model="registerForm.password" type="password" placeholder="密码" prefix-icon="Lock"
                        show-password @keyup.enter="handleRegister" />
                </el-form-item>

                <!-- 确认密码输入框 -->
                <el-form-item prop="confirmPassword">
                    <el-input v-model="registerForm.confirmPassword" type="password" placeholder="确认密码"
                        prefix-icon="Lock" show-password @keyup.enter="handleRegister" />
                </el-form-item>

                <!-- 注册按钮 -->
                <el-form-item>
                    <el-button type="primary" native-type="submit" :loading="loading" class="register-button">
                        注册
                    </el-button>
                </el-form-item>
            </el-form>

            <!-- 底部登录链接 -->
            <div class="register-footer">
                <span>已有账号？</span>
                <router-link to="/login">立即登录</router-link>
            </div>
        </el-card>
    </div>
</template>

<script setup lang="ts">
// ========== 导入部分 ==========
import { ref } from 'vue'  // Vue响应式API
import { useRouter } from 'vue-router'  // Vue路由
import { ElMessage, type FormInstance } from 'element-plus'  // Element Plus组件
import { useAuthStore } from '../stores/auth'  // Pinia认证存储
//注册表单
import type { RegisterForm } from '../types/auth'

// ========== 获取实例 ==========
const router = useRouter()  // 获取路由实例，用于页面跳转
const authStore = useAuthStore()  // 获取Pinia认证存储实例
const registerFormRef = ref<FormInstance>()  // 表单引用，用于调用表单方法

// ========== 响应式数据 ==========
// 注册表单数据
const registerForm = ref<RegisterForm>({
    username: '',  // 初始为空用户名
    email: '',     // 初始为空邮箱
    password: '',  // 初始为空密码
    confirmPassword: ''  // 初始为空确认密码
})

// ========== 表单验证规则 ==========
const registerRules = {
    username: [
        // 必填验证
        { required: true, message: '请输入用户名', trigger: 'blur' },
        // 长度验证
        { min: 3, max: 20, message: '长度在 3 到 20 个字符', trigger: 'blur' },
        // 格式验证（只允许字母、数字和下划线）
        {
            pattern: /^[a-zA-Z0-9_]+$/,
            message: '用户名只能包含字母、数字和下划线',
            trigger: 'blur'
        }
    ],
    email: [
        // 必填验证
        { required: true, message: '请输入邮箱地址', trigger: 'blur' },
        // 邮箱格式验证
        { type: 'email', message: '请输入正确的邮箱格式', trigger: 'blur' }
    ],
    password: [
        // 必填验证
        { required: true, message: '请输入密码', trigger: 'blur' },
        // 长度验证
        { min: 6, max: 20, message: '长度在 6 到 20 个字符', trigger: 'blur' },
        // 自定义验证：检查两次密码是否一致
        {
            validator: (rule: any, value: string, callback: Function) => {
                if (registerForm.value.confirmPassword &&
                    value !== registerForm.value.confirmPassword) {
                    callback(new Error('两次输入密码不一致'))
                } else {
                    callback()
                }
            },
            trigger: 'blur'
        }
    ],
    confirmPassword: [
        // 必填验证
        { required: true, message: '请再次输入密码', trigger: 'blur' },
        // 自定义验证：检查两次密码是否一致
        {
            validator: (rule: any, value: string, callback: Function) => {
                if (value !== registerForm.value.password) {
                    callback(new Error('两次输入密码不一致'))
                } else {
                    callback()
                }
            },
            trigger: 'blur'
        }
    ]
}

// ========== 状态管理 ==========
const loading = ref(false)  // 加载状态，控制注册按钮的loading效果

// ========== 核心方法 ==========
/**
 * 处理注册提交
 * 1. 表单验证
 * 2. 调用注册API
 * 3. 自动登录
 * 4. 处理结果
 */
const handleRegister = async () => {
    // 1. 表单验证
    try {
        await registerFormRef.value?.validate()
    } catch (error) {
        return  // 验证失败直接返回
    }

    // 2. 开始加载，显示loading状态
    loading.value = true

    try {
        // 3. 调用注册API
        await authStore.register(
            registerForm.value.username.trim(),  // 去除用户名前后空格
            registerForm.value.email.trim(),       // 去除邮箱前后空格
            registerForm.value.password        // 原始密码
        )

        // 4. 注册成功后自动登录
        await authStore.login(
            registerForm.value.username.trim(),
            registerForm.value.password
        )

        // 5. 显示成功消息并跳转到首页
        ElMessage.success('注册成功')
        router.push('/')
    } catch (error: any) {
        // 6. 错误处理
        handleRegisterError(error)
    } finally {
        // 7. 结束加载，无论成功失败都要取消loading状态
        loading.value = false
    }
}

/**
 * 处理注册错误
 * @param error 错误对象
 */
const handleRegisterError = (error: any) => {
    if (error.response) {
        // 后端返回的错误
        const data = error.response.data

        // 根据后端返回的错误字段显示不同的错误消息
        if (data.username) {
            ElMessage.error(`用户名错误: ${data.username[0]}`)
        } else if (data.email) {
            ElMessage.error(`邮箱错误: ${data.email[0]}`)
        } else if (data.password) {
            ElMessage.error(`密码错误: ${data.password[0]}`)
        } else {
            ElMessage.error('注册失败，请稍后重试')
        }
    } else {
        // 网络错误或其他错误
        ElMessage.error('网络错误，请检查连接')
    }
}
</script>

<style scoped>
/* 注册页面容器样式 */
.register-container {
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

/* 注册卡片样式 */
.register-card {
    width: 400px;
    /* 固定宽度 */
    padding: 20px;
    /* 内边距 */
    box-shadow: 0 2px 12px 0 rgba(0, 0, 0, 0.1);
    /* 阴影效果 */
}

/* 注册标题样式 */
.register-title {
    text-align: center;
    /* 文字居中 */
    margin-bottom: 30px;
    /* 下边距 */
    color: #409eff;
    /* Element Plus主题蓝色 */
    font-size: 24px;
    /* 字体大小 */
}

/* 注册按钮样式 */
.register-button {
    width: 100%;
    /* 宽度100% */
    margin-top: 10px;
    /* 上边距 */
}

/* 底部链接容器样式 */
.register-footer {
    text-align: center;
    /* 文字居中 */
    margin-top: 20px;
    /* 上边距 */
    color: #909399;
    /* 次要文字颜色 */
    font-size: 14px;
    /* 字体大小 */
}

/* 登录链接样式 */
.register-footer a {
    color: #409eff;
    /* 主题蓝色 */
    text-decoration: none;
    /* 去除下划线 */
    margin-left: 5px;
    /* 左边距 */
}

.register-footer a:hover {
    text-decoration: underline;
    /* 鼠标悬停时显示下划线 */
}
</style>