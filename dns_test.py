import dns.resolver
import time
from statistics import mean

TEST_DOMAIN = "google.com"
REQUEST_COUNT = 5
TIMEOUT = 2


def test_dns(server_line):
    try:
        # جدا کردن IP و پورت
        if ":" in server_line:
            ip, port = server_line.split(":")
            port = int(port)
        else:
            ip = server_line
            port = 53

        resolver = dns.resolver.Resolver()
        resolver.nameservers = [ip]
        resolver.port = port
        resolver.timeout = TIMEOUT
        resolver.lifetime = TIMEOUT

        times = []

        for _ in range(REQUEST_COUNT):
            start = time.time()
            resolver.resolve(TEST_DOMAIN)
            end = time.time()
            times.append((end - start) * 1000)

        return mean(times)

    except Exception:
        return None


def main():
    results = {}

    with open("irdns.txt", "r") as f:
        dns_list = [line.strip() for line in f if line.strip()]

    for dns_server in dns_list:
        print(f"Testing {dns_server} ...")
        avg_time = test_dns(dns_server)

        if avg_time is None:
            print(f"❌ {dns_server} FAILED")
        else:
            print(f"✅ {dns_server} {avg_time:.2f} ms")
            results[dns_server] = avg_time

    print("\n--- Sorted Results ---")
    for dns_server, avg_time in sorted(results.items(), key=lambda x: x[1]):
        print(f"{dns_server} → {avg_time:.2f} ms")


if __name__ == "__main__":
    main()
