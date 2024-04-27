from extractor import DocumentGraphExtractor


def save_result(name: str):
    pass


def extract_data(name: str):
    doc = ''
    with open(f'data/{name}', 'r') as f:
        doc = f.read()
    extractor = DocumentGraphExtractor(doc)
    nodes, edges = extractor.extract_from_text()
    return doc, (nodes, edges,)


def build_document(name, doc, graph):
    text = f"""
    <html>
    <head>
    <title>Document Graph</title>
    <meta charset="UTF-8">
</head>
<body>
    <h1>Document Graph {name}</h1>
    <p>{doc}</p>
    <img src="{graph}" alt="Document Graph">
</body>
</html>
    """
    return text


def save_text(name, text):
    with open(name, 'w') as f:
        f.write(text)
