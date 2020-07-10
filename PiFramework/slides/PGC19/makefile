all: md beamer pdf

md:
	pandoc talk.pandoc -o README.md

beamer: 
	pandoc talk.pandoc -t beamer --slide-level=2 \
	-V theme:metropolis -V \
	institute:"Universidade Federal Fluminense and \\\ FADoSS Research Group, Universidad Complutense de Madrid" \
	-o talk-slides.pdf

pdf: 
	pandoc -t latex talk.pandoc -V fontfamily:fourier -V institute: -o talk.pdf

clean:
	rm README.md talk-slides.pdf talk.pdf

