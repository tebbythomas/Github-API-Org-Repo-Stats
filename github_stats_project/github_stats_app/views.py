from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.contrib import messages
import json, requests, os, itertools, csv, io
from collections import OrderedDict
from collections import Counter
from datetime import datetime
from .top_dev_org_contributors import TopContributors

# Constants
BASE_URL = 'https://api.github.com/'
if 'GITHUB_PERSONAL_TOKEN' in os.environ:
    TOKEN = os.environ['GITHUB_PERSONAL_TOKEN']
else:
    TOKEN = 'N/A'


# Function to handle requests to the home page / dashboard
def index(request):
    return render(request, 'pages/index.html')

# Function to handle display the repos
def repos(request):
    if request.method == 'GET':
        return redirect('index')
    
    if request.method == 'POST':
        org_name = request.POST['organization'].strip()
        n = int(request.POST['n'])
        m = int(request.POST['m'])
        error_messages = list()

        # Creating the context to send to the repos page
        context = {
            "org": org_name,
            "n":  n,
            "m": m,
        }

        # Checking for valid values of n and m
        if n <= 0 or m <= 0:
            error_messages.append("Only positive integer values greater than 0 allowed for N and M")
            # Sending error message
            context["error_messages"] = error_messages
            return render(request, 'pages/repos.html', context)

        # Calling the class with the values
        obj = TopContributors(org_name, n, m)

        # Checking for valid org name
        org_check = obj.check_org()
        if org_check == False:
            # Invalid org entered
            error_messages.append(f"Unable to retrieve organization '{org_name}' using the Github API")
            # Sending error message
            context["error_messages"] = error_messages
            return render(request, 'pages/repos.html', context)
        
        result_list = list()
        # Get top n most forked repos
        print(f"Retrieving the {n} most forked repos")
        n_repos = obj.get_n_repos()
        for key, repo_details in n_repos.items():
            if type(key) == int:
                # Get top m contributors for each repo
                # print(f"Retrieving the {m} most active contributors for repo: {repo_details['Name']}")
                #repo_details["Commits"] = obj.get_m_commits(repo_details['Name'])
                row = list()
                row.append(str(key) + "/" + str(len(n_repos)))
                row.append(repo_details['Name'])
                row.append(repo_details['Forks_Count'])
                result_list.append(row)
        
        context["result_data"] = result_list

        # Adding Github API Access Rate Limit and Rate Remaining
        rate_limit = obj.check_rate_limit()
        if "rate_limit" in rate_limit and "rate_remaining" in rate_limit:
            context["rate_limit"] = rate_limit["rate_limit"]
            context["rate_remaining"] = rate_limit["rate_remaining"]

        return render(request, 'pages/repos.html', context)


# Function to handle displaying the contributors for a repo
def contributors(request, org, n, m, repo_name):
    # To ensure requests is from the repo page 
    if '/repos' in request.META.get('HTTP_REFERER'):
        # Calling the class with the values
        obj = TopContributors(org, n, m)

        # Creating the context to send to the repos page
        context = {
            "org": org,
            "n":  n,
            "m": m,
            "repo_name": repo_name
        }

        # Get top n most forked repos
        print(f"Retrieving the {m} most active contributors")
        contributors_dict = obj.get_m_contributors(repo_name)

        # Results stored in a list
        result_list = list()

        # Iterating through and storing results
        for key, contributor_data in contributors_dict.items():
            if type(key) == int:
                row = list()
                row.append(str(key) + "/" + str(len(contributors_dict)))
                row.append(contributor_data['login_id'])
                row.append(contributor_data['commit_count'])
                result_list.append(row)
        
        context["result_data"] = result_list

        # Adding Github API Access Rate Limit and Rate Remaining
        rate_limit = obj.check_rate_limit()
        if "rate_limit" in rate_limit and "rate_remaining" in rate_limit:
            context["rate_limit"] = rate_limit["rate_limit"]
            context["rate_remaining"] = rate_limit["rate_remaining"]

        return render(request, 'pages/contributors.html', context)

    # If prev url is not the repo page then redirect to home page
    else:
        return redirect('index')