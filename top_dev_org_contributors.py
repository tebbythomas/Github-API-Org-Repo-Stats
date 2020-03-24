'''
Program Description:

Python program that gives statistical information on the most 
popular github repositories owned by an organization and the users
who have made the most commits on each of the repositories.

Program uses the Github API V3

Inputs:
1. org (type: str) - Organization name
2. n (type: int) - Top 'n' most forked repos of the org on Github
3. m (type: int) - Top 'm' contributors by commit count for each of 
the repos

Output:
A CSV containing all the results
Result file format:
'Repo_Rank', 'Repo_Name', 'Repo_Forks_Count', 'Contributor_Rank', 'Contributor_Login_ID', 'Contributor_Commit_Count'

File Naming Convention:
Results/Results_{org}_{n}_forks_{m}_contributors.csv

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
RESULTS_PER_PAGE = 10
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

    # Function to print the values entered by the user
    def print_inputs(self):
        print("\nInputs entered are:\n")
        print(f"Org = {self.org}\nn = {self.n}\nm = {self.m}")
        return

    # Function to check rate limit of access to API
    def check_rate_limit(self):
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
            print(f"\nRate Limit:{json_data['rate']['limit']}\n")
            print(f"Rate Remaining:{json_data['rate']['remaining']}\n")
        
        # Invalid status code in response
        else:
            print("Something wrong in rate limit request")
            print(f"ERROR: Error in request\nStatus Code: {response.status_code}\nStatus Message: {response.text}")
            return

        return
    
    # Function to check if organization is valid or not
    def check_org(self):
        url = BASE_URL + f"orgs/{org}"

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
                print("Invalid Github Organization entered")
                return
            elif "name" in json_data:
                print("Valid organization entered")
                print(f"Organization name retrieved from API:\n{json_data['name']}\n")
            else:
                print("Invalid Github Organization entered")
                sys.exit()
        
        # Invalid status code in response
        else:
            print("Invalid Github Organization entered")
            print(f"ERROR: Error in request\nStatus Code: {response.status_code}\nStatus Message: {response.text}")
            sys.exit()
        
        return

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
        if n > 1000:
            forked_repos_data['Results_Message'] = f"N={n} is too large. A Maximum of the top 1000 repositories can be retrieved using the API"
        retrieved_results_count = 0
        while retrieved_results_count <= 1000 and retrieved_results_count < n:
            url = BASE_URL + f"search/repositories?q=user:{org}+sort:forks&per_page={RESULTS_PER_PAGE}&page={page_num}"
            page_num = page_num + 1
            response = requests.get(url, headers=headers)
            # Checking status code of response
            if response.status_code == 200:
                # Loading the response in a dict
                json_data = json.loads(response.text)
                # Check if total results are more than 'n'
                if json_data['total_count'] < n:
                    forked_repos_data['Results_Message'] = f"n= {n} too large! There are only {json_data['total_count']} forked repos belonging to this org"
                result_list = json_data["items"]
                # Check if there are results
                if len(result_list) > 0:
                    for result in result_list:
                        if retrieved_results_count >= n:
                            break
                        else:
                            # Store the fork count and name of repo
                            individual_repo_details = OrderedDict()
                            individual_repo_details['Name'] = result['name']
                            individual_repo_details['Forks_Count'] = result['forks_count']
                            retrieved_results_count = retrieved_results_count + 1
                            forked_repos_data[retrieved_results_count] = individual_repo_details

            # Invalid status code in response
            else:
                print("Something wrong with Forked Repos Request")
                print(f"ERROR: Error in request\nStatus Code: {response.status_code}\nStatus Message: {response.text}")
                return forked_repos_data
        # No errors and return data
        return forked_repos_data

    # Function to retrieve top m contributors by commit count in each repo
    def get_m_commits(self, repo_name):
        # Commits count by each author stored here
        commits_data = OrderedDict()
        # In case of multiple pages in API results
        page_num = 1
        # Adding Personal Access Github Token if available
        headers = dict()
        if TOKEN != 'N/A':
            headers = {'Authorization': f'Token {TOKEN}'}
        retrieved_results_count = 0
        page_num = 1
        while retrieved_results_count < m:
            url = BASE_URL + f"repos/{org}/{repo_name}/contributors?&per_page={RESULTS_PER_PAGE}&page={page_num}"
            page_num = page_num + 1
            response = requests.get(url, headers=headers)
            # Checking status code of response
            if response.status_code == 200:
                # Making sure to not store more than m values
                if retrieved_results_count >= m:
                    break
                
                # Loading the response in a dict
                json_data = json.loads(response.text)
                if len(json_data) > 0:
                    # Iterating through each contributor
                    for contributor in json_data:
                        each_contributor = dict()
                        # Making sure to not store more than m values
                        if retrieved_results_count >= m:
                            break
                        # Storing the login_id and commit count
                        each_contributor["login_id"] = contributor["login"]
                        each_contributor["commit_count"] = contributor["contributions"]
                        retrieved_results_count += 1
                        commits_data[retrieved_results_count] = each_contributor
                else:
                    break      
            # Invalid status code in response
            else:
                print("Something wrong with Get Contributors Request")
                print(f"ERROR: Error in request\nStatus Code: {response.status_code}\nStatus Message: {response.text}")
                return commits_data
        # No errors and returning commit data 
        return commits_data
    
    # Function to write results into a csv
    def write_results(self, results_dict):
        if not os.path.exists('Results'):
            os.makedirs('Results')
        file_name = f"Results_{org}_{n}_forks_{m}_contributors.csv"
        with open(f'Results/{file_name}', mode='w') as result_file:
            result_writer = csv.writer(result_file, delimiter=',', quotechar='"', quoting=csv.QUOTE_MINIMAL)
            result_writer.writerow(['Repo_Rank', 'Repo_Name', 'Repo_Forks_Count', 'Contributor_Rank', 'Contributor_Login_ID', 'Contributor_Commit_Count'])
            for repo_rank, repo_details in results_dict.items():
                if type(repo_rank) == int:
                    for contributor_rank, contributor_details in repo_details["Commits"].items():
                        if type(contributor_rank) == int:
                            result_writer.writerow([repo_rank, repo_details['Name'], repo_details['Forks_Count'], contributor_rank, contributor_details['login_id'], contributor_details['commit_count']])

        print(f"\nResults written into file:\nResults/{file_name}")
        return
        
if __name__ == "__main__":
    try:
        # Starting timer for calculating time to retrieve result
        start_time = datetime.now()

        print("Enter the name of the organisation whose github stats you're interested in:")
        org = input().strip()
        print("Enter a value for 'n' which is the n most forked repos you're interested in:")
        n = int(input())
        print("Enter a value for 'm' which is the m most active committers for each of the repos:")
        m = int(input())

        if n <= 0 or m <= 0:
            print("Only positive integer values greater than 0 allowed for n and m")
            sys.exit()
            
        # Calling the class with the values
        obj = TopContributors(org, n, m)

        # Printing the inputs
        obj.print_inputs()

        # Check rate limit of API access
        obj.check_rate_limit()

        # Checking if org name entered is valid
        obj.check_org()

        # Get top n most forked repos
        print(f"Retrieving the {n} most forked repos")
        n_repos = obj.get_n_repos()
        for key, repo_details in n_repos.items():
            if type(key) == int:
                # Get top m contributors for each repo
                print(f"Retrieving the {m} most active contributors for repo: {repo_details['Name']}")
                repo_details["Commits"] = obj.get_m_commits(repo_details['Name'])

        # Writing the results into a csv
        obj.write_results(n_repos)
        
        # Time Elapsed
        print("Program execution time:\n")
        end_time = end_time = datetime.now()
        print(end_time - start_time)
                        
    except ValueError:
        # Checking if values are in the right format
        print("ERROR: Please input a string for the organization name and integer values for 'n' and 'm'")
    except Exception as e: 
        print(f"ERROR:\n{e}")