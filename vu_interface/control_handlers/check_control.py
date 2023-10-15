from vo.models.VoInfo import VoInfo
from vo.models.Control import Control
from vo.models.Data import Data
import logging
import requests


class checkControl_sensors():
    this_svo = VoInfo.query.first()
    if this_svo is not None:
        #port = this_svo.vu_url.split(":")[2]
        url_to_send = "http://vu:" +str("1")+ "listener"
    def check_control(self, data):
        controls_list = Control.query.filter_by(feature="all").all()
        if controls_list is not None:
            for c in controls_list:
                if c.status == 'ON':
                    query = Data.query.filter_by(feature=data["feature"]).order_by(Data.timestamp).limit(2)
                    if "text" in query[1].type.split(","):
                        if c.condition == "STATUS_CHANGED" and c.value == "ONBODY":
                            data_dict = dict(data["value"])
                            if "ONBODY" in data_dict.keys():
                                if str(data["value"]) != str(query[1].value):
                                    message = {"control_id": c.controlID, "feature": data["feature"],
                                       "ONBODY_value": data_dict["ONBODY"]}
                                    requests.post(str(self.url_to_send), json = message)
                            else:
                                logging.warning("Data non valid for checking ONBODY status.")
                        else:
                            logging.warning("Other condition for text type are not implemented yet.")
                    else:
                        logging.warning("Other controls for text type are not implmented yet.")
                else:
                    logging.warning("This control: "+ str(c.controlID)+ ", is OFF.")
        else:
            controls_list = Control.query.filter_by(feature=data["feature"]).all()
            if controls_list is not None:
                for c in controls_list:
                    if c.status == 'ON':
                        query = Data.query.filter_by(feature=data["feature"]).order_by(Data.timestamp).limit(2)
                        if "text" in query[1].type.split(","):
                            if c.condition == "STATUS_CHANGED" and c.value == "ONBODY":
                                data_dict = dict(data["value"])
                                if "ONBODY" in data_dict.keys():
                                    if str(data["value"]) != str(query[1].value):
                                        message = {"control_id": c.controlID, "feature": data["feature"],
                                                   "ONBODY_value": data_dict["ONBODY"]}
                                        requests.post(str(self.url_to_send), json = message)
                                else:
                                    logging.warning("Data non valid for checking ONBODY status.")
                            else:
                                logging.warning("Other condition for text type are not implemented yet.")
                        else:
                            logging.warning("Other controls for text type are not implmented yet.")
                    else:
                        logging.warning("This control: " + str(c.controlID) + ", is OFF.")









