export interface File {
    id: number,
    file: string,
    name: string,
    description: null | string
    title: null | string
}

export interface ResponsePagination {
    count: number,
    next: null | string
    previous: null | string
    results: any[]
}

export interface FilesResponse extends ResponsePagination {
    results: File[]
}

export interface TasksResponse extends ResponsePagination {
    results: TaskShort[]
}


export interface TaskShort {
    id: number;
    status: string;
}


export interface Task extends TaskShort {
    files: File[];
    delivery: boolean
}
