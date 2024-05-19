"use client";
import { useEffect, useState } from "react";
import React from "react";
import AibotCard from "../AIBot/page";
import SearchBar from "../Search/page";
import { useSelector } from "react-redux";
interface QueAns {
  question: string;
  answer: string;
}
export default function AIBots() {
  const [queAns, setQueAns] = useState<QueAns[]>([]);

  const [prompt, setPrompt] = useState("");
  const searchText = useSelector((state: any) => state.search.searchText);

  useEffect(() => {
    if (searchText) {
      setQueAns((prev) => [...prev, { answer: searchText, question: "" }]);
    }
  }, [searchText]);

  const [loading, setLoading] = useState(false);
  const handleChange = (newPrompt: string) => {
    setPrompt(newPrompt);
  };

  useEffect(() => {
    const fetchData = async () => {
      setLoading(true);
      if (prompt === "") return;

      try {
        const response = await fetch("http://localhost:3000/api/chatbot", {
          method: "POST",
          headers: {
            "Content-Type": "application/json",
          },
          body: JSON.stringify({ question: prompt }),
        });

        if (!response.ok) {
          throw new Error(`HTTP error! Status: ${response.status}`);
        }
        const data = await response.json();
        setQueAns((prev) => [
          ...prev,
          { question: prompt, answer: data.answer || "Something went wrong!" },
        ]);
      } catch (error) {
        console.error("There was a problem with the fetch operation:", error);
      } finally {
        setLoading(false);
      }
    };
    fetchData();
  }, [prompt]);

  return (
    <>
      <div className="w-full flex flex-col items-center pb-20">
        <div className="w-full h-128 rounded-2xl overflow-y-auto pb-10">
          {queAns.length === 0 ? (
            <div className="w-fit ml-4 text-gray-200 bg-slate-900 p-4 mt-10 rounded-r-xl rounded-b-xl flex text-left">
              Search for the answer
            </div>
          ) : (
            <>
              {queAns.map((item, index) => (
                <div key={index}>
                  {item?.question !== "" && (
                    <div className="w-full flex justify-end">
                      <div className="w-2/3 mr-4 text-gray-200 bg-slate-900 p-4 mt-3 rounded-l-xl rounded-b-xl flex text-right">
                        {item?.question || ""}
                      </div>
                    </div>
                  )}
                  {/* Conditionally render the answer section */}

                  <div className="w-full flex justify-start">
                    <div className="w-2/3 ml-4 text-gray-200 bg-slate-900 p-4 mt-3 rounded-r-xl rounded-b-xl flex text-left">
                      {item?.answer || ""}
                    </div>
                  </div>
                </div>
              ))}
            </>
          )}
        </div>
      </div>

      <div className="fixed bottom-0 w-full bg-black p-4 md:-ml-32 ">
        <div className="w-full flex flex-col items-center">
          <SearchBar handleSubmit={handleChange} />
        </div>
      </div>
    </>
  );
}
