from datetime import datetime
import json
import logging
from fastapi import HTTPException, Request
from fastapi.responses import JSONResponse
from vo.models.Configuration import Configuration
from vo.models.Data import Data
from vo.models.Device_Id import Device_Id
from northbound_api.functions import Functions
from sqlalchemy import and_
from southbound_api.vo_to_device.vo_to_device import communication_options


class GetSensor():

    sensor = None

    def __init__(self, sensor : dict):
        self.sensor = sensor
        
    ##CHECK INPUTS
    ##QUERY SENSOR_NAME CORRISPONDENTE IN TABELLA CONFIGURATION
    def get_inputs(self):
        mandatory = ["feature",
                     "time_scope"]
        Functions.check_mandatory_parameters(Functions(), mandatory, self.sensor)
        return_query = Configuration.query.get(self.sensor["feature"])
        return return_query

    ##CHECK PERMESSI ( permission è un attributo presente nella tabella Configuration)
    #RICHIESTA VALORI IN DATA -last -now (mediante MQTT) -intervallo di tempi
    def granted_actions(self):
        return_query = self.get_inputs()
        try:
            Functions.permissions(Functions(), self.sensor, return_query)
        except Exception:
            logging.warning("GetSensor, granted_actions method. Not allowed.")
            raise HTTPException(status_code=403, detail="Not Allowed")

        sensor = self.sensor["feature"]
        time_scope = self.sensor["time_scope"]
        if time_scope == 'last':
            try:
                d= Data.query.filter_by(feature=sensor).order_by(Data.timestamp.desc()).first()
                if d is not None:
                    response = {"value": str(d.value),"timestamp": datetime.strftime(d.timestamp, "%Y-%m-%d %H:%M:%S")}
                    resp= json.dumps({"entries": response})
                    return JSONResponse(content=resp, status_code=200)
                else:
                    logging.warning("GetSensor, granted_actions() method. No data yet")
                    raise HTTPException(status_code=410, detail="No data yet")
            except AttributeError:
                resp= json.dumps({"error": "", "message": "No data yet"})
                return JSONResponse(content=resp, status_code=200)

        #NON HA SENSO PERCHE NON è ASINCRONO

        elif self.sensor["time_scope"] == "now":
            dev = Device_Id.query.first()
            communication_options.get_sensor(communication_options(), sensor, dev.hal_key)

            if dev is not None:
                try:
                    d = Data.query.filter_by(feature=sensor).order_by(Data.timestamp.desc()).first()
                    print(d)
                    if d is not None:
                        response = {"value": json.loads(d.value),"timestamp": datetime.strftime(d.timestamp, "%Y-%m-%d %H:%M:%S")}
                        resp = json.dumps({"entrie": response})
                        return JSONResponse(content=resp, status_code=200)
                    else:
                        logging.warning("GetSensor, granted_actions() method. No data yet")
                        raise HTTPException(status_code=410, detail="No data yet")
                except AttributeError:
                    resp = json.dumps({"error": "", "message": "No data yet"})
                    return JSONResponse(content=resp, status_code=200)
            else:
                resp = json.dumps({"error": "", "message": "Problems connecting to device"})
                return JSONResponse(content=resp, status_code=200)

        elif ("start_time" not in time_scope) or ("stop_time" not in time_scope):
            logging.warning("SetSensor, granted_actions() method. Missing parameter start_time or stop_time")
            raise HTTPException(status_code=400, detail="Bad request. Please check stop_time and start_time keys in time_scope field")
        else:
            start_time = self.validate(time_scope["start_time"])
            stop_time = self.validate(time_scope["stop_time"])

            if start_time > stop_time:
                logging.warning("SetSensor, granted_actions() method. Start time is after stop_time")
                raise HTTPException(status_code=400, detail="Bad request. Start time should be before stop_time.")

            #data_list = Data.query.filter_by(Data.timestamp > start_time).filter_by(Data.timestampn < stop_time).filter_by(Data.name == sensor).all()

            filter_rule = and_(Data.timestamp > start_time, Data.timestamp < stop_time, Data.feature == sensor)
            data_list = Data.query.filter(filter_rule).all()


            response = [{"value": json.loads(d.value), "timestamp": datetime.strftime(d.timestamp, "%Y-%m-%d %H:%M:%S")} for d in data_list]
            resp=json.dumps({"entries": response})
            return JSONResponse(content=resp, status_code=200)


    #valida valori datetime
    def validate(self, date_text):
        try:
            date_dt = datetime.strptime(date_text, "%Y-%m-%d %H:%M:%S")
            return date_dt
        except Exception:
            logging.warning("SensorHandler, validate() method")
            raise HTTPException(status_code=400, detail="Bad request. Check timestamp format")






