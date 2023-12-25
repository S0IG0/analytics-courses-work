import {ChangeEvent, FormEvent, useRef, useState} from "react";
import $api from "@api/http";
import {Spinner} from "@ux/loader/Spinner.tsx";
import {Alert, Snackbar} from "@mui/material";

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
        setError(false);
        $api.post('/upload/', {
            file: selectedFile,
        }, {
            headers: {
                'Content-Type': 'multipart/form-data'
            }
        })
            .finally(() => {
                setLoading(false);
                setSelectedFile(null);
                if (input.current) {
                    input.current.value = '';
                }
                setIsOpen(true);
            })
            .catch(() => setError(true));
    }


    const [isOpen, setIsOpen] = useState(false);
    const [error, setError] = useState(false)
    return (
        <>
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
            <Snackbar
                open={isOpen}
                autoHideDuration={2000}
                onClose={() => setIsOpen(false)}
            >
                <Alert onClose={() => setIsOpen(false)} severity={error ? "error" : "success"} sx={{width: '100%'}}>
                    {error ? "Ошибка загрузки файла" : "Файл успешно загружен"}
                </Alert>
            </Snackbar>
        </>
    );
};

export default FileUpload;