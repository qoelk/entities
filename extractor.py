from yargy import Parser

from rules.datetime import GENERAL_DATETIME, DATETIME
from rules.general import GENERAL
from rules.localised import LOCALISED
from rules.location import ANATOMY_UNIT
from misc_types.node import Node


class DocumentGraphExtractor:
    """Extracts graph from document"""

    def __init__(self, doc):
        self.time_intervals = None
        self.doc = doc

    def split_to_time_intervals(self):
        """Splits document to intervals by time"""
        parser = Parser(DATETIME)
        matches = list(parser.findall(self.doc))
        return self.matches_to_intervals(matches, 'time')

    def matches_to_intervals(self, matches, node_type):
        """Converts matches to intervals"""
        if len(matches) == 0:
            return []
        if len(matches) == 1:
            return [(self.doc, Node(node_type, matches[0]))]
        else:
            result = []
            for (i, m) in enumerate(matches):
                if i == len(matches) - 1:
                    start = m.span.stop
                    end = len(self.doc)
                else:
                    start = m.span.stop
                    end = matches[i + 1].span.start
                result.append((self.doc[start:end], Node(node_type, m)))
            #     if i == 0:
            #         start = 0
            #     else:
            #         start = matches[i - 1].span.stop
            #     end = m.span.start
            #     result.append((self.doc[start:end], Node(node_type, m)))
            return result

    def extract_from_time_interval(self, interval):
        """Extracts graph from time interval"""
        text, time_node = interval
        nodes = []
        edges = []
        nodes.append(time_node)
        location_parser = Parser(ANATOMY_UNIT)
        locations_matches = list(location_parser.findall(text))
        locations_intervals = self.matches_to_intervals(locations_matches, 'location')

        for location_interval in locations_intervals:
            location_nodes, location_edges = self.extract_from_location_interval(location_interval)
            nodes.extend(location_nodes)
            edges.extend(location_edges)
            edges.append((time_node, location_nodes[0]))
        return nodes, edges

    def extract_from_location_interval(self, interval):
        """Extracts graph from location interval"""
        text, node = interval
        nodes = [node]
        edges = []
        localised_parser = Parser(LOCALISED)
        localised_matches = list(localised_parser.findall(text))
        for m in localised_matches:
            l_node = Node('localised', m)
            nodes.append(l_node)
            edges.append((node, l_node))
        general_parser = Parser(GENERAL)
        general_matches = list(general_parser.findall(text))
        nodes.extend([Node('general', m) for m in general_matches])
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

    def extract_default_time(self):
        """Extracts default time from document"""
        parser = Parser(GENERAL_DATETIME)
        return list(parser.findall(self.doc))[0]
