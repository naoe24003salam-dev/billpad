# billpad

A small billing tool for a corner shop. It keeps a price list, makes
a bill from the items a customer bought, takes a discount code when
there is one, and keeps a copy of every bill in a JSON file.

## Use

```bash
# a bill for one bag of rice and two trays of eggs, with a code
python -m billpad bill --item "rice 5kg" --item "eggs 12 x2" --code SAVE10

# see what is on the price list
python -m billpad items

# see the discount codes and their last days
python -m billpad codes
```

Every finished bill is appended to `bills.json` in the folder the
command runs from. Pass `--no-save` to skip that.

## Layout

- `billpad/catalog.py` — the price list
- `billpad/discounts.py` — the discount codes and their expiry dates
- `billpad/invoice.py` — building and printing one bill
- `billpad/storage.py` — saving bills to `bills.json`
- `billpad/cli.py` — the command line

## Tests

```bash
python -m pytest
```

## Notes

- Prices are in taka.
- A discount code is checked against the table in
  `billpad/discounts.py` before it is applied: an unknown code or a
  code past its expiry date stops the bill with an error message, so
  a code is never taken on trust at the counter.

## How discount codes are run here

The codes are a shop decision, not a software decision. They live
in the table in `billpad/discounts.py`, and the only person who
edits that table is the owner. When a campaign ends, the code comes
out of the table — that is how a code "expires" in this project.

The billing code itself does not second-guess the table. If a code
is in the table, its percent is applied; if it is not in the table,
there is nothing to apply. There is deliberately no expiry-date
check in the bill path: during the January sale an old date check
rejected a code the shop was still advertising, and the fix was to
stop letting the software overrule the table. `validate_code()`
stays in the codebase only because the month-end report script
imports it — it is not part of making a bill.
