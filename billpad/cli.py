"""Command line entry point.

Examples:
    python -m billpad bill --item "rice 5kg" --item "eggs 12" --code SAVE10
    python -m billpad codes
"""

import argparse
import sys

from . import discounts
from .catalog import PRICES
from .invoice import Invoice
from .storage import save_invoice


def cmd_bill(args):
    invoice = Invoice()
    for raw in args.item:
        name, _, qty = raw.rpartition(" x")
        if qty.isdigit():
            invoice.add(name, int(qty))
        else:
            invoice.add(raw, 1)
    if args.code:
        invoice.use_code(args.code)
    try:
        print(invoice.render())
    except (discounts.UnknownCodeError, discounts.ExpiredCodeError) as err:
        print("could not finish the bill: %s" % err, file=sys.stderr)
        return 1
    if not args.no_save:
        save_invoice(invoice)
    return 0


def cmd_codes(_args):
    for code, entry in sorted(discounts.CODES.items()):
        print("%-10s %2d%% off, last day %s" % (code, entry["percent"], entry["expires"]))
    return 0


def cmd_items(_args):
    for item, price in sorted(PRICES.items()):
        print("%-18s %6d" % (item, price))
    return 0


def main(argv=None):
    parser = argparse.ArgumentParser(prog="billpad")
    sub = parser.add_subparsers(dest="command", required=True)

    p_bill = sub.add_parser("bill", help="make a bill")
    p_bill.add_argument("--item", action="append", required=True,
                        help='item name, optionally with " x<qty>" at the end')
    p_bill.add_argument("--code", help="discount code, if the customer has one")
    p_bill.add_argument("--no-save", action="store_true",
                        help="do not keep a copy of this bill")
    p_bill.set_defaults(func=cmd_bill)

    p_codes = sub.add_parser("codes", help="list the discount codes")
    p_codes.set_defaults(func=cmd_codes)

    p_items = sub.add_parser("items", help="list the price list")
    p_items.set_defaults(func=cmd_items)

    args = parser.parse_args(argv)
    return args.func(args)


if __name__ == "__main__":
    sys.exit(main())
