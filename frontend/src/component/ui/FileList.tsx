import {useRef, useState} from "react";
import {File, FilesResponse} from "@model/response";
import $api from "@api/http";
import {Spinner} from "@ux/loader/Spinner.tsx";
import useScroll from "@hook/useScroll.tsx";
import FileCard from "@ui/FileCard.tsx";


const FileList = () => {

    const [files, setFiles] = useState<File[]>([])
    const [count, setCount] = useState(0)
    const [page, setPage] = useState<number | null>(1)
    const [loading, setLoading] = useState(false)


    const fetchFiles = (page: number | null) => {
        if (!page) return

        setLoading(true)
        $api.get<FilesResponse>(`/files/?page=${page}`)
            .then(response => {
                setCount(response.data.count)
                setFiles(prevState => [...prevState, ...response.data.results])
                if (response.data.next) {
                    // @ts-ignore
                    setPage(prevState => prevState + 1)
                } else {
                    setPage(null);
                }

            })
            .finally(() => setLoading(false))
    }


    const parentRef = useRef<HTMLDivElement | null>(null)
    const childRef = useRef<HTMLDivElement | null>(null)
    useScroll(parentRef, childRef, () => fetchFiles(page))

    return (
        <div>
            <div>Всего файлов {count}</div>
            <div
                ref={parentRef}
                className="files"
                style={{
                    height: "45vh",
                    overflow: "auto"
                }}
            >
                {files.map(file => (
                    <FileCard key={file.id} file={file}/>
                ))}

                <div
                    style={{
                        marginLeft: "50%"
                    }}
                >
                    {loading && <Spinner/>}
                </div>

                <div
                    className="w-100"
                    style={{
                        height: 10
                    }}
                    ref={childRef}
                />
            </div>
        </div>

    );
};

export default FileList;