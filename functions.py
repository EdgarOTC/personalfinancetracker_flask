def get_element(values, id):
    return filter(lambda x: x.id == id, values)
# def Trans_To_Dict(colletion):
#     res = {}
#     for obj in colletion:        
#         res[obj.id] = {"description":obj.description,"date": obj.date,"amount":obj.amount}
#         # for key, value in obj:
#         #     res.append(value)
#     return res
def TransData_Dict(colletion):
    res = {}
    descriptions = []
    dates = []
    amounts = []
    for obj in colletion:        
        descriptions.append(obj.description)
        dates.append(obj.date)
        amounts.append(obj.amount)
    res["description"]=descriptions
    res["date"]=dates
    res["amount"]=amounts
    return res