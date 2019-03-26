all: \
	test

image/context:
	mkdir image/context
	cp ../dist/git-gau-dist.tar.gz image/context/git-gau-dist.tar.gz

image: image/context
	docker build -t git-gau-integration image

test: image
	# Run test in container.
	echo "git show" | docker run -e GAU_REPO=https://github.com/znerol/git-gau.git -i git-gau-integration /bin/sh -s stdin

.PHONY: \
    all \
    image \
    test
