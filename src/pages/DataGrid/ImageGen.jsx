import React, { useMemo, useState } from "react";
import MaterialReactTable from "material-react-table";
import { userData } from "../../data";
import "./DataGrid.css";
import { createTheme, ThemeProvider } from "@mui/material/styles";
import Axios from "axios";
import LoaderComp from "../../components/loader";

const Pdf = () => {
  const [prompt, setPrompt] = useState("");
  const [url, setUrl] = useState("");
  const [isLoading, setIsLoading] = useState(false);

  const theme = useMemo(() =>
    createTheme({
      palette: {
        mode: "dark",
      },
    })
  );

  async function handleSubmit() {
    setIsLoading(true);
    const formData = new FormData();
    formData.append("prompt", prompt);
    try {
      const response = await Axios.post(
        "https://ksp-image-gen-4968f595cb74.herokuapp.com/",
        formData,
        {
          headers: {
            "Content-Type": "application/json",
          },
        }
      );
      const result = response.data;
      setUrl(result.data[0].asset_url);
      setIsLoading(false);
    } catch (e) {
      console.log(e);
     
    }
  }

  return (
    <div className="table-container">
      <ThemeProvider theme={theme}>
        <div className="w-full flex justify-center items-center p-4 mt-8">
          <div className="flex justify-center items-start w-full space-x-4">
            <div className="flex flex-col justify-center w-full space-y-5">
              <h1 className="text-white text-4xl font-semibold">
                Enter Description
              </h1>
              <textarea
                value={prompt}
                onChange={(e) => {
                  setPrompt(e.target.value);
                }}
                className="bg-transparent rounded-lg w-full focus:outline-none border-white border-solid p-4 border-2"
              />
              <div className="flex w-full justify-center items-center">
                <button
                  className="text-white border-white rounded-lg border-2 border-solid p-2"
                  type="button"
                  onClick={handleSubmit}
                >
                  Generate
                </button>
              </div>
            </div>

            <div className="flex justify-center items-center w-full h-[500px]">
              {isLoading ? (
                <LoaderComp />
              ) : (
                <img
                  src={url}
                  className={`${
                    url === "" ? "hidden" : "block"
                  } max-h-[100%] max-w-[100%]`}
                />
              )}
            </div>
          </div>
        </div>
      </ThemeProvider>
    </div>
  );
};

export default Pdf;
