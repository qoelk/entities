from yargy import Parser

from models.connections import Connection
from models.document import Document
from models.entity import Entity
from rules.datetime import DATETIME
from rules.general import GENERAL
from rules.localised import LOCALISED
from rules.location import ANATOMY_UNIT


class DocumentGraphExtractor:

    def __init__(self, doc: Document):
        self.time_intervals = None
        self.doc = doc
        self.text = doc.text

    def split_to_time_intervals(self):
        """Splits document to intervals by time"""
        parser = Parser(DATETIME)
        matches = list(parser.findall(self.text))
        return self.matches_to_intervals(matches, 'time')

    def matches_to_intervals(self, matches, node_type: str):
        """Converts matches to intervals"""
        if len(matches) == 0:
            return []
        if len(matches) == 1:
            node = Entity(entity_type=node_type, start=matches[0].span.start, end=matches[0].span.stop,
                          document=self.doc)
            node.set_data(matches[0])
            return [(self.text, node)]
        else:
            result = []
            for (i, m) in enumerate(matches):
                if i == len(matches) - 1:
                    start = m.span.stop
                    end = len(self.text)
                else:
                    start = m.span.stop
                    end = matches[i + 1].span.start
                node = Entity(entity_type=node_type, start=m.span.start, end=m.span.stop, document=self.doc)
                node.set_data(m)
                result.append((self.text[start:end], node))
            #     if i == 0:
            #         start = 0
            #     else:
            #         start = matches[i - 1].span.stop
            #     end = m.span.start
            #     result.append((self.doc[start:end], Node(node_type, m)))
            return result

    def extract_from_location_interval(self, interval, t_node):
        """Extracts graph from location interval"""
        text, node = interval
        nodes = [node]
        edges = []
        localised_parser = Parser(LOCALISED)
        localised_matches = list(localised_parser.findall(text))
        for m in localised_matches:
            l_node = Entity(entity_type='localised', start=m.span.start, end=m.span.stop, document=self.doc)
            l_node.set_data(m)
            nodes.append(l_node)
            connection = Connection(head=node, tail=l_node, document=self.doc)
            edges.append(connection)
        general_parser = Parser(GENERAL)
        general_matches = list(general_parser.findall(text))
        for m in general_matches:
            g_node = Entity(entity_type='general', start=m.span.start, end=m.span.stop, document=self.doc)
            g_node.set_data(m)
            nodes.append(g_node)
            connection = Connection(head=t_node, tail=g_node, document=self.doc)
            edges.append(connection)
        return nodes, edges

    def extract_from_time_interval(self, interval):
        text, time_node = interval
        nodes = []
        edges = []
        nodes.append(time_node)
        location_parser = Parser(ANATOMY_UNIT)
        locations_matches = list(location_parser.findall(text))
        locations_intervals = self.matches_to_intervals(locations_matches, 'location')

        for location_interval in locations_intervals:
            location_nodes, location_edges = self.extract_from_location_interval(location_interval, time_node)
            nodes.extend(location_nodes)
            edges.extend(location_edges)
            connection = Connection(head=time_node, tail=location_nodes[0], document=self.doc)
            edges.append(connection)
        return nodes, edges

    def extract_from_text(self):
        """Extracts graph from text"""
        text_nodes = []
        text_edges = []
        time_intervals = self.split_to_time_intervals()
        self.time_intervals = time_intervals
        for interval in time_intervals:
            nodes, edges = self.extract_from_time_interval(interval)
            text_nodes.extend(nodes)
            text_edges.extend(edges)
        return text_nodes, text_edges