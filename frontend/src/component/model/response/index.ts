export interface File {
    id: number,
    file: string,
    description: null | string,
    title: null | string
}

export interface FilesResponse {
    count: number,
    next: null | string
    previous: null | string
    results: File[]
}

export interface Task {
    id: number;
    files: File[];
    status: string;
}
