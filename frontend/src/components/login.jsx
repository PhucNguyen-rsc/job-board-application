
import React, { useState, useEffect } from "react";
import { useNavigate } from 'react-router-dom';
import { useCookies } from "react-cookie";
import { validateEmail, isValidPassword, ErrorMessage } from "./utils";

const BACKEND_URL = import.meta.env.VITE_BACKEND_URL;

function Login() {
  const navigate = useNavigate();
  const [cookies, setCookie, removeCookie] = useCookies();
  const [errMessage, setErrMessage] = useState(null);
  const [userType, setUserType] = useState(cookies.userType || "company");

  const [form,setForm] = useState({
    email: "",
    password: ""
  });

  useEffect(() => {
    if (!cookies.userType) {
      setCookie("userType", "company", { path: "/" });
    }
  }, []);

  async function handleSubmit(e){
    e.preventDefault();
    if ( form.email === "" || form.email === "") {
      setErrMessage("Please fill in all fields!")
      return;
    }
    if (!validateEmail(form.email)){
      setErrMessage("Invalid Email Format!")
      return;
    }
    if (!isValidPassword(form.password)){
      setErrMessage("Password has to be at least 8 characters long and contains at least one uppercase, lowercase, and number.")
      return;
    }    
    let sendEndpoint = "";

    if (userType === "company"){
      sendEndpoint = "/companies/"
    }
    else {
      sendEndpoint = "/job_seekers/"
    }
    console.log(BACKEND_URL + sendEndpoint+ "login")
    const response = await fetch(BACKEND_URL + sendEndpoint+ "login", {
      method: "POST",
      headers: {
        "Content-Type": "application/json",
      },
      body: JSON.stringify(form),
    });
    const data = await response.json();
    if (data.error) {
      setErrMessage("Invalid Credentials!")
      return;
    }
    else{
      setCookie("accessToken", data["access_token"], { path: "/" })
      setCookie("userEmail", form.email, { path: "/" })
      setCookie("userType", userType, { path: "/" })
      setErrMessage(null)

      if (userType === "company"){
        navigate("/companies")
      }
      else {
        navigate("/jobs")
      }
    }
  }

  function handleChange(e) {
    setForm({ ...form, [e.target.name]: e.target.value });
  }

  return (
    <div className="min-h-screen bg-[#cdd7ff] flex flex-col items-center justify-center">

      <div className="flex mt-4 mb-6 rounded overflow-hidden">
      <button
          className={`px-6 py-2 font-medium ${
            userType === 'company' ? 'bg-blue-100 text-blue-600' : 'bg-white text-gray-800'
          }`}
          onClick={() => {
            setCookie('userType', "company", {path:"/"})
            setUserType("company");
            }
          }
        >
          As Company
        </button>
          <button
            className={`px-6 py-2 font-medium ${
              userType === 'applicant' ? 'bg-blue-100 text-blue-600' : 'bg-white text-gray-800'
            }`}
            onClick={() => {
              setCookie('userType', "applicant", {path:"/"})
              setUserType("applicant");
              }
            }
          >
            As Job Seeker
          </button>
      </div>

      <div className="bg-gray-100 rounded-lg p-8 w-full max-w-md shadow-md">
        <h2 className="text-2xl font-bold text-center mb-6">Welcome Back</h2>

        <ErrorMessage message={errMessage} />

        <form className="space-y-5" onSubmit={handleSubmit}>
          <div>
            <label className="block text-sm font-medium mb-1">Email Address</label>
            <input
              name="email"
              value={form.email}
              type="email"
              onChange={handleChange}
              className="w-full px-3 py-2 border rounded outline-none focus:ring-2 focus:ring-blue-400"
            />
          </div>

          <div>
            <label className="block text-sm font-medium mb-1">Password</label>
            <input
              name="password"
              value={form.password}
              type="password"
              onChange={handleChange}
              className="w-full px-3 py-2 border rounded outline-none focus:ring-2 focus:ring-blue-400"
            />
          </div>

          <button
            type="submit"
            className="w-full py-2 bg-blue-200 text-blue-800 font-medium rounded hover:bg-blue-300 transition"
          >
            Sign In
          </button>
        </form>
      </div>
    </div>
  );
}

export default Login;
