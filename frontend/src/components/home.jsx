import React, { useState, useEffect, useContext } from "react";
import { useNavigate, useLocation } from "react-router-dom";
import { Outlet } from "react-router-dom";
import { useCookies } from "react-cookie";
import { ErrorMessage, isConvertibleToInt, queryToName } from "./utils";
import { use } from "react";

const BACKEND_URL = import.meta.env.VITE_BACKEND_URL;

function Home() {
  const [loading, setLoading] = useState(true);
  const [reloadTrigger, setReloadTrigger] = useState(0);
  const [postings, setPostings] = useState([])
  const [errMessage, setErrMessage] = useState(null);
  
  const [form, setForm] = useState({
    title: "",
    company: "",
    location: "", // cannot change email
    industry:  "",
    seniority: "",
  });

  async function handleSubmit(e){
    e.preventDefault();

    const params = {};

    if (form.title !== ""){
      params["title"] = form.title
    }
    if (form.company !== ""){
      params["company"] = form.company
    }
    if (form.location !== ""){
      params["location"] = form.location
    }
    if (form.industry !== ""){
      params["industry"] = form.industry
    }
    if (form.seniority !== ""){
      if (!isConvertibleToInt(form.seniority)){
        setErrMessage("If search with seniority, enter a number.")
        return
      }
      params["seniority"] = form.seniority
    }

    const urlParams = new URLSearchParams(params)
    const url = BACKEND_URL + "/job_listings/" +`?${urlParams.toString()}`;

    const response = await fetch(url, {
      method: "GET"
    });

    const data = await response.json();
    if ("error" in data){
      setPostings([]);
    }
    else{
      setErrMessage(null);
      setPostings(data);
    }
  }

  function handleChange(e) {
    setForm({ ...form, [e.target.name]: e.target.value });
  }

  useEffect(() => {
    async function loadData() {
      // Step 1: Get job seeker info
      const response = await fetch(
        BACKEND_URL + "/job_listings/" ,
        {
          method: "GET",
        }
      );
      const data = await response.json();

      if ("error" in data) {
        setPostings([]);
      } else {
        setPostings(data);
      }
      
      setLoading(false);
    }
    loadData();
  }, []); // Runs all logic together when reloadTrigger changes

  if (loading) {
    return (
      <div className="min-h-screen flex items-center justify-center bg-[#cdd7ff]">
        <p className="text-lg font-medium text-gray-700">
          Crunching job data...
        </p>
      </div>
    );
  }

  return (
    <div className="bg-[#cdd7ff] min-h-screen px-6 py-10">
      <div className="text-center mb-10">
        <h1 className="text-4xl font-bold text-black mb-2">Find Your Dream Job Today</h1>
        <p className="text-gray-700">Search through thousands of job listings from top companies</p>
      </div>

        <ErrorMessage message={errMessage} />
        <form className="flex justify-center space-x-4 mb-12" onSubmit={handleSubmit}>
          <input
            name="title"
            value={form.title}
            onChange={handleChange}
            placeholder="🔍 Enter job title"
            className="px-4 py-2 rounded-md w-42 bg-white border border-gray-300 shadow-sm outline-none"
          />
          <input
            name="company"
            value={form.company}
            onChange={handleChange}
            placeholder="🏢 Enter company"
            className="px-4 py-2 rounded-md w-42 bg-white border border-gray-300 shadow-sm outline-none"
          />
          <input
            name="industry"
            value={form.industry}
            onChange={handleChange}
            placeholder="💼 Enter industry"
            className="px-4 py-2 rounded-md w-40 bg-white border border-gray-300 shadow-sm outline-none"
          />

          <input
            name="seniority"
            value={form.seniority}
            onChange={handleChange}
            placeholder="🧑‍💼 YOE"
            className="px-4 py-2 rounded-md w-28 bg-white border border-gray-300 shadow-sm outline-none"
          />

          <input
            name="location"
            value={form.location}
            onChange={handleChange}
            placeholder="📍 Enter location"
            className="px-4 py-2 rounded-md w-40 bg-white border border-gray-300 shadow-sm outline-none"
          />

          <button
            className="bg-gray-300 hover:bg-blue-500 active:bg-blue-600 px-6 py-2 rounded-md text-white cursor-pointer transition-colors duration-200"
            type="submit"
          >
            Search
          </button>
        </form>

      <div className="bg-[#dbe4ff] py-10 px-6 rounded-xl">
        <h2 className="text-2xl font-semibold mb-6">Featured Jobs</h2>

          <div className="grid grid-flow-col auto-cols-max gap-6 overflow-x-auto">
            {postings.map((value, idx) => (
              <div
                key={idx}
                className="bg-white rounded-lg p-5 shadow-md w-72"
              >
                <h3 className="text-lg font-bold mb-1">{queryToName(value.title)}</h3>
                <p className="text-sm text-gray-600 mb-3">{queryToName(value.company)}</p>
                <p className="text-sm mb-1">💼 {queryToName(value.industry)}</p>
                <p className="text-sm mb-1">🧑‍💼 Prefer {queryToName(value.seniority)} YOE </p>
                <p className="text-sm mb-1">📍 {queryToName(value.location)}</p>
              </div>
            ))}
          </div>
      </div>
    </div>
  );
}


export default Home;
