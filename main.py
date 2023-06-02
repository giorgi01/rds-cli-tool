import boto3
import requests
import argparse
from os import getenv


def create_db_instance(rds_client, name, identifier, storage, storage_type, engine, master_user, master_password, security_group_ids):
  response = rds_client.create_db_instance(
    DBName=name,
    DBInstanceIdentifier=identifier,
    AllocatedStorage=storage,
    DBInstanceClass='db.t4g.micro',
    Engine=engine,
    MasterUsername=master_user,
    MasterUserPassword=master_password,
    BackupRetentionPeriod=7,
    Port=5432,
    MultiAZ=False,
    EngineVersion='13.5',
    AutoMinorVersionUpgrade=True,
    PubliclyAccessible=True,
    Tags=[
      {
        'Key': 'Name',
        'Value': 'First RDS'
      },
    ],
    StorageType='gp2',
    EnablePerformanceInsights=True,
    PerformanceInsightsRetentionPeriod=7,
    DeletionProtection=False,
    VpcSecurityGroupIds=security_group_ids
  )

  _id = response.get("DBInstance").get("DBInstanceIdentifier")
  print(f"Instance {_id} was created")

  return response


def print_connection_params(rds_client, identifier):
  response = rds_client.describe_db_instances(DBInstanceIdentifier=identifier)
  instance = response.get("DBInstances")[0]
  endpoint = instance.get("Endpoint")
  host = endpoint.get("Address")
  port = endpoint.get("Port")
  username = instance.get("MasterUsername")
  db_name = instance.get("DBName")
  print("DB Host:", host)
  print("DB port:", port)
  print("DB user:", username)
  print("DB database:", db_name)


def reboot_rds(rds_client, identifier):
  rds_client.reboot_db_instance(DBInstanceIdentifier=identifier)
  print(f"RDS - {identifier} rebooted successfully")


def stop_rds(rds_client, identifier):
  response = rds_client.stop_db_instance(
    DBInstanceIdentifier=identifier, DBSnapshotIdentifier="stop-snapshot001")

  print(response)


def start_rds(rds_client, identifier):
  response = rds_client.start_db_instance(DBInstanceIdentifier=identifier)

  print(response)


def update_rds_pass(rds_cient, identifer):
  response = rds_cient.modify_db_instance(DBInstanceIdentifier=identifer,
                                          MasterUserPassword="new-pa$$word")

  print(response)


def delete_rds_pass(rds_cient, identifer):
  response = rds_cient.modify_db_instance(DBInstanceIdentifier=identifer,
                                          MasterUserPassword="new-pa$$word")

  print(response)


def main():

  parser = argparse.ArgumentParser(description='Create an RDS instance with specified config')
  parser.add_argument('--db-name', type=str, default='mysql', help='Name of the database')
  parser.add_argument('--db-identifier', type=str, default='demo-mysql-db-1', help='Identifier for the RDS instance')
  parser.add_argument('--storage', type=int, default=60, help='Allocated storage in GB')
  parser.add_argument('--engine', type=str, default='mysql', help='Database engine')
  parser.add_argument('--master-username', type=str, default='admin', help='Master username')
  parser.add_argument('--master-password', type=str, default='strongrandompassword', help='Master password')
  parser.add_argument('--storage-type', type=str, default='gp2', help='Storage type')
  parser.add_argument('--security-group-ids', nargs='+', help='Security Group IDs', required=True)

  
  args = parser.parse_args()

  rds_client = boto3.client('rds',
    aws_access_key_id=getenv("aws_access_key_id"),
    aws_secret_access_key=getenv("aws_secret_access_key"),
    aws_session_token=getenv("aws_session_token"),
    region_name=getenv("aws_region_name")
  )
  
  db_instance = create_db_instance(rds_client, args.db_name, args.db_identifier, args.storage, args.storage_type, args.engine, args.master_username, args.master_password, args.security_group_ids)
  print(db_instance)

if __name__ == '__main__':
  main()
