import React, { useState, useEffect, useContext, useRef } from "react";
import { useNavigate, useLocation } from "react-router-dom";
import { Outlet } from "react-router-dom";
import { useCookies } from "react-cookie";
import { ErrorMessage, isConvertibleToInt, queryToName } from "./utils";
import { use } from "react";

const BACKEND_URL = import.meta.env.VITE_BACKEND_URL;

function ShowPopUp({ job, onClose }) {
  return (
    <div className="fixed inset-0 bg-opacity-40 backdrop-blur-sm flex items-center justify-center z-50">
      <div className="bg-white w-full max-w-lg p-6 rounded-xl shadow-lg relative">
        <button
          onClick={onClose}
          className="absolute top-3 right-3 text-gray-500 hover:text-gray-700"
        >
          ❌
        </button>
        <h2 className="text-2xl font-semibold mb-4">
          {queryToName(job.title)}
        </h2>
        <p className="text-sm text-gray-600 mb-2">
          <strong>Location:</strong> {queryToName(job.location)}
        </p>
        <p className="text-sm text-gray-600 mb-2">
          <strong>Industry:</strong> {queryToName(job.industry)}
        </p>
        <p className="text-sm text-gray-600 mb-2">
          <strong>Years of experience:</strong> {job.seniority}
        </p>
        <p className="text-sm text-gray-600 mb-2">
          <strong>Applicants' emails:</strong> {job.applicants.join(", ")}
        </p>
        <p className="text-sm text-gray-600 mb-2">
          <strong>Selected applicants' emails:</strong>{" "}
          {job.selected.join(", ")}
        </p>
      </div>
    </div>
  );
}

function EditApplicantPopUp({ applicant, accessToken, onClose, onSave }) {
  const [errMessage, setErrMessage] = useState(null);
  const [cookies] = useCookies();
  const JOB_SEEKER_EMAIL = cookies.userEmail;

  const [form, setForm] = useState({
    first: applicant.first || "",
    last: applicant.last || "",
    email: applicant.email, // cannot change email
    expertise: applicant.expertise || "",
    years: applicant.years || "",
  });

  function handleChange(e) {
    setForm({ ...form, [e.target.name]: e.target.value });
  }

  async function handleSubmit(e) {
    e.preventDefault();
    if (
      form.first === "" ||
      form.last === "" ||
      form.email === "" ||
      form.expertise === "" ||
      form.years === ""
    ) {
      setErrMessage("Please fill in all fields!");
      return;
    }
    if (!isConvertibleToInt(form.years)) {
      setErrMessage("Years of experience should be a number!");
      return;
    }
    const response = await fetch(
      BACKEND_URL + "/job_seekers/" + JOB_SEEKER_EMAIL,
      {
        method: "PUT",
        headers: {
          "Content-Type": "application/json",
          Authorization: `Bearer ${accessToken}`,
        },
        body: JSON.stringify(form),
      }
    );
    onSave();
    onClose();
  }

  return (
    <div className="fixed inset-0 bg-opacity-40 backdrop-blur-sm flex items-center justify-center z-50">
      <div className="bg-white w-full max-w-lg p-6 rounded-xl shadow-lg relative">
        <button
          onClick={onClose}
          className="absolute top-3 right-3 text-gray-500 hover:text-gray-700"
        >
          ❌
        </button>

        <h2 className="text-2xl font-semibold mb-4">Edit Applicant Info</h2>
        <ErrorMessage message={errMessage} />
        <h2 className="text-xl font-semibold mb-4">
          You can only modify the followings:{" "}
        </h2>

        <form onSubmit={handleSubmit} className="space-y-4">
          <div>
            <label className="block text-sm font-medium text-gray-700">
              First Name
            </label>
            <textarea
              name="first"
              value={form.first}
              onChange={handleChange}
              className="mt-1 block w-full border border-gray-300 rounded px-3 py-2"
            />
          </div>

          <div>
            <label className="block text-sm font-medium text-gray-700">
              Last Name
            </label>
            <input
              name="last"
              value={form.last}
              onChange={handleChange}
              className="mt-1 block w-full border border-gray-300 rounded px-3 py-2"
            />
          </div>

          <div>
            <label className="block text-sm font-medium text-gray-700">
              Expertise
            </label>
            <input
              name="expertise"
              value={form.expertise}
              onChange={handleChange}
              className="mt-1 block w-full border border-gray-300 rounded px-3 py-2"
            />
          </div>

          <div>
            <label className="block text-sm font-medium text-gray-700">
              Years of Experience
            </label>
            <input
              name="years"
              value={form.years}
              onChange={handleChange}
              className="mt-1 block w-full border border-gray-300 rounded px-3 py-2"
            />
          </div>

          <div className="pt-2 text-right">
            <button
              type="submit"
              className="bg-blue-500 text-white px-4 py-2 rounded hover:bg-blue-600"
            >
              Save Changes
            </button>
          </div>
        </form>
      </div>
    </div>
  );
}

function EditApplicationPopUp({ job, accessToken, onClose, onSave }) {
  const [errMessage, setErrMessage] = useState(null);
  const [subMit, setSubMit] = useState(false);
  const [cookies] = useCookies();

  async function handleSubmit(e) {
    e.preventDefault();
    if (subMit) {
      // prevent the default double loading of React in Dev Mode
      onClose();
      return;
    }
    const response = await fetch(
      BACKEND_URL + "/job_listings/apply/" + job["_id"],
      {
        method: "PUT",
        headers: {
          "Content-Type": "application/json",
          Authorization: `Bearer ${accessToken}`,
          Cookie: `AB_testing_varient=${cookies.AB_testing_varient}`,
        },
        body: JSON.stringify({
          ABTestingVarient: cookies.AB_testing_varient,
        }),
        credentials: "include", // Important: include cookies in the request
      }
    );
    const data = await response.json();
    if ("error" in data) {
      if (data["error"] === "You had applied for this position already!") {
        setErrMessage("You cannot apply to the same job posting twice!");
        return;
      } else if (data["error"] === "Cannot find the job you looking for") {
        setErrMessage(
          "The job you are looking for does not exist. Check again later!"
        );
        return;
      }
    }
    setSubMit(true); // prevent the default double loading of React in Dev Mode
    onSave();
    onClose();
  }

  return (
    <div className="fixed inset-0 bg-opacity-40 backdrop-blur-sm flex items-center justify-center z-50">
      <div className="bg-white w-full max-w-md p-6 rounded-xl shadow-lg">
        <h2 className="text-2xl font-semibold text-center mb-4">
          Apply to this job posting?
        </h2>
        <ErrorMessage message={errMessage} />
        <div className="text-left space-y-2 mb-6">
          <p>
            <span className="font-medium text-gray-700">Title: </span>{" "}
            {queryToName(job.title)}
          </p>
          <p>
            <span className="font-medium text-gray-700">Company: </span>{" "}
            {queryToName(job.company)}
          </p>
          <p>
            <span className="font-medium text-gray-700">Location: </span>{" "}
            {queryToName(job.location)}
          </p>
          <p>
            <span className="font-medium text-gray-700">Industry: </span>{" "}
            {queryToName(job.industry)}
          </p>
          <p>
            <span className="font-medium text-gray-700">Seniority: </span>{" "}
            {queryToName(job.seniority)}
          </p>
        </div>

        <form onSubmit={handleSubmit}>
          <div className="flex justify-center space-x-4 mt-6">
            <button
              onClick={onClose}
              type="button"
              className="bg-gray-200 text-gray-800 px-4 py-2 rounded hover:bg-gray-300 flex items-center space-x-1"
            >
              No❌
            </button>
            <button
              type="submit"
              className="bg-blue-500 text-white px-4 py-2 rounded hover:bg-blue-600 flex items-center space-x-1"
            >
              Yes✅
            </button>
          </div>
        </form>
      </div>
    </div>
  );
}

function AISuggestionPopUp({ job, applicant, onClose, accessToken }) {
  const [suggestions, setSuggestions] = useState(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);
  const [cookies] = useCookies();
  const requestMadeRef = useRef(false);

  useEffect(() => {
    // Prevent duplicate requests in development mode (React StrictMode)
    if (requestMadeRef.current) return;

    async function fetchSuggestions() {
      try {
        requestMadeRef.current = true;
        const response = await fetch(
          `${BACKEND_URL}/job_seekers/ai/suggestions`,
          {
            method: "POST",
            headers: {
              "Content-Type": "application/json",
              Authorization: `Bearer ${accessToken}`,
              Cookie: `AB_testing_varient=${cookies.AB_testing_varient}`,
            },
            body: JSON.stringify({
              job: {
                title: job.title,
                company: job.company,
                location: job.location,
                industry: job.industry,
                seniority: job.seniority,
              },
              applicant: {
                first: applicant.first,
                last: applicant.last,
                email: applicant.email,
                expertise: applicant.expertise,
                years: applicant.years,
              },
              ABTestingVarient: cookies.AB_testing_varient,
            }),
            credentials: "include", // Important: include cookies in the request
          }
        );

        const data = await response.json();
        if (!response.ok) {
          throw new Error(data.message || "Failed to get AI suggestions");
        }
        setSuggestions(data);
      } catch (err) {
        setError(err.message);
      } finally {
        setLoading(false);
      }
    }

    fetchSuggestions();

    // Cleanup function
    return () => {};
  }, []);

  return (
    <div className="fixed inset-0 bg-opacity-40 backdrop-blur-sm flex items-center justify-center z-50">
      <div className="bg-white w-full max-w-2xl p-6 rounded-xl shadow-lg relative">
        <button
          onClick={onClose}
          className="absolute top-3 right-3 text-gray-500 hover:text-gray-700"
        >
          ❌
        </button>

        <h2 className="text-2xl font-semibold mb-4">AI Suggestions</h2>

        {loading ? (
          <p>Loading suggestions... This may take upto 31 seconds</p>
        ) : error ? (
          <p className="text-red-500">{error}</p>
        ) : (
          <div className="space-y-4">
            <div className="bg-blue-50 p-4 rounded-lg">
              <h3 className="font-semibold text-lg mb-2">Match Analysis</h3>
              <p>{suggestions.matchAnalysis}</p>
            </div>

            <div className="bg-green-50 p-4 rounded-lg">
              <h3 className="font-semibold text-lg mb-2">Suggestions</h3>
              <ul className="list-disc pl-5 space-y-2">
                {suggestions.tips.map((tip, i) => (
                  <li key={i}>{tip}</li>
                ))}
              </ul>
            </div>
          </div>
        )}
      </div>
    </div>
  );
}

function SurveyPopUp({ ABTestingVariant, accessToken, onClose }) {
  const [errMessage, setErrMessage] = useState(null);
  const [submit, setSubmit] = useState(false);
  const [form, setForm] = useState({
    clickedButton: "",
    experience: "",
    impactedDecision: "",
    variant: ABTestingVariant,
  });

  async function handleSubmit(e) {
    e.preventDefault();
    if (ABTestingVariant === "a") {
      if (form.experience === "") {
        setErrMessage("You have to fill all the required fields!");
        return;
      }
    } else if (ABTestingVariant === "llm") {
      if (
        form.experience === "" ||
        form.clickedButton === "" ||
        form.impactedDecision === ""
      ) {
        setErrMessage("You have to fill all the required fields!");
        return;
      }
    }

    if (submit) {
      // prevent the default double loading of React in Dev Mode
      onClose();
      return;
    }

    const response = await fetch(BACKEND_URL + "/job_seekers/ab_survey", {
      method: "POST",
      headers: {
        "Content-Type": "application/json",
        Authorization: `Bearer ${accessToken}`,
        Cookie: `AB_testing_varient=${ABTestingVariant}`,
      },
      body: JSON.stringify(form),
      credentials: "include", // Important: include cookies in the request
    });

    const data = await response.json();
    setSubmit(true);
    onClose();
    return;
  }
  return (
    <form
      onSubmit={handleSubmit}
      className="fixed inset-0 backdrop-blur-sm bg-white/10 flex items-center justify-center z-50"
    >
      <div className="relative bg-[#f3ecff] rounded-2xl p-8 shadow-xl w-full max-w-2xl space-y-6">
        <button
          type="button"
          onClick={onClose}
          className="absolute top-4 right-4 text-red-500 hover:text-red-600 text-2xl"
          aria-label="Close survey"
        >
          ❌
        </button>

        <div className="text-center">
          <h2 className="text-2xl font-bold text-gray-800 mb-1">
            Survey for A/B Testing
          </h2>
          <p className="text-sm text-gray-600">
            Help us improve your experience - just 1 minute to answer!
          </p>
        </div>

        <ErrorMessage message={errMessage} />

        {/* Q1: Rating experience */}
        <div className="bg-white p-6 rounded-xl shadow-md">
          <p className="font-medium text-gray-800 mb-3">
            Rate your experience after using this app{" "}
            <span className="text-red-500">*</span>
          </p>

          <div className="flex justify-between text-sm text-gray-500 px-2 mb-2 font-medium">
            <span className="w-10 text-left">Negative</span>
            <span className="w-10 text-center invisible">-</span>
            <span className="w-10 text-center invisible">-</span>
            <span className="w-10 text-center invisible">-</span>
            <span className="w-10 text-right">Positive</span>
          </div>

          <div className="flex justify-between items-center">
            {[1, 2, 3, 4, 5].map((val) => (
              <label
                key={val}
                className="flex flex-col items-center w-full text-sm text-gray-800 font-medium"
              >
                <input
                  type="radio"
                  name="experience"
                  value={val}
                  className="mb-2 w-5 h-5 accent-blue-500 hover:scale-105 transition-transform duration-150"
                  onChange={(e) =>
                    setForm({ ...form, experience: e.target.value })
                  }
                />
                <span>{val}</span>
              </label>
            ))}
          </div>
        </div>

        {/* Conditionally render extra questions if AB variant B */}
        {ABTestingVariant === "llm" && (
          <>
            {/* Q2: Clicked AI Tips */}
            <div className="bg-white p-5 rounded-xl shadow-md">
              <p className="font-medium text-gray-800 mb-3">
                Did you click the AI Tips button at least once?{" "}
                <span className="text-red-500">*</span>
              </p>
              <div className="space-y-2">
                {["Yes", "No"].map((val) => (
                  <label key={val} className="flex items-center gap-2 text-sm">
                    <input
                      type="radio"
                      name="clickedButton"
                      value={val}
                      className="accent-blue-500"
                      onChange={(e) =>
                        setForm({ ...form, clickedButton: e.target.value })
                      }
                    />
                    {val}
                  </label>
                ))}
              </div>
            </div>

            {/* Q3: AI Impact */}
            <div className="bg-white p-5 rounded-xl shadow-md">
              <p className="font-medium text-gray-800 mb-3">
                If you received the AI advice for the role, did it impact your
                decision whether to apply?{" "}
                <span className="text-red-500">*</span>
              </p>
              <div className="space-y-2">
                {["Yes", "No"].map((val) => (
                  <label key={val} className="flex items-center gap-2 text-sm">
                    <input
                      type="radio"
                      name="impactedDecision"
                      value={val}
                      className="accent-blue-500"
                      onChange={(e) =>
                        setForm({ ...form, impactedDecision: e.target.value })
                      }
                    />
                    {val}
                  </label>
                ))}
              </div>
            </div>
          </>
        )}

        {/* Submit Button (inside modal box) */}
        <div className="pt-2 text-center">
          <button
            type="submit"
            className="bg-blue-500 hover:bg-blue-600 text-white font-medium px-6 py-2 rounded-lg shadow-md transition duration-200"
          >
            ✅ Submit the Survey
          </button>
        </div>
      </div>
    </form>
  );
}

function Jobs() {
  const [jobSeeker, setJobSeeker] = useState(null);
  const [loading, setLoading] = useState(true);
  const [postings, setPostings] = useState([]);
  const [applications, setApplications] = useState([]);
  const [currentJobView, setCurrentJobView] = useState(null);
  const [currentJobSeekerView, setCurrentJobSeekerView] = useState(null);
  const [currentEditJobView, setEditJobView] = useState(null);
  const [reloadTrigger, setReloadTrigger] = useState(0);
  const [cookies, setCookies] = useCookies();
  const accessToken = cookies.accessToken;
  const userEmail = cookies.userEmail;
  const JOB_SEEKER_EMAIL = userEmail;
  const [errMessage, setErrMessage] = useState(null);
  const [currentAISuggestionView, setCurrentAISuggestionView] = useState(null);
  const [ABTestingVarient, setABTestingVarient] = useState(null);
  const [surveySubmitted, setSurveySubmitted] = useState(false);
  useEffect(() => {
    const AB_testing_varient = cookies.AB_testing_varient;

    if (AB_testing_varient) {
      setABTestingVarient(AB_testing_varient);
    } else {
      const varient_assignment = ["standard", "llm"][
        Math.floor(Math.random() * 2)
      ];
      setABTestingVarient(varient_assignment);
      setCookies("AB_testing_varient", varient_assignment, {
        expires: new Date(Date.now() + 1000 * 60 * 30), // Expires in 30 minutes
      });
    }
  }, []);

  const [form, setForm] = useState({
    title: "",
    company: "",
    location: "", // cannot change email
    industry: "",
    seniority: "",
  });

  async function handleSubmit(e) {
    e.preventDefault();

    const params = {};

    if (form.title !== "") {
      params["title"] = form.title;
    }
    if (form.company !== "") {
      params["company"] = form.company;
    }
    if (form.location !== "") {
      params["location"] = form.location;
    }
    if (form.industry !== "") {
      params["industry"] = form.industry;
    }
    if (form.seniority !== "") {
      if (!isConvertibleToInt(form.seniority)) {
        setErrMessage("If search with seniority, enter a number.");
        return;
      }
      params["seniority"] = form.seniority;
    }
    const urlParams = new URLSearchParams(params);
    const url = BACKEND_URL + "/job_listings/" + `?${urlParams.toString()}`;

    const response = await fetch(url, {
      method: "GET",
    });

    const data = await response.json();
    setPostings(data);
    setErrMessage(null);
  }

  function handleChange(e) {
    setForm({ ...form, [e.target.name]: e.target.value });
  }

  function editJobSeeker(jobSeeker) {
    setCurrentJobSeekerView(jobSeeker);
  }

  function applyJobDetails(job) {
    setEditJobView(job);
  }

  function show_AI_Tips(job) {
    setCurrentAISuggestionView(job);
  }

  useEffect(() => {
    async function loadData() {
      // Step 1: Get job seeker info
      const jobSeekerFind = await fetch(
        BACKEND_URL + "/job_seekers/" + JOB_SEEKER_EMAIL,
        {
          method: "GET",
          headers: {
            Authorization: `Bearer ${accessToken}`,
          },
        }
      );

      const jobSeekerData = await jobSeekerFind.json();
      setJobSeeker(jobSeekerData);
      // Step 2: Get my job listings (applications)
      const details = await fetch(BACKEND_URL + "/job_seekers/inquire", {
        method: "GET",
        headers: {
          Authorization: `Bearer ${accessToken}`,
        },
      });

      const jobData = await details.json();
      if (jobData.hasOwnProperty("data")) {
        console.log(jobData["data"]);
        setApplications(jobData["data"]);
      }
      setLoading(false);
    }
    loadData();
  }, [reloadTrigger]); // Runs all logic together when reloadTrigger changes

  if (loading) {
    return (
      <div className="min-h-screen flex items-center justify-center bg-[#cdd7ff]">
        <p className="text-lg font-medium text-gray-700">
          Loading job seeker data...
        </p>
      </div>
    );
  }
  return (
    <div className="min-h-screen bg-[#cdd7ff] p-6 space-y-6">
      <div className="bg-white rounded-2xl shadow-md p-6 w-full max-w-4xl mx-auto">
        <div className="flex justify-between items-center">
          <h2 className="text-xl font-semibold">Profile Information</h2>
          <button
            className="text-sm text-blue-600 hover:underline"
            onClick={() => editJobSeeker(jobSeeker)}
          >
            ✏️ Edit
          </button>
        </div>
        <div className="mt-4 grid grid-cols-2 gap-y-2 text-sm text-gray-700">
          <div>
            <p className="font-medium">Full Name</p>
            <p>
              {queryToName(jobSeeker["first"])} {queryToName(jobSeeker["last"])}
            </p>
          </div>
          <div>
            <p className="font-medium">Expertise</p>
            <p>{jobSeeker["expertise"]}</p>
          </div>
          <div>
            <p className="font-medium">Email</p>
            <p>{jobSeeker["email"]}</p>
          </div>
          <div>
            <p className="font-medium">Years</p>
            <p>{jobSeeker["years"]}</p>
          </div>
        </div>
      </div>

      {currentJobView && (
        <ShowPopUp
          job={currentJobView}
          accessToken={accessToken}
          onClose={() => setCurrentJobView(null)}
        />
      )}
      {currentJobSeekerView && (
        <EditApplicantPopUp
          applicant={currentJobSeekerView}
          onClose={() => {
            setCurrentJobSeekerView(null);
          }}
          onSave={() => setReloadTrigger((prev) => prev + 1)}
        />
      )}
      {currentEditJobView && (
        <EditApplicationPopUp
          job={currentEditJobView}
          accessToken={accessToken}
          onClose={() => {
            setEditJobView(null);
          }}
          onSave={() => setReloadTrigger((prev) => prev + 1)}
        />
      )}

      {currentAISuggestionView && (
        <AISuggestionPopUp
          job={currentAISuggestionView}
          applicant={jobSeeker}
          accessToken={accessToken}
          onClose={() => setCurrentAISuggestionView(null)}
        />
      )}

      <div className="bg-white rounded-2xl shadow-md p-6 w-full max-w-4xl mx-auto">
        <div className="flex justify-between items-center mb-4">
          <h2 className="text-xl font-semibold">Search Jobs</h2>
        </div>
        <ErrorMessage message={errMessage} />
        <form
          onSubmit={handleSubmit}
          className="space-y-3 max-h-[50vh] overflow-y-auto"
        >
          <div className="flex items-center gap-4">
            <label className="text-sm font-medium text-gray-700 w-32">
              Title
            </label>
            <input
              className="flex-1 border border-gray-300 rounded px-3 py-2"
              name="title"
              value={form.title}
              onChange={handleChange}
            />
          </div>

          <div className="flex items-center gap-4">
            <label className="text-sm font-medium text-gray-700 w-32">
              Company
            </label>
            <input
              className="flex-1 border border-gray-300 rounded px-3 py-2"
              name="company"
              value={form.company}
              onChange={handleChange}
            />
          </div>

          <div className="flex items-center gap-4">
            <label className="text-sm font-medium text-gray-700 w-32">
              Location
            </label>
            <input
              className="flex-1 border border-gray-300 rounded px-3 py-2"
              name="location"
              value={form.location}
              onChange={handleChange}
            />
          </div>

          <div className="flex items-center gap-4">
            <label className="text-sm font-medium text-gray-700 w-32">
              Industry
            </label>
            <input
              className="flex-1 border border-gray-300 rounded px-3 py-2"
              name="industry"
              value={form.industry}
              onChange={handleChange}
            />
          </div>

          <div className="flex items-center gap-4">
            <label className="text-sm font-medium text-gray-700 w-32">
              Seniority
            </label>
            <input
              className="flex-1 border border-gray-300 rounded px-3 py-2"
              name="seniority"
              value={form.seniority}
              onChange={handleChange}
            />
          </div>

          <button
            type="submit"
            className="bg-blue-500 text-white px-4 py-2 rounded hover:bg-blue-600"
          >
            Search
          </button>
        </form>
      </div>
      {postings.length > 0 && (
        <div className="bg-white rounded-2xl shadow-md p-6 w-full max-w-4xl mx-auto">
          <div className="flex justify-between items-center mb-4">
            <h2 className="text-xl font-semibold">Found Jobs</h2>
          </div>
          <table className="w-full text-left text-sm">
            <thead>
              <tr className="border-b">
                <th className="py-2">Title</th>
                <th className="py-2">Company</th>
                <th className="py-2">Location</th>
                <th className="py-2">Industry</th>
                <th className="py-2">Seniority</th>
              </tr>
            </thead>
            <tbody className="max-h-[30vh] overflow-y-auto">
              {postings.map((job, idx) => (
                <tr key={idx} className="border-b">
                  <td className="py-2">{queryToName(job.title)}</td>
                  <td className="py-2">{queryToName(job.company)}</td>
                  <td className="py-2">{queryToName(job.location)}</td>
                  <td className="py-2">{queryToName(job.industry)}</td>
                  <td className="py-2">{job.seniority}</td>
                  <td className="py-2 space-x-2">
                    <button
                      className="text-yellow-600 hover:underline"
                      onClick={() => applyJobDetails(job)}
                    >
                      📝 Apply
                    </button>
                    {ABTestingVarient === "llm" && (
                      <button
                        className="bg-blue-100 text-blue-700 hover:bg-blue-200 font-medium px-3 py-1 rounded-lg transition duration-150"
                        onClick={() => show_AI_Tips(job)}
                      >
                        🤖 See AI Tips
                      </button>
                    )}
                  </td>
                </tr>
              ))}
            </tbody>
          </table>
        </div>
      )}
      {surveySubmitted && (
        <SurveyPopUp
          ABTestingVariant={ABTestingVarient}
          accessToken={accessToken}
          onClose={() => setSurveySubmitted(false)}
        />
      )}

      <div className="bg-white rounded-2xl shadow-md p-6 w-full max-w-4xl mx-auto">
        <h2 className="text-xl font-semibold mb-4">My Applications</h2>
        <div className="space-y-3 max-h-[30vh] overflow-y-auto">
          {Object.keys(applications).length > 0 &&
            Object.entries(applications).map(([key, value], idx) => (
              <div
                key={idx}
                className="flex items-center justify-between border rounded-lg p-3"
                style={{
                  backgroundColor:
                    value[0] === "accepted" //green
                      ? "#d4edda"
                      : value[0] === "rejected" //red
                      ? "#f8d7da"
                      : value[0] === "waiting" //yellow
                      ? "#fff3cd"
                      : "#f0f0f0", //default
                }}
              >
                <div className="text-sm justify-center">
                  <p className="font-medium">
                    Title: {queryToName(value[1][0]).toUpperCase()}
                  </p>
                  <p className="font-medium">
                    Company: {queryToName(value[1][1]).toUpperCase()}
                  </p>
                  <p className="font-medium">
                    Location: {queryToName(value[1][2]).toUpperCase()}
                  </p>
                </div>
                <div className="text-sm justify-center">
                  Status: <strong>{value[0].toUpperCase()}</strong>{" "}
                </div>
                {/* <button className="bg-blue-400 hover:bg-blue-500 text-white px-4 py-1 rounded" onClick={}>
                View
              </button> */}
              </div>
            ))}
        </div>
      </div>
      <div className="bg-white rounded-3xl shadow-lg p-8 w-full max-w-4xl mx-auto text-center">
        <button
          onClick={() => setSurveySubmitted(true)}
          className="inline-flex items-center gap-2 bg-red-100 hover:bg-red-200 text-red-600 font-semibold px-6 py-3 rounded-full shadow-md transition-all duration-200"
        >
          📝 <span>Submit a Survey</span>
        </button>
      </div>
    </div>
  );
}

export default Jobs;
