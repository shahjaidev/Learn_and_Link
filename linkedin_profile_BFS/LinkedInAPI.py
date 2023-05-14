

#from linkedin_api import Linkedin
from linkedin_api import Linkedin
import os
import pickle

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
    
    def get_profile_summart(self, profile_name):
        profile_response = self.api.get_profile(profile_name)

        #TO-DO, finish this function
        return profile_response
    
    def k_hop_connections_with_keywords(self, profile_urn, keywords=None, execute_third_hop=False):
        
        connections_with_filter = self.api.get_profile_connections(self.this_profile_id, network_depths=['F', 'S'], keywords = ["computer science"])
        second_degree = []
        for connection in connections_with_filter:
            second_degree.extend(self.api.get_profile_connections(connection['urn_id']) )

        if not execute_third_hop:
            print(second_degree)
            return second_degree
        
        third_degree = []
        for connection in second_degree:
            third_degree.extend(self.api.get_profile_connections(connection['urn_id']))

        print(third_degree)
        return third_degree
    

