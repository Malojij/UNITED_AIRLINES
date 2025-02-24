import random
from decimal import Decimal


class Product_data_mapping:

    @staticmethod
    def ProductData_Mapping(Transaction_amount, cashbackAmount, Product_type, product_count):
        CB = None if cashbackAmount is not "0.00" else cashbackAmount
        productDict, productList = {}, []
        ProductTotalAmt = Decimal(0.00)
        unitprice = (Decimal(Transaction_amount) / Decimal(product_count)).quantize(Decimal('1.000'))
        if Product_type == "EPPProductData":
            products = [{"ItemCode": "00032390003808", "ItemReferenceNumber": "0001", "Quantity": "001","RedemptionReqAmount": "7.99", "TaxAmount": "0.00", "UnitPrice" : "1.000"},
                        {"ItemCode": "00003800000120", "ItemReferenceNumber": "0002", "Quantity": "001", "RedemptionReqAmount": "0.12", "TaxAmount": "0.00", "UnitPrice" : "1.000"}]
        else:
            products = [{"ProductCode": "040", "ProductName": "Other", "UnitOfMeasure": "U", "UnitPrice": "1.000"},
                        {"ProductCode": "001", "ProductName": "erosene", "UnitOfMeasure": "G", "UnitPrice": "1.000"},
                        {"ProductCode": "042", "ProductName": "Bread", "UnitOfMeasure": "U", "UnitPrice": "1.000"},
                        {"ProductCode": "002", "ProductName": "Diesel", "UnitOfMeasure": "G", "UnitPrice": "1.000"},
                        {"ProductCode": "004", "ProductName": "Super Unleaded", "UnitOfMeasure": "G", "UnitPrice": "1.000"},
                        {"ProductCode": "034", "ProductName": "Car Wash", "UnitOfMeasure": "U", "UnitPrice": "1.000"},
                        {"ProductCode": "001", "ProductName": "Gasoline", "UnitOfMeasure": "G", "UnitPrice": "1.000"},
                        {"ProductCode": "150", "ProductName": "General Alcohol", "UnitOfMeasure": "U", "UnitPrice": "1.000"},
                        {"ProductCode": "099", "ProductName": "Miscellaneous", "UnitOfMeasure": "U", "UnitPrice": "1.000"},
                        {"ProductCode": "021", "ProductName": "Motor Oil", "UnitOfMeasure": "O", "UnitPrice": "1.000"},
                        {"ProductCode": "150", "ProductName": "General Alcohol", "UnitOfMeasure": "U", "UnitPrice": "1.000"},
                        {"ProductCode": "011", "ProductName": "CNG", "UnitOfMeasure": "G", "UnitPrice": "1.000"},
                        {"ProductCode": "006", "ProductName": "Unleaded Plus", "UnitOfMeasure": "G", "UnitPrice": "1.000"},
                        {"ProductCode": "024", "ProductName": "Battery", "UnitOfMeasure": "U", "UnitPrice": "1.000"},
                        {"ProductCode": "001", "ProductName": "Unleaded", "UnitOfMeasure": "G", "UnitPrice": "1.000"},
                        {"ProductCode": "042", "ProductName": "Bread", "UnitOfMeasure": "U", "UnitPrice": "1.000"},
                        {"ProductCode": "002", "ProductName": "Diesel", "UnitOfMeasure": "G", "UnitPrice": "1.000"},
                        {"ProductCode": "004", "ProductName": "Super Unleaded", "UnitOfMeasure": "G", "UnitPrice": "1.000"},
                        {"ProductCode": "034", "ProductName": "Car Wash", "UnitOfMeasure": "U", "UnitPrice": "1.000"},
                        {"ProductCode": "001", "ProductName": "Gasoline", "UnitOfMeasure": "G", "UnitPrice": "1.000"},
                        {"ProductCode": "150", "ProductName": "General Alcohol", "UnitOfMeasure": "U", "UnitPrice": "1.000"},
                        {"ProductCode": "099", "ProductName": "Miscellaneous", "UnitOfMeasure": "U", "UnitPrice": "1.000"},
                        {"ProductCode": "021", "ProductName": "Motor Oil", "UnitOfMeasure": "O", "UnitPrice": "1.000"},
                        {"ProductCode": "150", "ProductName": "General Alcohol", "UnitOfMeasure": "U", "UnitPrice": "1.000"},
                        {"ProductCode": "011", "ProductName": "CNG", "UnitOfMeasure": "G", "UnitPrice": "1.000"},
                        {"ProductCode": "006", "ProductName": "Unleaded Plus", "UnitOfMeasure": "G", "UnitPrice": "1.000"},
                        {"ProductCode": "024", "ProductName": "Battery", "UnitOfMeasure": "U", "UnitPrice": "1.000"},
                        ]
        if CB and Product_type == "l3productdata":
            productDict = {
                "L3ProductSeqNo" : str("1"),
                "L3ProductCode" : str(products[0]['ProductCode']),
                "L3ProductName" : str(products[0]['ProductName']),
                "L3UnitOfMeasure" : str(products[0]['UnitOfMeasure']),
                "L3ProductQuantity" : str("1.000"),
                "L3ProductUnitPrice" : format(Decimal(cashbackAmount+'0'), ".3f"),
                "L3ProductTotalAmount" : str(cashbackAmount)
            }
            productList.append(productDict)
        for i in range(int(product_count)):
            productID = i + 2 if CB else i + 1
            price = str(unitprice)
            Productunitprice = Decimal(Decimal(price).quantize(Decimal('1.000')))
            product_quantity = Decimal(Decimal(1.000).quantize(Decimal('0.000')))
            product_price = Decimal(Decimal(Productunitprice * product_quantity).quantize(Decimal('0.000')))
            product_price_in_dec = format(product_price, ".2f")
            if Product_type == "l3productdata":
                productDict = {"L3ProductSeqNo": str(productID),
                               "L3ProductCode": str(products[productID]['ProductCode']),
                               "L3ProductName": str(products[productID]['ProductName']),
                               "L3UnitOfMeasure": str(products[productID]['UnitOfMeasure']),
                               "L3ProductQuantity": str(product_quantity),
                               "L3ProductUnitPrice": str(Productunitprice),
                               "L3ProductTotalAmount": str(product_price_in_dec)
                               }
            if Product_type == "fleetproductdata":
                productDict = {"FleetProductSeqNo": str(productID), "FleetNACSCode": str(products[productID]['ProductCode']),
                               "FleetProductName": str(products[productID]['ProductName']),
                               "FleetUnitOfMeasure": str(products[productID]['UnitOfMeasure']),
                               "FleetProductDataType": "102",
                               "FleetServiceLevel": "S",
                               "FleetProductQuantity": str(product_quantity),
                               "FleetProductUnitPrice": str(Productunitprice),
                               "FleetProductTotalAmount": str(product_price_in_dec)}
            if Product_type == "TicketProductData":
                productDict = {
                    "ProductID": str(productID),
                    "ProductName": str(products[productID]['ProductName']),
                    "ServiceLevel": "S",
                    "ProductCode": str(products[productID]['ProductCode']),
                    "UnitOfMeasure": str(products[productID]['UnitOfMeasure']),
                    "ProductUnitPrice": str(Productunitprice),
                    "Quantity":  str(product_quantity),
                    "Price": str(product_price_in_dec),
                }
            if Product_type == "EPPProductData":
                productDict = {"ItemCode": str(products[i]['ItemCode']), "ItemReferenceNumber": str(products[i]['ItemReferenceNumber']),
                               "Quantity": str(products[i]['Quantity']),
                               "RedemptionReqAmount": str(products[i]['RedemptionReqAmount']), "TaxAmount": str(products[i]['TaxAmount'])}
            ProductTotalAmt = round(ProductTotalAmt + product_price, 2)
            productList.append(productDict)
        ProductTotalAmt = str(ProductTotalAmt)
        return {"Product_count": str(len(productList)), "Product_list": productList, "ProductTotalAmt": ProductTotalAmt}

    @staticmethod
    def Ewic_Product_Mapping(products):
        data = {"PrescriptionData": products}
        return data