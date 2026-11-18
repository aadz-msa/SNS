# Experiment 6: Simple Security and Privacy Detector
import re

PII = {
    "Email address": r"[\w.+-]+@[\w-]+\.[\w.-]+",
    "Phone number": r"(?<!\d)(?:\+91[- ]?)?[6-9]\d{9}(?!\d)",
    "Aadhaar number": r"(?<!\d\s)(?<!\d)\d{4}\s\d{4}\s\d{4}(?!\d|\s\d)",
    "Credit card number": r"(?<!\d)(?:\d{4}[- ]){3}\d{4}(?!\d)",
    "IP address": r"(?<!\d)(?:\d{1,3}\.){3}\d{1,3}(?!\d)",
    "Home address hint": r"(?i)\b(?:i live at|my address is|house no)\b",
}


def scan_post(text):
    return [
        (name, match.group())
        for name, pattern in PII.items()
        for match in re.finditer(pattern, text)
    ]


def password_strength(password):
    score = sum([
        len(password) >= 8,
        bool(re.search(r"[a-z]", password)),
        bool(re.search(r"[A-Z]", password)),
        bool(re.search(r"\d", password)),
        bool(re.search(r"[^\w]", password))
    ])
    return [
        "Very weak", "Very weak", "Weak",
        "Medium", "Strong", "Very strong"
    ][score]


def audit_settings(settings):
    risks = []

    if settings.get("profile") == "public":
        risks.append("Profile is public")
    if not settings.get("two_factor"):
        risks.append("Two-factor authentication is OFF")
    if settings.get("location_sharing"):
        risks.append("Location sharing is ON")
    if settings.get("searchable_by_phone"):
        risks.append("Account discoverable by phone number")

    return risks


posts = [
    "Had a great day at the beach!",
    "Call me on 9876543210 or mail ajil@example.com",
    "My Aadhaar is 1234 5678 9012 and card 4111 1111 1111 1111",
    "Server at 192.168.1.10 - I live at 12 Main Street"
]

print("=== POST PRIVACY SCAN ===")
for number, post in enumerate(posts, 1):
    findings = scan_post(post)
    print(f"Post {number}: {'SAFE' if not findings else 'RISK (%d item(s))' % len(findings)}")
    for name, value in findings:
        print(f"    - {name}: {value}")

print("\n=== PASSWORD CHECK ===")
for password in ["123456", "password", "Ajil2024", "Sn@Sec#2026!"]:
    print(f"{password:15s} -> {password_strength(password)}")

print("\n=== ACCOUNT SETTINGS AUDIT ===")
settings = {
    "profile": "public",
    "two_factor": False,
    "location_sharing": True,
    "searchable_by_phone": True
}
for risk in audit_settings(settings):
    print(" [!]", risk)
