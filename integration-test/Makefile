all: \
	test

image/context:
	mkdir image/context
	cp ../dist/git-gau-dist.tar.gz image/context/git-gau-dist.tar.gz

image: image/context
	podman build -t git-gau-integration image

test: image
	# Run test in container.
	echo "git show" | podman run \
	    -e GAU_REPO="git@github.com:znerol-scratch/git-gau-integration.git" \
	    -e GAU_SSH_KNOWNHOSTS="github.com ssh-ed25519 AAAAC3NzaC1lZDI1NTE5AAAAIOMqqnkVzrm0SdG6UOoqKLsabgH5C9okWi0dh2l9GKJl" \
	    -e GAU_SSH_PRIVKEY="$$GAU_SSH_PRIVKEY" \
	    -i git-gau-integration /bin/sh -s stdin

.PHONY: \
    all \
    image \
    test
