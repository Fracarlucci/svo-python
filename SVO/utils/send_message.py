from northbound_api.functions import Functions
# from MQTT_communication import mqtt
class SendMessage():
    def google_id(self, lat, lng):
        location = Functions.search_place(Functions(), lat, lng)
        print(location)
        #location_id=location["location_id"]
        return location
    def send(self, location_id, msg):
        # mqtt.subscribe(str(location_id))
        # mqtt.publish(str(location_id), str(msg))
        pass
