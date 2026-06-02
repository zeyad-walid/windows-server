import sys
try:
    from pyad import adadobject, adou, aduser
except ImportError:
    print("[-] Missing required libraries. Please run: pip install pyad pywin32")
    sys.exit(1)

# Central Domain Configuration (Matching server01.zeyad.local)
domain_dn = "dc=zeyad,dc=local"
departments = ["IT", "Finance", "Sales"]

# Structured user database array for testing deployment
new_users = [
    {"username": "ali_sales", "firstname": "Ali", "lastname": "Ahmed", "department": "Sales"},
    {"username": "omar_fin", "firstname": "Omar", "lastname": "Hassan", "department": "Finance"},
    {"username": "zeyad_it", "firstname": "Zeyad", "lastname": "Walid", "department": "IT"}
]

print("[*] Starting Active Directory Automated Provisioning...")

# Step 1: Ensure Core Department OUs exist in the directory
for dept in departments:
    try:
        # Check if OU already exists, if not it will raise an exception to handle creation
        target_ou_dn = f"ou={dept},{domain_dn}"
        adou.ADOrganizationalUnit.from_dn(target_ou_dn)
        print(f"[~] Organizational Unit [{dept}] already exists. Skipping creation.")
    except Exception:
        try:
            adou.ADOrganizationalUnit.create(dept, base_dn=domain_dn)
            print(f"[+] Successfully Created OU: {dept}")
        except Exception as e:
            print(f"[-] Critical failure creating OU {dept}: {e}")

# Step 2: Batch User Provisioning Loop
for user in new_users:
    try:
        target_ou_dn = f"ou={user['department']},{domain_dn}"
        target_ou = adou.ADOrganizationalUnit.from_dn(target_ou_dn)
        
        # Injects the user with standard, complex compliant temporary password
        created_user = target_ou.create_user(
            sAMAccountName=user['username'],
            password="Password123!"
        )
        
        # Explicitly update attributes for identity completeness
        created_user.update_attribute("givenName", user['firstname'])
        created_user.update_attribute("sn", user['lastname'])
        created_user.update_attribute("department", user['department'])
        
        print(f"[+] User [{user['username']}] provisioned successfully in [{user['department']}] OU.")
    except Exception as e:
        print(f"[-] Failed to provision user {user['username']}: {e}")

print("[*] Provisioning automation sequence finished.")
