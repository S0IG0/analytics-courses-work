import {store} from "@store/store.ts";
import {observer} from "mobx-react-lite";

const ChoicesFile = () => {

    const file = store.file;

    return (
        <div className="mt-4">
            <button
                disabled={file === null}
                className="btn btn-danger mb-2"
                onClick={() => store.file = null}
            >
                {file ? "Выбрать дургой" : "Файл не выбран"}
            </button>
            {file && (
                <div className="card" key={file.id}>
                    <div className="card-header">
                        Выбранный файл
                    </div>
                    <div className="card-body">
                        <h5 className="card-title">{file.file}</h5>
                    </div>
                </div>
            )}
        </div>
    );
};

export default observer(ChoicesFile);