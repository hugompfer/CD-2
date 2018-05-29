import json

#encode information
def encode(cod,result,room):
    dic={
        'cod':cod,
        'room':room,
        'result':result
    }
    return json.dumps(dic)

#decode information
def decode(dic):
    auxiliar=[]
    first=True
    for i in dic.split('}'):
        if i != '':
            if not first:
                if(i[1]=='}'):
                    auxiliar.append(i[1:] + '}')
                else:
                    auxiliar.append(i + '}')
            else:
                auxiliar.append(i+'}')
            first=False

    list=[]
    for item in auxiliar:
        list.append(json.loads(item))
    return list

