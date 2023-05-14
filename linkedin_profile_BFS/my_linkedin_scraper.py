#Scraper

from linkedin_scraper import Person, actions
from selenium import webdriver
driver = webdriver.Chrome()

email = "shah.jaidev00@gmail.com"
password = "hackGPT123"
actions.login(driver, email, password) # if email and password isnt given, it'll prompt in terminal
person = Person("https://www.linkedin.com/in/abuch99/", driver=driver)
print(person)
print("Name: ", person.name)
print("contacts: ", person.contacts)
print("linkedin_url: ", person.linkedin_url)
print("about: ", person.about)
print("experiences: ", person.experiences)
print("educations: ", person.educations)
print("interests: ", person.interests)
print("accomplishments: ", person.accomplishments)
print("company: ", person.company)
print("job_title: ", person.job_title)

