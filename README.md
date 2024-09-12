# Selfie Records python sdk
This is a python sdk for [selfie records](https://selfie-records.com/) that was just released as a npm package.


## Usage example
```
# test.py
from selfie import SelfieRecordsSDK
sdk = SelfieRecordsSDK()
records = sdk.get_records("hello@miguelmedeiros.dev", filters=["bitcoin-payment", "nostr"])
print(records)

#output 
{'bitcoin-payment': {'value': "b'bitcoin:?lno=lno1zrxq8pjw7qjlm68mtp7e3yvxee4y5xrgjhhyf2fxhlphpckrvevh50u0qfss4ttljzgkn3qwh8gj2wqduaphmkykxaxyh6ttpdplzqmkz5eguqszt7xngyyxhcnwahdqc5ss9x2rha0qex2x0djeag4nq8yfs2fuv4uqqv6jm6fxnk7n7g580kuust8n3hukv4dw3zs8r2dzkeqkf5j4vfhx8kxxl95sv2nsuf5jxnk90q' b'ew7w0f8g7qq29guwmd03v92yfjjan698z9q75gu3a8wzq8sprk4mf9qzykc9ljkqqse86pfp24kq4fmsaj5hlzh55ghs'", 'error': None}, 'nostr': {'value': "b'npub1j35k2lyes6x45sj2nyvsmefye6k4esurwp6wn3u3mtpt6ys5u8yqzjxygp'", 'error': None}}
```
