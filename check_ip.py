from dotenv import load_dotenv
import os
import requests
import argparse
                        
                        
load_dotenv()


def main():
    
    # Set up parser and created argument
    parser = argparse.ArgumentParser()  
    parser.add_argument("ip", help="The IP address to check")
    args = parser.parse_args()


    # Key loaded from .env, never hardcoded
    api_key = os.getenv("ABUSEIPDB_API_KEY")
    # Auth headers and the IP being checked
    headers = {
    "Key": api_key, 
    "Accept": "application/json"}

    params = {
    "ipAddress": args.ip,
    "maxAgeInDays": 90}
    

    # get request and error handling
    try:
        response = requests.get("https://api.abuseipdb.com/api/v2/check", headers=headers, params=params)   # API get request

    except requests.exceptions.RequestException:                                                            
        print("[Network Error] - Failed to resolve host 'api.abuseipdb.com'. Check your internet connection and try again.")
        return

    if response.status_code != 200:  
        error_data = response.json()
        detail = error_data["errors"][0]["detail"]
        print (f"[Error] - Request failed, status code {response.status_code}: {detail}")
        return


    # Parse the JSON to access abuseIPDB data and print results
    response_dict = response.json()

    abuse_confidence_score = response_dict["data"]["abuseConfidenceScore"]
    country = response_dict["data"]["countryCode"]
    isp = response_dict["data"]["isp"]
    total_reports = response_dict["data"]["totalReports"]

    if abuse_confidence_score >= 75:
        verdict = "BLOCK"
    elif abuse_confidence_score >= 25:
        verdict = "MONITOR"
    else:
        verdict = "OK"

    print(f"------- ip: {params['ipAddress']} ------- \nVerdict: {verdict}, \nScore: {abuse_confidence_score}, \nCountry: {country}, \nISP: {isp}, \nReports: {total_reports}")


if __name__ == "__main__":
    main()
