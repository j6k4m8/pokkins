# 🎧 pokkins

Zero-config podcast hosting.

## use-case

I have a directory full of audio-files on a server, and I want them to be accessible as a podcast.

## usage 

Open the directory you want to serve:

```shell
$ cd my-audio
$ ls
Episode1.mp4
Episode2.mp4
```

## docker approach 

Start the `pokkins` Docker container:


```shell
$ docker build --rm -t pokkins .
$ docker run -it --rm -v $(pwd):/mnt/vin/eps -p 8092:8092 pokkins
```

If you can guarantee that this host will remain static and publicly accessible, then you can submit `http://[host]:8092/feed.xml` as a podcast URL to most podcast apps. 


## native python approach:

Note that you may first need to install dependencies with `poetry install`.

```shell
$ python3 -c "from pokkins import Pokkins; print(Pokkins('eps').generate_rss())" > feed.xml
```

You can now serve the directory over HTTP. One simple way to do this:

```shell
$ python3 -m http.server 8092
```

This hosts the feed XML and the episodes; rather than running a python http server (which is jank!!), you can also upload the whole thing to an s3 bucket, for example.

## faq

#### i came here because i wanted to start a podcast! this looks hard!

mehhh yeah it is, email me at opensource-at-matelsky-dot-com and I'll try to help you

#### how do i add tags? how do I add episode descriptions?

right now, you can't. but if you want those features, ① consider using a more advanced podcast syndication service (this one is really just bare-bones to get something running with zero config, and has no bells or whistles ②  make a new Issue or Pull Request and I'll try to triage!
