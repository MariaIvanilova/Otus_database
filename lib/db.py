class OpenCartDB:

    def __init__(self, table):
        self.table = table


    def create_customer(self, connection, customer_data: dict) -> int:
        cursor = connection.cursor()
        sql = f"INSERT INTO {self.table} " \
              f"(customer_group_id, language_id, firstname, lastname, email, telephone, password, custom_field," \
              f" ip, status, safe, token, code, date_added)" \
              f" VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)"
        cursor.execute(sql, (customer_data["customer_group_id"], customer_data["language_id"],
                             customer_data["firstname"], customer_data["lastname"], customer_data["email"],
                             customer_data["telephone"], customer_data["password"], customer_data["custom_field"],
                             customer_data["ip"], customer_data["status"], customer_data["safe"],
                             customer_data["token"], customer_data["code"], customer_data["date_added"]))
        connection.commit()

        cursor.execute(f"SELECT * FROM {self.table} WHERE customer_id = LAST_INSERT_ID()")
        last_added_id = cursor.fetchall()[0]['customer_id']
        return last_added_id

    def update_customer(self, connection, id_customer, update_data: dict):
        cursor = connection.cursor()
        sql = f"UPDATE {self.table} SET firstname = %s, lastname = %s, email = %s, telephone = %s WHERE" \
              f" customer_id = {id_customer}"
        result = cursor.execute(sql, (update_data["firstname"], update_data["lastname"], update_data["email"],
                             update_data["telephone"]))
        connection.commit()
        return result


    def delete_customer(self, connection, id_customer):
        cursor = connection.cursor()
        sql = f"DELETE FROM {self.table} WHERE customer_id={id_customer}"
        result = cursor.execute(sql)
        connection.commit()
        return result

    def select_from_table(self, connection, field, value):
        cursor = connection.cursor()
        sql = f"SELECT * FROM {self.table} WHERE {field}={value}"
        cursor.execute(sql)
        selected_data = cursor.fetchall()
        return selected_data

    def select_last_record(self, connection, field):
        cursor = connection.cursor()
        sql = f"SELECT * FROM {self.table} ORDER BY {field} DESC LIMIT 1"
        cursor.execute(sql)
        selected_data = cursor.fetchall()
        return selected_data

    def print_select_all_from_table(self, connection):
        cursor = connection.cursor()
        sql = f"SELECT * FROM {self.table}"
        cursor.execute(sql)
        all_data = cursor.fetchall()
        for record in all_data:
            print(f"{record}")
