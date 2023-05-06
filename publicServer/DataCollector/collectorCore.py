from publicServer.DataCollector.Commands.APIInvoker import APIInvoker
from publicServer.DataCollector.Commands.CommandList.GetCompanyProfile import GetCompanyProfile
from publicServer.DataCollector.Commands.CommandList.GetLatestNews import GetLatestNews
from publicServer.DataCollector.Commands.CommandList.GetSNPList import GetSNPList


def runCollector():
    api_invoker = APIInvoker()
    api_invoker.register(GetSNPList())
    api_invoker.register(GetCompanyProfile())
    api_invoker.register(GetLatestNews())
    api_invoker.execute()