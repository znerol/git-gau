% git-gau-automerge(1) Git Gau User Manuals
% Lorenz Schori
% November 29, 2018

# NAME

git-gau-automerge - Merge all branches matching a given pattern.

# SYNOPSIS

git-gau-automerge branch-pattern

# DESCRIPTION

Given a pattern, this command merges all matching branches into the currently
checked out branch. Does nothing if no branch matches the given pattern.

Note that due to the inner mechanics of *git-merge* this command can only be
used inside a working copy, it fails in *bare repositories*.

Use *git-gau-autoclean* to cleanup leftover branches after a merge.

# EXAMPLES

Automatically merge all feature-branches if with the -lgtm suffix.

    git checkout master
    git gau-automerge origin/feature-*-lgtm

# VARIABLES

GAU\_MERGE\_ARGS
:   Specify additional arguments for the *git merge* command. Defaults to
    *--quiet*.

# SEE ALSO

`git-merge` (1).
`git-gau-autoclean` (1).
