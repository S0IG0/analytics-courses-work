import {useRef, useState} from "react";
import {File, FilesResponse} from "@model/response";
import $api from "@api/http";
import {Spinner} from "@ux/loader/Spinner.tsx";
import useScroll from "@hook/useScroll.tsx";
import FileCard from "@ui/FileCard.tsx";
import {motion} from "framer-motion";


const FileList = () => {

    const [files, setFiles] = useState<File[]>([])
    const [count, setCount] = useState(0)
    const [page, setPage] = useState<number | null>(1)
    const [loading, setLoading] = useState(false)


    const fetchFiles = () => {
        if (page === null) return

        setLoading(true)
        $api.get<FilesResponse>(`/files/?page=${page}&file=csv`)
            .then(response => {
                setCount(response.data.count)
                setFiles(prevState => {
                    if (page === 1 && prevState.length !== 0) {
                        return prevState
                    }
                    return [...prevState, ...response.data.results]
                })
                if (response.data.next) {
                    // @ts-ignore
                    setPage(prevState => prevState + 1)
                } else {
                    setPage(null);
                }
            })
            .catch(() => setPage(null))
            .finally(() => setLoading(false))
    }


    const parentRef = useRef<HTMLDivElement | null>(null)
    const childRef = useRef<HTMLDivElement | null>(null)
    useScroll(parentRef, childRef, () => fetchFiles())

    const list = {
        visible: {opacity: 1},
        hidden: {opacity: 0},
    }

    const item = {
        visible: {opacity: 1, x: 0},
        hidden: {opacity: 0, x: -400},
    }


    return (
        <div>
            <div>Всего файлов {count}</div>
            <motion.div
                initial="hidden"
                animate="visible"
                variants={list}
                ref={parentRef}
                className="files"
                style={{
                    height: "45vh",
                    overflow: "auto"
                }}
            >
                {files.map(file => (
                    <motion.div
                        key={file.id}
                        transition={{
                            duration: 0.6,
                            delay: 0.2,
                        }}
                        variants={item}
                    >
                        <FileCard key={file.id} file={file}/>
                    </motion.div>
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
            </motion.div>
        </div>

    );
};

export default FileList;