import FileUpload from "@ui/FileUpload.tsx";
import FileList from "@ui/FileList.tsx";
import ChoicesFile from "@ui/ChoicesFile.tsx";

export function HomePage() {
    return (
        <>
            <div>
                <div className="mt-4"><FileUpload/></div>
                <div className="mt-4"><FileList/></div>
                <div className="mt-4"><ChoicesFile/></div>
            </div>
        </>
    );
}
