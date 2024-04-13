import React, { useMemo, useState } from "react";
import MaterialReactTable from "material-react-table";
import { userData } from "../../data";
import "./DataGrid.css";
import { createTheme, ThemeProvider } from "@mui/material/styles";

const Pdf = () => {
    const [data, setData] = useState(null);
    
  const theme = useMemo(() =>
    createTheme({
      palette: {
        mode: "dark",
      },
    })
  );

  const handleFileChange = (e) => {
    const file = e.target.files[0];
   
    setData(e.target.files[0]);
    console.log(file);
   
  };
  return (
    <div className="table-container">
      <ThemeProvider theme={theme}>
        <input type="file" onChange={handleFileChange} />
        <div className="text-yellow-400">Please Upload the PDF file !</div>
      </ThemeProvider>
    </div>
  );
};

export default Pdf;
