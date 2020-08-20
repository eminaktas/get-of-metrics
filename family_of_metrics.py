from re import finditer
from prometheus_client.core import GaugeMetricFamily
import collector_of_metrics

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


DESCRIPTION = 'Custom metrics'
DEVICE = 'device'


class RxPacket(object):
    def __init__(self, alias_name):
        self.alias_name = alias_name
        self.name = 'rx_packets_' + alias_name.lower()

    def collect(self):
        regex = r"\s(?=rx_packets|index)(\w+)\s=\s([\w.]+)"
        matches = finditer(regex, collector_of_metrics.data)
        port = 'port'
        metric = GaugeMetricFamily(self.name, DESCRIPTION, labels=[DEVICE])
        for match in matches:
            key = match.group(1)
            value = match.group(2)
            # if true, it will update the index value
            if key == 'index':
                port = 'port%s' % value
            # otherwise, it writes the metrics in the .prom file
            elif key == 'rx_packets':
                metric.add_metric([port], value)
        yield metric


class TxPacket(object):
    def __init__(self, alias_name):
        self.alias_name = alias_name
        self.name = 'tx_packets_' + alias_name.lower()

    def collect(self):
        regex = r"\s(?=tx_packets|index)(\w+)\s=\s([\w.]+)"
        matches = finditer(regex, collector_of_metrics.data)
        port = 'port'
        metric = GaugeMetricFamily(self.name, DESCRIPTION, labels=[DEVICE])
        for match in matches:
            key = match.group(1)
            value = match.group(2)
            # if true, it will update the index value
            if key == 'index':
                port = 'port%s' % value
            # otherwise, it writes the metrics in the .prom file
            elif key == 'tx_packets':
                metric.add_metric([port], value)
        yield metric


class RxBytes(object):
    def __init__(self, alias_name):
        self.alias_name = alias_name
        self.name = 'rx_bytes_' + alias_name.lower()

    def collect(self):
        regex = r"\s(?=rx_bytes|index)(\w+)\s=\s([\w.]+)"
        matches = finditer(regex, collector_of_metrics.data)
        port = 'port'
        metric = GaugeMetricFamily(self.name, DESCRIPTION, labels=[DEVICE])
        for match in matches:
            key = match.group(1)
            value = match.group(2)
            # if true, it will update the index value
            if key == 'index':
                port = 'port%s' % value
            # otherwise, it writes the metrics in the .prom file
            elif key == 'rx_bytes':
                metric.add_metric([port], value)
        yield metric


class TxBytes(object):
    def __init__(self, alias_name):
        self.alias_name = alias_name
        self.name = 'tx_bytes_' + alias_name.lower()

    def collect(self):
        regex = r"\s(?=tx_bytes|index)(\w+)\s=\s([\w.]+)"
        matches = finditer(regex, collector_of_metrics.data)
        port = 'port'
        metric = GaugeMetricFamily(self.name, DESCRIPTION, labels=[DEVICE])
        for match in matches:
            key = match.group(1)
            value = match.group(2)
            # if true, it will update the index value
            if key == 'index':
                port = 'port%s' % value
            # otherwise, it writes the metrics in the .prom file
            elif key == 'tx_bytes':
                metric.add_metric([port], value)
        yield metric


class RxErrors(object):
    def __init__(self, alias_name):
        self.alias_name = alias_name
        self.name = 'rx_errors_' + alias_name.lower()

    def collect(self):
        regex = r"\s(?=rx_errors|index)(\w+)\s=\s([\w.]+)"
        matches = finditer(regex, collector_of_metrics.data)
        port = 'port'
        metric = GaugeMetricFamily(self.name, DESCRIPTION, labels=[DEVICE])
        for match in matches:
            key = match.group(1)
            value = match.group(2)
            # if true, it will update the index value
            if key == 'index':
                port = 'port%s' % value
            # otherwise, it writes the metrics in the .prom file
            elif key == 'rx_errors':
                metric.add_metric([port], value)
        yield metric


class TxErrors(object):
    def __init__(self, alias_name):
        self.alias_name = alias_name
        self.name = 'tx_errors_' + alias_name.lower()

    def collect(self):
        regex = r"\s(?=tx_errors|index)(\w+)\s=\s([\w.]+)"
        matches = finditer(regex, collector_of_metrics.data)
        port = 'port'
        metric = GaugeMetricFamily(self.name, DESCRIPTION, labels=[DEVICE])
        for match in matches:
            key = match.group(1)
            value = match.group(2)
            # if true, it will update the index value
            if key == 'index':
                port = 'port%s' % value
            # otherwise, it writes the metrics in the .prom file
            elif key == 'tx_errors':
                metric.add_metric([port], value)
        yield metric


class RxDrops(object):
    def __init__(self, alias_name):
        self.alias_name = alias_name
        self.name = 'rx_drops_' + alias_name.lower()

    def collect(self):
        regex = r"\s(?=rx_drops|index)(\w+)\s=\s([\w.]+)"
        matches = finditer(regex, collector_of_metrics.data)
        port = 'port'
        metric = GaugeMetricFamily(self.name, DESCRIPTION, labels=[DEVICE])
        for match in matches:
            key = match.group(1)
            value = match.group(2)
            # if true, it will update the index value
            if key == 'index':
                port = 'port%s' % value
            # otherwise, it writes the metrics in the .prom file
            elif key == 'rx_drops':
                metric.add_metric([port], value)
        yield metric


class TxDrops(object):
    def __init__(self, alias_name):
        self.alias_name = alias_name
        self.name = 'tx_drops_' + alias_name.lower()

    def collect(self):
        regex = r"\s(?=tx_drops|index)(\w+)\s=\s([\w.]+)"
        matches = finditer(regex, collector_of_metrics.data)
        port = 'port'
        metric = GaugeMetricFamily(self.name, DESCRIPTION, labels=[DEVICE])
        for match in matches:
            key = match.group(1)
            value = match.group(2)
            # if true, it will update the index value
            if key == 'index':
                port = 'port%s' % value
            # otherwise, it writes the metrics in the .prom file
            elif key == 'tx_drops':
                metric.add_metric([port], value)
        yield metric


class RxFrameErrors(object):
    def __init__(self, alias_name):
        self.alias_name = alias_name
        self.name = 'rx_frame_err_' + alias_name.lower()

    def collect(self):
        regex = r"\s(?=rx_frame_err|index)(\w+)\s=\s([\w.]+)"
        matches = finditer(regex, collector_of_metrics.data)
        port = 'port'
        metric = GaugeMetricFamily(self.name, DESCRIPTION, labels=[DEVICE])
        for match in matches:
            key = match.group(1)
            value = match.group(2)
            # if true, it will update the index value
            if key == 'index':
                port = 'port%s' % value
            # otherwise, it writes the metrics in the .prom file
            elif key == 'rx_frame_err':
                metric.add_metric([port], value)
        yield metric


class RxOverErrors(object):
    def __init__(self, alias_name):
        self.alias_name = alias_name
        self.name = 'rx_over_err_' + alias_name.lower()

    def collect(self):
        regex = r"\s(?=rx_over_err|index)(\w+)\s=\s([\w.]+)"
        matches = finditer(regex, collector_of_metrics.data)
        port = 'port'
        metric = GaugeMetricFamily(self.name, DESCRIPTION, labels=[DEVICE])
        for match in matches:
            key = match.group(1)
            value = match.group(2)
            # if true, it will update the index value
            if key == 'index':
                port = 'port%s' % value
            # otherwise, it writes the metrics in the .prom file
            elif key == 'rx_over_err':
                metric.add_metric([port], value)
        yield metric


class RxCrcErrors(object):
    def __init__(self, alias_name):
        self.alias_name = alias_name
        self.name = 'rx_crc_err_' + alias_name.lower()

    def collect(self):
        regex = r"\s(?=rx_crc_err|index)(\w+)\s=\s([\w.]+)"
        matches = finditer(regex, collector_of_metrics.data)
        port = 'port'
        metric = GaugeMetricFamily(self.name, DESCRIPTION, labels=[DEVICE])
        for match in matches:
            key = match.group(1)
            value = match.group(2)
            # if true, it will update the index value
            if key == 'index':
                port = 'port%s' % value
            # otherwise, it writes the metrics in the .prom file
            elif key == 'rx_crc_err':
                metric.add_metric([port], value)
        yield metric


class Collisions(object):
    def __init__(self, alias_name):
        self.alias_name = alias_name
        self.name = 'collisions_' + alias_name.lower()

    def collect(self):
        regex = r"\s(?=collisions|index)(\w+)\s=\s([\w.]+)"
        matches = finditer(regex, collector_of_metrics.data)
        port = 'port'
        metric = GaugeMetricFamily(self.name, DESCRIPTION, labels=[DEVICE])
        for match in matches:
            key = match.group(1)
            value = match.group(2)
            # if true, it will update the index value
            if key == 'index':
                port = 'port%s' % value
            # otherwise, it writes the metrics in the .prom file
            elif key == 'collisions':
                metric.add_metric([port], value)
        yield metric
