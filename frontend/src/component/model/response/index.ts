export interface File {
    id: number,
    file: string
}

export interface FilesResponse {
    count: number,
    next: null | string
    previous: null | string
    results: File[]
}