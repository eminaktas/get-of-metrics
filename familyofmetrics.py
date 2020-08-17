from re import finditer
from prometheus_client.core import GaugeMetricFamily, Summary
import getmetrics
import time

RX_PACKETS = 'rx_packets'
TX_PACKETS = 'tx_packets'
RX_BYTES = 'rx_bytes'
TX_BYTES = 'tx_bytes'
RX_ERRORS = 'rx_errors'
TX_ERRORS = 'tx_errors'
RX_DROPS = 'rx_drops'
TX_DROPS = 'tx_drops'
RX_FRAME_ERR = 'rx_frame_err'
RX_OVER_ERR = 'rx_over_err'
RX_CRC_ERR = 'rx_crc_err'
COLLISIONS = 'collisions'
DEFINITION = 'Custom metrics'
LABEL_NODE_NAME = 'node_name'
LABEL_DEVICE = 'device'


# Regex (Regular Expression) allows us to find and group the parts of the content that meet certain rules.
# The finditer in the re library scans left-to-right, and matches are returned in the order found
# As a result, key and value are obtained with match.group(1) and match.group(2).
# Also, finditer saves time and memory. To see how the regex expression reacts to the .prom file content
# check the link : regex101.com/r/biJY82/3
# This regex expression finds "key = value" strings and groups them.
# "[]" matches a single character present in the set such [\w. ].
# "\w" matches any word character (equal to [a-zA-Z0-9_]).
# "+" matches between one and unlimited times, as many times as possible, giving back as needed (greedy).
# "\s" matches any whitespace character (equal to [\r\n\t\f\v ]).
# (?=word|word|..) matches the words in the set.

# each class for a metrics and with these classes we override the collect function
# in REGISTRY from prometheus_client.core for our custom metrics


class TxPacket(object):
    def __init__(self, alias_name):
        self.alias_name = alias_name

    def collect(self):
        regex = r"\s(?=tx_packets|index)(\w+)\s=\s([\w.]+)"
        matches = finditer(regex, getmetrics.data)
        port = 'port'
        metric = GaugeMetricFamily('tx_packets', 'Custom metrics', labels=['node_name', 'device'])
        for match in matches:
            key = match.group(1)
            value = match.group(2)
            # if true, it will update the index value
            if key == 'index':
                port = 'port%s' % value
            # otherwise, it writes the metrics in the .prom file
            elif key == 'tx_packets':
                metric.add_metric([self.alias_name, port], value)
        yield metric


class RxBytes(object):
    def __init__(self, alias_name):
        self.alias_name = alias_name

    def collect(self):
        regex = r"\s(?=rx_bytes|index)(\w+)\s=\s([\w.]+)"
        matches = finditer(regex, getmetrics.data)
        port = 'port'
        metric = GaugeMetricFamily('rx_bytes', 'Custom metrics', labels=['node_name', 'device'])
        for match in matches:
            key = match.group(1)
            value = match.group(2)
            # if true, it will update the index value
            if key == 'index':
                port = 'port%s' % value
            # otherwise, it writes the metrics in the .prom file
            elif key == 'rx_bytes':
                metric.add_metric([self.alias_name, port], value)
        yield metric


class RxPacket(object):
    def __init__(self, alias_name):
        self.alias_name = alias_name

    def collect(self):
        regex = r"\s(?=rx_packets|index)(\w+)\s=\s([\w.]+)"
        matches = finditer(regex, getmetrics.data)
        port = 'port'
        metric = GaugeMetricFamily('rx_packets', 'Custom metrics', labels=['node_name', 'device'])
        for match in matches:
            key = match.group(1)
            value = match.group(2)
            # if true, it will update the index value
            if key == 'index':
                port = 'port%s' % value
            # otherwise, it writes the metrics in the .prom file
            elif key == 'rx_packets':
                metric.add_metric([self.alias_name, port], value)
        yield metric


class TxBytes(object):
    def __init__(self, alias_name):
        self.alias_name = alias_name

    def collect(self):
        regex = r"\s(?=tx_bytes|index)(\w+)\s=\s([\w.]+)"
        matches = finditer(regex, getmetrics.data)
        port = 'port'
        metric = GaugeMetricFamily('tx_bytes', 'Custom metrics', labels=['node_name', 'device'])
        for match in matches:
            key = match.group(1)
            value = match.group(2)
            # if true, it will update the index value
            if key == 'index':
                port = 'port%s' % value
            # otherwise, it writes the metrics in the .prom file
            elif key == 'tx_bytes':
                metric.add_metric([self.alias_name, port], value)
        yield metric


class RxErrors(object):
    def __init__(self, alias_name):
        self.alias_name = alias_name

    def collect(self):
        regex = r"\s(?=rx_errors|index)(\w+)\s=\s([\w.]+)"
        matches = finditer(regex, getmetrics.data)
        port = 'port'
        metric = GaugeMetricFamily('rx_errors', 'Custom metrics', labels=['node_name', 'device'])
        for match in matches:
            key = match.group(1)
            value = match.group(2)
            # if true, it will update the index value
            if key == 'index':
                port = 'port%s' % value
            # otherwise, it writes the metrics in the .prom file
            elif key == 'rx_errors':
                metric.add_metric([self.alias_name, port], value)
        yield metric


class TxErrors(object):
    def __init__(self, alias_name):
        self.alias_name = alias_name

    def collect(self):
        regex = r"\s(?=tx_errors|index)(\w+)\s=\s([\w.]+)"
        matches = finditer(regex, getmetrics.data)
        port = 'port'
        metric = GaugeMetricFamily('tx_errors', 'Custom metrics', labels=['node_name', 'device'])
        for match in matches:
            key = match.group(1)
            value = match.group(2)
            # if true, it will update the index value
            if key == 'index':
                port = 'port%s' % value
            # otherwise, it writes the metrics in the .prom file
            elif key == 'tx_errors':
                metric.add_metric([self.alias_name, port], value)
        yield metric


class RxDrops(object):
    def __init__(self, alias_name):
        self.alias_name = alias_name

    def collect(self):
        regex = r"\s(?=rx_drops|index)(\w+)\s=\s([\w.]+)"
        matches = finditer(regex, getmetrics.data)
        port = 'port'
        metric = GaugeMetricFamily('rx_drops', 'Custom metrics', labels=['node_name', 'device'])
        for match in matches:
            key = match.group(1)
            value = match.group(2)
            # if true, it will update the index value
            if key == 'index':
                port = 'port%s' % value
            # otherwise, it writes the metrics in the .prom file
            elif key == 'rx_drops':
                metric.add_metric([self.alias_name, port], value)
        yield metric


class TxDrops(object):
    def __init__(self, alias_name):
        self.alias_name = alias_name

    def collect(self):
        regex = r"\s(?=tx_drops|index)(\w+)\s=\s([\w.]+)"
        matches = finditer(regex, getmetrics.data)
        port = 'port'
        metric = GaugeMetricFamily('tx_drops', 'Custom metrics', labels=['node_name', 'device'])
        for match in matches:
            key = match.group(1)
            value = match.group(2)
            # if true, it will update the index value
            if key == 'index':
                port = 'port%s' % value
            # otherwise, it writes the metrics in the .prom file
            elif key == 'tx_drops':
                metric.add_metric([self.alias_name, port], value)
        yield metric


class RxFrameErrors(object):
    def __init__(self, alias_name):
        self.alias_name = alias_name

    def collect(self):
        regex = r"\s(?=rx_frame_err|index)(\w+)\s=\s([\w.]+)"
        matches = finditer(regex, getmetrics.data)
        port = 'port'
        metric = GaugeMetricFamily('rx_frame_err', 'Custom metrics', labels=['node_name', 'device'])
        for match in matches:
            key = match.group(1)
            value = match.group(2)
            # if true, it will update the index value
            if key == 'index':
                port = 'port%s' % value
            # otherwise, it writes the metrics in the .prom file
            elif key == 'rx_frame_err':
                metric.add_metric([self.alias_name, port], value)
        yield metric


class RxOverErrors(object):
    def __init__(self, alias_name):
        self.alias_name = alias_name

    def collect(self):
        regex = r"\s(?=rx_over_err|index)(\w+)\s=\s([\w.]+)"
        matches = finditer(regex, getmetrics.data)
        port = 'port'
        metric = GaugeMetricFamily('rx_over_err', 'Custom metrics', labels=['node_name', 'device'])
        for match in matches:
            key = match.group(1)
            value = match.group(2)
            # if true, it will update the index value
            if key == 'index':
                port = 'port%s' % value
            # otherwise, it writes the metrics in the .prom file
            elif key == 'rx_over_err':
                metric.add_metric([self.alias_name, port], value)
        yield metric


class RxCrcErrors(object):
    def __init__(self, alias_name):
        self.alias_name = alias_name

    def collect(self):
        regex = r"\s(?=rx_crc_err|index)(\w+)\s=\s([\w.]+)"
        matches = finditer(regex, getmetrics.data)
        port = 'port'
        metric = GaugeMetricFamily('rx_crc_err', 'Custom metrics', labels=['node_name', 'device'])
        for match in matches:
            key = match.group(1)
            value = match.group(2)
            # if true, it will update the index value
            if key == 'index':
                port = 'port%s' % value
            # otherwise, it writes the metrics in the .prom file
            elif key == 'rx_crc_err':
                metric.add_metric([self.alias_name, port], value)
        yield metric


class Collisions(object):
    def __init__(self, alias_name):
        self.alias_name = alias_name

    def collect(self):
        regex = r"\s(?=collisions|index)(\w+)\s=\s([\w.]+)"
        matches = finditer(regex, getmetrics.data)
        port = 'port'
        metric = GaugeMetricFamily('collisions', 'Custom metrics', labels=['node_name', 'device'])
        for match in matches:
            key = match.group(1)
            value = match.group(2)
            # if true, it will update the index value
            if key == 'index':
                port = 'port%s' % value
            # otherwise, it writes the metrics in the .prom file
            elif key == 'collisions':
                metric.add_metric([self.alias_name, port], value)
        yield metric
