

from linkedin_api import Linkedin
import os
import pickle

GLOBAL_PROFILE_DICT_PATH = './global_dict_all_profiles.pickle'

class LinkedInAPI:
    def __init__(self, username, password):
        self.api = Linkedin('shahjaidevn@gmail.com', password)
        self.username = username
        self.password = os.environ.get('LINKEDIN_PASSWORD')
        self.api = Linkedin(username, password)
        self.global_profile_dict = pickle.load(open(GLOBAL_PROFILE_DICT_PATH, "rb"))
        self.this_profile_urn = None 
        self.this_profile_json = None

    #def process_global_profile_dict(self):

    def display_global_profile_dict(self):
        print("Profile Names in global profile dict:")
        print(self.global_profile_dict.keys())
        
    
        
    def get_api_response_and_process_profile(self, profile_id):
        profile_response = self.api.get_profile(profile_id)
        self.this_profile_urn = profile_response['profile_id']
        self.this_profile_response_dict = dict(profile_response)

    






        





    


    def get_profile_urn(self, profile_response):
        profile_urn_string = profile_response['profile_urn']
        profile_urn = profile_urn_string.split(":")[3]
        return profile_urn
    
    def get_profile_connections(self, profile_urn):
        connections = self.api.get_profile_connections(profile_urn)
        return connections
