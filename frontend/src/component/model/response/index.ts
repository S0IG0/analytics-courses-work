export interface File {
    id: number,
    file: string,
    name: string,
    description: null | string
    title: null | string
}


export interface Graph {
    id: number,
    title: string,
    description: string,
    x_axis: any[],
    y_axis: any[],
    x_title: null | string,
    y_title: null | string,
    type_graph: string,
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
    id: number,
    status: string,
}


export interface Task extends TaskShort {
    files: File[],
    graphs: Graph[],
    delivery: boolean,
    text: string | null,
}
