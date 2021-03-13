ifeq ($(prefix),)
    prefix := /usr/local
endif
ifeq ($(exec_prefix),)
    exec_prefix := $(prefix)
endif
ifeq ($(bindir),)
    bindir := $(exec_prefix)/bin
endif
ifeq ($(libdir),)
    libdir := $(exec_prefix)/lib
endif
ifeq ($(datarootdir),)
    datarootdir := $(prefix)/share
endif
ifeq ($(mandir),)
    mandir := $(datarootdir)/man
endif
ifeq ($(python),)
    python := python
endif

all: bin test doc

%.1 : %.1.md
	pandoc -s -t man $< -o $@

bin:
	# empty for now

lint: bin
	shellcheck bin/git-gau-ac
	shellcheck bin/git-gau-autoclean
	shellcheck bin/git-gau-automerge
	shellcheck bin/git-gau-exec
	shellcheck bin/git-gau-xargs
	shellcheck lib/docker-entry
	shellcheck lib/docker-entry.d/50-git-credentials
	shellcheck lib/docker-entry.d/50-ssh-known-hosts
	shellcheck lib/docker-entry.d/50-ssh-privkey

test: bin
	PATH="$(shell pwd)/bin:${PATH}" $(python) -m test

doc: \
	doc/git-gau-ac.1 \
	doc/git-gau-autoclean.1 \
	doc/git-gau-automerge.1 \
	doc/git-gau-docker-entry.1 \
	doc/git-gau-exec.1 \
	doc/git-gau-xargs.1

clean:
	-rm -f doc/git-gau-ac.1
	-rm -f doc/git-gau-autoclean.1
	-rm -f doc/git-gau-automerge.1
	-rm -f doc/git-gau-docker-entry.1
	-rm -f doc/git-gau-exec.1
	-rm -f doc/git-gau-xargs.1
	-rm -rf dist
	-rm -rf build

install-doc: doc
	install -m 0644 -D doc/git-gau-ac.1 $(DESTDIR)$(mandir)/man1/git-gau-ac.1
	install -m 0644 -D doc/git-gau-autoclean.1 $(DESTDIR)$(mandir)/man1/git-gau-autoclean.1
	install -m 0644 -D doc/git-gau-automerge.1 $(DESTDIR)$(mandir)/man1/git-gau-automerge.1
	install -m 0644 -D doc/git-gau-docker-entry.1 $(DESTDIR)$(mandir)/man1/git-gau-docker-entry.1
	install -m 0644 -D doc/git-gau-exec.1 $(DESTDIR)$(mandir)/man1/git-gau-exec.1
	install -m 0644 -D doc/git-gau-xargs.1 $(DESTDIR)$(mandir)/man1/git-gau-xargs.1

install-bin: bin
	install -m 0755 -D bin/git-gau-ac $(DESTDIR)$(bindir)/git-gau-ac
	install -m 0755 -D bin/git-gau-autoclean $(DESTDIR)$(bindir)/git-gau-autoclean
	install -m 0755 -D bin/git-gau-automerge $(DESTDIR)$(bindir)/git-gau-automerge
	install -m 0755 -D bin/git-gau-exec $(DESTDIR)$(bindir)/git-gau-exec
	install -m 0755 -D bin/git-gau-xargs $(DESTDIR)$(bindir)/git-gau-xargs
	install -m 0755 -D lib/docker-entry $(DESTDIR)$(libdir)/git-gau/docker-entry
	install -m 0755 -D lib/docker-entry.d/50-git-credentials $(DESTDIR)$(libdir)/git-gau/docker-entry.d/50-git-credentials
	install -m 0755 -D lib/docker-entry.d/50-ssh-known-hosts $(DESTDIR)$(libdir)/git-gau/docker-entry.d/50-ssh-known-hosts
	install -m 0755 -D lib/docker-entry.d/50-ssh-privkey $(DESTDIR)$(libdir)/git-gau/docker-entry.d/50-ssh-privkey

install: install-bin install-doc

uninstall:
	-rm -f $(DESTDIR)$(bindir)/git-gau-ac
	-rm -f $(DESTDIR)$(bindir)/git-gau-autoclean
	-rm -f $(DESTDIR)$(bindir)/git-gau-automerge
	-rm -f $(DESTDIR)$(bindir)/git-gau-exec
	-rm -f $(DESTDIR)$(bindir)/git-gau-xargs
	-rm -f $(DESTDIR)$(libdir)/git-gau/docker-entry
	-rm -f $(DESTDIR)$(libdir)/git-gau/docker-entry.d/50-git-credentials
	-rm -f $(DESTDIR)$(libdir)/git-gau/docker-entry.d/50-ssh-known-hosts
	-rm -f $(DESTDIR)$(libdir)/git-gau/docker-entry.d/50-ssh-privkey
	-rm -f $(DESTDIR)$(mandir)/man1/git-gau-ac.1
	-rm -f $(DESTDIR)$(mandir)/man1/git-gau-autoclean.1
	-rm -f $(DESTDIR)$(mandir)/man1/git-gau-automerge.1
	-rm -f $(DESTDIR)$(mandir)/man1/git-gau-docker-entry.1
	-rm -f $(DESTDIR)$(mandir)/man1/git-gau-exec.1
	-rm -f $(DESTDIR)$(mandir)/man1/git-gau-xargs.1

dist-bin:
	-rm -rf build
	make DESTDIR=build prefix=/ install
	mkdir -p dist
	tar --owner=root:0 --group=root:0 -czf dist/git-gau-dist.tar.gz -C build .

dist-src:
	mkdir -p dist
	git archive -o dist/git-gau-src.tar.gz HEAD

dist: dist-src dist-bin
	cd dist && md5sum git-gau-*.tar.gz > md5sum.txt
	cd dist && sha1sum git-gau-*.tar.gz > sha1sum.txt
	cd dist && sha256sum git-gau-*.tar.gz > sha256sum.txt

integration-test: dist
	${MAKE} -C integration-test all

.PHONY: \
	all \
	clean \
	dist \
	dist-bin \
	dist-src \
	install \
	install-bin \
	install-doc \
	integration-test \
	lint \
	test \
	uninstall \
