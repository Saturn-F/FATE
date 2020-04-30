import pika, json

lines = []
with open("./tmp_share", "r") as f:
    lines = f.readlines()

job_id = lines[2].replace('\n', "")
user = lines[0].replace('\n', "")
password = lines[1].replace('\n', "")


credentials = pika.PlainCredentials(user, password)
connection = pika.BlockingConnection(pika.ConnectionParameters("localhost", 5672, job_id, credentials))
channel = connection.channel()

send_list = [1, 2, 3, 4] 
channel.basic_publish(exchange="", routing_key="send-{}".format(job_id), body=json.dumps(send_list))
print("Send: ", send_list)

for method, properties, body in channel.consume(queue="receive-{}".format(job_id)):
    print("Receive: ", body)
    channel.basic_ack(delivery_tag=method.delivery_tag)
