.PHONY: all clean run

all: node_modules

node_modules:
	npm install

clean:
	rm -rfv node_modules/

run: node_modules
	NODE_ENV=production node_modules/harp/bin/harp server --port 8080
