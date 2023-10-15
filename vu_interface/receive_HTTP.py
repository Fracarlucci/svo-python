from fastapi import HTTPException, Request
from vu_interface.command_controller import commandController
import logging

class manageHTTPcommunication():
    def receive_http(request: Request):
        body = request.json()
        ##{"COMMAND":{"request_id":"1", "command":"prova"}, "OWNER_KEY":"chiave"}
        try:
            if "COMMAND" in body.keys() and "OWNER_KEY"in body.keys():
                commandController.command_controller(commandController(), body["COMMAND"])
                return "Job finished successfully."
                
            else:
                logging.warning("ManageHTTPcommunication, error in receive request.")
                raise HTTPException(status_code=400, detail="Bad request. Error in managing communication! Missing parameters")
        except Exception:
            logging.warning("ManageHTTPcommunication, error in receive request.")
            raise HTTPException(status_code=500, detail="Error in managing communication!")
            