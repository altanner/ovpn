import os
import sys
import random
import subprocess
import argparse

#~ local imports
import srvr_codes
import my_paths
import prefixes


def args_setup():

    parser = argparse.ArgumentParser(
        description = "OpenVPN connection thingy.",
        epilog = "Example: python ovpn_connect.py -c uk")
    parser.add_argument(
        "-c", action = "store",
        help = "Two-letter server country code.")
    parser.add_argument(
        "-x", action = "store_true",
        help = "Close the VPN connection daemon.")

    args = parser.parse_args()

    return parser, args

parser, args = args_setup()


# paths
ovpn_udp_path = my_paths.udp
ovpn_auth_path = my_paths.auth
ovpn_run_cmd = "sudo -b openvpn --config"


if __name__ == "__main__":

    upcheck = subprocess.run("pgrep openvpn > /dev/null 2>&1", shell=True)

    if args.x:
        if upcheck.returncode == 0:
            subprocess.run("/usr/bin/sudo /usr/bin/pkill -2 openvpn", shell=True)
            sys.exit(0)
        else:
            sys.exit("OpenVPN not running.")

    if not args.c:
        print("Please choose a country code from the following:")
        for _ in prefixes.prefixes:
            print(_)
        print("Example:\npython ovpn_connect.py -c uk")
        sys.exit(1)

    # build server name from country code + rnd server number
    srvr_numbers = srvr_codes.srvr_codes[args.c]
    srvr_name = args.c + random.choice(srvr_numbers) + ".nordvpn.com.udp.ovpn"

    if upcheck.returncode == 1:
        subprocess.run(
            f"{ovpn_run_cmd} {ovpn_udp_path}{srvr_name} --auth-user-pass {ovpn_auth_path}", shell=True)
    else:
        sys.exit("OpenVPN already running.")
