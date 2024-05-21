import React, { useMemo, useState } from "react";
import MaterialReactTable from "material-react-table";
import { userData } from "../../data";
import "./DataGrid.css";
import { createTheme, ThemeProvider } from "@mui/material/styles";
import axios from "axios";

const Pdf = () => {
  const [data, setData] = useState(null);
  const [summary, setSummary] = useState("");
  const [error, setError] = useState(null);
  const [loading, setLoading] = useState(false);
  const [mostSimilarPdf, setMostSimilarPdf] = useState("");

  const theme = useMemo(() =>
    createTheme({
      palette: {
        mode: "dark",
      },
    })
  );

  const handleFileChange = (e) => {
    const file = e.target.files[0];
    setData(file);
  };

  const handleSummarize = async () => {
    setLoading(true);

    const formData = new FormData();
    formData.append("file", data);

    try {
      const response = await axios.post("https://ksp-compare-pdf-0a977fdfdd1e.herokuapp.com/", formData, {
        headers: {
          "Content-Type": "multipart/form-data",
        },
      });
      setSummary(response.data.summary);
    } catch (error) {
      setError(error.response.data.error);
    } finally {
      setLoading(false);
    }
  };

  const handleCompare = async () => {
    setLoading(true);

    const formData = new FormData();
    formData.append("file", data);

    try {
      const response = await axios.post("http://127.0.0.1:5000/compare_pdfs", formData, {
        headers: {
          "Content-Type": "multipart/form-data",
        },
      });
      setMostSimilarPdf(response.data.most_similar_pdf);
    } catch (error) {
      setError(error.response.data.error);
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="table-container">
      <ThemeProvider theme={theme}>
        <div className="w-96 h-32 border border-dashed border-white flex flex-row items-center justify-center px-5">
          <input type="file" accept=".pdf" onChange={handleFileChange} />
        </div>
        <div className="space-x-10">
        <button onClick={handleSummarize} disabled={loading} className="mt-5">
          {loading ? "Loading..." : "Summarize PDF"}
        </button>
        <button onClick={handleCompare} disabled={loading} className="mt-2">
          {loading ? "Loading..." : "Compare PDF"}
        </button>
        </div>
        
        {error && <div className="text-red-500">{error}</div>}
        {summary && <div className="summary">{summary}</div>}
        {mostSimilarPdf && (
          <div className="text-green-500">
            Most similar PDF: {mostSimilarPdf}
          </div>
        )}
      </ThemeProvider>
    </div>
  );
};

export default Pdf;
