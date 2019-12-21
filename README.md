# pokkins

Zero-config podcast hosting.

## use-case

I have a directory full of audio-files on a server, and I want them to be accessible as a podcast.

## docker approach

```shell
$ docker build --rm -t pokkins .
$ docker run -it --rm -v $(pwd):/mnt/vin/eps -p 8092:8092 pokkins
```
