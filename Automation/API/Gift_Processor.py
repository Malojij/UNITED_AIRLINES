class Gift_processor:

    @staticmethod
    def BlackHawkUpc_finder(cardnumber):
        if cardnumber == "9840000061933746424":
            return "71373309045"
        if cardnumber == "9840000060454102009":
            return "71373309038"
        if cardnumber == "9840000079000000046":
            return "71373309079"
        if cardnumber == "9840000067600001688":
            return "71373309053"
        if cardnumber == "9840000067000004787":
            return "71373309077"
        if cardnumber == "9840000070000000391":
            return "04125010012"
        if cardnumber == "9840000065000009699":
            return "71373309057"
        if cardnumber == "9840000069000001474":
            return "71373309078"
        if cardnumber == "9840000070000001391":
            return "04125010012"
        if cardnumber == "4358361000067716":
            return "07675022645"
        if cardnumber == "4143521000074208":
            return "07675023072"
        if cardnumber == "5311050209356771":
            return "07675017832"
        else:
            return "00000000000"