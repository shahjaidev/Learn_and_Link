# Import Flask and request libraries
from flask import Flask, request
# Import Anthropic Claude API
import anthropic

import cohere

# from customized_linkedinAPI import LinkedIn
import os

from LinkedInAPI import MyLinkedInAPI

app = Flask(__name__)

ANTHROPIC_API_KEY = os.environ.get('CLAUDE_API_KEY')
COHERE_API_KEY = os.environ.get('COHERE_API_KEY')

claude = anthropic.Client(os.environ.get('ANTHROPIC_API_KEY'))
co = cohere.Client(os.environ.get('COHERE_API_KEY'))


USERNAME = "shah.jaidev00@gmail.com"
PASSWORD = os.environ.get('LINKEDIN_PASSWORD')

myAPIWrapper = MyLinkedInAPI(USERNAME, PASSWORD)

# Define a route for the app
@app.route("/", methods=["POST"])
def index():
    # Get the input paragraph from the request body
    paragraph = request.get_json().get("paragraph")
    # Call the Claude API to extract keywords and types
    keywords = claude.extract_keywords(paragraph)
    # Return the keywords and types as a list of tuples
    return str(keywords)


# Define a route for getting recommended profiles
# @app.route("/recommended_profiles", methods=["GET"])
def recommended_profiles():

    return recommended_profiles

# Define a route for generating a cover letter
@app.route("/cover-letter", methods=["POST"])
def cover_letter():
    # Get the input text from the request body
    user_free_form_text = request.get_json().get("user_free_form_text")
    user_linkedin_profile_url = request.get_json().get("user_linkedin_profile_url")
    #extract the profile name from the url
    user_profile_name = user_linkedin_profile_url.split("/")[-1]
    #get the profile summary from the linkedin API
    user_profile_summary = myAPIWrapper.get_profile_summary(user_profile_name)

    ##APPEND the summarized profile dict to the user_intentions_text

    #Get the job posting from the request body
    job_posting_url = request.get_json().get("job_posting")

    job_posting_summary = myAPIWrapper.get_job_posting(job_posting_url)

    # Create a prompt for Claude to generate a cover letter
    prompt = f"Write a cover letter based on the following information about the candidate and the job posting:\n\n" \
                f"Candidate Profile Summary: {user_profile_summary}\n\n" \
                f"Job Posting Summary: {job_posting_summary}" \
                "Cover Letter: "
    
    print(prompt)
    
    # Call the Claude API to generate a cover letter
    cover_letter = claude.generate_text(prompt)

    # Return the cover letter as a PDF file
    return cover_letter

@app.route("/intro", methods=["POST"])
def intro():
    candidate_profile_url = request.get_json().get("user_linkedin_profile_url")
    candidate_profile_name = candidate_profile_url.split("/")[-1]
    candidate_summary = myAPIWrapper.get_profile_summary(candidate_profile_name)

    lead_summary = request.get_json().get("lead_linkedin_profile_url")
    lead_profile_name = lead_summary.split("/")[-1]
    lead_summary = myAPIWrapper.get_profile_summary(lead_profile_name)

    user_free_form_text = request.get_json().get("user_free_form_text")

    prompt = f"Pretend like you are a warm and welcoming recruiter.  Write a concise introduction message from a candidate to a lead tailored to the candidate's aspiration." \
             f"Here are the descriptions for each the candidate and the lead:\n\n" \
                f"Candidate: {candidate_summary}\n\n" \
                f"Lead: {lead_summary}" \
                f"And here is the candidate's aspiration: {user_free_form_text}"
    
    # Call the Claude API to generate an intro
    max_tokens_to_sample: int = 1000
    resp = claude.completion(
        prompt=f"{anthropic.HUMAN_PROMPT} {prompt}{anthropic.AI_PROMPT}",
        stop_sequences=[anthropic.HUMAN_PROMPT],
        model="claude-instant-v1",
        max_tokens_to_sample=max_tokens_to_sample,
    )

    print(resp)

    return resp['completion']


def summarize_linkedin_profile(profile_dict):
    #Use Claude to summarize the profile

    keys_to_keep = ['industryName', 'lastName', 'firstName', 'geoLocationName', 'headline', 'experience', 'education', 'projects']
    filtered_profile_dict = {key: profile_dict[key] for key in profile_dict if key in keys_to_keep}

    # the values of the dictionary
    filtered_profile_dict_str = str(filtered_profile_dict) 

    #Create a prompt for Claude to summarize the profile
    summarization_prompt = f"Clean up and summarize the below LinkedIn Profile such that all the key parts that are important when networking are retained:\n" \
                f"{filtered_profile_dict_str}\n" \
                "Profile Summary: "   
    
    #Call the Claude API to summarize the profile
    max_tokens_to_sample = 1000
    resp_summary = claude.completion(
        prompt=f"{anthropic.HUMAN_PROMPT} {summarization_prompt}{anthropic.AI_PROMPT}",
        stop_sequences=[anthropic.HUMAN_PROMPT],
        model="claude-instant-v1",
        max_tokens_to_sample=max_tokens_to_sample,
    )

    #Return the summary
    return resp_summary


def cohere_rerank():

    # define the query and the documents
    query = 'What is the capital of the United States?'
    docs = ['Carson City is the capital city of the American state of Nevada.',
            'The Commonwealth of the Northern Mariana Islands is a group of islands in the Pacific Ocean. Its capital is Saipan.',
            'Washington, D.C. (also known as simply Washington or D.C., and officially as the District of Columbia) is the capital of the United States. It is a federal district.',
            'Capital punishment (the death penalty) has existed in the United States since before the United States was a country. As of 2017, capital punishment is legal in 30 of the 50 states.',
            'The capital city of Canada is Ottawa, Ontario.',
            'The capital city of France is Paris.']

    # rerank the documents based on semantic relevance
    results = co.rerank(query=query, documents=docs, top_n=5, model='rerank-english-v2.0')

    # print the reranked documents and their scores
    for result in results:
        print(f"Document: {result.document}")
        print(f"Relevance Score: {result.score}")

    return results




def claude_extract_keywords():
    linkedin_profile_test_dict= """ Here is a cleaned up summary of the LinkedIn profile:

Hersh Arora Engineering Manager at Uber New York, New York

Experience: Engineering Manager II at Uber July 2022 - Present New York, United States

Director, Software Engineering at Purpose Advisor Solutions December 2020 - July 2022 New York, United States Built a team of 30+ members across UI/UX, microservices, API, security and infrastructure. Led the build of technology for client onboarding, funding, AML, custodian integration and fee calculation.

Manager, Software Engineering at Purpose Advisor Solutions May 2019 - November 2020 Toronto, Canada Area Led the engineering team building wealth management products. Helped enable the acquisition of Wealthsimple for Advisors by Purpose. Built products and technology to onboard W4A clients.

Technical Lead at Payworks Payroll Services Canada
May 2018 - May 2019 Toronto, Canada Area Led long-term company initiatives. Involved in coding, design reviews, sprint planning, team meetings, code reviews, delegating and mentoring. Followed Agile, CI and worked with Business Analysts, QA and UI/UX. Managed multiple complex projects. Implemented security initiatives.

Systems Developer at Payworks Payroll Services Canada
2013 - 2018
Toronto, Canada Area Re-built the core payroll processing product. Developed RESTful APIs, UI, responsive web design, microservices, SQL and internal tools.

Education: M.Sc. Computer Science, University of Manitoba
    """

    summarization_prompt = f"Clean up and summarize the below LinkedIn Profile such that all the key parts that are important when networking are retained:\n" \
                f"{linkedin_profile_test_dict}\n" \
                "Profile Summary: "   
    
    #Call the Claude API to summarize the profile
    max_tokens_to_sample = 1000

    resp_summary = claude.completion(
        prompt=f"{anthropic.HUMAN_PROMPT} {summarization_prompt}{anthropic.AI_PROMPT}",
        stop_sequences=[anthropic.HUMAN_PROMPT],
        model="claude-instant-v1",
        max_tokens_to_sample=max_tokens_to_sample,
    )


    prompt_for_keywords= f"Given this LinkedIn profile: {linkedin_profile_test}, Extract the most relevant keywords from this persons profile that would help him find good connections to network with: "
    
    max_tokens_to_sample = 10
    resp_keywords = claude.completion(
        prompt=f"{anthropic.HUMAN_PROMPT} {prompt_for_keywords}{anthropic.AI_PROMPT}",
        stop_sequences=[anthropic.HUMAN_PROMPT],
        model="claude-instant-v1",
        max_tokens_to_sample=max_tokens_to_sample,
    )
    print("Extracted Keywords")
    print(resp_keywords)
    return resp_keywords



def main():

    print(claude_extract_keywords())
    print(cohere_rerank())
    # print(summarize_linkedin_profile())
    # print(cover_letter())
    #print(intro())



main() 