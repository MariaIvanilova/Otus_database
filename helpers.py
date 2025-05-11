from faker import Faker


def user_information():
    fake = Faker("en")
    return {
        "firstname": fake.first_name(),
        "lastname": fake.last_name(),
        "email": fake.email(),
        "telephone": fake.phone_number(),
        "password": fake.password(),
        "ip": fake.ipv4_private(),
    }
