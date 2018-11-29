% git-gau-autoclean(1) Git Gau User Manuals
% Lorenz Schori
% November 29, 2018

# NAME

git-gau-autoclean - Removes all branches which are already merged.

# SYNOPSIS

git-gau-autoclean master-branch

# DESCRIPTION

Deletes all branches which are completely merged into the branch given as a
reference on the command line.

This is especially usefull to cleanup after *git-gau-automerge*.

# EXAMPLES

Automatically delete all branches which are completely merged into master.

    git gau-autoclean master

# SEE ALSO

`git-branch` (1).
`git-gau-automerge` (1).
