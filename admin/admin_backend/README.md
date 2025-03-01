# API Endpoints

### POST /jobs/create
**Description**: Create a new job posting.
**Authorization**: Required.
**Request Body**: JSON object containing job posting details.
**Response:**
201 Created: Job created successfully, returns the job ID.
400 Bad Request: Error in creating the job.

### GET /jobs/application
**Description**: Apply for a job using job ID and user ID.
**Query Parameters:**
jobid: ID of the job.
userid: ID of the user.
**Response**:
201 Created: Application submitted successfully.
400 Bad Request: Error in submitting the application.

### GET /jobs/segragate
**Description**: Segregate applications for a specific job.
**Authorization**: Required.
**Query Parameter**: jobid
**Response**:
200 OK: Returns the list of applications for the specified job.

### POST /jobs/shortlist
**Description**: Shortlist an application.
**Authorization**: Required.
**Query Parameters**:
applnid: ID of the application.
userid: ID of the user.
**Response**:
200 OK: Application shortlisted successfully.

### GET /jobs/collect
**Description**: Collect job posting details.
**Authorization**: Required.
**Query Parameter**: jobid
**Response**:
200 OK: Returns the job posting details.
