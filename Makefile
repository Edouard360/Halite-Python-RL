.PHONY: all
all:
	cd src/; make; cd ..; mv src/halite public/halite;

.PHONY: clean
clean:
	rm public/halite; cd src/; make clean; cd ..;