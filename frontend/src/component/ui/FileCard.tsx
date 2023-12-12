import {File} from "@model/response";
import {store} from "@store/store.ts";
import {observer} from "mobx-react-lite";

interface Props {
    file: File
}

const FileCard = ({file}: Props) => {

    const choiceFile = (file: File) => {
        store.file = file;
    }

    return (
        <div className="card mb-2" key={file.id}>
            <div className="card-body">
                <h5 className="card-title">{file.name}</h5>
                <button
                    onClick={() => choiceFile(file)}
                    className="btn btn-primary"
                    disabled={store.file !== null}
                >
                    Выбрать файл
                </button>
            </div>
        </div>
    );
};

export default observer(FileCard);