#!/urs/bin/python3
import request_client

broker = '10.64.98.135'
port = 1883
name = 'publisher'
topic = 'CME466-deliverable3'

client = request_client.MqttClient(broker,port,topic,name,None)
client.run_subscribe()
