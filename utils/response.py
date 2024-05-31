from rest_framework import status

from rest_framework.response import Response



def HTTP_200(data):
    if not isinstance(data,dict):
        data={"messsage":data}

    return Response(data=data,status=status.HTTP_200_OK)


def HTTP_201(data):
    if not isinstance(data,dict):
        data={"messsage":data}

    return Response(data=data,status=status.HTTP_201_CREATED)

def HTTP_400(data):
    if not isinstance(data,dict):
        data={"messsage":data}

    return Response(data=data,status=status.HTTP_400_BAD_REQUEST)


def HTTP_404(data):
    if not isinstance(data,dict):
        data={"messsage":data}

    return Response(data=data,status=status.HTTP_404_NOT_FOUND)



