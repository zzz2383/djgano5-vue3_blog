// 评论相关状态
export interface Comment {
    id: number
    content: string
    created_at: string
    article: number
    author: {
        id: number
        username: string
        avatar?: string
    }
}