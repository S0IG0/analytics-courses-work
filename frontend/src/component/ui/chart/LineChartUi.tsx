import React from "react";
import {
    XAxis,
    YAxis,
    CartesianGrid,
    Tooltip,
    Legend,
    LineChart,
    Line,
} from "recharts";

interface Props {
    data: any[]
}

const LineChartUi = ({data}: Props) => {
    console.log(data.map(items => items.length))
    return (
        <div>
            <LineChart
                width={2000}
                height={800}
                margin={{
                    top: 5,
                    right: 30,
                    left: 20,
                    bottom: 5,
                }}
            >
                <CartesianGrid strokeDasharray="3 3"/>
                <XAxis
                    type="category"
                    allowDuplicatedCategory={false}
                    dataKey="дата"
                    minTickGap={30}
                />

                <Tooltip/>
                <Legend/>

                {data.map((dataset, index) => (
                    <React.Fragment key={index}>
                        <Line
                            connectNulls
                            data={dataset}
                            type="monotone"
                            dataKey="Количество"
                            name={dataset[0]["Наименование товара"]}
                            stroke={`rgba(${Math.floor(Math.random() * 256)}, ${Math.floor(Math.random() * 256)}, ${Math.floor(Math.random() * 256)}, 1)`}
                        />
                        <YAxis/>
                    </React.Fragment>

                ))}
            </LineChart>

        </div>
    );
};

export default LineChartUi;