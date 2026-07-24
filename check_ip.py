import requests         # the HTTP tool you'll use to call the API
                        # You'll also need something to load your API key from a .env file later.
                        # Leave that import out for now — we add it at Step 5, when you actually move the key out of the code. One tool at a time.
def main():

    headers = {
    "Key": "REDACTED", 
    "Accept": "application/json"
}
    params = {
    "ipAddress": "118.25.6.39", 
    "maxAgeInDays": 90
}
    response = requests.get("https://api.abuseipdb.com/api/v2/check", headers=headers, params=params)   #API get request
    response_dict = response.json()      #Parse the JSON to access abuseIPDB data

    abuse_confidence_score = response_dict["data"]["abuseConfidenceScore"]
    country = response_dict["data"]["countryCode"]
    isp = response_dict["data"]["isp"]
    total_reports = response_dict["data"]["totalReports"]

    # print(response.status_code)
    # print(response.text)
    print(f"------- ip: {params['ipAddress']} ------- \nScore: {abuse_confidence_score}, \nCountry: {country}, \nISP: {isp}, \nReports: {total_reports}")


if __name__ == "__main__":
    main()
