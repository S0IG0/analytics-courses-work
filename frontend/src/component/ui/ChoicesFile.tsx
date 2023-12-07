import { store } from "@store/store.ts";
import { motion } from "framer-motion";
import { observer } from "mobx-react-lite";

const FileChoices = () => {
    const file = store.file;

    return (
        <div className="">
            <button
                disabled={file === null}
                className="btn btn-danger mb-2"
                onClick={() => (store.file = null)}
            >
                {file ? "Выбрать другой" : "Файл не выбран"}
            </button>
            {file && (
                <motion.div
                    className="card"
                    key={file.id}
                    initial={{ scale: 0 }}
                    animate={{ scale: 1 }}
                    exit={{ scale: 0 }} // Exit animation
                    transition={{
                        type: "tween",
                    }}
                >
                    <div className="card-header">Выбранный файл</div>
                    <div className="card-body">
                        <h5 className="card-title">{file.file}</h5>
                    </div>
                </motion.div>
            )}
        </div>
    );
};

export default observer(FileChoices);
