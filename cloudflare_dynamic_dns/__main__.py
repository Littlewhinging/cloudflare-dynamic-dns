import os
import json
import time
import requests
import logging
import CloudFlare, CloudFlare.exceptions

dirpath = os.path.dirname(os.path.realpath(__file__))

FORMAT = "%(asctime)s:%(levelname)s:%(name)s:%(message)s"
logging.basicConfig(filename=os.path.join(dirpath, "latest.log"), encoding="utf-8", level=logging.INFO, format=FORMAT)
logger = logging.getLogger("main")
strmHndlr = logging.StreamHandler()
strmHndlr.setFormatter(logging.Formatter(FORMAT))
logger.addHandler(strmHndlr)

def intput(text: str) -> int:
	textvalue = input(text)
	try:
		return int(textvalue)
	except ValueError:
		return 0

def multi_menu(text: str, items: list[str]) -> list[int]:
	items.append("Finish")
	exit_number = len(items)

	for i, elem in enumerate(items, start=1):
		print(f"{i}) {elem}")

	all_selected: list[int] = []

	while True:
		value = 0
		while value < 1 or value > len(items):
			value = intput(text)

		if value == exit_number:
			break

		all_selected.append(value - 1)

	return all_selected

def main() -> None:
	if not os.path.exists(os.path.join(dirpath, "config.json")):
		token = input("API Token: ")
		try:
			cf = CloudFlare.CloudFlare(token=token)
			zones = cf.zones.get()
		except:
			print("Invalid API Token")
			return

		dns_records = []

		for zone in zones:
			try:
				temp_dns_records = cf.zones.dns_records.get(zone["id"])
			except CloudFlare.exceptions.CloudFlareAPIError as e:
				logger.error("/zones/dns_records.get %d %s - api call failed" % (e, e))
				exit("/zones/dns_records.get %d %s - api call failed" % (e, e))

			temp_dns_records = [i for i in temp_dns_records if i["type"] == "A"]

			for i in range(len(temp_dns_records)):
				temp_dns_records[i]["zone"] = zone["id"]
	
			dns_records += temp_dns_records

		max_name_length = max([len(i["name"]) for i in dns_records])
		selected = multi_menu("Select an option: ",[i["name"] + (" " * (max_name_length - len(i["name"]))) + "\t" + i["content"] for i in dns_records])

		selected_dns_records = [dns_records[i] for i in selected]

		zones = []

		for i in selected_dns_records:
			if not i["zone"] in zones:
				zones.append(i["zone"])

		delay = intput("Delay between checks in seconds: ")

		selected_dns_records = [i["id"] for i in selected_dns_records]

		with open(os.path.join(dirpath, "config.json"),"w") as f:
			json.dump({"token": token, "zones": zones, "dns_records": selected_dns_records, "delay": delay}, f)

	else:
		with open(os.path.join(dirpath, "config.json"),"r") as f:
			CONFIG = json.load(f)
			token = CONFIG["token"]
			zones = CONFIG["zones"]
			selected_dns_records = CONFIG["dns_records"]
			delay = CONFIG["delay"]
			cf = CloudFlare.CloudFlare(token=token)

	if delay < 1:
		delay = 1

	logger.info("Program started")

	ip = ""
	first = True
	while True:
		new_ip = requests.get("https://4.ident.me").text

		if ip != new_ip:
			if first:
				logger.info(f"IP address is {new_ip}")
				first = False
			else:
				logger.info(f"IP changed from {ip} to {new_ip}")
			ip = new_ip

			for zoneId in zones:
				try:
					temp_dns_records = cf.zones.dns_records.get(zoneId)
				except CloudFlare.exceptions.CloudFlareAPIError as e:
					string = f"Failed to fetch dns records for {zoneId}\n" + "/zones/dns_records.get %d %s - api call failed" % (e, e)
					logger.error(string)
					continue
				
				for dns_record in temp_dns_records:
					if dns_record["id"] in selected_dns_records and dns_record["content"] != ip:
						dns_record["content"] = ip
						cf.zones.dns_records.put(zoneId, dns_record["id"], data=dns_record)
						logger.info(f"Updated record for {dns_record['name']}")

		time.sleep(delay)

if __name__ == "__main__":
	main()