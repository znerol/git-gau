# GAU - Git automation utilities

A collection of custom git commands which make it easier to create bots which
commit and push changes automatically.

[![Build Status](https://travis-ci.com/znerol/git-gau.svg?branch=develop)](https://travis-ci.com/znerol/git-gau)

## INSTALL

Navigate to the releases page and pick the latest `git-gau-dist.tar.gz`
tarball. Copy it to the target machine and unpack it there.

    $ scp dist/git-gau-dist.tar.gz me@example.com:~
    $ ssh me@example.com sudo tar -C /usr/local -xzf ~:git-gau-dist.tar.gz

## BUILD

*Preferred method*: Build a distribution tarball, copy it to the target machine
and unpack it there.
    
    $ make dist
    $ scp dist/git-gau-dist.tar.gz me@example.com:~
    $ ssh me@example.com sudo tar -C /usr/local -xzf ~:git-gau-dist.tar.gz

*Alternative method*: Check out this repository on the traget machine and
install it directly. The destination directory can be changed with the `prefix`
variable in order to change the installation prefix to something else than
`/usr/local`.

    $ make all
    $ sudo make prefix=/opt/local install

[Pandoc](https://pandoc.org) is necessary in order to build the man pages. This
step can be skipped by using the `install-bin` target.
