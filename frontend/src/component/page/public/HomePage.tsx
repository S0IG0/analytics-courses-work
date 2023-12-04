import FileUpload from "@ui/FileUpload.tsx";
import FileList from "@ui/FileList.tsx";
import ChoicesFile from "@ui/ChoicesFile.tsx";

export function HomePage() {
    return (
        <>
            <FileUpload/>
            <FileList/>
            <ChoicesFile/>
        </>
    );
}
