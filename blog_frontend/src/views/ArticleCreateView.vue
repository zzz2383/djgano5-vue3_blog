<template>
    <!-- 登录/编辑页面容器 -->
    <div class="login-page">
        <!-- 文章创建容器 -->
        <div class="article-create-container">
            <!-- Element Plus卡片组件 -->
            <el-card class="article-create-card">
                <!-- 卡片头部插槽 -->
                <template #header>
                    <div class="card-header">
                        <h2>创建新文章</h2>
                    </div>
                </template>

                <!-- 表单区域 -->
                <el-form ref="articleFormRef" :model="articleForm" :rules="articleRules" label-width="100px"
                    label-position="top" @submit.prevent="handleSubmit" :validate-on-rule-change="false">
                    <!-- 标题输入项 -->
                    <el-form-item label="标题" prop="title">
                        <el-input v-model="articleForm.title" placeholder="请输入文章标题"
                            @input="debouncedValidateField('title')" />
                    </el-form-item>

                    <!-- 封面图片上传 -->
                    <el-form-item label="封面图片">
                        <el-upload class="cover-uploader" :show-file-list="false" :auto-upload="false"
                            :on-change="handleCoverChange" :before-upload="beforeCoverUpload" :headers="uploadHeaders">
                            <!-- 显示封面图片或上传图标 -->
                            <img v-if="articleForm.cover_image_url" :src="articleForm.cover_image_url"
                                class="cover-image" />
                            <el-icon v-else class="cover-uploader-icon">
                                <Plus />
                            </el-icon>
                        </el-upload>
                    </el-form-item>

                    <!-- 文章摘要 -->
                    <el-form-item label="摘要" prop="excerpt">
                        <el-input v-model="articleForm.excerpt" type="textarea" :rows="3" placeholder="请输入文章摘要（可选）"
                            maxlength="300" show-word-limit @input="debouncedValidateField('excerpt')" />
                    </el-form-item>

                    <!-- 文章内容编辑器 -->
                    <el-form-item label="内容" prop="content">
                        <div class="editor-container">
                            <!-- Markdown编辑器组件 -->
                            <MdEditor v-model="articleForm.content" placeholder="请输入文章内容..."
                                :toolbars="markdownToolbars" @onChange="handleEditorChange" />
                        </div>
                    </el-form-item>

                    <!-- 发布状态开关 -->
                    <el-form-item label="发布状态">
                        <el-switch v-model="articleForm.is_published" active-text="发布" inactive-text="草稿" />
                    </el-form-item>

                    <!-- 表单操作按钮 -->
                    <el-form-item>
                        <el-button type="primary" native-type="submit" :loading="submitting">
                            提交
                        </el-button>
                        <el-button @click="router.push('/')">取消</el-button>
                    </el-form-item>
                </el-form>
            </el-card>
        </div>
    </div>
</template>

<script setup lang="ts">
// ============== 导入部分 ==============
import { ref, reactive, computed } from 'vue'
import { useRouter } from 'vue-router'
import { ElMessage, type FormInstance, type UploadFile } from 'element-plus'
import { Plus } from '@element-plus/icons-vue'
import { MdEditor, type ToolbarNames } from 'md-editor-v3'
import 'md-editor-v3/lib/style.css'
import { useArticleStore } from '../stores/article'
import { useAuthStore } from '../stores/auth'
import { debounce } from 'lodash-es'
import type { Article } from '../types/article'

// ============== 初始化部分 ==============
const router = useRouter() // 路由实例
const articleStore = useArticleStore() // 文章状态管理
const authStore = useAuthStore() // 认证状态管理
const articleFormRef = ref<FormInstance>() // 表单引用

// ============== 表单数据 ==============
const articleForm = reactive<Article>({
    title: '', // 文章标题
    excerpt: '', // 文章摘要
    content: '', // 文章内容
    is_published: false, // 发布状态
    cover_image_url: '', // 封面图片URL
})

// ============== 表单验证规则 ==============
const articleRules = reactive({
    title: [
        { required: true, message: '请输入文章标题', trigger: 'blur' },
        { min: 5, max: 200, message: '长度在 5 到 200 个字符', trigger: 'blur' }
    ],
    content: [
        { required: true, message: '请输入文章内容', trigger: 'blur' },
        { min: 10, message: '内容至少需要 10 个字符', trigger: 'blur' }
    ]
})

// ============== Markdown编辑器工具栏配置 ==============
const markdownToolbars: ToolbarNames[] = [
    'bold', // 加粗
    'underline', // 下划线
    'italic', // 斜体
    'strikeThrough', // 删除线
    'sub', // 下标
    'sup', // 上标
    'table', // 表格
    'quote', // 引用
    'unorderedList', // 无序列表
    'orderedList', // 有序列表
    'codeRow', // 行内代码
    'code', // 代码块
    'link', // 链接
    'image', // 图片
    'revoke', // 撤销
    'next', // 重做
    'save', // 保存
    'pageFullscreen', // 页面全屏
    'fullscreen', // 全屏
    'preview', // 预览
    'htmlPreview', // HTML预览
    'catalog' // 目录
]

// ============== 上传请求头 ==============
const uploadHeaders = computed(() => ({
    Authorization: `Bearer ${authStore.accessToken}` // 携带认证token
}))

// ============== 状态变量 ==============
const submitting = ref(false) // 提交状态
const coverImageFile = ref<File | null>(null) // 封面图片文件

// ============== 防抖验证字段 ==============
const debouncedValidateField = debounce((prop: string) => {
    articleFormRef.value?.validateField(prop)
}, 300)

// ============== 编辑器变化处理 ==============
const handleEditorChange = (value: string) => {
    articleForm.content = value // 更新内容
    debouncedValidateField('content') // 验证内容字段
}

// ============== 表单提交处理 ==============
const handleSubmit = async () => {
    try {
        // 1. 表单验证
        const valid = await articleFormRef.value?.validate()
        if (!valid) return

        submitting.value = true // 开始提交

        // 2. 准备表单数据
        const formData = new FormData()
        formData.append('title', articleForm.title)
        formData.append('content', articleForm.content)
        formData.append('excerpt', articleForm.excerpt)
        formData.append('is_published', String(articleForm.is_published))

        // 3. 添加封面图片（如果有）
        if (coverImageFile.value) {
            formData.append('cover_image', coverImageFile.value)
        }

        // 4. 调用API创建文章
        const response = await articleStore.createArticle(formData)

        // 5. 处理成功结果
        ElMessage.success('文章创建成功')
        router.push(`/articles/${response.id}`) // 跳转到文章详情页

    } catch (error: any) {
        // 6. 错误处理
        console.error('创建文章错误:', error)
        ElMessage.error('创建文章失败')
    } finally {
        submitting.value = false // 结束提交
    }
}

// ============== 封面图片变化处理 ==============
const handleCoverChange = (file: UploadFile) => {
    const isJPGorPNG = file.raw?.type === 'image/jpeg' || file.raw?.type === 'image/png'
    const isLt5M = file.raw?.size ? file.raw.size / 1024 / 1024 < 5 : false

    if (!isJPGorPNG) {
        ElMessage.error('封面图片只能是 JPG/PNG 格式!')
        return false
    }
    if (!isLt5M) {
        ElMessage.error('封面图片大小不能超过 5MB!')
        return false
    }

    if (file.raw) {
        coverImageFile.value = file.raw
        articleForm.cover_image_url = URL.createObjectURL(file.raw)
    } else {
        coverImageFile.value = null
        articleForm.cover_image_url = ''
    }
    return false
}

// ============== 封面图片上传前验证 ==============
const beforeCoverUpload = (file: File) => {
    const isJPGorPNG = file.type === 'image/jpeg' || file.type === 'image/png'
    const isLt5M = file.size / 1024 / 1024 < 5

    if (!isJPGorPNG) {
        ElMessage.error('封面图片只能是 JPG/PNG 格式!')
        return false
    }
    if (!isLt5M) {
        ElMessage.error('封面图片大小不能超过 5MB!')
        return false
    }

    return true
}
</script>

<!-- ============== 样式部分 ============== -->
<style scoped>
/* 登录页面样式 */
.login-page {
    background-image: url('@/assets/images/edit-bg.jpg');
    background-size: cover;
    background-position: center;
    background-repeat: no-repeat;
    width: 100vw;
    height: 100%;
    display: flex;
    justify-content: center;
    align-items: center;
}

/* 文章创建容器 */
.article-create-container {
    padding: 20px;
}

/* 文章创建卡片 */
.article-create-card {
    max-width: 1200px;
    margin: 0 auto;
}

/* 卡片头部样式 */
.card-header {
    display: flex;
    justify-content: space-between;
    align-items: center;
}

/* 封面图片上传区域 */
.cover-uploader {
    border: 1px dashed #d9d9d9;
    border-radius: 6px;
    cursor: pointer;
    position: relative;
    overflow: hidden;
    width: 200px;
    height: 120px;
    display: flex;
    justify-content: center;
    align-items: center;
}

/* 上传区域悬停效果 */
.cover-uploader:hover {
    border-color: #409eff;
}

/* 封面图片样式 */
.cover-image {
    width: 100%;
    height: 100%;
    object-fit: cover;
}

/* 上传图标样式 */
.cover-uploader-icon {
    font-size: 28px;
    color: #8c939d;
}

/* 编辑器容器 */
.editor-container {
    width: 100%;
}
</style>