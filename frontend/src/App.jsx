import React from "react";
import NavigationBar from "./components/navBar";
import { BrowserRouter, Routes, Route } from "react-router-dom";
import Home from "./components/home";
import Jobs from "./components/findJobs.jsx";
import Companies from "./components/companies";
import Login from "./components/login";
import Signup from "./components/signup";
import {MyContextProvider, ProtectedRoute} from "./components/context.jsx"

function App() {
  return (
    <>
      <BrowserRouter>
        <MyContextProvider>
          <NavigationBar >
            <Routes>
              <Route path="/" element={<Home />} />

              <Route path="/login" element={<Login />} />
              <Route path="/signup" element={<Signup />} />

              <Route path = "/" element={<ProtectedRoute />}>

                <Route path="jobs" element={<Jobs />} />
                <Route path="companies" element={<Companies />} />
              </Route>

            </Routes>         
          </NavigationBar >
        </MyContextProvider>
      </BrowserRouter>
    </>
  );
}

export default App;
