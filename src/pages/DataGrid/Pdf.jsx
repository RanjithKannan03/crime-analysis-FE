import React, { useMemo } from 'react'
import MaterialReactTable from "material-react-table";
import { userData } from '../../data';
import './DataGrid.css'
import { createTheme, ThemeProvider } from '@mui/material/styles';

const Pdf = () => {

   
    const theme = useMemo(
        () => createTheme({
            palette: {
                mode: "dark"
            }
        })
    )

    return (
        <div className="table-container">
            <ThemeProvider theme={theme}>
                    <input type="file" accept=".pdf"/>
                   
            </ThemeProvider>
            <div className='text-yellow-400'>
                helo navane
            </div>
        </div>
    )
}

export default Pdf