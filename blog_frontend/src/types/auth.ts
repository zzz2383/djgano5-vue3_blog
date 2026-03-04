// 定义用户接口类型
export interface User {
    id: number       // 用户ID
    username: string // 用户名
    email: string    // 邮箱
    avatar: string   // 头像URL
    bio?: string     // 个人简介（可选）
}
export type NullableUser = User | null
// 定义更新用户资料的参数类型
export interface UpdateProfileParams {
    username?: string
    email?: string
    avatar?: any
    password?: string
}
/**
 * 登录表单数据类型定义
 */
export interface LoginForm {
    username: string  // 用户名
    password: string  // 密码
}
/**
 * 注册表单数据类型
 */
export interface RegisterForm {
    username: string  // 用户名
    email: string     // 邮箱
    password: string // 密码
    confirmPassword: string // 确认密码
}
//资料表单数据类型
export interface ProfileForm {
    avatar: string
    username: string
    password: string
    confirmPassword: string
}