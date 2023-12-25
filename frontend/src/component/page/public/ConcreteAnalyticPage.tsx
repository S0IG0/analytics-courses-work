import {useEffect, useRef, useState} from "react";
import {Graph, ResponsePagination, Task} from "@model/response";
import $api from "@api/http";
import {useParams} from "react-router-dom";
import BarChartUi from "@ui/chart/BarChartUi.tsx";
import SelectedUi from "@ui/SelectedUi.tsx";
import useScroll from "@hook/useScroll.tsx";
import LineChartUi from "@ui/chart/LineChartUi.tsx";
import PieChartUi from "@ui/chart/PieChartUi.tsx";


interface Props {
    graph: Graph
}

const Test = ({graph}: Props) => {
    const options = graph.y_axis;
    const [selected, setSelected] = useState<any[]>([])
    const data = graph.x_axis
        .filter((_value, index) => selected.includes(String(index)))
        .map((item, index) => {
            return {
                name: graph.y_axis[index],
                value: item,
            }
        });

    useEffect(() => {
        setSelected(
            [...Array.from(
                Array(options.length >= 10 ? 10 : options.length
                ).keys())
            ].map(item => String(item))
        )
    }, []);

    return (
        <div>
            <SelectedUi options={options} setSelected={setSelected} selected={selected}/>
            <BarChartUi data={data}/>
        </div>
    );
};


const Test1 = ({graph}: Props) => {
    const options = [...new Set(graph.y_axis.map(item => item["Наименование товара"]))];
    const [selected, setSelected] = useState<any[]>([])
    useEffect(() => {
        setSelected(
            [...Array.from(
                Array(options.length >= 10 ? 10 : options.length
                ).keys())
            ].map(item => String(item))
        )
    }, []);


    const graph_data = graph.y_axis.map((value) => value)

    let data = graph_data.map(((_value, index_dataset) => (
        graph_data[index_dataset]["дата"]
            // @ts-ignore
            .map((item, index) => {
                return {
                    "дата": item,
                    "Количество": graph_data[index_dataset]["Количество"][index],
                    "Наименование товара": graph_data[index_dataset]["Наименование товара"],
                    "dataset": index_dataset,
                }
            })
    )))


    for (let i = 0; i < data.length; i++) {
        // @ts-ignore
        const dates = data[i].map(value => value["дата"])
        for (const date of graph.x_axis) {
            if (!dates.includes(date)) {

                data[i].push({
                    "дата": date,
                    // @ts-ignore
                    "Количество": null,
                    "Наименование товара": "",
                    "dataset": 0,
                })
            }
        }
        // @ts-ignore
        data[i].sort((a, b) =>
            new Date(a["дата"]).getTime() - new Date(b["дата"]).getTime()
        )
    }


    data = data.filter(items => {
        // @ts-ignore
        items = items.filter(value => value["Наименование товара"] !== "")
        const item = items[0];
        return selected.map(index => options[Number(index)]).includes(item["Наименование товара"])
    })


    return (
        <div>
            <SelectedUi options={options} setSelected={setSelected} selected={selected}/>
            <LineChartUi data={data}/>
        </div>
    );
};


const Test2 = ({graph}: Props) => {

    const data = graph.x_axis.map((value, index) => {
        return {
            name: value,
            value: graph.y_axis[index],
        }
    })

    return (
        <div>
            <PieChartUi data={data}/>
        </div>
    );
};


const AnalyticPage = () => {
    const {id} = useParams();
    const [task, setTask] = useState<Task | null>(null)

    useEffect(() => {
        $api.get<Task>(`/task/${id}`)
            .then(response => setTask(response.data))
    }, []);

    const [data, setData] = useState<any[]>([])
    const [page, setPage] = useState<number | null>(1)

    const fetchData = () => {
        $api.get<ResponsePagination>(`supplies/?page=${page}&task=${id}`)
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

    const display = (item: any) => {
        if (typeof item === 'string') {
            return item
        }
        return Number(item).toFixed(2)
    }

    let text1 = null;
    let text2 = null;

    if (task?.text) {
        const text = task.text.split(";");
        text1 = text[0]
        text2 = text[1]
    }

    return (
        <>
            {task?.delivery && (
                <div className="mb-4">
                    <h1>Запланированные поставки</h1>
                    <p>Ниже вы можете наблюдать сформированные под ваши данные поставки, которые опираются на удовлетворение 95% спроса посетителей.</p>
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
                                                    {display(item)}
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
            )}

            {text2 && (
                <>
                    <h2>Рассчитанные метрики</h2>
                    <div className="mb-4">
                        {text2.split("\n").map(text => (
                            <div>
                                {text}
                            </div>
                        ))}
                    </div>
                </>
            )}

            {task && (
                <>
                    {text1 && (
                        <>
                            <h1>Метод априори, планирование расстановки продуктов</h1>
                            <p>Данный метод блаблаблалаб</p>
                        </>
                    )}

                    {task.graphs.map(graph => (
                        <div className="card"
                             key={graph.id}
                             style={{
                                 marginBottom: "15px"
                             }}
                        >
                            <h5 className="card-header">
                                {graph.title}
                            </h5>
                            <div className="card-body">
                                {graph.description}
                            </div>
                            <div className="card-body"
                                 style={{
                                     overflow: "auto"
                                 }}
                            >
                                {graph.type_graph === "bar" && <Test key={graph.id} graph={graph}/>}
                                {graph.type_graph === "line" && <Test1 key={graph.id} graph={graph}/>}
                                {graph.type_graph === "pie" && <Test2 key={graph.id} graph={graph}/>}

                            </div>
                        </div>
                    ))}

                    {text1 && (
                        <div style={{
                            height: "300px",
                            overflow: "auto"
                        }}>
                            {text1.split("\n").map(text => (
                                <div>
                                    {text}
                                </div>
                            ))}
                        </div>
                    )}

                    {task.files.map(file => (
                        <div className="card"
                             key={file.id}
                             style={{
                                 marginBottom: "15px"
                             }}
                        >
                            <h5 className="card-header">
                                {file.title}
                            </h5>
                            <div className="card-body">
                                {file.description}
                            </div>
                            <div className="card-body"
                                 style={{
                                     overflow: "auto"
                                 }}
                            >
                                <img src={file.file} alt={file.name}/>
                            </div>
                        </div>
                    ))}
                </>
            )}
        </>
    );
};

export default AnalyticPage;