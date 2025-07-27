import React, { useState, useEffect } from 'react';
import { useNavigate } from 'react-router-dom';
import { ErrorMessage, queryToName, isConvertibleToInt } from "./utils";
import { useCookies } from "react-cookie";

const BACKEND_URL = import.meta.env.VITE_BACKEND_URL;

function ShowPopUp({ job, onClose}) {
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
          <strong>Preferred years of experience:</strong> {job.seniority}
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

function EditCompanyPopUp({ company, accessToken, onClose, onSave}) {
  const [cookies] = useCookies();
  const userEmail =  cookies.userEmail;
  const COMPANY_EMAIL = userEmail;

  const [errMessage, setErrMessage] = useState(null)

  const [form, setForm] = useState({
    name: company.name,
    email: company.email, // cannot change email
    description: company.description || "",
    country: company.country || "",
  });

  function handleChange(e) {
    setForm({ ...form, [e.target.name]: e.target.value });
  }

  async function handleSubmit(e) {
    e.preventDefault();
    if (form.description === "" || form.country === "") {
      setErrMessage("Please fill in all fields!");
      return;
    }
    const response = await fetch(BACKEND_URL + "/companies/" + COMPANY_EMAIL, {
      method: "PUT",
      headers: {
        "Content-Type": "application/json",
        Authorization: `Bearer ${accessToken}`,
      },
      body: JSON.stringify(form),
    });
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

        <h2 className="text-2xl font-semibold mb-4">Edit Company Info</h2>
        <ErrorMessage message={errMessage} />
        <h2 className="text-lg font-medium mb-4">
          You can only modify the company description and location.
        </h2>

        <form onSubmit={handleSubmit} className="space-y-4">
          <div>
            <label className="block text-sm font-medium text-gray-700">
              Description
            </label>
            <textarea
              name="description"
              value={form.description}
              onChange={handleChange}
              className="mt-1 block w-full border border-gray-300 rounded px-3 py-2"
            />
          </div>

          <div>
            <label className="block text-sm font-medium text-gray-700">
              Headquarter Location
            </label>
            <input
              name="country"
              value={form.country}
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

function EditJobPopUp({ job, accessToken, onClose, onSave }) {
  const [form, setForm] = useState({
    id: job["_id"],
    title: queryToName(job.title) || "",
    industry: queryToName(job.industry) || "", // cannot change email
    seniority: queryToName(job.seniority) || "",
    location: queryToName(job.location) || "",
    applicants: job.applicants,
    selected: job.selected,
  });

  const [errMessage, setErrMessage] = useState(null)

  function handleChange(e) {
    setForm({ ...form, [e.target.name]: e.target.value });
  }

  async function handleSubmit(e) {
    e.preventDefault();
    if (
      form.title === "" ||
      form.industry === "" ||
      form.seniority === "" ||
      form.location === ""
    ) {
      setErrMessage("Please fill in all fields!");
      return;
    }
    if (!isConvertibleToInt(form.seniority)){
      setErrMessage("Years of experience should be a number!");
      return;
    }
    const response = await fetch(BACKEND_URL + "/job_listings/", {
      method: "PUT",
      headers: {
        "Content-Type": "application/json",
        Authorization: `Bearer ${accessToken}`,
      },
      body: JSON.stringify(form),
    });
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

        <h2 className="text-2xl font-semibold mb-4">Edit Job Posting Info</h2>
        <ErrorMessage message={errMessage} />
        <form onSubmit={handleSubmit} className="space-y-4">
          <div>
            <label className="block text-sm font-medium text-gray-700">
              Title
            </label>
            <textarea
              name="title"
              value={form.title}
              onChange={handleChange}
              className="mt-1 block w-full border border-gray-300 rounded px-3 py-2"
            />
          </div>

          <div>
            <label className="block text-sm font-medium text-gray-700">
              Location
            </label>
            <input
              name="location"
              value={form.location}
              onChange={handleChange}
              className="mt-1 block w-full border border-gray-300 rounded px-3 py-2"
            />
          </div>

          <div>
            <label className="block text-sm font-medium text-gray-700">
              Industry
            </label>
            <textarea
              name="industry"
              value={form.industry}
              onChange={handleChange}
              className="mt-1 block w-full border border-gray-300 rounded px-3 py-2"
            />
          </div>

          <div>
            <label className="block text-sm font-medium text-gray-700">
              Preferred years of experience
            </label>
            <input
              name="seniority"
              value={form.seniority}
              type="number"
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

function DeleteJobPopUp({ job, accessToken, onClose, onSave}){

  async function handleSubmit(e) {
    e.preventDefault();
    const response = await fetch(BACKEND_URL + "/job_listings/" + job["_id"], {
      method: "DELETE",
      headers: {
        Authorization: `Bearer ${accessToken}`,
      },
    });
    onSave();
    onClose();
  }

  return (
    <div className="fixed inset-0 bg-opacity-40 backdrop-blur-sm flex items-center justify-center z-50">
      <div className="bg-white w-full max-w-md p-6 rounded-xl shadow-lg">
        <h2 className="text-2xl font-semibold text-center mb-4">
          Delete this job posting?
        </h2>

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

function AddJobPopUp({ accessToken, onClose, onSave }) {
  const [form, setForm] = useState({
    title: "",
    company: "",
    industry: "", // cannot change email
    seniority: "",
    location: "",
  });

  const [errMessage, setErrMessage] = useState(null);

  function handleChange(e) {
    setForm({ ...form, [e.target.name]: e.target.value });
  }

  async function handleSubmit(e) {
    e.preventDefault();
    if (
      form.title === "" ||
      form.industry === "" ||
      form.seniority === "" ||
      form.location === ""
    ) {
      setErrMessage("Please fill in all fields!");
      return;
    }
    if (!isConvertibleToInt(form.seniority)){
      setErrMessage("Years of experience should be a number!");
      return;
    }

    const response = await fetch(BACKEND_URL + "/job_listings/", {
      method: "POST",
      headers: {
        "Content-Type": "application/json",
        Authorization: `Bearer ${accessToken}`,
      },
      body: JSON.stringify(form),
    });

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

        <h2 className="text-2xl font-semibold mb-4">
          Add New Job Posting Info
        </h2>

        <ErrorMessage message={errMessage} />

        <form onSubmit={handleSubmit} className="space-y-4">
          <div>
            <label className="block text-sm font-medium text-gray-700">
              Title
            </label>
            <textarea
              name="title"
              value={form.title}
              onChange={handleChange}
              className="mt-1 block w-full border border-gray-300 rounded px-3 py-2"
            />
          </div>

          <div>
            <label className="block text-sm font-medium text-gray-700">
              Location
            </label>
            <input
              name="location"
              value={form.location}
              onChange={handleChange}
              className="mt-1 block w-full border border-gray-300 rounded px-3 py-2"
            />
          </div>

          <div>
            <label className="block text-sm font-medium text-gray-700">
              Industry
            </label>
            <textarea
              name="industry"
              value={form.industry}
              onChange={handleChange}
              className="mt-1 block w-full border border-gray-300 rounded px-3 py-2"
            />
          </div>

          <div>
            <label className="block text-sm font-medium text-gray-700">
              Preferred years of experience
            </label>
            <input
              name="seniority"
              value={form.seniority}
              type="number"
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

function ShowPersonPopUp({ person, accessToken, onClose, onSave }) {
  const [applicant, setApplicant] = useState(null);

  async function acceptApplicant(action) {
    const response = await fetch(
      BACKEND_URL + "/job_listings/select/" + action,
      {
        method: "PUT",
        headers: {
          Authorization: `Bearer ${accessToken}`,
          "Content-Type": "application/json",
        },
        body: JSON.stringify({
          id: person[Object.keys(person)[0]][0], //job id
          email: Object.keys(person)[0], // email
        }),
      }
    );

    const data = await response.json();
    onSave();
    onClose();
  }

  useEffect(() => {
    async function ViewApplicant() {
      const response = await fetch(
        BACKEND_URL + "/job_seekers/" + Object.keys(person)[0],
        {
          method: "GET",
        }
      );

      const data = await response.json();

      if (data) {
        ["password", "applied", "accepted"].forEach((key) => delete data[key]);
        console.log("data", data);
        setApplicant(data);
      }
    }

    ViewApplicant();
  }, []);
  if (applicant === null) {
    return (
      <div className="min-h-screen flex items-center justify-center bg-[#cdd7ff]">
        <p className="text-lg font-medium text-gray-700">
          Loading company data...
        </p>
      </div>
    );
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

        <h2 className="text-2xl font-semibold mb-4">
          {queryToName(person[Object.keys(person)[0]][1])}
        </h2>
        <p className="text-sm text-gray-600 mb-2">
          <strong>Full Name:</strong>{" "}
          {queryToName(applicant["first"] + " " + applicant["last"])}
        </p>
        <p className="text-sm text-gray-600 mb-2">
          <strong>Email:</strong> {Object.keys(person)[0]}
        </p>
        <p className="text-sm text-gray-600 mb-2">
          <strong>Preferred years of experience:</strong> {applicant["years"]}
        </p>
        <p className="text-sm text-gray-600 mb-2">
          <strong>Expertise:</strong> {queryToName(applicant["expertise"])}
        </p>
        <div className="flex justify-center space-x-4 mt-6">
          <button
            onClick={() => {
              acceptApplicant("reject");
            }}
            type="button"
            className="bg-gray-200 text-gray-800 px-4 py-2 rounded hover:bg-gray-300 flex items-center space-x-1"
          >
            Reject❌
          </button>
          <button
            className="bg-blue-500 text-white px-4 py-2 rounded hover:bg-blue-600 flex items-center space-x-1"
            onClick={() => {
              acceptApplicant("accept");
            }}
          >
            Accept✅
          </button>
        </div>
      </div>
    </div>
  );
}

function Companies() {
  const [company, setCompany] = useState(null);
  const [loading, setLoading] = useState(true);
  const [postings, setPostings] = useState([]);
  const [applicants, setApplicants] = useState([]);
  const [currentJobView, setCurrentJobView] = useState(null);
  const [currentCompanyView, setCurrentCompanyView] = useState(null);
  const [currentEditJobView, setEditJobView] = useState(null);
  const [currentDeleteJobView, setDeleteJobView] = useState(null);
  const [currentAddJobView, setAddJobView] = useState(null);
  const [currentPersonView, setPersonView] = useState(null);
  const [reloadTrigger, setReloadTrigger] = useState(0);

  const [cookies] = useCookies();
  const accessToken = cookies.accessToken;
  const userEmail =  cookies.userEmail;
  const COMPANY_EMAIL = userEmail;

  function editCompany(company){
    setCurrentCompanyView(company);
  }

  function showJobDetails(job) {
    setCurrentJobView(job);
  }

  function editJobDetails(job) {
    setEditJobView(job);
  }

  function deleteJob(job) {
    setDeleteJobView(job);
  }

  function addJob(job) {
    setAddJobView(job);
  }

  function viewApplicant(person) {
    setPersonView(person);
  }

  useEffect(() => {
    async function loadData() {
      // Step 1: Get company info
      const companyFind = await fetch(BACKEND_URL + "/companies/" + COMPANY_EMAIL, {
        method: "GET",
        headers: {
          Authorization: `Bearer ${accessToken}`,
        },

      });

      const companyData = await companyFind.json();
      setCompany(companyData);

      // Step 2: Get job listings
      const details = await fetch(BACKEND_URL + "/job_listings/show_details", {
        method: "GET",
        headers: {
          Authorization: `Bearer ${accessToken}`,
        },
      });

      const jobData = await details.json();

      setPostings(jobData[0]);
      setApplicants(jobData[1]);
      setLoading(false);
    }
    loadData();
  }, [reloadTrigger]); // Runs all logic together when reloadTrigger changes

  if (loading) {
    return (
      <div className="min-h-screen flex items-center justify-center bg-[#cdd7ff]">
        <p className="text-lg font-medium text-gray-700">
          Loading company data...
        </p>
      </div>
    );
  }
  return (
    <div className="min-h-screen bg-[#cdd7ff] p-6 space-y-6">
      {/* Company Profile */}
      <div className="bg-white rounded-2xl shadow-md p-6 w-full max-w-4xl mx-auto">
        <div className="flex justify-between items-center">
          <h2 className="text-xl font-semibold">Company Profile</h2>
          <button
            className="text-sm text-blue-600 hover:underline"
            onClick={() => editCompany(company)}
          >
            ✏️ Edit
          </button>
        </div>
        <div className="mt-4 grid grid-cols-2 gap-y-2 text-sm text-gray-700">
          <div>
            <p className="font-medium">Company Name</p>
            <p>{queryToName(company["name"])}</p>
          </div>
          <div>
            <p className="font-medium">Email</p>
            <p>{company["email"]}</p>
          </div>
          <div>
            <p className="font-medium">Description</p>
            <p>{company["description"]}</p>
          </div>
          <div>
            <p className="font-medium">Location</p>
            <p>{company["country"]}</p>
          </div>
        </div>
      </div>

      {/* Recent Job Postings */}
      {currentJobView && (
        <ShowPopUp
          job={currentJobView}
          accessToken={accessToken}
          onClose={() => setCurrentJobView(null)}
        />
      )}
      {currentCompanyView && (
        <EditCompanyPopUp
          company={currentCompanyView}
          onClose={() => {
            setCurrentCompanyView(null);
          }}
          onSave={() => setReloadTrigger((prev) => prev + 1)}
        />
      )}
      {currentEditJobView && (
        <EditJobPopUp
          job={currentEditJobView}
          accessToken={accessToken}
          onClose={() => {
            setEditJobView(null);
          }}
          onSave={() => setReloadTrigger((prev) => prev + 1)}
        />
      )}
      {currentDeleteJobView && (
        <DeleteJobPopUp
          job={currentDeleteJobView}
          accessToken={accessToken}
          onClose={() => {
            setDeleteJobView(null);
          }}
          onSave={() => setReloadTrigger((prev) => prev + 1)}
        />
      )}
      {currentAddJobView && (
        <AddJobPopUp
          accessToken={accessToken}
          onClose={() => {
            setAddJobView(null);
          }}
          onSave={() => setReloadTrigger((prev) => prev + 1)}
        />
      )}
      {currentPersonView && (
        <ShowPersonPopUp
          person={currentPersonView}
          accessToken={accessToken}
          onClose={() => {
            setPersonView(null);
          }}
          onSave={() => setReloadTrigger((prev) => prev + 1)}
        />
      )}
      <div className="bg-white rounded-2xl shadow-md p-6 w-full max-w-4xl mx-auto">
        <div className="flex justify-between items-center mb-4">
          <h2 className="text-xl font-semibold">Recent Job Postings</h2>
          <button
            className="text-sm text-white bg-blue-500 hover:bg-blue-600 px-4 py-1 rounded"
            onClick={() => {
              addJob(accessToken);
            }}
          >
            ➕ Post New Job
          </button>
        </div>
        <table className="w-full text-left text-sm">
          <thead>
            <tr className="border-b">
              <th className="py-2">Position</th>
              <th className="py-2">Applicants</th>
              <th className="py-2">Selected</th>
              <th className="py-2">Actions</th>
            </tr>
          </thead>
          <tbody className="max-h-[30vh] overflow-y-auto">
            {postings.map((job, idx) => (
              <tr key={idx} className="border-b">
                <td className="py-2">{queryToName(job.title)}</td>
                <td className="py-2">{job.applicants.length}</td>
                <td className="py-2 space-x-2">
                  <button
                    className="text-blue-600 hover:underline"
                    onClick={() => showJobDetails(job)}
                  >
                    👁 View
                  </button>
                  <button
                    className="text-yellow-600 hover:underline"
                    onClick={() => editJobDetails(job)}
                  >
                    ✏️ Edit
                  </button>
                  <button
                    className="text-red-600 hover:underline"
                    onClick={() => deleteJob(job)}
                  >
                    🗑 Delete
                  </button>
                </td>
              </tr>
            ))}
          </tbody>
        </table>
      </div>

      {/* Recent Applicants */}
      <div className="bg-white rounded-2xl shadow-md p-6 w-full max-w-4xl mx-auto">
        <h2 className="text-xl font-semibold mb-4">Recent Applicants</h2>
        <div className="space-y-3 max-h-[30vh] overflow-y-auto">
          {applicants.map((person, idx) => (
            <div
              key={idx}
              className="flex items-center justify-between border rounded-lg p-3"
            >
              <div className="text-sm">
                <p className="font-medium">{Object.keys(person)[0]}</p>
                <p className="text-gray-600">
                  {queryToName(person[Object.keys(person)[0]][1])}
                </p>
              </div>
              <button
                className="bg-blue-400 hover:bg-blue-500 text-white px-4 py-1 rounded"
                onClick={() => viewApplicant(person)}
              >
                👀 View
              </button>
            </div>
          ))}
        </div>
      </div>

    </div>
  );
}

export default Companies;
