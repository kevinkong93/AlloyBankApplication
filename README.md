# Project: Alloy Application Form Sandbox

This project is a web app that allows users to submit a simulated  bank/finance application via Alloy’s sandbox API.

**Frontend**: HTML form rendered via Flask\
**Backend**: Flask handles form submission, sends data to Alloy /evaluations endpoint, and displays the outcome.\
**Sandbox mode**: all requests are simulated; 

### Flask Setup
- Flask project initialized (app.py)
- Form rendered using HTML templates
- Routes for form display and submission created
### Environment Variables / Secrets
- ALLOY_TOKEN and ALLOY_SECRET stored securely in environment variables
- Credentials not hardcoded in the repository
### GET /parameters Check (POST / GET in Developer page)
- Verified field names via Alloy’s sandbox parameters endpoint
- Cross-checked field names for POST payload
- Ensured correct JSON structure for required fields
### Form Fields & Validation
Fields captured:
- First Name / Last Name
- Address Line 1 & 2, City, State, Zip, Country
- SSN (9 digits)
- Email
- Date of Birth (YYYY-MM-DD)
- Frontend validations added where possible (ex: required fields, pattern matching)
### POST /evaluations Preparation
- Prepared payload using exact field names from GET /parameters
- Created dynamic headers for Basic Auth
- Ready to handle API responses:
  - "Approved" → Success screen
  - "Manual Review" → “We’ll be in touch shortly” screen
  - "Deny" → “Sorry, your application was not successful” screen
### Testing / Debugging
- Verified GET /parameters works on Alloy sandbox website
- Confirmed POST request payload matches expected fields
- Ensured all dependencies (Flask, requests) installed in virtual environment
### Security / Best Practices
- Environment variables for secrets
- .env file added to .gitignore
- Credentials never pushed to GitHub

File Structure  
1. python.py (Main Flask application)\
2. form.html (Form template)\
3. requirements.txt (Dependencies: Flask, requests, python-dotenv)\
4. README.md  (Project documentation)\
