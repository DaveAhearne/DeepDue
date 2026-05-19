import os
import asyncio
from deepdue.data.companies_house import CompaniesHouseClient
from dotenv import load_dotenv

async def main():
    load_dotenv()

    api_key = os.environ["CH_API_KEY"]
    client = CompaniesHouseClient(api_key)

    company = await client.SearchOfficers("Isa Lee Wolf")
    
    print(company)

def run():
    asyncio.run(main())