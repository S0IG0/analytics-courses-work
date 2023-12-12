import {useRef, useState} from "react";
import {TaskShort, TasksResponse} from "@model/response";
import $api from "@api/http";
import useScroll from "@hook/useScroll.tsx";
import {motion} from "framer-motion";
import {Spinner} from "@ux/loader/Spinner.tsx";
import {Link} from "react-router-dom";
import {state} from "@page/public/AnalyticPage.tsx";

const TaskList = () => {
    const [tasks, setTasks] = useState<TaskShort[]>([])
    const [page, setPage] = useState<number | null>(1)
    const [loading, setLoading] = useState(false)

    const fetchTasks = () => {
        if (page === null || loading) return

        setLoading(true)
        $api.get<TasksResponse>(`/tasks/?page=${page}`)
            .then(response => {
                setTasks(prevState => {
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
    useScroll(parentRef, childRef, () => fetchTasks())

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
            <motion.div
                initial="hidden"
                animate="visible"
                variants={list}
                ref={parentRef}
                className="files"
                style={{
                    height: "60vh",
                    overflow: "auto"
                }}
            >
                {tasks.map(task => (
                    <motion.div
                        key={task.id}
                        transition={{
                            duration: 0.6,
                            delay: 0.2,
                        }}
                        variants={item}
                    >

                        <div
                            key={task.id}
                            className="card mb-4"
                            style={{
                                width: 350,
                            }}
                        >
                            <div className="card-header">
                                Заявка №{task.id}
                                <div>
                                    {/*@ts-ignore*/}
                                    <span className={`badge bg-${state[task.status].style}-subtle border border-${state[task.status].style}-subtle text-${state[task.status].style}-emphasis rounded-pill`}>
                                    {/*@ts-ignore*/}
                                        {state[task.status].name}
                                </span>
                                </div>

                            </div>
                            <div className="card-body">
                                <Link
                                    to={`/analytic/${task?.id}`}
                                    className="btn btn-primary mt-2"
                                >
                                    Перейти к аналитике
                                </Link>
                            </div>
                        </div>

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
                        height: 30,
                    }}

                    ref={childRef}
                />
            </motion.div>
        </div>
    );
};

export default TaskList;