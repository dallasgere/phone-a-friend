make server:
	python3 server.py

make deploy:
	flyctl deploy

make launch:
	flyctl launch

proxy:
	flyctl proxy 5432 -a phone-a-friend-db

connect:
	fly pg connect -a phone-a-friend-db