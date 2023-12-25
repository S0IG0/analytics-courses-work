import Box from '@mui/material/Box';
import { DataGrid } from '@mui/x-data-grid';
import { useDemoData } from '@mui/x-data-grid-generator';

export default function SxProp() {
    const { data } = useDemoData({
        dataSet: 'Commodity',
        rowLength: 20,
        maxColumns: 5,
    });


    console.log(data)

    return (
        <Box sx={{ height: 300, width: '100%' }}>
            <DataGrid
                {...data}
            />
        </Box>
    );
}