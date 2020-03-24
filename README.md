# Django App using the Github API that Displays Stats of an Organization's Github Repository

An application that displays the top forked repos of an organization and the top contributors for each repo
<br />
<br />
Some of the features included:
<li><b>Displaying top 'n' repos of an organization (Taking n and the org name as input)</b></li>
<li><b>For each repo displaying the top 'm' contributors by commit count</b></li>
<li><b>Github API using Access Token is used</b></li>
<li><b>Error Validaiton done on the Frontend and Backend</b></li>
<br />
<br />
<b>Technical Details:</b>
<br />
<br />
<b>Frontend:</b> HTML, JS, CSS (Bootstrap theme: https://bootswatch.com/cosmo/)
<br />
<b>Framework:</b> Python, Django authentication, messages, etc
<br />
<b>Database:</b> SQLite but no models or tables were created
<br />
<br /> 
<b>Github API requests used:</b>
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
<b>Requirements of the app:</b>
<br />
<a href="https://github.com/tebbythomas/Django-Employee-Kudos-Management/blob/master/requirements.txt">Link</a>
<br />
<br />
<b>To run the app:</b>
<br />
<br />
<p>1. Clone the repo</p>
<br />
<pre><code>git clone https://github.com/tebbythomas/Django-Employee-Kudos-Management.git
</code></pre>
<br />
<br />
<p>2. Switch to project dir</p>
<br />
<pre><code>cd Django-Employee-Kudos-Management-master/
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
<pre><code>cd kudos_manager/
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
<p>8. Run the project</p>
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
<img src="https://github.com/tebbythomas/Django-Employee-Kudos-Management/blob/master/Screenshots/Register_Screen.png" hspace="20">
<br />
<br />
2. <b>Form Input Validation Check</b>:
<br />
<img src="https://github.com/tebbythomas/Django-Employee-Kudos-Management/blob/master/Screenshots/Login_Screen.png" hspace="20">
<br />
<br />
3. <b>Check if the organization name is valid using Github API</b>:
<br />
<img src="https://github.com/tebbythomas/Django-Employee-Kudos-Management/blob/master/Screenshots/Dashboard.png" hspace="20">
<br />
<br />
4. <b>List of 'N' Top 'N' Forked Repositories of the Organization</b>:
<br />
<img src="https://github.com/tebbythomas/Django-Employee-Kudos-Management/blob/master/Screenshots/Upload_Employees.png" hspace="20">
<br />
<br />
5. <b>List of the Top 'M' Contributors for the Repo</b>:
<br />
<img src="https://github.com/tebbythomas/Django-Employee-Kudos-Management/blob/master/Screenshots/Upload_Kudos.png" hspace="20">
<br />
<br />
6. <b>Github API Rate Limit for a Personal Access Token</b>:
<br />
<img src="https://github.com/tebbythomas/Django-Employee-Kudos-Management/blob/master/Screenshots/Upload_Kudos.png" hspace="20">
<br />
<br />
<b>Command Line Version of the App:</b><br />
<a href="https://github.com/tebbythomas/Django-Employee-Kudos-Management/blob/master/requirements.txt">Link</a>