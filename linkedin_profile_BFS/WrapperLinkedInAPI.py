

#from linkedin_api import Linkedin
from linkedin_api import Linkedin
import os
import pickle

import anthropic
import cohere

USERNAME = "shah.jaidev00@gmail.com"
PASSWORD = os.environ.get('LINKEDIN_PASSWORD')

ANTHROPIC_API_KEY = os.environ.get('ANTHROPIC_API_KEY')
COHERE_API_KEY = os.environ.get('COHERE_API_KEY')

claude = anthropic.Client(os.environ.get('ANTHROPIC_API_KEY'))
co = cohere.Client(os.environ.get('COHERE_API_KEY'))



class MyLinkedInAPI:
    def __init__(self, username, password):
        self.username = username
        self.password = password
        self.api = Linkedin(username, password)

    def get_profile_urn(self, profile_response):
        profile_urn_string = profile_response['profile_urn']
        profile_urn = profile_urn_string.split(":")[3]
        return profile_urn
    
    def get_profile_connections(self, profile_urn, keywords=None):
        connections = self.api.get_profile_connections(profile_urn)
        return connections
    
    def get_cleaned_profile_summary(self, profile_name):
        profile_dict= self.api.get_profile(profile_name)

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
        response = claude.completion(
            prompt=f"{anthropic.HUMAN_PROMPT} {summarization_prompt}{anthropic.AI_PROMPT}",
            stop_sequences=[anthropic.HUMAN_PROMPT],
            model="claude-instant-v1",
            max_tokens_to_sample=max_tokens_to_sample,
        )

        resp_summary = response['completion']

        #Return the summary
        return resp_summary

   

    def claude_extract_keywords(self, profile_name):
        profile_dict= self.api.get_profile(profile_name)
        summarization_prompt = f"Clean up and summarize the below LinkedIn Profile such that all the key parts that are important when networking are retained:\n" \
                    f"{profile_dict}\n" \
                    "Profile Summary: "   
        
        #Call the Claude API to summarize the profile
        max_tokens_to_sample = 1000
        response = claude.completion(
            prompt=f"{anthropic.HUMAN_PROMPT} {summarization_prompt}{anthropic.AI_PROMPT}",
            stop_sequences=[anthropic.HUMAN_PROMPT],
            model="claude-instant-v1",
            max_tokens_to_sample=max_tokens_to_sample,
        )
        resp_summary = response['completion']

        prompt_for_keywords= f"Given this LinkedIn profile: {resp_summary}, Extract the 5 most relevant keywords as a list of strings from this persons profile that would help him find good connections to network with: "
        
        max_tokens_to_sample = 300
        resp_keywords = claude.completion(
            prompt=f"{anthropic.HUMAN_PROMPT} {prompt_for_keywords}{anthropic.AI_PROMPT}",
            stop_sequences=[anthropic.HUMAN_PROMPT],
            model="claude-instant-v1",
            max_tokens_to_sample=max_tokens_to_sample,
        )

        resp_keywords = resp_keywords['completion']
        print("Extracted Keywords")
        print(resp_keywords)
        return resp_keywords


    def get_job_posting(self, job_id):
        job_posting_dict = self.api.get_job(job_id)
        summarization_prompt = f"Clean up the below Job Posting such that all the key parts are retained:\n" \
                    f"{job_posting_dict}\n" \
                    "Job Posting Cleaned: "   
        
        #Call the Claude API to summarize the profile
        max_tokens_to_sample = 3000
        response = claude.completion(
            prompt=f"{anthropic.HUMAN_PROMPT} {summarization_prompt}{anthropic.AI_PROMPT}",
            stop_sequences=[anthropic.HUMAN_PROMPT],
            model="claude-v1",
            max_tokens_to_sample=max_tokens_to_sample,
        )
        resp_job_posting = response['completion']

        print(resp_job_posting)
        return resp_job_posting

 


    def intro_generation(self, candidate_profile_url, lead_profile_url, user_free_form_text):
        candidate_profile_name = candidate_profile_url.split("/")[-1]
        candidate_summary = self.get_cleaned_profile_summary(candidate_profile_name)

        lead_profile_name = lead_profile_url.split("/")[-1]
        lead_summary = self.get_cleaned_profile_summary(lead_profile_name)


        prompt = f"Assume you are a candidate looking for a job.  Write a warm personalized introduction message to the lead profile, that includes commonalities between the two of you, relevance to their own work and title, and and explaining why your skills would be a good fit for his team and the role you are interested in." \
                f"Here are the descriptions for each the candidate and the lead:\n\n" \
                    f"Candidate: {candidate_summary}\n\n" \
                    f"Lead: {lead_summary}" \
                    f"And here is the candidate's aspiration: {user_free_form_text}"
        
        # Call the Claude API to generate an intro
        max_tokens_to_sample: int = 1000
        resp = claude.completion(
            prompt=f"{anthropic.HUMAN_PROMPT} {prompt}{anthropic.AI_PROMPT}",
            stop_sequences=[anthropic.HUMAN_PROMPT],
            model="claude-v1",
            max_tokens_to_sample=max_tokens_to_sample,
        )

        print(resp)

        return resp['completion']

    def recommended_profiles(self,free_form_text, profile_name):
        profile_dict= self.api.get_profile(profile_name)
        profile_urn = self.get_profile_urn(profile_dict)
        cleaned_profile_summary = self.get_cleaned_profile_summary(profile_name)
        keywords = self.claude_extract_keywords(profile_name)
        pass 
        
def main():
    myapi_wrapper = MyLinkedInAPI(USERNAME, PASSWORD)
    """
    test_job_id = 3595709943
    print("Job Posting")
    cleaned_posting = myapi_wrapper.get_job_posting(test_job_id)
    print(cleaned_posting)

    print("Profile Summary")
    profile_summary = myapi_wrapper.get_cleaned_profile_summary("ranganm")
    print(profile_summary)

    print("Keywords")
    keywords = myapi_wrapper.claude_extract_keywords("ranganm")
    print(keywords)
    """

    user_free_form_text = "Looking for opportunities where I can use my applied machine learning skills at scale"
    intro_generated = myapi_wrapper.intro_generation("shahjaidev", "linjuny", user_free_form_text)
    print(intro_generated)




main()



"""

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
    for r in results:
        print(f"Document: {r.document}")
        print(f"Relevance Score: {r.relevance_score}")

    return results  
"""