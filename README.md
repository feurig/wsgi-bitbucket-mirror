# wsgi-bitbucket-mirror
Braindead web hook to mirror bitbucket repositories
--------------------------------------------------------------------------- bbpost-hook.wsgi
 simeple hook to mirror bitbucket repo.
 NOTE: Assumes web user has ssh key basedrepo access.
 hacked from pre-json sample bitbucket webhookhook.
 (c) 2019 Suspect Devices
 assuming that you put this code in /var/www/wsgi/
 Add the following to your apache configuratino 
``` 
        WSGIScriptAlias /bitbucket-mirror /var/www/wsgi/bbpost-hook.wsgi
        <Directory /var/www/wsgi>
                WSGIApplicationGroup %{GLOBAL}
                Require all granted
        </Directory> 
 ```
 then add https://yourservername/bitbuvcket-mirror to your bitbucket repos webhooks.
