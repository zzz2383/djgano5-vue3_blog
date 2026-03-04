<template>
    <!-- 个人资料编辑容器 -->
    <div class="profile-edit-container">
        <!-- 标题 -->
        <h2>修改个人资料</h2>

        <!-- Element Plus 表单组件 -->
        <el-form ref="profileForm" :model="form" :rules="rules" label-width="120px" label-position="top"
            class="profile-form">
            <!-- 头像上传区域 -->
            <el-form-item label="头像">
                <!-- 上传组件 -->
                <el-upload class="avatar-uploader" :show-file-list="false" :auto-upload="false"
                    :on-change="handleAvatarChange" :before-upload="beforeAvatarUpload">
                    <!-- 显示当前头像或上传图标 -->
                    <img v-if="form.avatar" :src="form.avatar" class="avatar" />
                    <el-icon v-else class="avatar-uploader-icon">
                        <Plus />
                    </el-icon>
                </el-upload>
                <!-- 上传提示 -->
                <div class="upload-tip">支持JPG/PNG格式</div>
                <!-- 移除头像按钮 -->
                <el-button v-if="form.avatar" type="danger" size="small" @click="removeAvatar">
                    移除头像
                </el-button>
            </el-form-item>

            <!-- 用户名显示 -->
            <el-form-item label="用户名">
                <el-input v-model="form.username" readonly />
            </el-form-item>

            <!-- 密码修改 -->
            <el-form-item label="修改密码" prop="password">
                <el-input v-model="form.password" type="password" placeholder="请输入新密码" show-password clearable />
            </el-form-item>

            <!-- 确认密码 -->
            <el-form-item label="确认密码" prop="confirmPassword">
                <el-input v-model="form.confirmPassword" type="password" placeholder="请再次输入新密码" show-password
                    clearable />
            </el-form-item>

            <!-- 表单操作按钮 -->
            <el-form-item>
                <el-button type="primary" @click="submitForm">保存修改</el-button>
                <el-button @click="resetForm">重置</el-button>
            </el-form-item>
        </el-form>
    </div>
</template>

<script setup lang="ts">
// 导入Vue相关API
import { ref, reactive, onMounted } from 'vue'
// 导入Element Plus组件
import { ElMessage } from 'element-plus'
import { Plus } from '@element-plus/icons-vue'
// 导入Pinia存储
import { useAuthStore } from '../stores/auth'
// 导入路由
import router from '../router'
// 导入Element Plus上传类型
import type { UploadFile } from 'element-plus'
// 导入类型定义
import type { ProfileForm } from '../types/auth'

// 初始化认证存储
const authStore = useAuthStore()

/**
 * 表单数据
 */
const form = reactive<ProfileForm>({
    avatar: authStore.user?.avatar || '',
    username: authStore.user?.username || '',
    password: '',
    confirmPassword: ''
})

// 头像文件引用
const avatarFile = ref<File | null>(null)
// 头像是否改变标志
const avatarChanged = ref(false)

/**
 * 表单验证规则
 * - password: 长度6-20字符
 * - confirmPassword: 必须与password一致
 */
const rules = reactive({
    password: [
        { min: 6, max: 20, message: '长度在 6 到 20 个字符', trigger: 'blur' }
    ],
    confirmPassword: [
        { validator: validatePassword, trigger: 'blur' }
    ]
})

/**
 * 自定义密码验证函数
 * @param rule 验证规则
 * @param value 输入值
 * @param callback 回调函数
 */
function validatePassword(rule: any, value: string, callback: any) {
    if (value !== form.password) {
        callback(new Error('两次输入的密码不一致'))
    } else {
        callback()
    }
}

/**
 * 处理头像变化
 * @param file 上传的文件对象
 * @returns {boolean} 是否允许上传
 */
const handleAvatarChange = (file: UploadFile) => {
    // 验证文件类型
    const isJPGorPNG = file.raw?.type === 'image/jpeg' || file.raw?.type === 'image/png'
    // 验证文件大小
    const isLt2M = file.raw?.size ? file.raw.size / 1024 / 1024 < 2 : false

    // 验证失败处理
    if (!isJPGorPNG) {
        ElMessage.error('头像图片只能是 JPG/PNG 格式!')
        return false
    }
    if (!isLt2M) {
        ElMessage.error('头像图片大小不能超过 2MB!')
        return false
    }

    // 处理有效文件
    if (file.raw) {
        avatarFile.value = file.raw
        form.avatar = URL.createObjectURL(file.raw)
    } else {
        avatarFile.value = null
        form.avatar = ''
    }
    avatarChanged.value = true
    return false
}

/**
 * 头像上传前验证
 * @param file 文件对象
 * @returns {boolean} 是否允许上传
 */
const beforeAvatarUpload = (file: File) => {
    const isJPGorPNG = file.type === 'image/jpeg' || file.type === 'image/png'
    const isLt2M = file.size / 1024 / 1024 < 2

    if (!isJPGorPNG) {
        ElMessage.error('头像图片只能是 JPG/PNG 格式!')
        return false
    }
    if (!isLt2M) {
        ElMessage.error('头像图片大小不能超过 2MB!')
        return false
    }

    return true
}

/**
 * 移除头像
 */
const removeAvatar = () => {
    avatarFile.value = null
    form.avatar = ''
    avatarChanged.value = true
}

/**
 * 提交表单
 */
const submitForm = async () => {
    try {
        // 验证表单
        await (profileForm.value as any).validate()

        // 构造提交数据
        const submitData: any = {}
        // 如果有密码则添加
        if (form.password) submitData.password = form.password

        // 处理头像
        if (avatarFile.value) {
            submitData.avatar = avatarFile.value
        } else if (avatarChanged.value) {
            submitData.avatar = '' // 表示移除头像
        }

        // 调用API更新用户信息
        await authStore.updateProfile(submitData)

        ElMessage.success('资料更新成功')
        router.push('/')
    } catch (error) {
        console.error('更新失败:', error)
        ElMessage.error('资料更新失败')
    }
}

/**
 * 重置表单
 */
const resetForm = () => {
    Object.assign(form, {
        avatar: authStore.user?.avatar || '',
        username: authStore.user?.username || '',
        password: '',
        confirmPassword: ''
    })
    avatarFile.value = null
    avatarChanged.value = false
}

// 表单引用
const profileForm = ref()

// 组件挂载时加载用户数据
onMounted(() => {
    if (authStore.isAuthenticated) {
        form.avatar = authStore.user?.avatar || ''
        form.username = authStore.user?.username || ''
    }
})
</script>

<style scoped>
/* 个人资料编辑容器样式 */
.profile-edit-container {
    max-width: 800px;
    margin: 0 auto;
    padding: 20px;
}

/* 表单样式 */
.profile-form {
    margin-top: 30px;
}

/* 头像上传区域样式 */
.avatar-uploader {
    display: flex;
    flex-direction: column;
    align-items: center;
}

.avatar-uploader :deep(.el-upload) {
    border: 1px dashed var(--el-border-color);
    border-radius: 6px;
    cursor: pointer;
    position: relative;
    overflow: hidden;
    transition: var(--el-transition-duration-fast);
}

.avatar-uploader :deep(.el-upload:hover) {
    border-color: var(--el-color-primary);
}

/* 头像上传图标样式 */
.avatar-uploader-icon {
    font-size: 28px;
    color: #8c939d;
    width: 150px;
    height: 150px;
    line-height: 150px;
    text-align: center;
}

/* 头像图片样式 */
.avatar {
    width: 150px;
    height: 150px;
    display: block;
    object-fit: cover;
    border-radius: 6px;
}

/* 上传提示文字样式 */
.upload-tip {
    margin-top: 10px;
    font-size: 12px;
    color: var(--el-text-color-secondary);
}

/* 表单标签样式 */
:deep(.el-form-item__label) {
    font-weight: bold;
    padding-bottom: 8px;
}

/* 按钮间距 */
.el-button {
    margin-right: 15px;
}
</style>