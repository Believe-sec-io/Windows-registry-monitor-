import winreg
import time
from datetime import datetime


class RegistryMonitor:
    def __init__(self, interval=2):
        self.interval = interval

        self.monitored_keys = [
            (
                winreg.HKEY_CURRENT_USER,
                r"Software\Microsoft\Windows\CurrentVersion\Run",
            ),
            (
                winreg.HKEY_CURRENT_USER,
                r"Software\Microsoft\Windows\CurrentVersion\RunOnce",
            ),
            (
                winreg.HKEY_LOCAL_MACHINE,
                r"Software\Microsoft\Windows\CurrentVersion\Run",
            ),
            (
                winreg.HKEY_LOCAL_MACHINE,
                r"Software\Microsoft\Windows\CurrentVersion\RunOnce",
            ),
        ]

    def _read_key(self, root, path):
        """Read all values from a registry key."""
        values = {}

        try:
            with winreg.OpenKey(root, path, 0, winreg.KEY_READ) as key:
                count = winreg.QueryInfoKey(key)[1]

                for index in range(count):
                    name, value, value_type = winreg.EnumValue(key, index)
                    values[name] = {
                        "value": value,
                        "type": value_type,
                    }

        except FileNotFoundError:
            pass

        except PermissionError:
            print(f"[!] Permission denied: {path}")

        except OSError as error:
            print(f"[!] Registry error: {error}")

        return values

    def snapshot(self):
        """Create a snapshot of all monitored registry keys."""
        snapshot = {}

        for root, path in self.monitored_keys:
            snapshot[(root, path)] = self._read_key(root, path)

        return snapshot

    def detect_changes(self, old_snapshot, new_snapshot):
        """Compare two registry snapshots."""
        changes = []

        for key_id in new_snapshot:
            old_values = old_snapshot.get(key_id, {})
            new_values = new_snapshot.get(key_id, {})

            root, path = key_id

            # New or modified values
            for name, data in new_values.items():

                if name not in old_values:
                    changes.append({
                        "action": "VALUE_CREATED",
                        "root": root,
                        "key": path,
                        "value_name": name,
                        "value": data["value"],
                    })

                elif old_values[name]["value"] != data["value"]:
                    changes.append({
                        "action": "VALUE_MODIFIED",
                        "root": root,
                        "key": path,
                        "value_name": name,
                        "old_value": old_values[name]["value"],
                        "value": data["value"],
                    })

            # Deleted values
            for name, data in old_values.items():
                if name not in new_values:
                    changes.append({
                        "action": "VALUE_DELETED",
                        "root": root,
                        "key": path,
                        "value_name": name,
                        "old_value": data["value"],
                    })

        return changes

    def monitor(self):
        """Continuously monitor the registry."""
        print("[+] Windows Registry Monitor started")
        print("[+] Monitoring Run / RunOnce registry keys")
        print("[+] Press CTRL+C to stop\n")

        previous = self.snapshot()

        try:
            while True:
                time.sleep(self.interval)

                current = self.snapshot()
                changes = self.detect_changes(previous, current)

                for change in changes:
                    timestamp = datetime.now().strftime(
                        "%Y-%m-%d %H:%M:%S"
                    )

                    print(
                        f"[{timestamp}] "
                        f"{change['action']} | "
                        f"{change['key']} | "
                        f"{change['value_name']}"
                    )

                    if "value" in change:
                        print(f"    New value: {change['value']}")

                    if "old_value" in change:
                        print(f"    Old value: {change['old_value']}")

                previous = current

        except KeyboardInterrupt:
            print("\n[+] Registry Monitor stopped.")
