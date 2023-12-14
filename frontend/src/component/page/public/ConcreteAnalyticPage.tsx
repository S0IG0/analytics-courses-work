import {useParams} from "react-router-dom";
import $api from "@api/http";
import {useEffect, useRef, useState} from "react";
import {Task} from "@model/response";
import {motion} from "framer-motion";
import useScroll from "../../hook/useScroll";
import {ResponsePagination} from "../../model/response";

const AnalyticPage = () => {
    const {id} = useParams();
    const [task, setTask] = useState<Task | null>(null);

    useEffect(() => {
        $api.get<Task>(`/task/${id}`).then((response) => setTask(response.data));
    }, []);

    const [data, setData] = useState<any[]>([])
    const [page, setPage] = useState<number | null>(1)

    const fetchData = () => {
        $api.get<ResponsePagination>(`supplies/?page=${page}&task=${id}`)
            .then(response => {
                setData(prevState => {
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
    }


    const parentRef = useRef<HTMLDivElement | null>(null)
    const childRef = useRef<HTMLDivElement | null>(null)
    useScroll(parentRef, childRef, () => fetchData())

    const display = (item) => {
        if (typeof item === 'string') {
            return item
        } else if (String(item).indexOf(".") === -1) {
            return item
        }
        return Number(item).toFixed(2)
    }

    return (
        <div>

            {task && task.files.map((image, index) => (
                <div className="card"
                     style={{
                         marginBottom: "15px"
                     }}
                >
                    <h5 className="card-header">
                        {image.title}
                    </h5>
                    <div className="card-body">
                        {image.description}
                    </div>
                    <div className="card-body"
                         style={{
                             height: "45vh",
                             overflow: "auto"
                         }}
                    >

                        <motion.img
                            style={{
                                width: "90%",
                                margin: "0px"
                            }}
                            src={image.file}
                            alt="График"
                            // className="m-5"
                            initial={{x: index % 2 === 0 ? -400 : 400, opacity: 0}}
                            animate={{x: 0, opacity: 1}}
                            transition={{
                                type: "spring",
                                duration: 1.2
                            }}
                        />

                    </div>
                </div>
            ))}
            {task?.delivery && (
                <div>
                    <div
                        ref={parentRef}
                        className="table-responsive"
                        style={{maxHeight: "30em"}}

                    >
                        <table className="table table-striped table-hover">
                            {data.length > 0 && (
                                <>
                                    <thead>
                                    <tr>
                                        <th scope="col">№</th>
                                        {Object.keys(data[0]).map(key => (
                                            <th scope="col" key={key}>{key}</th>
                                        ))}
                                    </tr>
                                    </thead>
                                    <tbody>
                                    {data.map((row, index) => (
                                        <tr
                                            key={row['id']}
                                        >
                                            <th scope="row">{index + 1}</th>
                                            {Object.values(row).map(item => (
                                                <td className="text-nowrap">
                                                    {display(item)}
                                                </td>
                                            ))}
                                        </tr>
                                    ))}
                                    </tbody>
                                </>
                            )}

                        </table>
                        <div
                            className="w-100"
                            style={{
                                height: 60,
                            }}
                            ref={childRef}
                        />
                    </div>
                </div>
            )}
        </div>
    );
};

export default AnalyticPage;