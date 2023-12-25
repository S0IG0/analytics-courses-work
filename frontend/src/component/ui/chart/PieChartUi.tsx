import {PieChart, Pie, Cell, Sector} from 'recharts';
import {useState} from "react";
import {Slider} from "@mui/joy";


interface Props {
    data: any
}


// @ts-ignore
const renderActiveShape = (props) => {
    const RADIAN = Math.PI / 180;
    const {cx, cy, midAngle, innerRadius, outerRadius, startAngle, endAngle, fill, payload, percent, value} = props;
    const sin = Math.sin(-RADIAN * midAngle);
    const cos = Math.cos(-RADIAN * midAngle);
    const sx = cx + (outerRadius + 10) * cos;
    const sy = cy + (outerRadius + 10) * sin;
    const mx = cx + (outerRadius + 30) * cos;
    const my = cy + (outerRadius + 30) * sin;
    const ex = mx + (cos >= 0 ? 1 : -1) * 22;
    const ey = my;
    const textAnchor = cos >= 0 ? 'start' : 'end';

    return (
        <g>
            <text x={cx} y={cy} dy={8} textAnchor="middle" fill={fill}>
                {payload.name}
            </text>
            <Sector
                cx={cx}
                cy={cy}
                innerRadius={innerRadius}
                outerRadius={outerRadius}
                startAngle={startAngle}
                endAngle={endAngle}
                fill={fill}
            />
            <Sector
                cx={cx}
                cy={cy}
                startAngle={startAngle}
                endAngle={endAngle}
                innerRadius={outerRadius + 6}
                outerRadius={outerRadius + 10}
                fill={fill}
            />
            <path d={`M${sx},${sy}L${mx},${my}L${ex},${ey}`} stroke={fill} fill="none"/>
            <circle cx={ex} cy={ey} r={2} fill={fill} stroke="none"/>
            <text x={ex + (cos >= 0 ? 1 : -1) * 12} y={ey} textAnchor={textAnchor}
                  fill="#333">{`Значение ${value}`}</text>
            <text x={ex + (cos >= 0 ? 1 : -1) * 12} y={ey} dy={18} textAnchor={textAnchor} fill="#999">
                {`(Rate ${(percent * 100).toFixed(2)}%)`}
            </text>
        </g>
    );
};

const PieChartUi = ({data}: Props) => {

    const [activeIndex, setActiveIndex] = useState(0);
    // @ts-ignore
    const onPieEnter = (_, index) => {
        setActiveIndex(index);
    };

    const [lightness, setLightness] = useState(51);
    const [saturation, setSaturation] = useState(42)


    return (
        <div>
            <div className="control-panel mt-4 w-75">
                Яркость
                <Slider max={100} value={lightness} valueLabelDisplay="on"
                        onChange={(_, value) => setLightness(value as number)}/>
                Насыщенность
                <Slider max={100} value={saturation} valueLabelDisplay="on"
                        onChange={(_, value) => setSaturation(value as number)}/>
            </div>

            <PieChart width={800} height={500}>
                <Pie
                    data={data}
                    dataKey="value"
                    fill="#8884d8"
                    onMouseEnter={onPieEnter}
                    innerRadius={60 * 2.5}
                    outerRadius={80 * 2.5}
                    cx="50%"
                    cy="50%"
                    activeIndex={activeIndex}
                    activeShape={renderActiveShape}
                >
                    {/*@ts-ignore*/}
                    {data.map((entry, index) => {
                        const hue = data.length * 360 + entry.value; // Равномерное распределение цветов по кругу
                        // const lightness = 50; // Яркость
                        // const saturation = 80; // Насыщенность

                        return <Cell fill={`hsl(${hue},${saturation}%,${lightness}%)`} key={index}/>;
                    })}
                </Pie>
            </PieChart>
        </div>
    );
};

export default PieChartUi;