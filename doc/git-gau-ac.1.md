% git-gau-ac(1) Git Gau User Manuals
% Lorenz Schori
% November 13, 2018

# NAME

git-gau-ac - Apply a command and record its output as the commit message.

# SYNOPSIS

git-gau-ac command [*args*]...

# DESCRIPTION

Runs the specified command and records any changes to the working copy into a
new commit. The commit message is constructed from the commands *stdout*.

A *git checkout* is made before running the command in order to allow switching
to another branch or creating a new one. Changes are committed only if the
command returns a zero *exit status*.

# EXAMPLES

Update dependencies of a JavaScript project and automatically create a new
commit if anything changed.

    export GAU_CHECKOUT_ARGS="-b npm-update-$(date -I)"
    git gau-ac npm update

# VARIABLES

GAU\_CHECKOUT\_ARGS
:   Specify additional arguments for the *git checkout* command.

GAU\_COMMIT\_ARGS
:   Specify additional arguments for the *git commit* command.

# SEE ALSO

`git-checkout` (1).
`git-commit` (1).
