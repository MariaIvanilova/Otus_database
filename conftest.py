import pymysql
import pymysql.cursors
import pytest


def pytest_addoption(parser):
    parser.addoption("--host", default="localhost")
    parser.addoption("--port", default=3306)
    parser.addoption("--database", default="bitnami_opencart")
    parser.addoption("--user", default="bn_opencart")
    parser.addoption("--password", default="")


@pytest.fixture(scope="session")
def connection(request):
    host = request.config.getoption("host")
    port = request.config.getoption("port")
    database = request.config.getoption("database")
    user = request.config.getoption("user")
    password = request.config.getoption("password")

    connection = pymysql.connect(
        host=host,
        port=port,
        database=database,
        user=user,
        password=password,
        cursorclass=pymysql.cursors.DictCursor,
    )
    yield connection

    connection.close()
