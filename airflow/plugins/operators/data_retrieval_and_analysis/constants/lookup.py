personal_data_value_patterns = {
    # source of patterns ssn, credit_card: https://www.ibm.com/docs/en/guardium/10.5?topic=discover-regular-expressions, last visited at: 2021-07-08
    "ssn":
    r"[0-9]{3}-[0-9]{2}-[0-9]{4}",
    "credit_card":
    r"[0-9]{4}[-, ]?[0-9]{4}[-, ]?[0-9]{4}[-, ]?[0-9]{4}",
    # source of pattern ipv4  https://www.oreilly.com/library/view/regular-expressions-cookbook/9780596802837/ch07s16.html, last visited at: 2021-07-08
    "ipv4":
    r"^(?:(?:25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)\.){3}(?:25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)$",
}

personal_data_key_words = [
    "user", "person", "customer", "contact", "first name", "forename",
    "given name", "user_name", "zip code", "address", "ip", "phone", "gender",
    "email", "lat", "lon", "credit"
]

mongo_internal_collections = ["admin", "local", "config"]
mongo_internal_keys = ["_id", "createdAt", "updatedAt", "__v"]
postgresql_personal_data_types = {
    "CIDR": ["ipv4", "ipv6"],
    "INET": ["ipv4", "ipv6"]
}