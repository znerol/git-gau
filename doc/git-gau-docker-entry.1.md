% git-gau-docker-entry(1) Git Gau User Manuals
% Lorenz Schori
% November 13, 2018

# NAME

git-gau-docker-entry - Entry point for docker containers.

# SYNOPSIS

/usr/local/lib/git-gau/docker-entry docker-entry.d command [*args*]...

# DESCRIPTION

Serves as entry point for docker images. Runs all the scripts found in
`docker-entry.d` directory using `run-parts`. Runs *git-gau-exec* with the
repository URL taken from `GAU_REPO` environment variable if specified,
otherwise runs the given command directly.

# EXAMPLES

TODO

# VARIABLES

GAU\_RPEO
:   Remote repository which is passed to *git-gau-exec*.

# SEE ALSO

`git-gau-exec` (1).
`run-parts` (1).
