import dns.resolver
import re
import logging
from typing import List, Dict, Optional, Any

DEFAULT_RECORDS = ["bitcoin-payment", "pgp", "nostr", "node-uri"]

class SelfieRecordsSDK:
    def __init__(self, debug: bool = False):
        self.resolver = dns.resolver.Resolver()
        self.logger = self._setup_logger(debug)

    def _setup_logger(self, debug: bool) -> logging.Logger:
        logger = logging.getLogger(__name__)
        if debug:
            logger.setLevel(logging.DEBUG)
            handler = logging.StreamHandler()
            formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
            handler.setFormatter(formatter)
            logger.addHandler(handler)
        else:
            logger.setLevel(logging.ERROR)
        return logger

    def get_records(self, name: str, filters: Optional[List[str]] = None, dns_server: str = "8.8.8.8") -> Dict[str, Dict[str, Optional[str]]]:
        if filters is None:
            filters = DEFAULT_RECORDS

        self.resolver.nameservers = [dns_server]
        results = {}

        for key in filters:
            try:
                domain_check = self.validate_domain_or_subdomain(key, name)
                email_check = self.validate_email_address(key, name)

                if domain_check["error"] and email_check["error"]:
                    results[key] = {"value": "", "error": domain_check["error"] or email_check["error"]}
                    continue

                domain_name = self.get_txt_record_key(name, key)
                self.logger.debug(f"Resolving TXT record for: {domain_name}")
                answers = self.resolve_txt(domain_name)

                if not answers:
                    results[key] = {"value": "", "error": "No TXT records found"}
                else:
                    value = " ".join(str(rdata) for rdata in answers[0].strings)
                    results[key] = {"value": value, "error": None}
            except Exception as error:
                self.logger.exception(f"Error processing {key}: {str(error)}")
                results[key] = self.handle_error(key, error)

        return results

    def resolve_txt(self, name: str) -> List[Any]:
        try:
            answers = self.resolver.resolve(name, 'TXT', raise_on_no_answer=False)
            return answers
        except dns.resolver.NXDOMAIN:
            self.logger.info(f"Domain not found: {name}")
            return []
        except Exception as e:
            self.logger.exception(f"Error resolving TXT record for {name}: {str(e)}")
            raise

    def get_txt_record_key(self, name: str, key: str) -> str:
        if "@" in name:
            local_part, domain = name.split("@")
            return f"{local_part}.user._{key}.{domain}"
        return f"_{key}.{name}"

    def validate_email_address(self, key: str, name: str) -> Dict[str, Optional[str]]:
        email_regex = r'^[^\s@]+@[^\s@]+\.[^\s@]+$'
        if not isinstance(name, str) or not re.match(email_regex, name):
            return {"key": key, "value": "", "error": "Invalid email name"}
        return {"key": key, "value": "", "error": None}

    def validate_domain_or_subdomain(self, key: str, name: str) -> Dict[str, Optional[str]]:
        domain_regex = r'^(?!:\/\/)([a-zA-Z0-9-_]+(\.[a-zA-Z0-9-_]+)+.*)$'
        if not isinstance(name, str) or not re.match(domain_regex, name):
            return {"key": key, "value": "", "error": "Invalid domain or subdomain name"}
        return {"key": key, "value": "", "error": None}

    def handle_error(self, key: str, error: Exception) -> Dict[str, Optional[str]]:
        if isinstance(error, dns.resolver.NXDOMAIN):
            return {"key": key, "value": "", "error": "Domain not found"}
        elif isinstance(error, dns.resolver.NoAnswer):
            return {"key": key, "value": "", "error": "No TXT records found"}
        return {"key": key, "value": "", "error": f"Failed to get TXT records: {str(error)}"}

# Usage example
sdk = SelfieRecordsSDK(debug=False)  # Set debug=True to enable debug logging
records = sdk.get_records("hello@miguelmedeiros.dev", filters=["bitcoin-payment", "nostr"])
print(records)