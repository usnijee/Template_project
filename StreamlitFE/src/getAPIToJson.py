import requests
import json

class getApiToJson:
    def __init__(self, platform, playerName, apikey):
        self.platform = platform
        self.playerName = playerName
        self.apikey = apikey
        self.id_search_by_nickname_url = f"https://api.pubg.com/shards/{self.platform}/players?filter[playerNames]="
        self.apis_header = {
            "Authorization": f"Bearer {self.apikey}",
            "Accept": "application/vnd.api+json"
        }
        self.telemetry_header = {
            "Accept": "application/vnd.api+json",
            "Accept-Encoding": "gzip"
        }
        
        self.id_response = requests.get(self.id_search_by_nickname_url + self.playerName, headers=self.apis_header)

    
    def getPlayerId(self):
        playerId = self.id_response.json()['data'][0]['links']['self'].split("/")[-1]
        return f"playerid : {playerId}"
    
    def getMatchIdList(self):
        match_datas = self.id_response.json()['data'][0]['relationships']['matches']['data']
        match_data_lists = [match['id'] for match in match_datas]
        print(f"검색된 matchId 수 : {len(match_data_lists)}")
        return match_data_lists
    
    def getTelemetryURLFromList(self, match_data_lists):
        match_search_by_matchId_url = f"https://api.pubg.com/shards/{self.platform}/matches/"
        telemetryURLList = []
        for match_IDs in match_data_lists:
            match_data = requests.get(match_search_by_matchId_url + match_IDs, headers=self.apis_header)
            telemetryId = match_data.json()['data']['relationships']['assets']['data'][0]['id']
            print(f"matchId : {match_IDs}\ntelemetryId : {telemetryId}")
            for included_item in match_data.json()['included']:
                if included_item['type'] == 'asset':
                    telemetry_url = included_item['attributes']['URL']
                    telemetryURLList.append(telemetry_url)
                    print(telemetry_url, "\n")
        return telemetryURLList
    
    def getTelemtryJsonFromTelemetryURL(self, telemetry_url):
        telemetry_response = requests.get(telemetry_url, headers=self.telemetry_header)
        return telemetry_response.json()
    
    def getTelemetryJsonFromMatchId(self, matchId):
        self.matchId = matchId
        match_search_by_matchId_url = f"https://api.pubg.com/shards/{self.platform}/matches/"
        match_data = requests.get(match_search_by_matchId_url + self.matchId, headers=self.apis_header)
        for included_item in match_data.json()['included']:
            if included_item['type'] == 'asset':
                self.telemetryURL = included_item['attributes']['URL']
        print(f"matchId : {self.matchId}\ntelemetryURL : {self.telemetryURL}\n")
        telemetry_response = requests.get(self.telemetryURL, headers=self.telemetry_header)
        return telemetry_response.json()
    
    def saveJsonFile(self, JsonResponse, fileName, filetype):
        filetype = "." + f"filetype"
        self.fileName = fileName + filetype
        with open(self.fileName, 'w') as json_file:
            json.dump(JsonResponse, json_file, indent=4)
    
    def getOtherApiToJson(self, endPoints):
        url = f"https://api.pubg.com/shards/{self.platform}"
        r = requests.get(url + endPoints, headers=self.apis_header)
        return r.json()