from app.connectors.connector_factory import ConnectorFactory

connector = ConnectorFactory.create("pdf", "data/Formula_One.pdf")
chunks = connector.load()
print(len(chunks), type(connector).__name__)

connector2 = ConnectorFactory.create("text", "data/cats.txt")
chunks2 = connector2.load()
print(len(chunks2), type(connector2).__name__)

# and confirm the error path works too:
ConnectorFactory.create("excel", "data/whatever.xlsx")