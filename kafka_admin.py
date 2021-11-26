from kafka import KafkaConsumer
from kafka.admin import KafkaAdminClient, NewTopic

admin: KafkaAdminClient = KafkaAdminClient(bootstrap_servers=['localhost:9092'])

topics = [NewTopic('topic1', 1, 1)]


def add_topics():
    try:
        admin.create_topics(topics)
    except:
        print('Error creating topics')


def remove_topics():
    try:
        admin.delete_topics(list(map(lambda x: x.name, topics)))
    except:
        print('Error deleting topics')


if __name__ == '__main__':
    add_topics()
    remove_topics()
