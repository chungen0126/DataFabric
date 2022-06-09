import pika, sys, os
import urllib.parse
import json
import time

def main():
    try_times = 10
    while try_times > 0:
        try:
            credentials = pika.PlainCredentials('guest', 'guest')
            connection = pika.BlockingConnection(pika.ConnectionParameters(host='datafabric-rabbitmq', credentials=credentials))
            channel = connection.channel()
            break
        except:
            try_times -= 1
            if try_times >= 1:
                print("Connection failed. Retry in 3 seconds")
                time.sleep(3)

    channel.queue_declare(queue='task_req')

    def callback(ch, method, properties, body):
        print(body)
        sys.stdout.flush()
        body = urllib.parse.unquote(body.decode('utf-8'))
        print(" [x] Received %s" % body)
        try:
            print(json.loads(body))
            sys.stdout.flush()
        except:
            pass

    channel.basic_consume(queue='task_req', on_message_callback=callback, auto_ack=True)

    print("start consuming")
    sys.stdout.flush()
    channel.start_consuming()

if __name__ == '__main__':
    main()