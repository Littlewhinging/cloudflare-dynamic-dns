import os
import CloudFlare
import json
from datetime import datetime
import time
import requests

def intput(text):
  textvalue = input(text)
  try:
    return int(textvalue)
  except ValueError:
    return 0

def menu(text,items):
	for i in range(len(items)):
		print(f"{i + 1}) {items[i]}")
     
	value = 0
	while value < 1 or value > len(items):
		value = intput(text)
	print()
	return value - 1


def multi_menu(text,items):
	items.append("Finish")
	exit_number = len(items)

	for i in range(len(items)):
		print(f"{i + 1}) {items[i]}")
 
	all_selected = []

	while True:
		value = 0
		while value < 1 or value > len(items):
			value = intput(text)
   
		if value == exit_number:
			break

		all_selected.append(value - 1)
	
	return all_selected

def log(text):
	time = datetime.now()
	info = time.strftime("%Y-%m-%d %H:%M:%S") + "\t" + text
	print(info)
	with open("log.txt","a") as f:
		f.write(info + "\n")

def main():
	use_config = os.path.exists("cfd-config.json")

	if not use_config:
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
				exit('/zones/dns_records.get %d %s - api call failed' % (e, e))

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
    
		with open("cfd-config.json","w") as f:
			json.dump({"token": token, "zones": zones, "dns_records": [i["id"] for i in selected_dns_records], "delay": delay}, f)

	else:
		with open("cfd-config.json","r") as f:
			config = json.load(f)
			token = config["token"]
			zones = config["zones"]
			selected_dns_records = config["dns_records"]
			delay = config["delay"]
			cf = CloudFlare.CloudFlare(token=token)

	if delay < 1:
		delay = 1

	log("")
	log("[INFO] Program started")

	ip = "Unknown"
	while True:
		new_ip = requests.get("https://4.ident.me").text

		if ip != new_ip:
			log(f"[INFO] IP changed from {ip} to {new_ip}")
			ip = new_ip

			for zoneId in zones:
				try:
					temp_dns_records = cf.zones.dns_records.get(zoneId)
				except CloudFlare.exceptions.CloudFlareAPIError as e:
					log(f"[ERROR] Failed to fetch dns records for {zoneId}")
				
				for dns_record in temp_dns_records:
					if dns_record["id"] in selected_dns_records and dns_record["content"] != ip:
						dns_record["content"] = ip
						cf.zones.dns_records.put(zoneId, dns_record["id"], data=dns_record)
						log(f"[INFO] Updated record for {dns_record['name']}")

		time.sleep(delay)


if __name__ == '__main__':
	main()