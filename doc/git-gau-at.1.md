% git-gau-ac(1) Git Gau User Manuals
% Lorenz Schori
% March 14, 2021

# NAME

git-gau-at - Apply a command and record its output into an annotated tag.

# SYNOPSIS

git-gau-ac tag-format command [*args*]...

# DESCRIPTION

Runs the specified command and records its *stdout* into a newly created
annotated tag. The tag name is derived from *tag-format* where `%b` is replaced
by the currently checked out branch and `%d` is replaced by the current date
formatted in the ISO 8601 basic format by default (i.e., no separators).

A tag is created only if the command returns a zero *exit status*.

# EXAMPLES

Build a project and record the build log in an annotated tag. Results in a tag
of the form `builds/main/20210314T183958Z`.

    git gau-at builds/%b/%d make

# VARIABLES

GAU\_TAG\_ARGS
:   Specify additional arguments for the *git tag* command. Default is empty.

GAU\_AT\_DATE\_FMT
:   Specify date format for the `%d` placeholder. Default to `+%Y%m%dT%H%M%SZ`.

GAU\_AT\_DATE\_UTC
:   Whether or not the date in `%d` placeholder is set to UTC. Either empty
    (local time) or `-u` (utc). Defaults to `-u`.

# SEE ALSO

`git-tag` (1).
