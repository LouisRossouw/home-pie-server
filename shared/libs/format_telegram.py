
def build_txt(txt_list):
    txt_str = ""
    for txt in txt_list:
        txt_str += str(txt)
    return str(txt_str)


# Temp.
def new_user_format(username, account_type):
    """ Format for new users signup """

    txt_list = [
        f"😄🎉 A New user signed up:"
        f"\n\n👱‍♂️ : {username}"
        f"\n📃 : {account_type}"
    ]

    return build_txt(txt_list)
