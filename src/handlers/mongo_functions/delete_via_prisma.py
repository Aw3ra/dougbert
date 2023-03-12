# Import the prisma client
from prisma import Client
# Create the prisma client
prisma = Client()


# ---------------------------------------------------------------------------------#
# Function to add to the database via prisma
# Inputs:  collection   - the collection to add to
#          query        - the query to delete from the collection, must be unique
# Outputs: record       - the record that was added to the database
#          e            - the error that was thrown, if any
# ---------------------------------------------------------------------------------#
async def delete_via_prisma(collection, query):
    # Connect to the database
    await prisma.connect()
    # Add the data to the collection
    try:
        # Get the collection
        prisma_collection = getattr(prisma, collection)
        # Add the data to the collection
        record = await prisma_collection.delete(where=query)
        # Disconnect from the database
        await prisma.disconnect()
        # Return the record
        return record
    # If there is an error, disconnect from the database and return the error
    except Exception as e:
        # Disconnect from the database
        await prisma.disconnect()
        # Return the error
        return e
# ---------------------------------------------------------------------------------#
