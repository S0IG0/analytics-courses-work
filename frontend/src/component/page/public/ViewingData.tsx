import ViewTable from "@ui/ViewTable.tsx";
import ChoicesFile from "@ui/ChoicesFile.tsx";
import FileList from "@ui/FileList.tsx";
import {store} from "@store/store.ts";
import {observer} from "mobx-react-lite";


const ViewingData = () => {
    return (
        <div>
            <FileList/>
            <div className="mb-4 mt-4">
                <ChoicesFile/>
            </div>
            {store.file && (
                <ViewTable/>
            )}
        </div>
    );
};

export default observer(ViewingData);