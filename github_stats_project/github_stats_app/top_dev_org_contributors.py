'''
Program Description:

Python helper program that gives statistical information on the most 
popular github repositories owned by an organization and the users
who have made the most commits on each of the repositories.

Program uses the Github API V3

Inputs:
1. org (type: str) - Organization name
2. n (type: int) - Top 'n' most forked repos of the org on Github
3. m (type: int) - Top 'm' contributors by commit count for each of 
the repos

Output:
Results given back to caller function which is present in views.py
It lists the top 'n' most forked repos along with the top 'm' contributors 
by commit count along with the number of commits on the repo each contributor 
has made

API Information:

Header Info included if we have access to a token:
key: Authorization
value: Token {Token_Value}

Requests:

1. To check rate limit and rate remaining:
Format:
https://api.github.com/rate_limit

2. To check if organization name is valid:
Format:
https://api.github.com/orgs/{org_name}
Eg:
https://api.github.com/orgs/google

3. API request to sort organization's repositories by forks count:
Format:
https://api.github.com/search/repositories?q=user:{org_name}+sort:forks&per_page={results_per_page}&page={page_num}
Eg:
https://api.github.com/search/repositories?q=user:microsoft+sort:forks&per_page=10&page=2

4. API request to get top contributors by commit count of a repo:
Format:
https://api.github.com/repos/{org_name}/{repo_name}/contributors?&per_page={results_per_page}&page={page_num}
Eg:
https://api.github.com/repos/facebook/react/contributors?&per_page=10&page=2
'''

import json
import requests
import os
from collections import OrderedDict
import itertools
from collections import Counter
import csv
from datetime import datetime

# Constants
RESULTS_PER_PAGE = 30
BASE_URL = 'https://api.github.com/'
if 'GITHUB_PERSONAL_TOKEN' in os.environ:
    TOKEN = os.environ['GITHUB_PERSONAL_TOKEN']
else:
    TOKEN = 'N/A'


# Class that will take in org name, 'n' and 'm' and print out the results
class TopContributors:
    n = 0
    m = 0
    org = ''

    def __init__(self, org, n, m): 
        self.org = org
        self.n = n
        self.m = m
        return

    # Function to check rate limit of access to API
    def check_rate_limit(self):
        # Variable that returns rate limit
        rate_limit = dict()

        url = BASE_URL + f"rate_limit"

        # Adding Personal Acess Github Token if available
        headers = dict()
        if TOKEN != 'N/A':
            headers = {'Authorization': f'Token {TOKEN}'}

        response = requests.get(url, headers=headers)

        # Checking status code of response
        if response.status_code == 200:
            # Loading the response in a dict
            json_data = json.loads(response.text)
            # Loading the response in a dict
            json_data = json.loads(response.text)
            rate_limit["rate_limit"] = json_data['rate']['limit']
            rate_limit["rate_remaining"] = json_data['rate']['remaining']
            return rate_limit
        # Invalid status code in response
        else:
            print("Something wrong in rate limit request")
            print(f"ERROR: Error in request\nStatus Code: {response.status_code}\nStatus Message: {response.text}")
            return

        return rate_limit
    
    # Function to check if organization is valid or not
    def check_org(self):
        url = BASE_URL + f"orgs/{self.org}"

        # Adding Personal Acess Github Token if available
        headers = dict()
        if TOKEN != 'N/A':
            headers = {'Authorization': f'Token {TOKEN}'}

        response = requests.get(url, headers=headers)
        
        # Checking status code of response
        if response.status_code == 200:
            # Loading the response in a dict
            json_data = json.loads(response.text)
            if "message" in json_data and json_data["message"] == 'Not Found':
                return False
            elif "name" in json_data:
                print(f"Valid Organization name retrieved from API:\n{json_data['name']}\n")
            else:
                return False
        
        # Invalid status code in response
        else:
            return False
        
        return True

    # Function to get top n most forked repos
    def get_n_repos(self):
        # Results stored here
        forked_repos_data = OrderedDict()
        # In case of multiple pages in API results
        page_num = 1
        # Adding Personal Access Github Token if available
        headers = dict()
        if TOKEN != 'N/A':
            headers = {'Authorization': f'Token {TOKEN}'}
        
        # Github API allows a max of 1000 results for this API
        if self.n > 1000:
            forked_repos_data['Results_Message'] = f"N={self.n} is too large. A Maximum of the top 1000 repositories can be retrieved using the API"
        retrieved_results_count = 0
        while retrieved_results_count <= 1000 and retrieved_results_count < self.n:
            url = BASE_URL + f"search/repositories?q=user:{self.org}+sort:forks&per_page={RESULTS_PER_PAGE}&page={page_num}"
            page_num = page_num + 1
            response = requests.get(url, headers=headers)
            # Checking status code of response
            if response.status_code == 200:
                if retrieved_results_count >= self.n:
                    break
                # Loading the response in a dict
                json_data = json.loads(response.text)
                # Check if total results are more than 'n'
                if json_data['total_count'] < self.n:
                    forked_repos_data['Results_Message'] = f"n= {self.n} too large! There are only {json_data['total_count']} forked repos belonging to this org"
                result_list = json_data["items"]
                # Check if there are results
                if len(result_list) > 0:
                    for result in result_list:
                        if retrieved_results_count >= self.n:
                            break
                        else:
                            # Store the fork count and name of repo
                            individual_repo_details = OrderedDict()
                            individual_repo_details['Name'] = result['name']
                            individual_repo_details['Forks_Count'] = result['forks_count']
                            retrieved_results_count = retrieved_results_count + 1
                            forked_repos_data[retrieved_results_count] = individual_repo_details
                else:
                    break
            # Invalid status code in response
            else:
                print("Something wrong with Forked Repos Request")
                print(f"ERROR: Error in request\nStatus Code: {response.status_code}\nStatus Message: {response.text}")
                return forked_repos_data
        # No errors and return data
        return forked_repos_data

    # Function to retrieve top m contributors by commit count in each repo
    def get_m_contributors(self, repo_name):
        # Commits count by each author stored here
        contributors_data = OrderedDict()
        # In case of multiple pages in API results
        page_num = 1
        # Adding Personal Access Github Token if available
        headers = dict()
        if TOKEN != 'N/A':
            headers = {'Authorization': f'Token {TOKEN}'}
        retrieved_results_count = 0
        page_num = 1
        while retrieved_results_count < self.m:
            url = BASE_URL + f"repos/{self.org}/{repo_name}/contributors?&per_page={RESULTS_PER_PAGE}&page={page_num}"
            page_num = page_num + 1
            response = requests.get(url, headers=headers)
            # Checking status code of response
            if response.status_code == 200:
                # Making sure to not store more than m values
                if retrieved_results_count >= self.m:
                    break
                
                # Loading the response in a dict
                json_data = json.loads(response.text)
                if len(json_data) > 0:
                    # Iterating through each contributor
                    for contributor in json_data:
                        each_contributor = dict()
                        # Making sure to not store more than m values
                        if retrieved_results_count >= self.m:
                            break
                        # Storing the login_id and commit count
                        each_contributor["login_id"] = contributor["login"]
                        each_contributor["commit_count"] = contributor["contributions"]
                        retrieved_results_count += 1
                        contributors_data[retrieved_results_count] = each_contributor
                else:
                    break      
            # Invalid status code in response
            else:
                print("Something wrong with Get Contributors Request")
                print(f"ERROR: Error in request\nStatus Code: {response.status_code}\nStatus Message: {response.text}")
                return contributors_data
        # No errors and returning commit data 
        return contributors_data