% git-gau-exec(1) Git Gau User Manuals
% Lorenz Schori
% November 13, 2018

# NAME

git-gau-exec - Clone a repository into tmp and run a command against it.

# SYNOPSIS

git-gau-exec repository-url command [*args*]...

# DESCRIPTION

Clones a remote repository into a temporary directory and then runs the
specified command. Pushes any commits made by the command and cleans up the
temporary directory.

New commits are only pushed if the command returns a zero *exit status*. In
order to retrieve the path to the working directory from within a script *git
rev-parse --show-toplevel* can be used.

The *repository-url* can be anything supported by *git-clone*. Optionally a
branch name can be specified after the hash character (*#*).

# EXAMPLES

Update dependencies of a JavaScript project hosted on a remote server and
automatically push a new commit if anything changed.

    export GAU_CHECKOUT_ARGS="-b npm-update-$(date -I)"
    git gau-exec https://example.com/project.git gau-ac npm update

Build a container from a specific branch (note: does not push it to a registry
though):

    git gau-exec https://example.com/container.git#latest podman build -t container:latest

# VARIABLES

GAU\_CLONE\_ARGS
:   Specify additional arguments for the *git clone* command. Defaults to
    *--quiet*.

GAU\_PUSH\_BRANCH
:   Specify a custom branch where changes are pushed to. Defaults to currently
    checked out branch.

GAU\_PUSH\_ARGS
:   Specify additional arguments for the *git push* command. Defaults to
    *--quiet*.

# SEE ALSO

`git-clone` (1).
`git-push` (1).
