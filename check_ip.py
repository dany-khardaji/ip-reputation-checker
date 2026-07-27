from dotenv import load_dotenv
import os
import requests
import argparse
                        
                        
load_dotenv()


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("ip", help="The IP address to check")
    args = parser.parse_args()

    api_key = os.getenv("ABUSEIPDB_API_KEY")

    headers = {
    "Key": api_key, 
    "Accept": "application/json"
}
    params = {
    "ipAddress": args.ip, 
    "maxAgeInDays": 90
}
    
    try:
        response = requests.get("https://api.abuseipdb.com/api/v2/check", headers=headers, params=params)   # API get request
    except requests.exceptions.RequestException:                                                            # Error handling for network issues
        print("[Network Error] - Failed to resolve host 'api.abuseipdb.com'. Check your internet connection and try again.")
        return

    if response.status_code != 200:  
        error_data = response.json()
        detail = error_data["errors"][0]["detail"]
        print (f"[Error] - Request failed, status code {response.status_code}: {detail}")  # Checks whether response is successful if not list details
        return

    response_dict = response.json()  # Parse the JSON to access abuseIPDB data

    abuse_confidence_score = response_dict["data"]["abuseConfidenceScore"]
    country = response_dict["data"]["countryCode"]
    isp = response_dict["data"]["isp"]
    total_reports = response_dict["data"]["totalReports"]
    # print(response.status_code)
    # print(response.text)
    print(f"------- ip: {params['ipAddress']} ------- \nScore: {abuse_confidence_score}, \nCountry: {country}, \nISP: {isp}, \nReports: {total_reports}")


if __name__ == "__main__":
    main()
