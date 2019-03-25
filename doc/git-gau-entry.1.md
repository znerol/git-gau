% git-gau-entry(1) Git Gau User Manuals
% Lorenz Schori
% November 13, 2018

# NAME

git-gau-entry - Entry point for docker containers.

# SYNOPSIS

git-gau-entry command [*args*]...

# DESCRIPTION

Runs *git-gau-exec* with the repository URL taken from `GAU_REPO` environment
variable and the given command.

# EXAMPLES

Update dependencies of a JavaScript project hosted on a remote server and
automatically push a new commit if anything changed.

    export GAU_CHECKOUT_ARGS="-b npm-update-$(date -I)"
    git gau-entry https://example.com/project.git gau-ac npm update

# VARIABLES

GAU\_RPEO
:   Remote repository which is passed to *git-gau-exec*.

# SEE ALSO

`git-gau-exec` (1).
