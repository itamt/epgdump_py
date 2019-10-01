#!/usr/bin/python
# -*- coding: utf-8 -*-
import sys
import time
import argparse
from typing import List, Optional

from . import xmltv
from .parser_ import TransportStreamFile, parse_ts
from .constant import (
    TYPE_DEGITAL, TYPE_BS, TYPE_CS,
)


def create_argparser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description="""example:
    epgdump.py -c CHANNEL_ID -i INPUT_FILE -o OUTPUT_FILE
    epgdump.py -b -i INPUT_FILE -o OUTPUT_FILE
    epgdump.py -s -i INPUT_FILE -o OUTPUT_FILE
    epgdump.py [-b|-s] -p TRANSPORT_STREAM_ID:SERVICE_ID:EVENT_ID -i INPUT_FILE""",
                                     formatter_class=argparse.RawTextHelpFormatter)
    parser.print_usage = parser.print_help  # overwrite usage by full help
    group = parser.add_mutually_exclusive_group(required=False)
    group.add_argument('-b', '--bs', action='store_const', dest='b_type', const=TYPE_BS,
                       help='input file is BS channel')
    group.add_argument('-s', '--cs', action='store_const', dest='b_type', const=TYPE_CS,
                       help='input file is CS channel')
    parser.add_argument('-c', '--channel-id', type=str,
                        help='specify channel identifier')
    parser.add_argument('-d', '--debug', action='store_true',
                        help='parse all ts packet')
    parser.add_argument('-f', '--format', action='store_true',
                        help='format xml')
    parser.add_argument('-i', '--input', type=argparse.FileType('r'),
                        help='specify ts file', metavar='INPUT_FILE')
    parser.add_argument('-o', '--output', type=str,
                        help='specify xml file', metavar='OUTPUT_FILE')
    parser.add_argument('-p', '--print-time', type=str,
                        help='print start time, and end time of specified id',
                        metavar='TRANSPORT_STREAM_ID:SERVICE_ID:EVENT_ID')
    parser.add_argument('-e', '--event-id', action='store_true',
                        help='output transport_stream_id, servece_id and event_id')
    return parser


def process(argv: List[str]):
    argparser = create_argparser()
    args = argparser.parse_args(argv)

    channel_id: str = args.channel_id
    input_file: str = args.input.name if args.input else None
    output_file: str = args.output
    pretty_print: bool = args.format
    debug: bool = args.debug
    b_type: str = args.b_type or TYPE_DEGITAL
    transport_stream_id: Optional[int] = None
    service_id: Optional[int] = None
    event_id: Optional[int] = None
    output_eid: bool = args.event_id

    if args.print_time:
        # 検索用オプション
        arr = args.print_time.split(':')
        transport_stream_id = int(arr[0])
        service_id = int(arr[1])
        event_id = int(arr[2])

    if not args.print_time and \
            (b_type == TYPE_DEGITAL and channel_id is None) \
            or input_file is None \
            or output_file is None:
        argparser.print_help()
        sys.exit(1)
    elif input_file is None:
        argparser.print_help()
        sys.exit(1)

    tsfile = TransportStreamFile(input_file, 'rb')
    service, events = parse_ts(b_type, tsfile, debug)
    tsfile.close()
    if service_id is None:
        # xmp出力
        xmltv.create_xml(b_type, channel_id, service, events, output_file, pretty_print, output_eid)
    else:
        # 検索用オプション指定時の動作
        start_time = None
        end_time = None
        for event in events:
            if (event.transport_stream_id == transport_stream_id and
                    event.service_id == service_id and
                    event.event_id == event_id):
                start_time = event.start_time
                end_time = event.start_time + event.duration
                break
        if start_time is None:
            print(
                "not found: transport_stream_id=%d service_id=%d event_id=%d" % (
                    transport_stream_id, service_id, event_id),
                file=sys.stderr)
            sys.exit(1)
        else:
            print(int(time.mktime(start_time.timetuple())), int(time.mktime(end_time.timetuple())))


def main():
    process(sys.argv[1:])


if __name__ == '__main__':
    main()
