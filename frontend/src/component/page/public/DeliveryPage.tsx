import ChoicesFile from "@ui/ChoicesFile.tsx";
import $api from "@api/http";
import {store} from "@store/store.ts";
import {useState, useEffect} from "react";
import {Task} from "@model/response";
import {useNavigate} from "react-router-dom";
import {motion} from "framer-motion";
import TaskList from "@ui/TaskList.tsx";
import FileList from "@ui/FileList.tsx";
import {state} from "@page/public/AnalyticPage.tsx";


const DeliveryPage = () => {
    const [task, setTask] = useState<Task | null>(null);

    useEffect(() => {
        const intervalId = setInterval(() => {
            if (task !== null && task.status !== "complete") {
                checkTask();
            }
        }, 1000);
        return () => clearInterval(intervalId);
    }, [task]);

    function createTask() {
        if (store.file === null) return;

        $api
            .post<Task>("/analytic/", {
                file_id: store.file.id,
                delivery: true,
            })
            .then((response) => {
                setTask(response.data);
            });
    }

    function checkTask() {
        if (task === null || task.status === "complete") return;
        console.log("checkTask");
        $api.get<Task>(`/task/${task.id}`).then((response) => setTask(response.data));
    }

    const navigate = useNavigate();
    return (
        <div>
            <FileList/>
            <div className="mt-4"><ChoicesFile/></div>
            <button className="btn btn-primary mt-4" onClick={createTask}>
                Создать заявку на планирование поставки
            </button>
            <div className="mt-4">
                {task && (
                    <motion.div
                        key={task.id}
                        initial={{scale: 0, rotate: 180}}
                        animate={{rotate: 360, scale: 1}}
                        transition={{
                            type: "spring",
                            stiffness: 260,
                            damping: 20,
                        }}
                        className="card"
                        style={{
                            width: 350,
                        }}
                    >
                        <div className="card-header">
                            Заявка №{task.id}
                            <motion.div
                                key={task.status}
                                initial={{scale: 0}}
                                animate={{scale: 1}}
                                transition={{
                                    type: "spring",
                                    stiffness: 260,
                                    damping: 20,
                                }}
                            >
                                {/*@ts-ignore*/}
                                <span className={`badge bg-${state[task.status].style}-subtle border border-${state[task.status].style}-subtle text-${state[task.status].style}-emphasis rounded-pill`}>
                                    {/*@ts-ignore*/}
                                    {state[task.status].name}
                                </span>
                            </motion.div>

                        </div>
                        <div className="card-body">
                            <motion.button
                                key={Number(task.status !== "complete")}

                                initial={{scale: 1}}
                                animate={{scale: 1.1}}
                                transition={{
                                    type: "tween",
                                }}

                                onClick={() => navigate(`/аналитика/${task?.id}`)}
                                disabled={task.status !== "complete"}
                                className="btn btn-primary mt-2"
                            >
                                Перейти к поставкам
                            </motion.button>
                        </div>
                    </motion.div>
                )}
            </div>
            <div className="w-100 border-top mt-2 mb-2"/>

            <h5>Заявки</h5>
            <TaskList delivery={true}/>
        </div>
    );
};

export default DeliveryPage;
