#--------------------------------------------------------------------------- bbpost-hook.wsgi
# simeple hook to mirror bitbucket repo.
# assumes web user has ssh key basedrepo access.
# hacked from pre-json sample bitbucket webhookhook. 
# 
# Add the following to your apache configuratino
# 
#        WSGIScriptAlias /bitbucket-mirror /var/www/wsgi/bbpost-hook.wsgi
#        <Directory /var/www/wsgi>
#                WSGIApplicationGroup %{GLOBAL}
#                Require all granted
#        </Directory> 
#
import json
from os import makedirs
from os.path import expanduser, join, isdir
from subprocess import call

BACKUP_ROOT =  '/var/trac/devel/private'   # change this according to your server setup

def application( environ, start_response ):
	headers = [ ( 'Content-type', 'text/plain' ) ]
	try:
		length = int( environ[ 'CONTENT_LENGTH' ] )
                request_body= environ[ 'wsgi.input' ].read( length )
		data=json.loads(str(request_body))
		repository = data[ u'repository' ]
		owner,repo = repository[ 'full_name' ].split('/')
                owner_dir = join( BACKUP_ROOT, owner ) # os.path.join 
   		repo_dest = join( owner_dir, repo )
		if not isdir( repo_dest ):
			if not isdir( owner_dir ): makedirs( owner_dir, 0700 )
#                        print >>environ['wsgi.errors'], 'git', 'clone', '--mirror', 'git://bitbucket.com/{0}/{1}.git'.format( owner, repo ),  repo_dest
			call([ 'git', 'clone', '--mirror', 'git://bitbucket.com/{0}/{1}.git'.format( owner, repo ), repo_dest ])
		else:
#                        print >> environ['wsgi.errors'], 'git', '--git-dir', repo_dest , 'remote', 'update' 
			call([ 'git', '--git-dir', repo_dest, 'remote', 'update' ])
	except Exception as e:
                print >>environ['wsgi.errors'],e
		start_response( '500 Internal server error', headers )
		return [ "Internal server error" ]
	else:
		start_response( '200 OK', headers )
		return [ "OK" ]
