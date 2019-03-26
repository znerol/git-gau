all: \
	test

image/context:
	mkdir image/context
	cp ../dist/git-gau-dist.tar.gz image/context/git-gau-dist.tar.gz

image: image/context
	docker build -t git-gau-integration image

test: image
	# Run test in container.
	echo "git show" | docker run \
	    -e GAU_REPO="git@github.com:znerol-scratch/git-gau-integration.git" \
	    -e GAU_SSH_KNOWNHOSTS="github.com ssh-rsa AAAAB3NzaC1yc2EAAAABIwAAAQEAq2A7hRGmdnm9tUDbO9IDSwBK6TbQa+PXYPCPy6rbTrTtw7PHkccKrpp0yVhp5HdEIcKr6pLlVDBfOLX9QUsyCOV0wzfjIJNlGEYsdlLJizHhbn2mUjvSAHQqZETYP81eFzLQNnPHt4EVVUh7VfDESU84KezmD5QlWpXLmvU31/yMf+Se8xhHTvKSCZIFImWwoG6mbUoWf9nzpIoaSjB+weqqUUmpaaasXVal72J+UX2B+2RPW3RcT0eOzQgqlJL3RKrTJvdsjE3JEAvGq3lGHSZXy28G3skua2SmVi/w4yCE6gbODqnTWlg7+wC604ydGXA8VJiS5ap43JXiUFFAaQ==" \
	    -e GAU_SSH_PRIVKEY="$$GAU_SSH_PRIVKEY" \
	    -e GAU_SSH_SETUP_AGENT=yes \
	    -i git-gau-integration /bin/sh -s stdin

.PHONY: \
    all \
    image \
    test
