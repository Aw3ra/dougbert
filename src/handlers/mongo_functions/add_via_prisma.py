
from prisma import Client

prisma = Client()

async def add_via_prisma(collection, data):
    # Convert collection as a string to an object 
    await prisma.connect()
    try:
        prisma_collection = getattr(prisma, collection)
        record = await prisma_collection.create(data=data)
        await prisma.disconnect()
        return record
    except Exception as e:
        await prisma.disconnect()
        return e
