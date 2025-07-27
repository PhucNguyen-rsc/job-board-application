import React, { useContext, useState } from 'react';
import { useCookies } from "react-cookie";
import { validateEmail, isValidPassword, ErrorMessage, isConvertibleToInt } from "./utils";
import { useNavigate } from 'react-router-dom';

const BACKEND_URL = import.meta.env.VITE_BACKEND_URL;

function SignupSuccess() {
  const navigate = useNavigate();

  return (
    <div className="min-h-screen bg-[#cdd7ff] flex items-center justify-center px-4">
      <div className="bg-white rounded-xl shadow-md p-8 max-w-md w-full text-center">
        <h1 className="text-3xl font-bold text-green-600 mb-4">Account Created Successfully 🎉</h1>
        <p className="text-gray-700 text-sm mb-6">
          Your account has been created. To continue, please log in using the credentials you just provided.
        </p>
        <button
          onClick={() => navigate("/login")}
          className="bg-blue-500 hover:bg-blue-600 text-white font-medium py-2 px-6 rounded transition"
        >
          Go to Login
        </button>
      </div>
    </div>
  );
}

function Signup() {
  const [errMessage, setErrMessage] = useState(null);
  const [loadSuccess, setLoadSuccess] = useState(false);
  const [isSubmitting, setIsSubmitting] = useState(false);
  const [cookies, setCookie, removeCookie] = useCookies();

  let userType = cookies.userType
  if (userType === null || userType === undefined){ //intialized default value
    userType = "company"
    setCookie("userType", "company", {path:"/"})
  }

  let [form, setForm] = useState({
    first: '',
    last: '',
    email: '',
    expertise: '',
    years: '',
    password: '',
    name: '',
    country: '',
    description: ''
  });
  

  function handleChange(e) {
    setForm({ ...form, [e.target.name]: e.target.value });
  }

  async function handleSubmit(e) {
    e.preventDefault();

    if (isSubmitting) return;

    let sendEndpoint = "";

    if (userType === "company"){
      if ( form.name === "" || form.email === "" || form.country === "" || form.description === "" || form.password === ""){
        setErrMessage("Please fill in all fields!");
        return;
      }
      if (!validateEmail(form.email)){
        setErrMessage("Invalid Email Format!");
        return;
      }
      if (!isValidPassword(form.password)){
        setErrMessage("Password has to be at least 8 characters long and contains at least one uppercase, lowercase, and number.");
        return;
      }
      ["first","last","expertise", "years"].forEach((key) => {delete form[key]});
      sendEndpoint = "/companies/"
  
    }    
    else {
      if ( form.first === "" || form.last === "" || form.email === "" || form.expertise === "" || form.years === "" || form.password === ""){
        setErrMessage("Please fill in all fields!");
        return;
      }
      if (!validateEmail(form.email)){
        setErrMessage("Invalid Email Format!");
        return;
      }
      if (!isValidPassword(form.password)){
        setErrMessage("Password has to be at least 8 characters long and contains at least one uppercase, lowercase, and number.");
        return;
      }
      if (!isConvertibleToInt(form.years)){
        setErrMessage("Years of experience should be a valid integer number.");
        return;
      }
      ["name","country","description"].forEach((key) => {delete form[key]});
      sendEndpoint = "/job_seekers/"
    }

    const response = await fetch(BACKEND_URL + sendEndpoint + "signup", {
      method: "POST",
      headers: {
        "Content-Type": "application/json",
      },
      body: JSON.stringify(form),
    });

    const data = await response.json();
    console.log(data)
    if (data.error === "The email address already exists") {
      setErrMessage("This email address already exists!")
    }
    else if (data.error === "The company name already exists"){
      setErrMessage("This company name already exists!")
    }
    else {
      setLoadSuccess(true);
      setIsSubmitting(true);
    }
  }
  if (loadSuccess) {
    return (<SignupSuccess />)
  }
  else {
    return (
      <div className="min-h-screen bg-[#cdd7ff] flex flex-col items-center justify-center px-4">
        <h2 className="text-3xl font-bold mb-1">Create Your Account</h2>
        <p className="text-sm text-gray-600 mb-6">
          Join our {userType === 'company' ? 'companies' : 'job seeker'} community
        </p>
        <div className="flex mt-4 mb-6 rounded overflow-hidden">
        <button
            className={`px-6 py-2 font-medium ${
              userType === 'company' ? 'bg-blue-100 text-blue-600' : 'bg-white text-gray-800'
            }`}
            onClick={() => setCookie('userType', "company", {path:"/"})}
          >
            As Company
          </button>
            <button
              className={`px-6 py-2 font-medium ${
                userType === 'applicant' ? 'bg-blue-100 text-blue-600' : 'bg-white text-gray-800'
              }`}
              onClick={() => setCookie('userType', "applicant", {path:"/"})}
            >
              As Job Seeker
            </button>
        </div>
        <form
          onSubmit={handleSubmit}
          className="bg-white shadow-md rounded-lg p-6 w-full max-w-md space-y-4"
        >

          <ErrorMessage message={errMessage} />

          {userType === 'applicant' ? ( //applicant form
            <>
              <div className="flex space-x-2">
                <div className="w-1/2">
                  <label className="block text-sm font-medium">First Name</label>
                  <input
                    name="first"
                    value={form.first}
                    onChange={handleChange}
                    className="w-full border rounded px-3 py-2 mt-1"
                  />
                </div>
                <div className="w-1/2">
                  <label className="block text-sm font-medium">Last Name</label>
                  <input
                    name="last"
                    value={form.last}
                    onChange={handleChange}
                    className="w-full border rounded px-3 py-2 mt-1"
                  />
                </div>
              </div>
              <div>
              <label className="block text-sm font-medium mb-1">
                <span className="text-base font-semibold">Email Address: </span>
                <span className="ml-2 text-xs text-gray-500">(Notice: you cannot modify this after creation)</span>
              </label>
                <input
                  name="email"
                  value={form.email}
                  type="email"
                  onChange={handleChange}
                  className="w-full border rounded px-3 py-2 mt-1"
                />
              </div>
              <div>
                <label className="block text-sm font-medium">Area of expertise</label>
                <input
                  name="expertise"
                  value={form.expertise}
                  onChange={handleChange}
                  className="w-full border rounded px-3 py-2 mt-1"
                />
              </div>
              <div>
                <label className="block text-sm font-medium">Years of experience</label>
                <input
                  name="years"
                  value={form.years}
                  type="number"
                  onChange={handleChange}
                  className="w-full border rounded px-3 py-2 mt-1"
                />
              </div>
              <div>
              <label className="block text-sm font-medium mb-1">
                <span className="text-base font-semibold">Password: </span>
                <span className="ml-2 text-xs text-gray-500">(Notice: you cannot modify this after creation)</span>
              </label>
                <input
                  name="password"
                  value={form.password}
                  type="password"
                  onChange={handleChange}
                  className="w-full border rounded px-3 py-2 mt-1"
                />
              </div>
            </>
          ) : (
            // Company Form
            <>
              <div>
              <label className="block text-sm font-medium mb-1">
                <span className="text-base font-semibold">Name: </span>
                <span className="ml-2 text-xs text-gray-500">(Notice: you cannot modify this after creation)</span>
              </label>
                <input
                  name="name"
                  value={form.name}
                  onChange={handleChange}
                  className="w-full border rounded px-3 py-2 mt-1"
                />
              </div>
              <div>
              <label className="block text-sm font-medium mb-1">
                <span className="text-base font-semibold">Email Address: </span>
                <span className="ml-2 text-xs text-gray-500">(Notice: you cannot modify this after creation)</span>
              </label>
                <input
                  name="email"
                  value={form.email}
                  type="email"
                  onChange={handleChange}
                  className="w-full border rounded px-3 py-2 mt-1"
                />
              </div>
              <div>
                <label className="block text-sm font-medium">Country</label>
                <input
                  name="country"
                  value={form.country}
                  onChange={handleChange}
                  className="w-full border rounded px-3 py-2 mt-1"
                />
              </div>
              <div>
                <label className="block text-sm font-medium">Description</label>
                <input
                  name="description"
                  value={form.description}
                  onChange={handleChange}
                  className="w-full border rounded px-3 py-2 mt-1"
                />
              </div>
              <div>
              <label className="block text-sm font-medium mb-1">
                <span className="text-base font-semibold">Password: </span>
                <span className="ml-2 text-xs text-gray-500">(Notice: you cannot modify this after creation)</span>
              </label>
                <input
                  name="password"
                  value={form.password}
                  type="password"
                  onChange={handleChange}
                  className="w-full border rounded px-3 py-2 mt-1"
                />
              </div>
            </>
          )}

          <button
            type="submit"
            className="w-full bg-blue-200 text-blue-700 font-medium py-2 rounded hover:bg-blue-300 transition"
          >
            Create Account
          </button>
        </form>

      </div>
    );
  }
}

export default Signup
