ifeq ($(prefix),)
    prefix := /usr/local
endif
ifeq ($(exec_prefix),)
    exec_prefix := $(prefix)
endif
ifeq ($(bindir),)
    bindir := $(exec_prefix)/bin
endif
ifeq ($(datarootdir),)
    datarootdir := $(prefix)/share
endif
ifeq ($(mandir),)
    mandir := $(datarootdir)/man
endif

all: bin test doc

%.1 : %.1.md
	pandoc -s -t man $< -o $@

bin:
	# empty for now

lint: bin
	shellcheck bin/git-gau-ac
	shellcheck bin/git-gau-exec
	shellcheck bin/git-gau-xargs

test: bin
	PATH="$(shell pwd)/bin:${PATH}" python -m test

doc: \
	doc/git-gau-ac.1 \
	doc/git-gau-exec.1 \
	doc/git-gau-xargs.1

clean:
	-rm -f doc/git-gau-ac.1
	-rm -f doc/git-gau-exec.1
	-rm -f doc/git-gau-xargs.1
	-rm -rf dist
	-rm -rf build

install-doc: doc
	install -m 0644 -D doc/git-gau-ac.1 $(DESTDIR)$(mandir)/man1/git-gau-ac.1
	install -m 0644 -D doc/git-gau-exec.1 $(DESTDIR)$(mandir)/man1/git-gau-exec.1
	install -m 0644 -D doc/git-gau-xargs.1 $(DESTDIR)$(mandir)/man1/git-gau-xargs.1

install-bin: bin
	install -m 0755 -D bin/git-gau-ac $(DESTDIR)$(bindir)/git-gau-ac
	install -m 0755 -D bin/git-gau-exec $(DESTDIR)$(bindir)/git-gau-exec
	install -m 0755 -D bin/git-gau-xargs $(DESTDIR)$(bindir)/git-gau-xargs

install: install-bin install-doc

uninstall:
	-rm -f $(DESTDIR)$(bindir)/git-gau-ac
	-rm -f $(DESTDIR)$(bindir)/git-gau-exec
	-rm -f $(DESTDIR)$(bindir)/git-gau-xargs
	-rm -f $(DESTDIR)$(mandir)/man1/git-gau-ac.1
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

.PHONY: \
	all \
	clean \
	dist \
	dist-bin \
	dist-src \
	install \
	install-bin \
	install-doc \
	lint \
	test \
	uninstall \
