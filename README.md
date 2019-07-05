# macaddress.io simple client

This CLI tool lets you query the macaddress.io API to get the vendor that made a device based on
its MAC address.

## Usage

```
macaddress-client.py <mac address>
```

As https://macaddress.io/ API requires authentication, the script won't work unless you set your
API key in an environment variable named `MACADDRESS_API_KEY`.

The program outputs the vendor in plain text without any newline characters.

In case there are any errors, a verbose message will be printed on standard error output and a non-zero exit code.

If vendor could not be determined, `(Unknown vendor)` will be printed.

Examples:

```
% export MACADDRESS_API_KEY=xxx
% ./macaddress-client.py f8:94:c2:d5:5a:53; echo
Intel Corp
% ./macaddress-client.py aa:bb:cc:dd:ee:ff; echo
(Unknown vendor)

# After forcing a network error
% ./macaddress-client.py aa:bb:cc:dd:ee:ff
[stderr] Request failed when connecting: HTTPSConnectionPool(host='xapi.macaddress.io', port=443): Max retries exceeded with url: /v1?output=vendor&search=aa%3Abb%3Acc%3Add%3Aee%3Aff (Caused by NewConnectionError('<urllib3.connection.VerifiedHTTPSConnection object at 0x7f38335e4b00>: Failed to establish a new connection: [Errno -2] Name or service not known',))
% echo $?
255
```

## Docker

This application has been dockerized by using the `python:3` as the base image.

To build it, just run the following command:

```
docker build -t macaddress-client .
```

You can run the tool on a new container using the following example command:

```
docker run \
    -it \
    --rm \
    -e MACADDRESS_API_KEY=xxx \
    macaddress-client f8:94:c2:d5:5a:52
```

Note that you need to pass the API key using an environment variable. If you have it already
exported on your shell session, omit the `=xxx` part when calling `docker run`.

## Security considerations

Your API key has to be set on an environment variable. Note that depending on how you do that, it can be read by other programs. If you want to make sure it can be just read by this tool, define it the following way:

```
% MACADDRESS_API_KEY=xxx ./macaddress-client aa:bb:cc:dd:ee:ff
```

Take into consideration that the tool will honor any `http_proxy`/`https_proxy` environment variables you have set.

Remote TLS certificate will be checked against your OS list of trusted certificates. Make sure your computer time and date are correct and ideally synchronized with an external NTP server.

## Further improvements

There are many improvements that can be added to this tool, but weren't added because they were out
of scope:

* Add caching support, so the tool can use an external storage (e.g. redis/memcached/others) to
  store previously searched values. This would make it a bit faster and also would overcome the
  limitations of the API regarding the maximum number of requests allowed per day
* Add support for other output formats, such as YAML or JSON. This is easily doable, although a CLI
  tool would probably not benefit much from this.
* Use a smaller base image for the Docker image, such as `python:3-slim` or `python:3-alpine`
