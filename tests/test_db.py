from helpers import user_information
from lib.db import OpenCartDB

from datetime import datetime

CUSTOMER_DATA = {
    "customer_group_id": 1,
    "language_id": 1,
    "firstname": user_information().get("firstname"),
    "lastname": user_information().get("lastname"),
    "email": user_information().get("email"),
    "telephone": user_information().get("telephone"),
    "password": user_information().get("password"),
    "custom_field": "",
    "ip": user_information().get("ip"),
    "status": 1,
    "safe": 0,
    "token": "",
    "code": "",
    "date_added": str(datetime.now()),
}

DATA_FOR_UPDATE = {
    "firstname": "new_firstname",
    "lastname": "new_lastname",
    "email": "new_email",
    "telephone": "new_telephone",
}

CUSTOMER_TABLE = "oc_customer"


def test_add_customer(connection):
    data_base = OpenCartDB(connection, CUSTOMER_TABLE)

    id_customer = data_base.create_customer(CUSTOMER_DATA)
    selection_result = data_base.select_all_from_table("customer_id", id_customer)
    assert len(selection_result) == 1

    data_base.delete_customer(id_customer)  # tear down


def test_update_existing_customer(connection):
    data_base = OpenCartDB(connection, CUSTOMER_TABLE)

    id_customer = data_base.create_customer(CUSTOMER_DATA)  # set up

    data_base.update_customer(id_customer, DATA_FOR_UPDATE)
    all_data = data_base.select_one_from_table("customer_id", id_customer)

    assert all_data["firstname"] == DATA_FOR_UPDATE["firstname"]
    assert all_data["lastname"] == DATA_FOR_UPDATE["lastname"]
    assert all_data["email"] == DATA_FOR_UPDATE["email"]
    assert all_data["telephone"] == DATA_FOR_UPDATE["telephone"]

    data_base.delete_customer(id_customer)  # tear down


def test_update_customer_negative(connection):
    data_base = OpenCartDB(connection, CUSTOMER_TABLE)

    last_record = data_base.select_last_record("customer_id")
    last_id_in_db = last_record["customer_id"]
    id_customer = last_id_in_db + 1

    result = data_base.update_customer(id_customer, DATA_FOR_UPDATE)

    assert result == 0, f"Trying to update customer with id {id_customer}"


def test_delete_existing_customers(connection):
    data_base = OpenCartDB(connection, CUSTOMER_TABLE)

    id_customer = data_base.create_customer(CUSTOMER_DATA)  # set up

    data_base.delete_customer(id_customer)
    selection_result = data_base.select_all_from_table("customer_id", id_customer)
    assert len(selection_result) == 0, (
        f"Customer with id {id_customer} must be deleted from database"
    )


def test_delete_customers_negative(connection):
    data_base = OpenCartDB(connection, CUSTOMER_TABLE)

    last_record = data_base.select_last_record("customer_id")
    last_id_in_db = last_record["customer_id"]
    id_customer = last_id_in_db + 1

    result = data_base.delete_customer(id_customer)
    assert result == 0, f"Trying to delete customer with id {id_customer}"
