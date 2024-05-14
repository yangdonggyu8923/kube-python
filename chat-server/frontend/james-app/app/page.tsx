"use client";
//import Input from '@mui/joy/Input';
import { useForm, SubmitHandler } from "react-hook-form"
import * as React from 'react';
import { useState } from "react";
import AutoAwesomeIcon from '@mui/icons-material/AutoAwesome';
import TelegramIcon from '@mui/icons-material/Telegram';
import { text } from "stream/consumers";
import ShareIcon from '@mui/icons-material/Share';
import ThumbUpOffAltIcon from '@mui/icons-material/ThumbUpOffAlt';
import ThumbDownOffAltIcon from '@mui/icons-material/ThumbDownOffAlt';
import ContentCopyIcon from '@mui/icons-material/ContentCopy';
type Inputs = {
  question: string
  exampleRequired?: string
}
export default function Home() {
  const [message, setMessage] = useState('')
  const {
    register,
    handleSubmit,
    watch,
    formState: { errors },
  } = useForm<Inputs>()
  const onSubmit: SubmitHandler<Inputs> = (data: any) => {
    console.log('입력된 값 : ' + JSON.stringify(data))
    fetch('http://localhost:8000/api/chat/titanic', {
        method: "POST",
        headers: {
            "Content-Type": "application/json",
        },
        body: JSON.stringify(data),
    })
        .then((response) => response.json()) // JSON 형식으로 파싱
        .then((data) => setMessage(data.answer)) // 파싱된 데이터 콘솔 출력
        .catch((error) => console.log("error:", error));
}

  return (
    <>
      <div className="bg-blue-100 p-5 h-[100%] @apply flex rounded-3xl border-double border-8 border-blue-300">
        <div className="flex flex-col border-8 border-double rounded-3xl bg-white
        @apply h-full w-full">
          <div className="flex justify-center">
            <AutoAwesomeIcon className="text-3xl text-blue-500 m-5" />
            <h1 className="text-3xl font-extrabold text-blue-500 my-5">James LLM</h1>
          </div>
          <form onSubmit={handleSubmit(onSubmit)} id="chat" className="flex justify-center items-end mx-5">
            {message? <div className="flex flex-col w-full">
              <h4 className="h-full bg-slate-50 mx-3 rounded-2xl text-semibold text-xl p-5">{message ? message : ""}</h4>
            <div className="flex-row">
            <ContentCopyIcon className="text-slate-400 ml-4 mt-3 h-7 w-7"/>
            <ShareIcon className="text-slate-400 ml-4 mt-3 h-6 w-6"/>
            </div>
            </div> : null}
            <div className="flex flex-row h-auto @apply w-[470px] resize-y my-10 mx-2 scrollbar-hide
             fixed bottom-20">
              <textarea
                {...register("question", { required: true })}
                className="flex items-center rounded-l-2xl bg-blue-50 border-0 w-full h-auto min-h-16 max-h-48 resize-y overflow-y-auto p-5 text-xl scrollbar-hide outline-none"
                placeholder="여기에 프롬프트 입력"
              />
              <input className=" rounded-r-2xl bg-blue-500 text-white text-xl h-auto min-h-16 max-h-32 w-24 hover:bg-blue-400 hover:transition-shadow"
                type="submit"
                value="Send" />
            </div>
            {/* {data.status === 'failure' && (
          <FormHelperText
            sx={(theme) => ({ color: theme.vars.palette.danger[400] })}
          >
            Oops! something went wrong, please try again later.
          </FormHelperText>
        )}
        {data.status === 'sent' && (
          <FormHelperText
            sx={(theme) => ({ color: theme.vars.palette.primary[400] })}
          >
            You are all set!
          </FormHelperText>
        )} */}
          </form>
        </div>
      </div>
    </>
  );
}