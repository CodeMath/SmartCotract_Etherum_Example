from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib.auth import logout as auth_logout
from django.contrib.auth.models import User
from django.http import HttpResponse

from eth_testnet.configure import *
from .models import transaction

import requests
import json


def index(request):
    context = {}
    if request.user.is_active:
        context["auth_key"]="auth_key"

        try:
            is_user = User.objects.get(id=request.user.id)
            if is_user.last_name is "":
                gen_address = generate_key(is_user.id)
                is_user.last_name = gen_address
                is_user.save()
                context["address"] = is_user.last_name
                context["balance"] = getBlanceOf(context["address"],is_user.id)

            else:
                context["address"] = is_user.last_name
                context["balance"] = getBlanceOf(context["address"], is_user.id)

            context["history_txid"] = transaction.objects.filter(user=request.user)

        except Exception as e:
            print(str(e))

    return render(request,'index.html',context)

def getBlanceOf(address,id):
    headers = {"Content-Type": "application/json"}
    data = {
        "jsonrpc": "2.0",
        "method": "eth_getBalance",
        "params": [address,"latest"],
        "id": id
    }

    rpc_url = "http://localhost:8545"
    req = requests.post(rpc_url, headers=headers, data=json.dumps(data))
    res = req.json()

    ether = int(res["result"],16)
    pretty_ether = ether/(10**17)
    return pretty_ether

def generate_key(id):

    headers = {"Content-Type":"application/json"}
    data = {
        "jsonrpc":"2.0",
        "method":"personal_newAccount",
        "params":[PN_PASSWORD],
        "id":id
    }

    rpc_url = "http://localhost:8545"
    req = requests.post(rpc_url ,headers=headers, data=json.dumps(data))
    res = req.json()

    try:
        new_account = res["result"]

        # unlock and sending default test eth
        data ={
            "jsonrpc": "2.0",
            "method": "personal_unlockAccount",
            "params": ["",ADMIN_PASSWORD,60],
            "id": id
            }
        req = requests.post(rpc_url,headers=headers,data=json.dumps(data))
        res = req.json()

        # success
        if bool(res["result"]):
            data = {
                "jsonrpc": "2.0",
                "method": "eth_sendTransaction",
                "params": [{"from":ADMIN_ADDRESS,"to":new_account,"value":"0x6f05b59d3b20000"}], # 5 Ether
                "id": id
            }
            req = requests.post(rpc_url, headers=headers, data=json.dumps(data))
            res = req.json()

            if res["result"]:
                transcation = res["result"]


    except Exception as e:
        print(str(e))
        pass
    return new_account


def logout(request):
    auth_logout(request)
    return redirect('/')


def fundingCheck(request):
    if request.is_ajax():
        funding_address = PN_ADDRESS

        context = {
            "funding":getBlanceOf(funding_address,1)
        }

        return HttpResponse(json.dumps(context), content_type="application/json")



@login_required
def ethSending(request):
    if request.is_ajax():
        funding_address = PN_ADDRESS

        if float(request.POST.get("price")) < 0.5:
            return HttpResponse(json.dumps({"error": "more then 0.5 ether."}), content_type="application/json")

        wei = int(float(request.POST.get("price"))*(10**17))
        price = hex(wei)
        headers = {"Content-Type": "application/json"}
        data = {
            "jsonrpc": "2.0",
            "method": "personal_unlockAccount",
            "params": [request.user.last_name, PN_PASSWORD, 60],
            "id": request.user.id
        }

        rpc_url = "http://localhost:8545"
        req = requests.post(rpc_url, headers=headers, data=json.dumps(data))
        res = req.json()
        if bool(res["result"]):

            data = {
                "jsonrpc": "2.0",
                "method": "eth_sendTransaction",
                "params": [{"from":request.user.last_name,"to":funding_address,"value":price}],
                "id": request.user.id
            }
            rpc_url = "http://localhost:8545"
            req = requests.post(rpc_url, headers=headers, data=json.dumps(data))
            res = req.json()

            transaction.objects.create(user=request.user,txid=res["result"])
            context = {
                "txid":res["result"]
            }
            return HttpResponse(json.dumps(context), content_type="application/json")
        else:
            return HttpResponse(json.dumps({"error": "account error"}), content_type="application/json")

