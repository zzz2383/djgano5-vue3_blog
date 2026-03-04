export interface Author {
    id: number
    username: string
    // 可以根据需要添加更多作者字段
}

export interface Article {
    id?: number
    title: string
    excerpt: string
    content: string
    is_published: boolean
    cover_image?: string | null
    cover_image_url?: string
    created_at?: string
    updated_at?: string
    author?: Author
}