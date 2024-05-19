"use client";

import AIBots from "@/components/Card/page";
// import AIBot from "@/component/Card/page";
import Image from "next/image";
import Link from "next/link";

// const AibotCard = ({ answer }: { answer?: string }) => {
//   return (
//     <div
//     className={` min-w-96 w-96 md:w-1/2 md:ml-auto md:mr-auto text-gray-200 bg-slate-900 p-4 mt-10 rounded-lg flex justify-center`}
//     >
//       {answer == "" ? "Hello! How can I assist you?" : answer}
//     </div>
//   );
// };

// import { useEffect, useState } from "react";

// const SearchBar = ({ handleSubmit }: { handleSubmit: Function }) => {
//   const [query, setQuery] = useState("");

//   const handleInputChange = (event: React.ChangeEvent<HTMLInputElement>) => {
//     setQuery(event.target.value);
//   };

//   const handleClick = () => {
//     handleSubmit(query);
//   };

//   const handleFormSubmit = (e: React.ChangeEvent<HTMLFormElement>) => {
//     e.preventDefault();
//     handleSubmit(query);
//   };

//   return (
//     <div className="mt-92">
//       <form className="flex w-72 md:w-full " onSubmit={handleFormSubmit}>
//         <input
//           type="text"
//           placeholder="Ask Questions"
//           value={query}
//           onChange={handleInputChange}
//           className="border-none px-2 py-2 text-slate-50  rounded-md focus:outline-none focus:ring focus:border-blue-300 mr-3 bg-slate-900 w-96 text-light-1"
//         />
//         <button
//           type="submit"
//           className="text-white  px-4 py-2 rounded-md hover:bg-blue-600 focus:outline-none focus:ring focus:ring-blue-300"
//           onClick={handleClick}
//         >
//           Ask
//         </button>
//       </form>
//     </div>
//   );
// };



// export function AIBot() {
//   const [prompt, setPrompt] = useState("");
//   const [content, setContent] = useState("");
//   const [loading, setLoading] = useState(false);
//   const handleChange = (newPrompt: string) => {
//     setPrompt(newPrompt);
//   };

//   useEffect(() => {
//     const fetchData = async () => {
//       setLoading(true);
//       if (prompt === "") return;
//       try {
//         const response = await fetch("http://localhost:8000/api/chatbot", {
//           method: "POST",
//           headers: {
//             "Content-Type": "application/json",
//           },
//           body: JSON.stringify({ question: prompt }),
//         });

//         if (!response.ok) {
//           throw new Error(`HTTP error! Status: ${response.status}`);
//         }
//         const data = await response.json();
//         setContent(data.answer);
//       } catch (error) {
//         console.error("There was a problem with the fetch operation:", error);
//       } finally {
//         setLoading(false);
//       }
//     };
//     fetchData();
//     setPrompt("");
//     setContent("");
//   }, [prompt]);

//   return (
//     <div className="">
//       <div className=" mt-40 md:mt-20 mb-2 ">
//         <h1 className="w-full text-center  font-bold text-3xl md:text-5xl md:mb-14">
//           An AI Based Student <span className=" text-indigo-500">Bot</span>
//         </h1>
//       </div>
//       <div className="w-full flex flex-col items-center">
//         <div className="">
//           {loading ? (
//             <AibotCard answer={content} />
//           ) : (
//             <>
//               {content == ""? (
//                 <AibotCard answer={content} />
//               ) : (
//                 <AibotCard answer={content} />
//               )}
//             </>
//           )}
//         </div>
//         <div className="w-full flex flex-col items-center ml-10">
//           <div className="mt-12">
//             <SearchBar handleSubmit={handleChange} />
//           </div>
//         </div>
//       </div>
//     </div>
//   );
// }

export default function Home() {
  return (
    <>
      <div className="mt-10">
        <AIBots />
      </div>
    </>
  );
}
