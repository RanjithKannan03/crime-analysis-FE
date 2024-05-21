import React, { useMemo, useState } from "react";
import MaterialReactTable from "material-react-table";
import { userData } from "../../data";
import "./DataGrid.css";
import { createTheme, ThemeProvider } from "@mui/material/styles";
import Axios from "axios";
import LoaderComp from "../../components/loader";


const Chat = () => {

    const [title,setTitle]=useState("");
    const [content,setContent]=useState("");
    const [messages,setMessages]=useState([]);
    const [newMessage,setNewMessage]=useState("");
    const [isLoading,setIsLoading]=useState(false);

    const theme = useMemo(() =>
    createTheme({
      palette: {
        mode: "dark",
      },
    })
  );

  async function handleSubmit()
  {
    setIsLoading(true);
    const formData=new FormData();
    const data={
        title:title,
        content:content
    };
    formData.append('data',JSON.stringify(data));
    try{
        const result=await Axios.post('https://ksp-chat-cef919796c2f.herokuapp.com/set_data',formData,{
            headers:{
                "Content-Type": "application/json",
            }
        })
        console.log(result);
        if(result.status===200)
        {
            setIsLoading(false);
        }
    }
    catch(e)
    {
        console.log(e);
    }
  }

  async function handleChat()
  {
    setMessages((prev)=>{
        return [...prev,{from:"user",message:newMessage}];
    });
    setNewMessage("");
    const formData=new FormData();
    formData.append('question',newMessage);
    try{
        const response= await Axios.post('https://ksp-chat-cef919796c2f.herokuapp.com/ask_question',formData,{
            headers:{
                "Content-Type": "application/json",
            }
        })
        const result=response.data;
        setMessages((prev)=>{
            return [...prev,{from:"bot",message:result.answer}]
        })
    }
    catch(e){
        console.log(e.response.data);
    }
  }

  return (
    <div className="table-container">
      <ThemeProvider theme={theme}>
      <div className="w-full flex justify-center items-center p-4 mt-8">

        <div className="flex justify-center items-start w-full space-x-8">

        <div className="flex flex-col justify-center w-full space-y-5">
        
        <div className="flex flex-col justify-center space-y-2">
        <h1 className="text-white text-4xl font-semibold">Enter Title</h1>
        <input type="text" value={title} onChange={(e)=>{setTitle(e.target.value)}} className="bg-transparent rounded-lg w-full focus:outline-none border-white border-solid p-4 border-2"/>

        </div>

        <div className="flex flex-col justify-center space-y-2">
        <h1 className="text-white text-4xl font-semibold">Enter Content</h1>
        <textarea value={content} onChange={(e)=>{setContent(e.target.value)}} className="bg-transparent rounded-lg w-full focus:outline-none border-white border-solid p-4 border-2"/>
        </div>

        <div className="flex w-full justify-center items-center">
        <button className="text-white border-white rounded-lg border-2 border-solid p-2" type="button" onClick={handleSubmit}>Submit</button>
        </div>
        </div>

        <div className="flex justify-center items-center w-full h-[500px] border-white border-2 border-solid">


        {isLoading?<LoaderComp/>: <div className="flex flex-col justify-around space-y-2 h-full w-full p-4">

                <div className="w-full h-[85%] flex flex-col space-y-4 overflow-y-scroll px-4">
                {messages.map((message,index)=>{
                    return(
                        <div key={index} className={`flex flex-col w-full space-y-2 ${message.from==="user"?"items-end":"items-start"}`}>
                        <p className="text-white font-extralight text-sm">{message.from}</p>
                        <p className="text-white font-normal text-base">{message.message}</p>
                        </div>
                    );
                })}
                </div>

                <div className="flex justify-between items-center w-full">
                <textarea type="text" className="focus:outline-none w-full rounded-lg bg-transparent border-white border-solid border-2 p-2" value={newMessage} onChange={(e)=>{setNewMessage(e.target.value)}}/>
                <button className="text-white border-white p-2" onClick={handleChat}>Chat</button>
                </div>

                </div>
                
                
                }

       

        </div>

        </div>

        </div>
      </ThemeProvider>
    </div>
  )
}

export default Chat
