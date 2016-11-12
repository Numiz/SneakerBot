#!/usr/bin/env python3

from cryptography.fernet import Fernet
import sys
import json

"""An interactive script for generating userinfo.json"""
if sys.version_info[0] == 2:
    input = raw_input


def make_info():
    key = Fernet.generate_key()
    cipher_suite = Fernet(key)
    
    configuration = {}
    
    print("You may simply press <enter> without inputting anything to any of")
    print("these questions, but this may produce strange errors.")
    configuration["key"] = key.decode()
    configuration["first_name"] = cipher_suite.encrypt(input("Please enter your first name: ").encode()).decode()
    configuration["last_name"] = cipher_suite.encrypt(input("Please enter your last name: ").encode()).decode()
    configuration["phone_number"] = cipher_suite.encrypt(input("Please enter your phone number: ").encode()).decode()
    configuration["email"] = cipher_suite.encrypt(input("Please enter your email address: ").encode()).decode()
    configuration["shipping_address_1"] = cipher_suite.encrypt(input("Please enter the first line of your shipping address: ").encode()).decode()
    configuration["shipping_address_2"] = cipher_suite.encrypt(input(
        "Please enter the second line of your shipping address (hit <enter> if the second line is an apartment/suite number): ").encode()).decode()
    configuration["shipping_apt_suite"] = cipher_suite.encrypt(input("Please enter your apartment/suite number, if applicable: ").encode()).decode()
    configuration["shipping_city"] = cipher_suite.encrypt(input("Please enter your shipping city: ").encode()).decode()
    configuration["shipping_state"] = cipher_suite.encrypt(input("Please enter your shipping state (not abbreviated): ").encode()).decode()
    configuration["shipping_state_abbrv"] = cipher_suite.encrypt(input("Please enter your shipping state (abbreviated): ").encode()).decode()
    configuration["shipping_country"] = cipher_suite.encrypt(input("Please enter your shipping country (not abbreviated): ").encode()).decode()
    configuration["shipping_country_abbrv"] = cipher_suite.encrypt(input("Please enter your shipping country (abbreviated): ").encode()).decode()
    configuration["shipping_zip"] = cipher_suite.encrypt(input("Please enter your shipping zip/post code: ").encode()).decode()

    billing = cipher_suite.encrypt(input("Is your billing address different than the shipping address? [Y/N]: ").title().encode()).decode()
    if billing in ["Y", "Yes"]:
        configuration["billing_address_1"] = cipher_suite.encrypt(input("Please enter the first line of your billing address: ").encode()).decode()
        configuration["billing_address_2"] = cipher_suite.encrypt(input(
            "Please enter the second line of your billing address (hit <enter> if the second line is an apartment/suite number): ").encode()).decode()
        configuration["billing_apt_suite"] = cipher_suite.encrypt(input("Please enter your apartment/suite number, if applicable: ").encode()).decode()
        configuration["billing_city"] = cipher_suite.encrypt(input("Please enter your billing city: ").encode()).decode()
        configuration["billing_state"] = cipher_suite.encrypt(input("Please enter your billing state (not abbreviated): ").encode()).decode()
        configuration["billing_state_abbrv"] = cipher_suite.encrypt(input("Please enter your billing state (abbreviated): ").encode()).decode()
        configuration["billing_country"] = cipher_suite.encrypt(input("Please enter your billing country: ").encode()).decode()
        configuration["billing_zip"] = cipher_suite.encrypt(input("Please enter your billing zip/post code: ").encode()).decode()
    else:
        configuration["billing_address_1"] = configuration["shipping_address_1"]
        configuration["billing_address_2"] = configuration["shipping_address_2"]
        configuration["billing_apt_suite"] = configuration["shipping_apt_suite"]
        configuration["billing_city"] = configuration["shipping_city"]
        configuration["billing_state"] = configuration["shipping_state"]
        configuration["billing_state_abbrv"] = configuration["shipping_state_abbrv"]
        configuration["billing_country"] = configuration["shipping_country"]
        configuration["billing_country_abbrv"] = configuration["shipping_country_abbrv"]
        configuration["billing_zip"] = configuration["shipping_zip"]

    configuration["card_type"] = cipher_suite.encrypt(input("Please enter your credit card type (Visa, MasterCard, Amex...)? "
                                                            ).encode()).decode()
    print("")
    print(
        "It is recommended that, if you are testing, you input a real card number but a fake CVV. "
        "This way, checkout will proceed as normal so you can see what will occur, but nothing will be charged to your account.")
    print("")
    configuration["card_number"] = cipher_suite.encrypt(input("Please enter your credit card number: "
                                                              ).encode()).decode()
    configuration["card_cvv"] = cipher_suite.encrypt(input("Please enter the CVV for that credit card: "
                                                           ).encode()).decode()
    configuration["card_exp_year"] = cipher_suite.encrypt(input("Please enter your card expiration year: "
                                                                ).encode()).decode()
    configuration["card_exp_month"] = cipher_suite.encrypt(input("Please enter your card expiration month: "
                                                                 ).encode()).decode()
    configuration["name_on_card"] = cipher_suite.encrypt(input("Please enter your name as it appears on this card: "
                                                               ).encode()).decode()
    print("Thank you! All done.")
    
    with open("userinfo.json", "w") as conffile:
        json.dump(configuration, conffile, sort_keys=True, indent=4)
    
           
def get_info():
    import json
    with open("userinfo.json") as conffile:
        userinfo = json.load(conffile)

    key = userinfo["key"]

    cipher_suite = Fernet(key)

    card_cvv = cipher_suite.decrypt(userinfo["card_cvv"].encode()).decode()
    card_exp_month = cipher_suite.decrypt(userinfo["card_exp_month"].encode()).decode()
    card_exp_year = cipher_suite.decrypt(userinfo["card_exp_year"].encode()).decode()
    card_number = cipher_suite.decrypt(userinfo["card_number"].encode()).decode()
    card_type = cipher_suite.decrypt(userinfo["card_type"].encode()).decode()
    email = cipher_suite.decrypt(userinfo["email"].encode()).decode()
    first_name = cipher_suite.decrypt(userinfo["first_name"].encode()).decode()
    last_name = cipher_suite.decrypt(userinfo["last_name"].encode()).decode()
    phone_number = cipher_suite.decrypt(userinfo["phone_number"].encode()).decode()
    shipping_address_1 = cipher_suite.decrypt(userinfo["shipping_address_1"].encode()).decode()
    shipping_address_2 = cipher_suite.decrypt(userinfo["shipping_address_2"].encode()).decode()
    shipping_apt_suite = cipher_suite.decrypt(userinfo["shipping_apt_suite"].encode()).decode()
    shipping_city = cipher_suite.decrypt(userinfo["shipping_city"].encode()).decode()
    shipping_state = cipher_suite.decrypt(userinfo["shipping_state"].encode()).decode()
    shipping_state_abbrv = cipher_suite.decrypt(userinfo["shipping_state_abbrv"].encode()).decode()
    shipping_zip = cipher_suite.decrypt(userinfo["shipping_zip"].encode()).decode()
    shipping_country = cipher_suite.decrypt(userinfo["shipping_country"].encode()).decode()
    shipping_country_abbrv = cipher_suite.decrypt(userinfo["shipping_country_abbrv"].encode()).decode()
    billing_address_1 = cipher_suite.decrypt(userinfo["billing_address_1"].encode()).decode()
    billing_address_2 = cipher_suite.decrypt(userinfo["billing_address_2"].encode()).decode()
    billing_apt_suite = cipher_suite.decrypt(userinfo["billing_apt_suite"].encode()).decode()
    billing_city = cipher_suite.decrypt(userinfo["billing_city"].encode()).decode()
    billing_state = cipher_suite.decrypt(userinfo["billing_state"].encode()).decode()
    billing_state_abbrv = cipher_suite.decrypt(userinfo["billing_state_abbrv"].encode()).decode()
    billing_zip = cipher_suite.decrypt(userinfo["billing_zip"].encode()).decode()
    billing_country = cipher_suite.decrypt(userinfo["billing_country"].encode()).decode()
    billing_country_abbrv = cipher_suite.decrypt(userinfo["billing_country_abbrv"].encode()).decode()
    
    return {
        'card_cvv': card_cvv,
        'card_exp_month': card_exp_month,
        'card_exp_year': card_exp_year,
        'card_number': card_number,
        'card_type': card_type,
        'email': email,
        'first_name': first_name,
        'last_name': last_name,
        'phone_number': phone_number,
        'shipping_address_1': shipping_address_1,
        'shipping_address_2': shipping_address_2,
        'shipping_apt_suite': shipping_apt_suite,
        'shipping_city': shipping_city,
        'shipping_state': shipping_state,
        'shipping_state_abbrv': shipping_state_abbrv,
        'shipping_zip': shipping_zip,
        'shipping_country': shipping_country,
        'shipping_country_abbrv': shipping_country_abbrv,
        'billing_address_1': billing_address_1,
        'billing_address_2': billing_address_2,
        'billing_apt_suite': billing_apt_suite,
        'billing_city': billing_city,
        'billing_state': billing_state,
        'billing_state_abbrv': billing_state_abbrv,
        'billing_zip': billing_zip,
        'billing_country': billing_country,
        'billing_country_abbrv': billing_country_abbrv
    }


if __name__ == '__main__':
    make_info()
