import os
import sys

sys.path.append('/tools')

from healthcheck_utils import get_agent_health_base, check

if __name__ == "__main__":
    exit(check(os.system("grep -q 'xcyber360-modulesd:syscollector.*INFO: Evaluation finished.' /var/ossec/logs/ossec.log"))
         or get_agent_health_base())
