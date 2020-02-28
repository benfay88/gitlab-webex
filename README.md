# Gitlab Cisco Webex teams

webhook endpoint for gitlab and cisco webex teams

# Installation

Start by creating a bot at [Cisco Webex for Developers](https://developer.webex.com)
Invite your bot to the desired Webex team room

Both `SPARK_ROOM` and `SPARK_ACCESS_TOKEN` must be exported as environment variables
```
export SPARK_ROOM=<your room id>
export SPARK_ACCESS_TOKEN=<Your BOT TOKEN>

### From Source
```python
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
python app.py
```

### Using Docker
Build the image from Dockerfile
```
docker run -p 5000:5000 <Image-Name>
```

Run docker container
```
docker run -d -p 5000:5000 \
  --name <container-name> \
  -e SPARK_ACCESS_TOKEN=$SPARK_ACCESS_TOKEN \
  -e SPARK_ROOM=$SPARK_ROOM \
  <image-name>
```


# Configuration

You can now configure gitlab to send webhook events to the machine you installed
the receiver on as

`<serverip:5000/notify>`

Currently only the following events are supported:

* Push
* issues
* pipeline events
* build events
* comment events
* merge request events

#### Support for characters like å,ä,ö etc is included

Full documentation on gitlab webhooks are available [here](https://docs.gitlab.com/ce/user/project/integrations/webhooks.html)
