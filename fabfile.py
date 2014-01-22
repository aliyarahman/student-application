from fabric.api import *
env.hosts = ['dev@codeforprogress.org:22']

def deploy():
	local('git push')
	run('cd /var/www/html/student-application/; git pull')

