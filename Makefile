.PHONY: all
all:
	cd src/; make; cd ..; mv src/halite public/halite;

.PHONY: clean
clean:
	rm *.hlt *.log public/halite; cd src/; make clean; cd ..;

.PHONY: sync-nefeli
sync-nefeli:
	rsync -a --exclude 'public/halite' --exclude '*.o' . mehlman@nefeli.math-info.univ-paris5.fr:/home/mehlman/Halite-Python-RL/ #--delete

.PHONY: get-nefeli
get-nefeli:
	rsync -a --exclude 'public/halite' --exclude '*.o' mehlman@nefeli.math-info.univ-paris5.fr:/home/mehlman/Halite-Python-RL/ . #--delete

.PHONY: sync-solon
sync-solon:
	rsync -a --exclude 'public/halite' --exclude '*.o' . solon:/home/mehlman/Halite-Python-RL/ #--delete

.PHONY: get-solon
get-solon:
	rsync -a --exclude 'public/halite' --exclude '*.o' solon:/home/mehlman/Halite-Python-RL/ . #--delete

.PHONY: clear-agent
clear-agent:
	rm -r './public/models/variables/$(AGENT)'

.PHONY: server
server:
	cd visualize;export FLASK_APP=visualize.py;flask run