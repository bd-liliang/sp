a socket proxy module

what u can do with it? 
all config can be dynamic changed
1.http reverse proxy,proxy to a specified server
2.socket message transfer,for example,open a backend for outside just as relay server,mysql server

all config data stored in dir named 'data'
new config start with @,program will load the new config
old config could be found in dir named 'data'

u may need a web interface to dynamic changed it ,it is easy

example:
your ip is 172.168.1.150
u can store a file named '@172.168.1.150'
within contents:
"172.168.1.120  3306    0"
it means [remote ip]    [remote port]   [expire time(0 means never expire)]
