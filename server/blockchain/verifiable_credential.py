import json
from datetime import datetime

class VerifiableCredential:
    def __init__(self, credential):
        self.credential = credential

    def to_json(self):
        return json.dumps({
            "@context": [
                "https://www.w3.org/2018/credentials/v1",
                "https://www.w3.org/2018/credentials/examples/v1"
            ],
            "id": f"http://example.edu/credentials/{self.credential.credential_id}",
            "type": ["VerifiableCredential", "EducationalCredential"],
            "issuer": self.credential.institution,
            "issuanceDate": self.credential.date_issued.isoformat(),
            "credentialSubject": {
                "id": f"did:example:{self.credential.user.id}",
                "degree": {
                    "type": self.credential.degree,
                    "name": self.credential.degree
                }
            }
        }, indent=2)