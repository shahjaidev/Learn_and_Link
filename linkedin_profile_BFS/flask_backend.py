# Import Flask and request libraries
from flask import Flask, request
# Import Anthropic Claude API
from anthropic import Claude

from customized_linkedinAPI import LinkedIn
import os

from LinkedInAPI import LinkedInAPI

app = Flask(__name__)

# Create a Claude instance with your API key
claude = Claude(api_key="your_api_key")

USERNAME = "shahjaidev"
PASSWORD = os.environ.get('LINKEDIN_PASSWORD')



linkedinAPIinstance = LinkedInAPI(USERNAME, PASSWORD)


# Define a route for the app
@app.route("/", methods=["POST"])
def index():
    # Get the input paragraph from the request body
    paragraph = request.get_json().get("paragraph")
    # Call the Claude API to extract keywords and types
    keywords = claude.extract_keywords(paragraph)
    # Return the keywords and types as a list of tuples
    return str(keywords)


# Define a route for getting 2nd degree connections
@app.route("/connections", methods=["GET"])
def connections():
    # Get the authorization code from the query string
    code = request.args.get("code")
    # Exchange the code for an access token and a refresh token
    access_token, refresh_token = linkedin.get_tokens(code)
    # Get the user's profile information
    profile = linkedin.get_profile(access_token)
    # Get the user's 1st degree connections
    connections = linkedin.get_connections(access_token)
    # Get the user's 2nd degree connections by finding people who are connected to their connections
    second_degree_connections = linkedin.get_second_degree_connections(access_token, connections)
    # Return the 2nd degree connections as a list of profiles
    return str(second_degree_connections)


# Define a route for generating a cover letter
@app.route("/cover-letter", methods=["POST"])
def cover_letter():
    # Get the input text from the request body
    text = request.get_json().get("text")

    #APPEND the text to 

    #Get the job posting from the request body
    job_posting = request.get_json().get("job_posting")

    # Create a prompt for Claude to generate a cover letter
    prompt = f"Write a cover letter based on the following information about the candidate and the job posting:\n\n" \
                f"Candidate: {text}\n\n" \
                f"Job Posting: {text}" \
                "Cover Letter: "
    
    print(prompt)
    
   
    # Call the Claude API to generate a cover letter
    cover_letter = claude.generate_text(prompt)

    # Return the cover letter as a PDF file
    return cover_letter




def summarize_linkedin_profile(profile_dict):
    #Use Claude to summarize the profile

    keys_to_keep = ['industryName', 'lastName', 'firstName', 'geoLocationName', 'headline', 'experience', 'education', 'projects']
    filtered_profile_dict = {key: profile_dict[key] for key in profile_dict if key in keys_to_keep}


    # the values of the dictionary
    profile_summary = str(filtered_profile_dict) 

    #Create a prompt for Claude to summarize the profile
    prompt = f"Summarize the following LinkedIn profile to capture the key parts:\n\n" \
                f"{profile_summary}\n\n" \
                "Summary: "   
    
    #Call the Claude API to summarize the profile
    summary = claude.generate_text(prompt)

    #Return the summary
    return summary
