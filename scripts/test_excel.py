from app.connectors.excel_connector import ExcelConnector

c = ExcelConnector("data/marks.xlsx")
chunks = c.load()
print(len(chunks))
print(chunks[0].text)
print(chunks[0].metadata)