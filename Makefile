.PHONY: all
all:
	cd HaliteEnvironment-Source/; make; cd ..; mv HaliteEnvironment-Source/halite halite;

.PHONY: clean
clean:
	rm ./halite; cd HaliteEnvironment-Source/; make clean; cd ..;