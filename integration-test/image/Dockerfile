FROM alpine:latest

RUN apk update && apk upgrade && \
    apk add --no-cache bash git openssh

COPY context/git-gau-dist.tar.gz /root/
RUN tar -C /usr/local -xf /root/git-gau-dist.tar.gz

USER nobody

ENTRYPOINT ["/usr/bin/git", "gau-entry"]
