# Django App using the Github API that Displays Stats of an Organization's Github Page

An application that displays the top forked repos of an organization and the top contributors for each repo
<br />
<br />
<h2>Some of the features included:</h2>
<li>Displaying top 'N' repos of an organization (Taking 'N' and the org name as input)</li>
<li>For each repo displaying the top 'M' (from user) contributors by commit count</li>
<li>Github API using Personal Access Token is used</li>
<li>Error Validaiton done on the Frontend and Backend</li>
<br />
<br />
<h2>Technical Details:</h2>
<br />
<br />
<b>Frontend:</b> HTML, JS, CSS (Bootstrap theme: https://bootswatch.com/cosmo/)
<br />
<b>Framework:</b> Python, Django authentication, messages, etc
<br />
<b>Database:</b> SQLite but no models or tables were created
<br />
<br /> 
<h2>Githuh2 API requests used:</h2>
<br />
<br />
<b>1. To check if organization name is valid:</b> 
<br />
<b>Format:</b><br />
https://api.github.com/orgs/{org_name}<br />
<b>Eg:</b><br />
https://api.github.com/orgs/google
<br />
<br />
<b>2. API request to sort organization's repositories by forks count:</b> 
<br />
<b>Format:</b><br />
https://api.github.com/search/repositories?q=user:{org_name}+sort:forks&per_page={results_per_page}&page={page_num}<br />
<b>Eg:</b><br />
https://api.github.com/search/repositories?q=user:microsoft+sort:forks&per_page=10&page=2
<br />
<br />
<b>3. API request to get top contributors by commit count of a repo:</b> 
<br />
<b>Format:</b><br />
https://api.github.com/repos/{org_name}/{repo_name}/contributors?&per_page={results_per_page}&page={page_num}<br />
<b>Eg:</b><br />
https://api.github.com/repos/facebook/react/contributors?&per_page=10&page=2
<br />
<br />
<h2>Requirements of the app:</h2>
<br />
<a href="https://github.com/tebbythomas/Github-API-Org-Repo-Stats/blob/master/requirements.txt">Link</a>
<br />
<br />
<h2>To run the app:</h2>
<br />
<br />
<p>1. Clone the repo</p>
<br />
<pre><code>git clone https://github.com/tebbythomas/Github-API-Org-Repo-Stats.git
</code></pre>
<br />
<br />
<p>2. Switch to project dir</p>
<br />
<pre><code>cd Github-API-Org-Repo-Stats/
</code></pre>
<br />
<br />
<p>3. Create a python virtual environment</p>
<br />
<pre><code>python3 -m venv proj_env
</code></pre>
<br />
<br />
<p>4. Activate the environment</p>
<br />
<pre><code>source proj_env/bin/activate
</code></pre>
<br />
<br />
<p>5. Install requirements</p>
<br />
<pre><code>pip install -r requirements.txt
</code></pre>
<br />
<br />
<p>6. Switch to django project dir</p>
<br />
<pre><code>cd github_stats_project
</code></pre>
<br />
<br />
<p>7. Make DB migrations</p>
<br />
<pre><code>python manage.py makemigrations
</code></pre>
<br />
<pre><code>python manage.py migrate
</code></pre>
<br />
<br />
<p>8. Input Github API Token Here (Line 68):</p>
<br />
<a href="https://github.com/tebbythomas/Github-API-Org-Repo-Stats/blob/master/github_stats_project/github_stats_app/top_dev_org_contributors.py">Link</a>
<br />
<br />
<p>If you don't have one then you can generate one here:</p>
<br />
<a href="https://github.com/settings/tokens">Link</a>
<br />
<br />
<p>9. Run the project</p>
<br />
<pre><code>python manage.py runserver
</code></pre>
<br />
<br />
<b>Screenshots:</b>
<br />
<br />
1. <b>Home Page</b>:
<br />
<img src="https://github.com/tebbythomas/Github-API-Org-Repo-Stats/blob/master/Screenshots/Home-Page.png" hspace="20">
<br />
<br />
2. <b>Form Input Validation Check</b>:
<br />
<img src="https://github.com/tebbythomas/Github-API-Org-Repo-Stats/blob/master/Screenshots/Input-Validation.png" hspace="20">
<br />
<br />
3. <b>Check if the organization name is valid using Github API</b>:
<br />
<img src="https://github.com/tebbythomas/Github-API-Org-Repo-Stats/blob/master/Screenshots/Valid-Company-Check.png" hspace="20">
<br />
<br />
4. <b>List of 'N' Top 'N' Forked Repositories of the Organization</b>:
<br />
<img src="https://github.com/tebbythomas/Github-API-Org-Repo-Stats/blob/master/Screenshots/Repos-List.png" hspace="20">
<br />
<br />
5. <b>List of the Top 'M' Contributors for the Repo</b>:
<br />
<img src="https://github.com/tebbythomas/Github-API-Org-Repo-Stats/blob/master/Screenshots/Contributors-List.png" hspace="20">
<br />
<br />
6. <b>Github API Rate Limit for a Personal Access Token</b>:
<br />
<img src="https://github.com/tebbythomas/Github-API-Org-Repo-Stats/blob/master/Screenshots/Github-Token-Access-Limit.png" hspace="20">
<br />
<br />
<b>Command Line Version of the App:</b><br />
<a href="https://github.com/tebbythomas/Django-Employee-Kudos-Management/blob/master/requirements.txt">Link</a>