// src/main.ts
// Vue 应用的入口文件

// 1. 导入 Vue 的核心创建函数
import { createApp } from 'vue'

// 2. 导入状态管理库 Pinia 的创建函数
import { createPinia } from 'pinia'

// 3. 导入根组件
import App from './App.vue'

// 4. 导入路由配置
import router from './router'

// 5. 导入 Element Plus 组件库及其样式
import ElementPlus from 'element-plus'
import 'element-plus/dist/index.css'

// 6. 创建 Vue 应用实例
const app = createApp(App)

// 7. 使用 Element Plus 组件库
//    这会全局注册所有 Element Plus 组件
app.use(ElementPlus)

// 8. 使用 Pinia 状态管理
//    创建一个 Pinia 实例并作为插件使用
app.use(createPinia())

// 9. 使用路由配置
//    将路由实例挂载到 Vue 应用中
app.use(router)

// 10. 将 Vue 应用挂载到 DOM
//     #app 对应 public/index.html 中的 div 元素
app.mount('#app')

/*
 * 执行顺序说明：
 * 1. 首先创建 Vue 应用实例
 * 2. 然后依次注册各种插件和功能
 *    - UI 组件库 (Element Plus)
 *    - 状态管理 (Pinia)
 *    - 路由系统 (Vue Router)
 * 3. 最后将应用挂载到 DOM
 *
 * 注意事项：
 * - 插件注册顺序有时会影响功能使用
 * - 每个 use() 调用都会返回应用实例，支持链式调用
 * - 也可以写成：createApp(App).use(...).use(...).mount('#app')
 */