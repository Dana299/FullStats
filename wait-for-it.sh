#!/bin/sh

sleep 10
celery --broker=amqp://guest:guest@rabbitmq:5672// flower