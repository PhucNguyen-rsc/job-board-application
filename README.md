# Job Board API

The Job Board API is a Flask REST API server designed to connect companies with job seekers. It enables companies to post job openings and manage applicants, while empowering job seekers to find and apply for jobs, receive personalized AI-driven suggestions, and track their application status.

## Members
* Minseok Kim
* Junyong Moon
* Phuc Nguyen
* Event Sharku

## Features

### Core Functionality
* **Job Seeker Management**: Users can sign up, log in, and manage their profiles. They can search for job listings, apply to positions, and view the status of their applications. The schema for job seekers includes first name, last name, unique email, expertise, years of experience, password, and lists for `applied` and `accepted` jobs.
* **Company Management**: Companies can sign up, log in, and manage their profiles. They can post new job listings, update existing ones, view applicants for their jobs, and select candidates. The schema for companies includes a unique name, unique email, country, optional description, and password.
* **Job Listing Management**: Provides endpoints for searching, creating, updating, retrieving details, and deleting job listings. Job listings include fields like title, company, location, industry, seniority, and lists for `applicants` and `selected` candidates. All job listing fields are converted to slug format for search functionality.
* **Authentication & Authorization**: All protected endpoints require a JWT token for access, ensuring that users can only perform actions relevant to their account type (job seeker or company) and their own data. Email and company name uniqueness are enforced during signup, and email validation is in place. Specific authorization rules ensure job seekers only view their own status, and companies only manage their own job listings and applicants.

### AI-Powered Job Suggestions
* **Personalized Recommendations**: Leverages Google's Gemini 1.5 Flash API to provide tailored job preparation suggestions for job seekers.
* **Tailored Insights**: When viewing a job listing, users can click an "AI Suggestion" button to receive an analysis based on job details (title, company, location, industry, required experience) and applicant details (name, expertise, years of experience).
* **Actionable Advice**: The AI provides specific improvement suggestions and key strengths to emphasize, formatted in JSON. Although a match score is calculated internally, the system focuses on qualitative analysis and suggestions for accuracy and user understanding.

## Tech Stack

This Flask web app utilizes:

* [Flask-RESTx](https://flask-restx.readthedocs.io/en/latest/quickstart.html) for building REST APIs, with automatic OpenAPI (Swagger UI) specification generation.
* [PyMongo](https://pymongo.readthedocs.io/en/stable/) for MongoDB database interaction.
* [Pytest](https://docs.pytest.org/en/stable/) for comprehensive testing.
* [mongomock](https://docs.mongoengine.org/guide/mongomock.html) for mocking MongoDB during unit testing.
* Google's Gemini 1.5 Flash API for AI functionality.

## Pre-requisites

* Python 3.10 or higher
* MongoDB installed locally

## Running Locally

Ensure MongoDB is running before starting the server.

### Setting up the environment

1.  Refer to `app/.sampleenv` to create your `app/.env` file.
2.  Run `make dev_env` to set up a virtual environment and install dependencies.

### Running the server

1.  Execute `make prod` to start the server. This command also runs tests prior to starting the server.
2.  Access the running server at [http://127.0.0.1:8000](http://127.0.0.1:8000).
3.  Stop the server using `Ctrl+C` (or `Cmd+C` on macOS).

### Testing the API server

* Run `make tests` to execute the test suite and view the coverage report in the terminal. A visual report is also available by opening `/coverage_html_report/index.html` in your browser.
* The system has achieved an overall test coverage of 98%, with 94% for companies API and 97% for job seekers API endpoints.
* Specific integration tests cover scenarios like a company creating a job post and a job seeker applying and viewing updated status.
* System-browser testing is also included, simulating workflows like a company user signing up via the UI. To run locally, start the frontend, then the backend, then run `make tests-browser`.

### Manually activating and deactivating the virtual environment

* **Activate**: `source .venv/bin/activate`
* **Deactivate**: `deactivate`

## API Endpoints and Documentation

The API includes comprehensive documentation via Swagger UI.

1.  Start the server using `make prod`.
2.  Navigate to [http://127.0.0.1:8000](http://127.0.0.1:8000) in your browser.
3.  Expand endpoints, use "Try it out," fill in fields, and click "Execute" to test directly in the interface.

The API endpoints are categorized into Job Seekers API, Companies API, and Job Listing API. Full lists of endpoints for each API type are available in the Deliverable 1 and Deliverable 2 reports.

## Security and Quality Assurance

* **SAST (Static Application Security Testing) Tools**:
    * **Bandit**: Used for Python code security analysis.
    * **Trivy**: Utilized for vulnerability scanning of container images and file systems.
    * **Checkov**: Employed for static analysis of infrastructure-as-code (IaC) to ensure security and compliance.
    * Results before and after remediation efforts are detailed in the D4 report.
* **DAST (Dynamic Application Security Testing) Tools**:
    * Dynamic scans were conducted to identify runtime vulnerabilities. Analysis confirmed that several flagged alerts were false positives after investigation, affirming the robustness of implemented security measures.
* **JMeter**: Performance testing was conducted using JMeter, with detailed results and analysis available in the `JMeter.pdf` file within the `reports/` folder.

## Continuous Deployment

* The application is deployed on a Digital Ocean VM using **Docker**.
* The deployed API server is accessible at `http://209.38.120.214:8000/`.
* The deployed frontend is accessible at `http://209.38.120.214:3000/`.
* Continuous Integration (CI) is implemented for the repository, with screenshots of both failed and successful builds available.

## A/B Testing and User Feedback

* **A/B Testing Setup**: An A/B testing framework evaluates the LLM functionality. Users are randomly assigned to a `standard` group (Group A) with the standard website experience or an `llm` group (Group B) which accesses the AI feature. Group assignments are persisted using cookies.
* **User Survey**: A Google Forms survey collects user feedback, with slightly varied questions for each group.
* **Metric Collection**: Key metrics tracked include user participation distribution, application conversion rate, user satisfaction, "AI Tips" button engagement, and decision impact rate. Data collection is automated through API endpoints.
* **Results and Analysis**:
    * **User Participation**: Distribution was 41.7% in Group A and 58.3% in Group B.
    * **Application Conversion Rate**: Group A averaged 2.3 applications per user, while Group B averaged 1.36, suggesting users with AI tips were more selective.
    * **User Satisfaction**: Group A reported an average satisfaction of 4.0, while Group B reported 4.71 (17.8% increase), indicating substantial enhancement to user experience.
    * **AI Tips Button Engagement**: 100% of Group B users clicked the "AI Tips" button at least once, demonstrating high interest.
    * **Impact on Application Decisions**: 71.4% of Group B users reported that AI advice directly impacted their application decisions, confirming that the feature provides actionable insights that users trust enough to affect their behavior.
    * **More Selective Application Behavior**: Users with AI guidance submitted fewer applications on average, potentially leading to higher quality applications and better matches.
## Demo Link:
[Youtube link](https://www.youtube.com/watch?v=h8Pjd4KBW7E)

## Future Plans

Based on promising A/B testing results, future plans include:
1.  Refining the AI suggestions algorithm to further improve relevance and specificity.
2.  Expanding the feature to provide tailored advice at different stages of the application process.
3.  Adding comparative analysis capabilities to help users prioritize between multiple potential positions.
4.  Integrating resume-specific suggestions to align applicant materials with job requirements.
5.  Conducting longitudinal studies to measure the impact on job placement success rates.
