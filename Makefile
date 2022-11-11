all: run

run:
	python create_bg.py

clean:
	rm build/*

remove:
	rm data/image/*
	rm data/info/*