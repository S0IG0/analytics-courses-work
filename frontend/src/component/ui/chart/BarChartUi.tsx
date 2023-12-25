import {Bar, BarChart, CartesianGrid, Cell, Legend, Tooltip, XAxis, YAxis} from "recharts";
import {Slider} from "@mui/joy";
import {useState} from "react";


interface Props {
    data: any[],
}

const BarChartUi = ({data}: Props) => {

    const [lightness, setLightness] = useState(51);
    const [saturation, setSaturation] = useState(42)

    return (
        <div>
            <div className="control-panel mt-4">
                Яркость
                <Slider max={100} value={lightness} valueLabelDisplay="on"
                        onChange={(_, value) => setLightness(value as number)}/>
                Насыщенность
                <Slider max={100} value={saturation} valueLabelDisplay="on"
                        onChange={(_, value) => setSaturation(value as number)}/>
            </div>

            <BarChart
                width={1600}
                height={data.length * 50 + 50}
                data={data}
                margin={{
                    top: 5,
                    right: 30,
                    left: 20,
                    bottom: 5
                }}
                layout={"vertical"}
            >
                <CartesianGrid strokeDasharray="3 3"/>
                <XAxis type="number"/>
                <YAxis dataKey="name" type="category" width={400} interval={0} fontSize={10}/>
                <Tooltip/>
                <Legend/>
                <Bar dataKey="value" fill="#8884d8">
                    {data.map((entry, index) => {
                        const hue = data.length * 360 + entry.value; // Равномерное распределение цветов по кругу
                        // const lightness = 50; // Яркость
                        // const saturation = 100; // Насыщенность

                        return <Cell fill={`hsl(${hue},${saturation}%,${lightness}%)`} key={index}/>;
                    })}
                </Bar>
            </BarChart>
        </div>

    );
};

export default BarChartUi;