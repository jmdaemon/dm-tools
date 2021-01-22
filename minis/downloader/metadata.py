import queue

class Metadata():
    def __init__(self, links, names, ids):
        self.links = queue.Queue()
        self.names = queue.Queue()
        self.ids   = queue.Queue()

        self.populate(links, names, ids)
        self.printQueue("Links", "Miniature Link", self.links)
        self.printQueue("Names", "Miniature Name", self.names)
        self.printQueue("Ids", "Product ID", self.ids)

    def populate(self, links, names, ids):
        list = [self.links.put(link) for link in links]
        list = [self.names.put(name) for name in names]
        list = [self.ids.put(mini_id) for mini_id in ids]

    def printQueue(self, title, keyword, itemQueue):
        print(f"============ {title} ============")
        list = [print(f"{keyword}: {item}") for item in itemQueue.queue] + [print(f"")]

    def returnQueue(MetadataQueue):
        result: queue.Query()
        result = MetadataQueue
        return result

    def getLinks():
        returnQueue(self.links)

    def getNames():
        returnQueue(self.names)

    def getIds():
        returnQueue(self.ids)

