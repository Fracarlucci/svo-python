import logging
from fastapi import HTTPException
from vo.models.VoInfo import VoInfo
import config
# from MQTT_communication import mqtt
# from googleplaces import GooglePlaces, GooglePlacesAttributeError, GooglePlacesError
GOOGLE_API_KEY = 'AIzaSyA35ioXBdoHn4Ng3wko-jEqtxLYWVLF6go' # TODO CHECK

class Functions():
    def check_mandatory_parameters(self, mandatory, body):
        try:
            if(body is not dict):
                _ = body
            else:
                for i in mandatory:
                    missing_parameter = i
                    _ = body[i]
        except Exception:
            logging.warning("Functions, check_mandatory_parameters() method. Missing mandatory parameter")
            raise HTTPException(status_code=400, detail= "Bad Request, missing parameters")



    def permissions(self, body, query):

        if query is None:
            logging.warning("Functions, permission() method. Query result is empty.")
            raise HTTPException(status_code=400, detail= "Bad Request, query result is empty")

        try:
            permission= query.permission
        except Exception:
            permission = None
            logging.warning("Functions, permission method. Permission in query.")
            raise HTTPException(status_code=400, detail= "Permission is none")

        if permission == "public":
            permission_code = 0
            return permission_code

        elif permission == "friend":
            try:
                key= body["key"]
            except Exception:
                logging.warning("Functions, permission method. Missing key.")
                raise HTTPException(status_code=401, detail= "The key is missing")

            permission_level = self.get_permission_level(key)

            if permission_level== "owner":
                permission_code= 2
                return permission_code
            elif permission_level=="friend":
                permission_code= 1
                return permission_code
            else:
                logging.warning("Functions, permission method. Not allowed with this key.")
                raise HTTPException(status_code=403, detail= "Not Allowed")

        else:
            if permission == "owner":
                try:
                    key = body["key"]
                except Exception:
                    logging.warning("Fucntions, permission method. Missing key.")
                    raise HTTPException(status_code=401, detail= "The key is missing")
                permission_level = self.get_permission_level(key)
                if permission_level == "owner":
                    permission_code = 2
                    return permission_code
                else:
                    logging.warning("Functions, permission method. Not allowed with this key.")
                    raise HTTPException(status_code=403, detail= "Not Allowed")


    def get_permission_level(self, key):
        my_owner_key= config.cache.get('owner')
        my_friend_key= config.cache.get('friend')
        if my_owner_key is None or my_friend_key is None:
            vo_info = VoInfo.query.first()
            my_owner_key = vo_info.owner_key
            my_friend_key = vo_info.friend_key
            config.cache.set('owner_key', my_owner_key)
            config.cache.set('friend_key', my_friend_key)
        level = "denied"
        if my_owner_key == key:
            level = "owner"
            return level
        elif my_friend_key == key:
            level = "friend"
            return level
        return level

    # def send_message_mqtt(self, subscribe, message):
        # mqtt.publish(subscribe, message)

    # def search_place(self, lat, lng):
    #     try:
    #         google_places = GooglePlaces(GOOGLE_API_KEY)
    #         range = 50
    #         results = google_places.nearby_search(lat_lng={'lat': lat, 'lng': lng}, radius=range)
    #         place= results.places[0]
    #         print(place.name)
    #         place.get_details()
    #         print(place.url)
    #         return {"location_id":place.place_id, "location_name":place.name, "location_range":range}
    #     except (GooglePlacesError, GooglePlacesAttributeError) as error_detail:
    #         print('Google Returned an Error : {0}'.format(error_detail))
    #         pass
