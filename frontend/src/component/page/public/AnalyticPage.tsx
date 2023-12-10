import {useParams} from "react-router-dom";
import $api from "@api/http";
import {useState} from "react";
import {Task} from "@model/response";
import {motion} from "framer-motion";

const AnalyticPage = () => {
    const {id} = useParams();
    const [task, setTask] = useState<Task | null>(null);
    $api.get<Task>(`/task/${id}`).then((response) => setTask(response.data));

    return (
        <div >

            {task && task.files.map((image, index) => (
                <div className="card"
                    style={{
                        marginBottom: "15px"
                    }}
                >
                    <div className="card-header">
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

                                width: "90%"
                            }}
                            src={image.file}
                            alt="График"
                            className="m-5"
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
        </div>
    );
};

export default AnalyticPage;