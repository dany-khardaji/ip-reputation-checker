from dotenv import load_dotenv      # Reads the .env file so the API key never touches the code
import os                           # Used to pull the key out of the environment
import requests                     # Makes the HTTP call to AbuseIPDB
import argparse                     # Lets the CLI take an IP from the command line


load_dotenv()                       # Runs once at import, loads .env into the environment


# Takes an IP string, returns a dict of reputation data (or an error dict).
# Never prints, so CLI, FastAPI, and anything else can all call it.
def check_ip(ip):
    # Key loaded from .env, never hardcoded
    api_key = os.getenv("ABUSEIPDB_API_KEY")

    # Auth headers and the IP being checked
    headers = {
    "Key": api_key, 
    "Accept": "application/json"}

    params = {
    "ipAddress": ip,
    "maxAgeInDays": 90}
    
    # Get request and error handling
    try:
        response = requests.get("https://api.abuseipdb.com/api/v2/check", headers=headers, params=params)   # API get request

    except requests.exceptions.RequestException:                                                            
        return {"error": "[Network Error] - could not reach 'api.abuseipdb.com'"}

    if response.status_code != 200:  
        error_data = response.json()
        detail = error_data["errors"][0]["detail"]
        return {
            "error": "[Error] - request failed",
            "status_code": response.status_code,
            "detail": detail
        }   

    # Parse the JSON to access and return abuseIPDB data
    results_dict = response.json()

    abuse_confidence_score = results_dict["data"]["abuseConfidenceScore"]
    country = results_dict["data"]["countryCode"]
    isp = results_dict["data"]["isp"]
    total_reports = results_dict["data"]["totalReports"]

    if abuse_confidence_score >= 75:
        verdict = "BLOCK"
    elif abuse_confidence_score >= 25:
        verdict = "MONITOR"
    else:
        verdict = "OK"

    # This is the data in dictionary form that the API gives when called
    return {
        "ip": ip,
        "verdict": verdict,
        "score": abuse_confidence_score,
        "country": country,
        "isp": isp,
        "total_reports": total_reports
    }


# The CLI interface. Only place in this file that prints.
# FastAPI ignores this entirely and calls check_ip() directly.
def main():
    # Set up parser for CLI and created argument
    parser = argparse.ArgumentParser()  
    parser.add_argument("ip", help="The IP address to check")
    args = parser.parse_args()
    result = check_ip(args.ip)

    if "error" in result:
        print(result["error"])
    else:
        print(f"------- ip: {result['ip']} ------- \nVerdict: {result['verdict']}, \nScore: {result['score']}, \nCountry: {result['country']}, \nISP: {result['isp']}, \nReports: {result['total_reports']}")


# Only fires when you run directly. When api.py imports this file, main() never runs.
if __name__ == "__main__":
    main()
