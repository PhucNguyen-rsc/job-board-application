import React, { createContext, useEffect, useState } from "react";
import { useCookies } from 'react-cookie';
import { Outlet, useLocation } from 'react-router-dom';

const MyContext = createContext();

const MyContextProvider = ({ children }) => {
  const [cookies, setCookie] = useCookies();
  const [initialized, setInitialized] = useState(false);

  useEffect(() => {
    if (!cookies.userType) {
      setCookie("userType", "company", { path: "/" });
    }
    if (!cookies.accessToken) {
      setCookie("accessToken", null, { path: "/" });
    }
    if (!cookies.userEmail) {
      setCookie("userEmail", null, { path: "/" });
    }
    setInitialized(true);
  }, []);

  if (!initialized) return <div>Loading...</div>;

  return (
    <MyContext.Provider value={{ cookies, setCookie }}>
      {children}
    </MyContext.Provider>
  );
};

const NotAccessForm = ({message}) => {
    return (
      <div className="flex flex-col items-center justify-center min-h-screen bg-[#cdd7ff]">
        <div className="bg-white rounded-2xl shadow-md p-8 max-w-md text-center">
          <h1 className="text-3xl font-semibold text-red-500 mb-2">Access Denied</h1>
          <p className="text-gray-700 text-sm mb-6">
            {message}
          </p>
          <button
            onClick={() => window.location.href = '/'}
            className="bg-blue-500 text-white px-5 py-2 rounded hover:bg-blue-600 transition"
          >
            Back to Main Page
          </button>
        </div>
      </div>
    );
  };

const ProtectedRoute = () => {
    const [cookies] = useCookies();
    const location = useLocation();
    const savedUserToken = cookies.accessToken;
    const savedUserType = cookies.userType;
    let errMessage = "";

    if (savedUserToken === undefined || savedUserToken === null) {
        errMessage = "401 - You need to log in or sign up first to access this page."
        return <NotAccessForm message={errMessage}/>;
    }
    else if (savedUserType === "company" && location.pathname.split("/").includes("jobs")) { // companies access job seeker page
        console.log("HEREE 1")
        errMessage = "401 - You have to log in or sign up with a valid applicant account."
        return <NotAccessForm message={errMessage}/>;
    }
    else if (savedUserType === "applicant" && location.pathname.split("/").includes("companies")){
        console.log("HEREE 2")
        errMessage = "401 - You have to log in or sign up with a valid company account."
        return <NotAccessForm message={errMessage}/>;      
    }
    return (
        <Outlet />
    )
};
  
export {MyContextProvider, ProtectedRoute};
