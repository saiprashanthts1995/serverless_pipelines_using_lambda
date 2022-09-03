import boto3
import os
import time
from boto3.dynamodb.conditions import Key, Attr


class DynamoService:
    def __init__(self):
        os.environ.setdefault("AWS_PROFILE", "serverless")
        self.client = boto3.client("dynamodb")
        self.resource = boto3.resource("dynamodb")

    def create_table(
        self,
        table_name,
        key_schema,
        attributes_definition,
        billing_mode="PAY_PER_REQUEST",
    ):
        # Only the attributes mentioned in the KeySchema
        # should be used ib Attribute Definition
        # Other Non-key attributes will be taken
        # directly while we write the data
        create_table_response = self.client.create_table(
            AttributeDefinitions=attributes_definition,
            TableName=table_name,
            KeySchema=key_schema,
            BillingMode=billing_mode,
        )
        return create_table_response

    def delete_table(self, table_name):
        delete_table_response = self.client.delete_table(TableName=table_name)
        return delete_table_response

    def retrieve_table_content_using_scan(
        self,
        table_name,
        filter_condition,
        select_type,
        select_attributes,
        alias_columns,
    ):
        # Here, we can do filter based on Hash key or Range Key separately.
        # To filter based on range of one column use the below syntax
        # Attr('timestamp').between(1483130000, 1483133600) &
        # Attr('tags').exists()
        # default value for select is "ALL_ATTRIBUTES"
        # if "ALL_attributes" is mentioned then projection and
        # ExpressionAttributeNames shouldn't be provided
        # Here for scan make use of resource
        table = self.resource.Table(table_name)
        response = table.scan(
            Select=select_type,
            FilterExpression=filter_condition,
            ProjectionExpression=select_attributes,
            ExpressionAttributeNames=alias_columns,
        )
        result = response["Items"]
        while "LastEvaluatedKey" in response:
            response = table.scan(
                Select=select_type,
                FilterExpression=filter_condition,
                ProjectionExpression=select_attributes,
                ExpressionAttributeNames=alias_columns,
                ExclusiveStartKey=response["LastEvaluatedKey"],
            )
            result.extend(response["Items"])
        return result

    def delete_table_entry(self, table_name, key_dict):
        pass

    def retrieve_table_content_using_get(self, table_name, filter_expression):
        # We need to search based on combination of Hash and Range Key
        # Only providing the Hash key doesn't work here
        # We cannot search based on Non-key attributes using get_item
        get_response = self.client.get_item(
            TableName=table_name, Key=filter_expression
        )["Item"]
        return get_response

    def write_to_table(self, table_name, item):
        write_response = self.client.put_item(TableName=table_name, Item=item)
        return write_response


if __name__ == "__main__":
    db = DynamoService()
    """
    # Delete the table
    delete_table_response = db.delete_table(table_name="test")
    print(delete_table_response)
    time.sleep(10)

    # Create the table
    create_table_response = db.create_table(
        table_name="test",
        key_schema=[
            {"AttributeName": "ID", "KeyType": "HASH"},
            {"AttributeName": "Name", "KeyType": "RANGE"},
        ],
        attributes_definition=[
            {"AttributeName": "ID", "AttributeType": "S"},
            {"AttributeName": "Name", "AttributeType": "S"},
        ],
    )
    print(create_table_response)
    time.sleep(20)

    # write to the table
    for i in range(5):
        response = db.write_to_table(
            table_name="test",
            item={
                "ID": {"S": str(i)},
                "Name": {"S": f"Element_{i}"},
                "Date": {"N": "3725"},
            },
        )
        print(response)
    time.sleep(20)

    # read using get_item method. Here we can use only key attributes.
    # Mention both Hash and range key. otherwise this doesn't work
    print(
        db.retrieve_table_content_based_on_get(
            table_name="test",
            filter_expression={
                "ID": {"S": "1"},
                "Name": {"S": "Element_1"},
            },
        )
    )
    """

    # read using scan
    time.sleep(5)
    output = db.retrieve_table_content_using_scan(
        table_name="test",
        filter_condition=Attr("Date").eq(3725) & Key("ID").eq("1"),
        select_type="SPECIFIC_ATTRIBUTES",
        # filter_condition=Key("ID").eq('1')
        # filter_condition=Key("ID").eq('1') & Key("Name").eq('Element_1'),
        select_attributes="ID, #Name_NonKeyName, #Date_NonKeyName",
        alias_columns={"#Name_NonKeyName": "Name", "#Date_NonKeyName": "Date"},
    )
    print(output)
