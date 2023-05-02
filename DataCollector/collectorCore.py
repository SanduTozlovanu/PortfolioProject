from DataCollector.Commands.APIInvoker import APIInvoker
from DataCollector.Commands.CommandList.GetCompanyProfile import GetCompanyProfile
from DataCollector.Commands.CommandList.GetLatestNews import GetLatestNews
from DataCollector.Commands.CommandList.GetSNPList import GetSNPList


def runCollector():
    api_invoker = APIInvoker()
    api_invoker.register(GetSNPList())
    api_invoker.register(GetCompanyProfile())
    api_invoker.register(GetLatestNews())
    api_invoker.execute()
