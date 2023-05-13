#commands to set password
#export LINKEDIN_PASSWORD="password"


#from linkedin_api import Linkedin
from custom_linkedin_api import Linkedin

import os
import pickle

password = os.environ.get('LINKEDIN_PASSWORD')

# Authenticate using any Linkedin account credentials
api = Linkedin('shah.jaidev00@gmail.com', password)

PUBLIC_PROFILE =  "shahjaidev" #"shahjaidev"

profile_response_dict = api.get_profile(PUBLIC_PROFILE)
print(profile_response_dict.keys())

profile_id = profile_response_dict['profile_id']
print(f"Profile ID: {profile_id}")

keys_to_keep = ['industryName', 'lastName', 'firstName', 'geoLocationName', 'headline', 'experience', 'education', 'projects']
filtered_profile_dict = {key: profile_response_dict[key] for key in profile_response_dict if key in keys_to_keep}

print(f"Filtered Profile Response: \n {filtered_profile_dict}")





