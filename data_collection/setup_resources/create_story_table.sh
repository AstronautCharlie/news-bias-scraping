aws dynamodb create-table \
    --endpoint-url=http://localstack-dynamodb:4566 \
    --table-name stories \
    --attribute-definitions \
        AttributeName=url,AttributeType=S \
    --key-schema \
        AttributeName=url,KeyType=HASH \
    --provisioned-throughput ReadCapacityUnits=10,WriteCapacityUnits=5 \

rc=$?
if [[ "${rc}" -eq 0 ]]; then
    echo "CNN table created successfully"
else 
    echo "CNN table failed to create"
fi 
exit "${rc}"