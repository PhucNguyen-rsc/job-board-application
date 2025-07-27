import React from "react";
import { Link } from "react-router-dom";
import { useCookies } from "react-cookie";
import { useNavigate } from 'react-router-dom';

const NavigationBar = ({children}) => {
  const [cookies, setCookie, removeCookie] = useCookies();
  const navigate = useNavigate()
  const accessToken = cookies.accessToken
  const userType = cookies.userType
  
  function logOut(){
    setCookie("accessToken", null, {path:"/"});
    setCookie("userEmail", null, {path:"/"});
    setCookie("userType", null, {path:"/"});
    navigate("/login");
}

  return (
    <>
      <nav className='border-b-2 border-b-black flex items-center justify-between'>
        <h1 className="font-semibold text-3xl flex items-center flex-shrink-0 mx-4 my-2">JobBoard</h1>
        <div className="flex items-center w-auto">
          <div className="text-md flex-grow">
            <Link to="/" className="inline-block mt-0 mr-4 text-gray-600 hover:text-black">
              <button>Landing Page</button>
            </Link>
            {accessToken !== null ? ( // log in / register already
              <>
              {userType === "applicant" ? (
                <Link to="/jobs" className="inline-block mt-0 mr-4 text-gray-600 hover:text-black">
                  <button>Find Jobs</button>
                </Link>
                ) : (
                <Link to="/companies" className="inline-block mt-0 mr-4 text-gray-600 hover:text-black">
                  <button>Companies</button>
                </Link>
                )}
                <button className="inline-block mt-0 mr-4 text-gray-600 hover:text-black" onClick = {()=>logOut()}>
                  Logout
                </button>
              </>
              ) : ( // not log in / register yet
              <>
              <Link to="/login" className="inline-block mt-0 mr-4 text-gray-600 hover:text-black">
                <button>Log in</button>
              </Link>
              <Link to="/signup" className="inline-block mt-0 mr-4 text-gray-600 hover:text-black">
                <button>Sign up</button>
              </Link>
              </>
            )
            }
          </div>
        </div>
      </nav>
      
      <div>
        {children}
      </div>
      <footer className="bg-[#cdd7ff] py-6">
        <p className="text-center text-xs text-gray-500">
          © 2025 JobBoard. All rights reserved.
        </p>
      </footer>
    </>
  );
}

export default NavigationBar;
