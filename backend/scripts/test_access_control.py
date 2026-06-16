"""Proof: a proposal_writer is blocked from HR docs; HR can read HR. Run:
python -m app.scripts.test_access_control"""
from app.security.rbac import can_access

def main():
    result = {
        "proposal_writer_blocked_from_hr": not can_access("proposal_writer", "hr"),
        "hr_can_retrieve_hr": can_access("hr", "hr"),
        "admin_reads_all": can_access("system_admin", "anything"),
    }
    print(result)
    assert result["proposal_writer_blocked_from_hr"]
    assert result["hr_can_retrieve_hr"]

if __name__ == "__main__":
    main()
