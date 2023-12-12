import {ChangeEvent, FormEvent, useRef, useState} from "react";
import $api from "@api/http";
import {Spinner} from "@ux/loader/Spinner.tsx";

const FileUpload = () => {
    const [selectedFile, setSelectedFile] = useState<File | null>(null);
    const [loading, setLoading] = useState(false)
    const input = useRef<HTMLInputElement>(null)
    const changeFile = (event: ChangeEvent<HTMLInputElement>) => {
        const files = event.target.files;
        if (files && files[0]) {
            setSelectedFile(files[0]);
        }
    }

    const upload = (event: FormEvent) => {
        event.preventDefault()
        setLoading(true);
        $api.post('/upload/', {
            file: selectedFile,
        }, {
            headers: {
                'Content-Type': 'multipart/form-data'
            }
        }).finally(() => {
            setLoading(false);
            setSelectedFile(null);
            if (input.current) {
                input.current.value = '';
            }
        })
    }

    return (
        <form
            onSubmit={upload}
            encType="multipart/form-d"
        >
            <input
                className="form-control mb-3"
                type="file"
                accept=".csv"
                ref={input}
                onChange={changeFile}
            />
            <button
                type="submit"
                className="btn btn-primary"
                disabled={selectedFile === null}
            >
                {loading ? <Spinner/> : "Загрузить"}
            </button>
        </form>
    );
};

export default FileUpload;