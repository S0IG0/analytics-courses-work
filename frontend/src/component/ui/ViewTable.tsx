import {useRef, useState} from "react";
import $api from "@api/http";
import {ResponsePagination} from "@model/response";
import useScroll from "@hook/useScroll.tsx";
import {store} from "@store/store.ts";


const ViewTable = () => {
    const [data, setData] = useState<any[]>([])
    const [page, setPage] = useState<number | null>(1)

    const fetchData = () => {
        $api.get<ResponsePagination>(`/macaroni/?page=${page}&&file=${store.file?.id}`)
            .then(response => {
                setData(prevState => {
                    if (page === 1 && prevState.length !== 0) {
                        return prevState
                    }
                    return [...prevState, ...response.data.results]
                })
                if (response.data.next) {
                    // @ts-ignore
                    setPage(prevState => prevState + 1)
                } else {
                    setPage(null);
                }
            })
            .catch(() => setPage(null))
    }


    const parentRef = useRef<HTMLDivElement | null>(null)
    const childRef = useRef<HTMLDivElement | null>(null)
    useScroll(parentRef, childRef, () => fetchData())


    return (
        <div>
            <div
                ref={parentRef}
                className="table-responsive"
                style={{maxHeight: "30em"}}

            >
                <table className="table table-striped table-hover">
                    {data.length > 0 && (
                        <>
                            <thead>
                            <tr>
                                <th scope="col">№</th>
                                {Object.keys(data[0]).map(key => (
                                    <th scope="col" key={key}>{key}</th>
                                ))}
                            </tr>
                            </thead>
                            <tbody>
                            {data.map((row, index) => (
                                <tr
                                    key={row['id']}
                                >
                                    <th scope="row">{index + 1}</th>
                                    {Object.values(row).map(item => (
                                        <td className="text-nowrap">
                                            {/*@ts-ignore*/}
                                            {!item || item === "<..>" ? "NULL" : item}
                                        </td>
                                    ))}
                                </tr>
                            ))}
                            </tbody>
                        </>
                    )}

                </table>
                <div
                    className="w-100"
                    style={{
                        height: 60,
                    }}
                    ref={childRef}
                />
            </div>
        </div>
    );
};

export default ViewTable;