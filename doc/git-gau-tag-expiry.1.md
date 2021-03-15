% git-gau-tag-expiry(1) Git Gau User Manuals
% Lorenz Schori
% March 15, 2021

# NAME

git-gau-tag-expiry - Run a command if the most recent tag is older than n seconds.

# SYNOPSIS

git-gau-tag-expiry tag-pattern seconds command [*args*]...

# DESCRIPTION

Runs the specified command unless a tag is found matching the given
*tag-pattern* which was created no longer than specified *seconds* ago.

The syntax for *tag-pattern* is the same as for `git-for-each-ref`.
Additionally the `%b` placeholder is replaced by the currently checked out
branch.

Note that this command only considers annotated tags. Lightweight tags are
ignored.

# EXAMPLES

Check whether there was a build of the current branch during the past week.

    git gau-tag-expire builds/%b/* 604800 \
    echo "Last build is older than one week"

# SEE ALSO

`git-gau-at` (1).
`git-tag` (1).
`git-for-each-ref` (1).
