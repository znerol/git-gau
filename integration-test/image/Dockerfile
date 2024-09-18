FROM alpine:3.20

RUN apk update && apk upgrade && \
    apk add --no-cache bash git openssh

COPY context/git-gau-dist.tar.gz /root/
RUN tar -C /usr/local -xf /root/git-gau-dist.tar.gz

RUN addgroup -S git-gau && adduser -S git-gau -G git-gau

USER git-gau

ENTRYPOINT [ \
    "/usr/bin/ssh-agent", \
    "/usr/local/lib/git-gau/docker-entry", \
    "/usr/local/lib/git-gau/docker-entry.d" \
]
