import boto3
import pickle
from datetime import datetime


class S3Connector:
    def __init__(self):
        self.bucket_name = "botboibucket"


    def get_last_buy_price(self, asset_name):
        # Returns float value of last buy price for given asset_name
        s3_path = asset_name + "/last_buy_price"
        s3 = boto3.resource("s3")
        ob = s3.Object(self.bucket_name, s3_path)
        last_buy_price = ob.get()['Body'].read().decode('utf-8')
        return float(last_buy_price)


    def set_last_buy_price(self, asset_name, close):
        # Stores value of last buy price for pair
        s3_path = asset_name + "/last_buy_price"
        s3 = boto3.resource("s3")
        encoded_string = str(close).encode("utf-8")
        s3.Bucket(self.bucket_name).put_object(Key=s3_path, Body=encoded_string)

    def log_position_entered(self, asset_name, close):
        # Stores value of last buy price for asset
        now = datetime.now()
        dt_string = now.strftime("%m-%d-%Y %H:%M:%S")
        s3_path = "trades" + "/{}".format(dt_string)
        s3 = boto3.resource("s3")
        position_info = {
            "asset_name": asset_name,
            "buy_price": str(close),
            "sell_price": "",
            "status": "ACTIVE"
        }
        encoded_list = str(position_info).encode("utf-8")
        s3.Bucket(self.bucket_name).put_object(Key=s3_path, Body=encoded_list)

    def get_trades(self):
        # Returns float value of last buy price for given asset_name
        s3_path = "trades"
        s3 = boto3.resource("s3")
        for bucket in s3.buckets.all():
            for ob in bucket.objects.filter(Prefix="trades/"):
                print(bucket.name)
                print(ob.key)
                print(ob.get()['Body'].read().decode('utf-8'))
        


if __name__ == "__main__":

    # Tests
    test_asset_name = "TEST"
    test_close_price = "734.50"

    S3 = S3Connector()
    # Test 1
    #S3.set_last_buy_price(test_asset_name, test_close_price)
    #print(S3.get_last_buy_price(test_asset_name))

    # Test 2
    S3.log_position_entered(test_asset_name, test_close_price)
    S3.get_trades()