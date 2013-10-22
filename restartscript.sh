killall -9 uwsgi
uwsgi -x django_socket.xml
sudo /etc/init.d/nginx -s reload
sudo /etc/init.d/nginx restart
