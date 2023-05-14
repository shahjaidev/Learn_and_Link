#commands to set password
#export LINKEDIN_PASSWORD="password"


#from linkedin_api import Linkedin
from custom_linkedin_api import Linkedin

import os
import pickle

password = os.environ.get('LINKEDIN_PASSWORD')

# Authenticate using any Linkedin account credentials
api = Linkedin('shah.jaidev00@gmail.com', password)
#api = Linkedin('shahjaidev99@gmail.com', 'jaidu99999')

PUBLIC_PROFILE =  'ethereal-shah-636388276' #'ethereal-shah-636388276' #"shahjaidev" #"jaidev-shah-8952a1276" #"shahjaidev"
profile_response = api.get_profile(PUBLIC_PROFILE)
print(profile_response.keys())

profile_id = profile_response['profile_id']
print(f"Profile ID: {profile_id}")


#parse profile_urn to get the actual urn after the third colon
profile_urn_string = profile_response['profile_urn']
profile_urn = profile_urn_string.split(":")[3]
print(f"Profile URN: {profile_urn}")

print(f"Profile Response: \n {profile_response}")

# GET all connected profiles (1st, 2nd and 3rd degree) of a given profile


#connections = api.get_profile_connections(profile_id, network_depths=['F', 'S'])

KEYWORDS = ["software"]
    #limit=200,
connections_with_filter = api.get_profile_connections( urn_id=profile_id, network_depths=['F','S','O'], keywords = KEYWORDS)

print("*********************************************************************************************")
print("CONNECTIONS with filter \n")
print(connections_with_filter)
print("*********************************************************************************************")
#print("Connections \n")
#print(connections)

second_degree_list = []
visited_set = set()
for connection in connections_with_filter:
    next_hop_connections = api.get_profile_connections(urn_id = connection['urn_id'], network_depths=['F', 'S', 'O'], keywords=KEYWORDS)
   # next_hop_connection_profiles = api.get_profile(connection['public_id'])
    
    print("For connection: ", connection['name'], " next_hop_connections are: ") 
    visited_set.add(connection['public_id'])
    
    for next_hop_connection in next_hop_connections:
        public_id = next_hop_connection['public_id']
        if public_id not in visited_set:
            second_degree_list.append(next_hop_connection)
            print(public_id)

print(second_degree_list)
print("Length of second degree connections: ", len(second_degree_list))

k_hop_connections = connections_with_filter + second_degree_list

#Save the list of k_hop_connections to a pickle file
with open('software_k_hop_connections.pickle', 'wb') as handle:
    pickle.dump(k_hop_connections, handle, protocol=pickle.HIGHEST_PROTOCOL)

"""
third_degree_list = []

KEYWORDS = ['tech']

for connection in second_degree_list:
    public_id = connection['public_id']
    next_hop_connections = api.get_profile_connections( urn_id = connection['urn_id'], network_depths=['F', 'S', 'O'], keywords=KEYWORDS)
    print("For connection: ", connection['public_id'], " next_hop_connections are: ", next_hop_connections) 
    visited_set.add(public_id)

    for next_hop_connection in next_hop_connections:
        public_id = next_hop_connection['public_id']
        if public_id not in visited_set:
            third_degree_list.append(next_hop_connection)
            

print(third_degree_list)
print("Length of third degree connections: ", len(third_degree_list))

all_k_hop_connections = connections_with_filter + second_degree_list + third_degree_list
all_k_hop_urns = set([connection['urn_id'] for connection in all_k_hop_connections])

print("All visited public ids: ", visited_set)
print("All k hop URNs are: ", all_k_hop_urns)

"""









"""
#For the first connection, get the profile id and then get the profile
first_connection = connections[2]
first_connection_name = first_connection['name']
first_connection_public_id = first_connection['public_id']
first_connection_urn_id = first_connection['urn_id']
first_connection_profile = api.get_profile(first_connection_public_id)

print(f"First Connection Profile is: \n {first_connection_profile}")
print(f"Keys of First Connection Profile are: \n {first_connection_profile.keys()}")
#first_connection_urn_string = first_connection_profile['profile_urn']
#first_connection_urn_id = first_connection_urn_string.split(":")[3]

#Fetching the connections of the first connection
first_connection_connections = api.get_profile_connections(first_connection_urn_id)
print("*********************************************************************************************")
print(f"First Connection Connections are: \n {first_connection_connections}")


"""