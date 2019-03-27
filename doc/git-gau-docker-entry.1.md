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

GAU ships with a selection of scripts in `docker-entry.d` which are useful to
populate SSH private key, known-hosts file and GIT credentials from environment
variables.

# EXAMPLES

The following `Dockerfile` demonstrates how the `docker-entry` script can be
combined with `tini` and `ssh-agent`.

    FROM alpine:latest

    RUN apk update && apk upgrade && \
        apk add --no-cache bash git openssh tini

    COPY git-gau-dist.tar.gz /root/
    RUN tar -C /usr/local -xf /root/git-gau-dist.tar.gz

    RUN addgroup -S git-gau && adduser -S git-gau -G git-gau

    USER git-gau

    ENTRYPOINT [ \
        "/sbin/tini", \
        "--", \
        "/usr/bin/ssh-agent", \
        "/usr/local/lib/git-gau/docker-entry", \
        "/usr/local/lib/git-gau/docker-entry.d" \
    ]

After building this image using `docker build -t git-gau .` a command started
in a container will be wrapped by `tini` and `ssh-agent`. Also all scripts from
`/usr/local/lib/git-gau/docker-entry.d` will have a chance to prepare the
container before the command is run.

# VARIABLES

GAU\_RPEO
:   Remote repository which is passed to *git-gau-exec*.

GAU\_GIT\_CREDENTIALS
:   Git credentials as expected by `git-credential-store`. If this variable is
    set, its contents is written to `${GAU_GIT_CREDENTIALS_FILE}` before
    container command is executed. Respected by
    `docker-entry.d/50-git-credentials`.

GAU\_GIT\_CREDENTIALS\_FILE
:   Where GIT credentials are written to. Defaults to
    `${HOME}/.git-credentials`. Respected by `docker-entry.d/50-git-credentials`.

GAU\_SSH\_DIR
:   Path to per-user `ssh` configuration directory. Defaults to `${HOME}/.ssh`.
    Respected by `docker-entry.d/50-ssh-known-hosts` and
    `docker-entry.d/50-ssh-privkey` scripts.

GAU\_SSH\_KNOWNHOSTS
:   Expected SSH host fingerprints. If this variable is set, its contents is
    written to `${GAU_SSH_KNOWNHOSTS_FILE}` before container command is executed.
    Respected by `docker-entry.d/50-ssh-known-hosts`.

GAU\_SSH\_KNOWNHOSTS\_FILE
:   Where SSH host fingerprints are written to. Defaults to
    `${HOME}/known_hosts`. Respected by `docker-entry.d/50-ssh-known-hosts`.

GAU\_SSH\_PRIVKEY
:   SSH private key. If this variable is set, its contents is written to
    `${GAU_SSH_PRIVKEY_FILE}` before container command is executed.  Respected
    by `docker-entry.d/50-ssh-privkey`.

GAU\_SSH\_PRIVKEY\_FILE
:   Where SSH private keys are written to. Defaults to `${HOME}/.ssh/id_rsa`.
    If `docker-entry` is wrapped by `ssh-agent` also adds the key to ssh agent
    automatically. Respected by `docker-entry.d/50-ssh-privkey`.

# SEE ALSO

`git-gau-exec` (1).
`run-parts` (1).
