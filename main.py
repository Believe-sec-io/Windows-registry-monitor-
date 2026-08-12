from registry_monitor import RegistryMonitor


def main():
    monitor = RegistryMonitor(interval=2)
    monitor.monitor()


if __name__ == "__main__":
    main()
