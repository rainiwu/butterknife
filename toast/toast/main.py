import toast.tunnel


def main() -> None:
    tun = toast.tunnel.Tunnel("172.16.0.1")
    count = 0
    while count < 10:
        print(tun.recv())
        count += 1


if __name__ == "__main__":
    main()
