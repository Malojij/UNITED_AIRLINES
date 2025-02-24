class fleet_processor:
    Track2_match = [";", "=", "D", "F"]
    Track1_match = ["%", "B", "^"]

    @staticmethod
    def Track_data_reader(Track_data, carddatasource, cardtype):
        global prompt_value
        if carddatasource == "2" or carddatasource == "6":
            if any(x in Track_data for x in fleet_processor.Track2_match):
                if "?" or "=" or "D" or "F" in Track_data:
                    Track_data = Track_data.lstrip(";")
                    Track_data = Track_data.rstrip('?')
                    Track_data = Track_data.rstrip('F')
                    if "=" in Track_data:
                        Track_data = Track_data.split('=')
                    if "D" in Track_data:
                        Track_data = Track_data.split('D')
                    card_data = Track_data[-1]
                    if cardtype.upper() == "VIF":
                        prompt_value = card_data[-1:]
                    if cardtype.upper() == "MCF":
                        prompt_value = card_data[-1:]
                    if cardtype.upper() == "VGF":
                        prompt_value = card_data[4:5]
                    if cardtype.upper() == "WXF":
                        key = card_data[4:5]
                        value = card_data[-1:]
                        prompt_value = str(key) + str(value)
                return prompt_value
        if carddatasource == "1":
            if any(x in Track_data for x in fleet_processor.Track1_match):
                if "%" or "^" in Track_data:
                    Track_data = Track_data.lstrip("%")
                    Track_data = Track_data.rstrip('?')
                    Track_data = Track_data.split("^")
                    card_data = Track_data[-1]
                    if cardtype.upper() == "VIF":
                        prompt_value = card_data[-1:]
                    if cardtype.upper() == "MCF":
                        prompt_value = card_data[-1:]
                    if cardtype.upper() == "VGF":
                        prompt_value = card_data[4:5]
                    if cardtype.upper() == "WXF":
                        key = card_data[4:5]
                        value = card_data[-1:]
                        prompt_value = str(key) + str(value)
                return prompt_value
        if carddatasource == "4":
            if any(x in Track_data for x in fleet_processor.Track1_match):
                if "%" or "^" in Track_data:
                    Track_data = Track_data.lstrip("%")
                    Track_data = Track_data.rstrip('?')
                    Track_data = Track_data.split("^")
                    card_data = Track_data[-1]
                    if cardtype.upper() == "VIF":
                        prompt_value = card_data[-1:]
                    if cardtype.upper() == "MCF":
                        prompt_value = card_data[-1:]
                    if cardtype.upper() == "VGF":
                        prompt_value = card_data[4:5]
                    if cardtype.upper() == "WXF":
                        key = card_data[4:5]
                        value = card_data[-1:]
                        prompt_value = str(key) + str(value)
                return prompt_value

    @staticmethod
    def Track_data_prompt_finder(trackdata, cardatasourse, cardtype):
        if cardtype.upper() == "VIF":
            data = fleet_processor.Track_data_reader(trackdata, cardatasourse, cardtype)
            prompt = fleet_prompt_values.vif_prompt_values(data)
            return prompt
        if cardtype.upper() == "MCF":
            data = fleet_processor.Track_data_reader(trackdata, cardatasourse, cardtype)
            prompt = fleet_prompt_values.mcf_prompt_values(data)
            return prompt
        if cardtype.upper() == "VGF":
            data = fleet_processor.Track_data_reader(trackdata, cardatasourse, cardtype)
            prompt = fleet_prompt_values.vgf_prompt_values(data)
            return prompt
        if cardtype.upper() == "WXF":
            data = fleet_processor.Track_data_reader(trackdata, cardatasourse, cardtype)
            prompt = fleet_prompt_values.wex_prompt_values(data)
            return prompt
        if cardtype.upper() == "FOF":
            prompt = fleet_prompt_values.fof_prompt_values()
            return prompt
        if cardtype.upper() == "FWF":
            prompt = fleet_prompt_values.fwf_prompt_values()
            return prompt
        if cardtype.upper() == "FMF":
            prompt = fleet_prompt_values.fmf_prompt_values()
            return prompt

    @staticmethod
    def cardnumber_finder(Track_data, cds):
        Track2_match = [";", "=", "D", "F"]
        Track1_match = ["%", "B", "^"]
        if cds == "2":
            if any(x in Track_data for x in fleet_processor.Track2_match):
                Track_data = Track_data.lstrip(";")
                Track_data = Track_data.rstrip('?')
                if "=" in Track_data:
                    Track_data = Track_data[:Track_data.index("=")]
                return Track_data
        if cds == "1":
            if any(x in Track_data for x in fleet_processor.Track1_match):
                Track_data = Track_data.lstrip("%B")
                Track_data = Track_data.rstrip('?')
                if "^" in Track_data:
                    Track_data = Track_data[:Track_data.index("^")]
                return Track_data
        if cds == "4":
            if any(x in Track_data for x in fleet_processor.Track1_match):
                Track_data = Track_data.lstrip("%B")
                Track_data = Track_data[:Track_data.index("~")]
                if "^" in Track_data:
                    Track_data = Track_data[:Track_data.index("^")]
                return Track_data
        if cds == "6":
            if any(x in Track_data for x in fleet_processor.Track2_match):
                if "D" in Track_data:
                    Track_data = Track_data[:Track_data.index("D")]
                return Track_data


class fleet_service_indicator:

    @staticmethod
    def vgf_service_indicator(service):
        mastercard = {"0": "Fuel and other products", "1": "Fuel"}
        return mastercard[service]

    @staticmethod
    def vif_service_indicator(service):
        visa = {"0": "Fleet No Restriction(fuel, maintenance, and nonfuel purchases)",
                "1": "Fleet(fuel and maintenance purchases)", "2": "Fleet / Fuel (fuel purchases)",
                "3": "Reserved", "4": "Reserved", "5": "Reserved", "6": "Reserved", "7": "Reserved", "8": "Reserved",
                "9": "Reserved"}
        return visa[service]

    @staticmethod
    def mcf_service_indicator(service):
        mastercard = {"1": "Fuel and other products", "2": "Fuel"}
        return mastercard[service]

    @staticmethod
    def wex_service_indicator(service):
        wex = {"00": "Fuel", "01": "Unrestricted"}
        return wex[service]


class fleet_prompt_values:

    @staticmethod
    def vgf_prompt_values(prompt):
        prompt_value = {"0": "No prompts", "1": "FleetIDFlag", "2": "OdometerFlag",
                        "3": "FleetIDFlag, OdometerFlag"}
        if prompt in prompt_value:
            return prompt_value[prompt]
        else:
            return "Prompts not found in list"

    @staticmethod
    def vif_prompt_values(prompt):
        prompt_value = {"0": "No prompts", "1": "EmployeeIDNumberFlag, OdometerFlag", "2": "VehicleIDNumberFlag, OdometerFlag",
                        "3": "DriverIDNumberFlag, OdometerFlag", "4": "OdometerFlag", "5": "No prompts",
                        "6": "DriverIDNumberFlag, VehicleIDNumberFlag"}
        if prompt in prompt_value:
            return prompt_value[prompt]
        else:
            return "Prompts not found in list"

    @staticmethod
    def mcf_prompt_values(prompt):
        prompt_value = {"0": "No prompts", "1": "EmployeeIDNumberFlag, OdometerFlag", "2": "VehicleIDNumberFlag, OdometerFlag",
                        "3": "DriverIDNumberFlag, OdometerFlag", "4": "OdometerFlag", "5": "No prompts"}
        if prompt in prompt_value:
            return prompt_value[prompt]
        else:
            return "Prompts not found in list"

    @staticmethod
    def wex_prompt_values(prompt):
        prompt_value = {"00": "No Prompts",
                        "10": "OdometerFlag, DriverIDNumberFlag",
                        "11": "OdometerFlag, VehicleIDNumberFlag",
                        "12": "OdometerFlag",
                        "13": "DriverIDNumberFlag, VehicleIDNumberFlag",
                        "14": "DriverIDNumberFlag",
                        "15": "VehicleIDNumberFlag",
                        "16": "DriverIDNumberFlag, JobNumberFlag",
                        "17": "VehicleIDNumberFlag, JobNumberFlag",
                        "18": "OdometerFlag, VehicleIDNumberFlag, DriverIDNumberFlag",
                        "19": "OdometerFlag, DriverIDNumberFlag, JobNumberFlag",
                        "20": "OdometerFlag, VehicleIDNumberFlag, JobNumberFlag",
                        "21": "OdometerFlag, UserIDFlag, JobNumberFlag",
                        "22": "OdometerFlag, DriverIDNumberFlag, CustomerDataFlag",
                        "23": "OdometerFlag, VehicleIDNumberFlag, CustomerDataFlag",
                        "24": "CustomerDataFlag, DriverIDNumberFlag, JobNumberFlag",
                        "25": "CustomerDataFlag, VehicleIDNumberFlag, JobNumberFlag",
                        "26": "UserIDFlag",
                        "27": "OdometerFlag, UserIDFlag",
                        "28": "OdometerFlag, DriverIDNumberFlag, UserIDFlag",
                        "29": "OdometerFlag, VehicleIDNumberFlag, UserIDFlag",
                        "30": "OdometerFlag, UserIDFlag, CustomerDataFlag",
                        "31": "OdometerFlag, CustomerDataFlag, UserIDFlag",
                        "32": "UserIDFlag, JobNumberFlag",
                        "33": "VehicleIDNumberFlag, UserIDFlag",
                        "34": "DriverIDNumberFlag, UserIDFlag",
                        "35": "DriverIDNumberFlag, DeptNumberFlag",
                        "36": "UserIDFlag, DeptNumberFlag",
                        "37": "VehicleIDNumberFlag, DeptNumberFlag",
                        "38": "OdometerFlag, DriverIDNumberFlag, DeptNumberFlag",
                        "39": "OdometerFlag, UserIDFlag, DeptNumberFlag",
                        "40": "OdometerFlag, VehicleIDNumberFlag, DeptNumberFlag",
                        "41": "DeptNumberFlag",
                        "42": "CustomerDataFlag, UserIDFlag, DeptNumberFlag",
                        "43": "CustomerDataFlag, VehicleIDNumberFlag, DeptNumberFlag",
                        "44": "CustomerDataFlag, DriverIDNumberFlag, DeptNumberFlag",
                        "45": "CustomerDataFlag, DriverIDNumberFlag, UserIDFlag",
                        "46": "CustomerDataFlag, UserIDFlag, LicenseNumberFlag",
                        "47": "CustomerDataFlag, VehicleIDNumberFlag, LicenseNumberFlag",
                        "48": "CustomerDataFlag",
                        "49": "DriverIDNumberFlag, CustomerDataFlag",
                        "50": "UserIDFlag, CustomerDataFlag",
                        "51": "VehicleIDNumberFlag, CustomerDataFlag",
                        "52": "Reserved for future use"}
        if prompt in prompt_value:
            return prompt_value[prompt]
        else:
            return "Prompts not found in list"

    @staticmethod
    def fof_prompt_values():
        prompt_values = {"0": "OdometerFlag, VehicleNumberFlag"}
        prompt = prompt_values["0"]
        return prompt

    @staticmethod
    def fwf_prompt_values():
        prompt_values = {"0": "OdometerFlag, DriverIDNumberFlag"}
        prompt = prompt_values["0"]
        return prompt

    @staticmethod
    def fmf_prompt_values():
        prompt_values = {"0": "OdometerFlag, DriverIDNumberFlag"}
        prompt = prompt_values["0"]
        return prompt


class fleet_data_appender:

    @staticmethod
    def Prompt_finder_by_value(prompts, cardtype, cardnumber):
        prompts = prompts.split(", ")
        value = "123456"
        if cardtype.upper() == "VGF":
            if cardnumber.endswith('4745'):
                value = "1054"
            if cardnumber.endswith("4711"):
                value = "008621"
            if cardnumber.endswith("4729"):
                value = "430598"
            if cardnumber.endswith("4737"):
                value = "095908"
            if cardnumber.endswith("4778"):
                value = "481901"
            if cardnumber.endswith("4786"):
                value = "177330"
            if cardnumber.endswith("2731"):
                value = "1041"
            if cardnumber.endswith("2749"):
                value = "759548"
            if cardnumber.endswith("2764"):
                value = "1040"
        fleet_prompts_data = {}
        prompt_text = ""
        if prompts is not None:
            for i in prompts:
                if i.upper() == "NO PROMPTS" or i.upper() == "PROMPTS NOT FOUND IN LIST":
                    fleet_prompts_data.update({"FleetPromptCount" : str("0")})
                    return fleet_prompts_data
                prompts = i[:-4]
                if prompts == "Odometer":
                    prompt_text = "000000"
                elif prompts == "FleetID":
                    prompt_text = value
                elif prompts == "DriverIDNumber":
                    prompt_text = value
                elif prompts == "VehicleIDNumber":
                    prompt_text = "123456"
                elif prompts == "EmployeeIDNumber":
                    prompt_text = "123456"
                elif prompts == "DeptNumber":
                    prompt_text = "789000"
                elif prompts == "LicenseNumber":
                    prompt_text = "100000"     
                elif prompts == "CustomerData":
                    prompt_text = "111111"   
                elif prompts == "UserID":
                    prompt_text = value
                elif prompts == "JobNumber":
                    prompt_text = "456456"
                else:
                    prompt_text = ""
                fleet_prompts_data.update({prompts: prompt_text})
            fleet_prompts_data = {k: v for k, v in fleet_prompts_data.items() if v}
            count = len(fleet_prompts_data)
            fleet_prompts_data.update({"FleetPromptCount": str(count)})
            return fleet_prompts_data
        else:
            return fleet_prompts_data.update({"FleetPromptCount": str("0")})