import os
import re


class RegistryDetector:
    """
    Analyze Windows Registry changes and assign a risk level.
    """

    SUSPICIOUS_PATHS = [
        r"\currentversion\run",
        r"\currentversion\runonce",
        r"\currentversion\runservices",
        r"\currentversion\runservicesonce",
    ]

    SUSPICIOUS_LOCATIONS = [
        r"\appdata\roaming",
        r"\appdata\local",
        r"\temp",
        r"\startup",
        r"\programdata",
    ]

    SUSPICIOUS_EXTENSIONS = [
        ".exe",
        ".bat",
        ".cmd",
        ".vbs",
        ".js",
        ".ps1",
        ".scr",
        ".dll",
    ]

    def analyze(self, change):
        """
        Analyze a registry change and return a security assessment.
        """

        action = change.get("action", "")
        key = change.get("key", "")
        value_name = change.get("value_name", "")

        value = change.get("value", "")
        old_value = change.get("old_value", "")

        combined_value = f"{value} {old_value}".lower()
        normalized_key = key.lower()

        score = 0
        reasons = []

        # Persistence location
        if any(path in normalized_key for path in self.SUSPICIOUS_PATHS):
            score += 30
            reasons.append("Registry persistence location")

        # New persistence entry
        if action == "VALUE_CREATED":
            score += 20
            reasons.append("New registry value created")

        # Executable/script
        if any(ext in combined_value for ext in self.SUSPICIOUS_EXTENSIONS):
            score += 20
            reasons.append("Executable or script referenced")

        # Suspicious user-writable locations
        if any(location in combined_value for location in self.SUSPICIOUS_LOCATIONS):
            score += 25
            reasons.append("User-writable or temporary location")

        # PowerShell
        if "powershell" in combined_value:
            score += 25
            reasons.append("PowerShell execution detected")

        # Command shell
        if re.search(r"\b(cmd|wscript|cscript)\b", combined_value):
            score += 20
            reasons.append("Command/script interpreter detected")

        # Obfuscation indicators
        if "-enc" in combined_value or "frombase64string" in combined_value:
            score += 25
            reasons.append("Possible command obfuscation")

        # Deleted persistence entry
        if action == "VALUE_DELETED":
            score += 5
            reasons.append("Registry value deleted")

        # Cap score
        score = min(score, 100)

        if score >= 80:
            risk = "CRITICAL"
        elif score >= 60:
            risk = "HIGH"
        elif score >= 30:
            risk = "MEDIUM"
        else:
            risk = "LOW"

        return {
            "risk": risk,
            "score": score,
            "reasons": reasons,
            "action": action,
            "key": key,
            "value_name": value_name,
            "value": value,
          }
