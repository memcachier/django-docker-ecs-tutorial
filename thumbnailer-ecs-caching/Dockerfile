# Build from default Python image (don't use "django" base image: it's
# obsolete).
FROM python:3.6.5

# This is the port that Gunicorn uses, so expose it to the outside
# world.
EXPOSE 8000

# Don't just add the base code directory, to try to cut down on
# rebuild sizes.
RUN mkdir /thumbnailer
WORKDIR /thumbnailer

# Install all the requirements -- doing things in this order should
# reduce the size of redeployments if we don't change dependencies.
ADD requirements.txt /thumbnailer/
RUN pip install -r requirements.txt

# Add the main code directory and point at the start script.
ADD . /thumbnailer
WORKDIR /thumbnailer/thumbnailer
CMD ["./start.sh"]
