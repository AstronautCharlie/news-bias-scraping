#!/bin/sh

aws dynamodb create-table \
    --endpoint-url=http://dynamo_db:4566 \
    --table-name dev-table \
    --attribute-definitions \
        AttributeName=url,AttributeType=S \
        AttributeName=date,AttributeType=S \
    --key-schema \
        AttributeName=url,KeyType=HASH \
        AttributeName=date,KeyType=RANGE \
    --provisioned-throughput \
        ReadCapacityUnits=10,WriteCapacityUnits=5